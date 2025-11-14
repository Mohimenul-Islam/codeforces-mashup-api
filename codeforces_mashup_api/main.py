import json
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session
from contextlib import asynccontextmanager

from .db import create_db_and_tables, get_session
from .models.models import MashupRequest, MashupResponse, Mashup, Problem
from .core.cf_api import generate_mashup_problems

# This is a new, advanced FastAPI feature
# It defines code to run on "startup" and "shutdown"
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run on startup
    print("App is starting up...")
    create_db_and_tables()
    yield
    # Code to run on shutdown
    print("App is shutting down...")

# Update our app instance to use the 'lifespan'
app = FastAPI(title="Codeforces Mashup API", lifespan=lifespan)


@app.get("/")
def read_root():
    """
    Root endpoint for the API.
    Returns a welcome message.
    """
    return {"message": "Welcome to the Codeforces Mashup API!"}


@app.post("/generate-mashup/", response_model=MashupResponse)
def create_mashup(
    request: MashupRequest, 
    session: Session = Depends(get_session)
):
    """
    Generate a new mashup contest.
    """
    print(f"Received request for user: {request.username}")

    # 1. Call our "Core Logic" (the chef)
    problems_list = generate_mashup_problems(
        username=request.username,
        min_rating=request.min_rating,
        max_rating=request.max_rating,
        num_problems=request.num_problems
    )

    # 2. Handle Failure
    if problems_list is None:
        print("Failed to generate problems.")
        raise HTTPException(
            status_code=400, 
            detail="Could not generate mashup. Check user or ratings."
        )

    # 3. Handle Success: Save to Database
    
    # Convert request and problem list to JSON strings for DB
    request_json = request.model_dump_json()
    problems_json = json.dumps([p.model_dump() for p in problems_list])

    db_mashup = Mashup(
        request_data=request_json,
        problems=problems_json
    )
    
    session.add(db_mashup)
    session.commit()
    session.refresh(db_mashup)
    
    print(f"Successfully created and saved mashup ID: {db_mashup.id}")

    # 4. Return the Response
    return MashupResponse(
        mashup_id=db_mashup.id,
        problems=problems_list
    )

@app.get("/mashup/{mashup_id}", response_model=MashupResponse)
def get_mashup(
    mashup_id: int, 
    session: Session = Depends(get_session)
):
    """
    Retrieve a previously generated mashup by its ID.
    """
    
    # 1. Find the mashup in the database by its ID
    db_mashup = session.get(Mashup, mashup_id)
    
    # 2. Handle if not found
    if not db_mashup:
        raise HTTPException(status_code=404, detail="Mashup not found")

    # 3. Re-create the data for the response
    # We need to convert the JSON strings back into objects
    problems_list = [Problem(**p) for p in json.loads(db_mashup.problems)]
    
    # 4. Return the Response
    return MashupResponse(
        mashup_id=db_mashup.id,
        problems=problems_list
    )