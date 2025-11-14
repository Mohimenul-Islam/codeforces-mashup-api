from fastapi import FastAPI

#create an instance of the FastAPI class
app = FastAPI(title = "Codeforces Mashup API")

#Define a route or endpoint
@app.get("/")
def read_root():
    """
    Root endpoint that returns a welcome message.
    """
    return {"message":  "Welcome to the codeforces mashup API!"}