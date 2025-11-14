from sqlmodel import SQLModel, create_engine, Session

#1. Define the database file
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

#2. Create the database engine
