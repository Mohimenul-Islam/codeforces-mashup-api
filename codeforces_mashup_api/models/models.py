from sqlmodel  import SQLModel, Field, JSON, Column
from typing import Optional, List

#1. API request model
#This is the data we except from the user when they make a request to create a new mashup
class MashupRequest(SQLModel):
    username: str
    num_problems: int = 5
    min_rating: int = 1400
    max_rating: int = 1600

#2.Problem Data Model
#This defines  the shape of a single problem
#It is not a table in our database
class Problem(SQLModel):
    name: str
    contest_id: int
    index: str
    raing: int

#3.Database Table Model
#This is the model that defines our DB table
# 'table=True' tells SQLModel to create a table for this
class Mashup(SQLModel, table = True):
    id: Optional[int] = Field(default = None, primary_key = True)
    request_data = str #We will store the request as string 

    #We store the list of problems as a JSON string
    #This is simpler than creating a complex table relationship
    problems: str = Field(sa_column = Column(JSON))

#4. API Response Model
#This is the data we will send back to the user when they request a mashup
class MashupResponse(SQLModel):
    mashup_id: int
    problems: List[Problem]