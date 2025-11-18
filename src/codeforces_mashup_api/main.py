import json
import logging
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session
from contextlib import asynccontextmanager

from .db import create_db_and_tables, get_session
from .models.models import MashupRequest, MashupResponse, Mashup, Problem
from .core.cf_api import generate_mashup_problems

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup")
    create_db_and_tables()
    yield
    logger.info("Application shutdown")


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
    if request.min_rating > request.max_rating:
        raise HTTPException(
            status_code=400,
            detail="Minimum rating cannot be greater than maximum rating"
        )

    logger.info(f"Generating mashup for user: {request.username}")

    problems_list = generate_mashup_problems(
        username=request.username,
        min_rating=request.min_rating,
        max_rating=request.max_rating,
        num_problems=request.num_problems
    )

    if problems_list is None:
        logger.error(f"Failed to generate mashup for user: {request.username}")
        raise HTTPException(
            status_code=400,
            detail="Could not generate mashup. Check user or ratings."
        )

    request_json = request.model_dump_json()
    problems_json = json.dumps([p.model_dump() for p in problems_list])

    db_mashup = Mashup(
        request_data=request_json,
        problems=problems_json
    )

    session.add(db_mashup)
    session.commit()
    session.refresh(db_mashup)

    logger.info(f"Successfully created mashup with ID: {db_mashup.id}")

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
    db_mashup = session.get(Mashup, mashup_id)

    if not db_mashup:
        raise HTTPException(status_code=404, detail="Mashup not found")

    problems_list = [Problem(**p) for p in json.loads(db_mashup.problems)]

    return MashupResponse(
        mashup_id=db_mashup.id,
        problems=problems_list
    )