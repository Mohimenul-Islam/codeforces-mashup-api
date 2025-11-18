# Codeforces Mashup API

A Python RESTful API built with FastAPI that generates custom Codeforces practice contests based on user preferences. The API filters out already-solved problems and creates personalized problem sets for competitive programmers.

## Features

* **Custom Mashup Generation** - Generate problem sets by username, rating range, and number of problems
* **Smart Filtering** - Automatically excludes problems already solved by the user
* **Database Persistence** - Stores generated mashups in SQLite for later retrieval
* **RESTful Design** - Clean API endpoints with automatic documentation
* **Input Validation** - Comprehensive validation for all user inputs

## Tech Stack

* **FastAPI** - Modern, fast web framework for building APIs
* **SQLModel** - SQL database ORM with Pydantic validation
* **SQLite** - Lightweight database for persistence
* **Poetry** - Dependency management and packaging
* **Uvicorn** - ASGI server implementation

## Installation

### Prerequisites

* Python 3.10 or higher
* Poetry

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Mohimenul-Islam/codeforces-mashup-api.git
cd codeforces-mashup-api
```

2. Install dependencies:
```bash
poetry install
```

3. Run the server:
```bash
poetry run uvicorn codeforces_mashup_api.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

## API Usage

### Interactive Documentation

Visit `http://127.0.0.1:8000/docs` for the interactive Swagger UI documentation.

### Generate a Mashup

**POST** `/generate-mashup/`

```bash
curl -X POST "http://127.0.0.1:8000/generate-mashup/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "tourist",
    "num_problems": 5,
    "min_rating": 1800,
    "max_rating": 2200
  }'
```

**Response:**
```json
{
  "mashup_id": 1,
  "problems": [
    {
      "name": "Problem Name",
      "contest_id": 1234,
      "index": "A",
      "rating": 1900
    }
  ]
}
```

### Retrieve a Mashup

**GET** `/mashup/{mashup_id}`

```bash
curl "http://127.0.0.1:8000/mashup/1"
```

## Project Structure

```
codeforces-mashup-api/
├── src/
│   └── codeforces_mashup_api/
│       ├── __init__.py
│       ├── main.py          # FastAPI application and endpoints
│       ├── db.py            # Database configuration
│       ├── models/
│       │   └── models.py    # Pydantic models
│       └── core/
│           └── cf_api.py    # Codeforces API integration
├── pyproject.toml
├── poetry.lock
└── README.md
```

## Development

### Running Tests

```bash
poetry run pytest
```

### Code Formatting

```bash
poetry run black src/
poetry run isort src/
```

## License

This project is open source and available under the MIT License.

## Author

Mohimenul Islam
* GitHub: [@Mohimenul-Islam](https://github.com/Mohimenul-Islam)
* Email: islam15-5725@diu.edu.bd
