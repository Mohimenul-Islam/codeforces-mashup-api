from sqlmodel import SQLModel, create_engine, Session

# 1. Define the database file
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# 2. Create the database engine
# connect_args are needed for SQLite to work smoothly
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})


# 3. Create a function to be called on startup
def create_db_and_tables():
    # This line tells SQLModel to find all classes
    # that inherited from SQLModel (like the Mashup class)
    # and create tables for them in the database.
    SQLModel.metadata.create_all(engine)


# 4. Create a function for "dependency injection"
# This is a key FastAPI concept.
# It gives us a 'session' to talk to the DB
# and guarantees it closes when we're done.
def get_session():
    with Session(engine) as session:
        yield session