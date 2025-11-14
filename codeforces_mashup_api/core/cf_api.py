import requests
import random
from ..models.models import Problem  # Use '..' to go up one level to models

# Codeforces API endpoints
USER_STATUS_URL = "https://codeforces.com/api/user.status"
PROBLEMSET_URL = "https://codeforces.com/api/problemset.problems"

def get_solved_problems(username: str) -> set:
    """
    Fetches all unique solved problems for a given user.
    """
    try:
        params = {"handle": username}
        response = requests.get(USER_STATUS_URL, params=params)
        response.raise_for_status()  # Raise an error on a bad response (4xx or 5xx)
        
        data = response.json()
        if data['status'] != 'OK':
            return None  # Handle API error

        solved_problems = set()
        for sub in data['result']:
            if sub['verdict'] == 'OK':
                problem = sub['problem']
                # Create a unique ID for each problem
                solved_problems.add(f"{problem['contestId']}{problem['index']}")
        
        return solved_problems

    except requests.exceptions.RequestException as e:
        print(f"Error fetching solved problems: {e}")
        return None

def get_problemset(tags: list = None) -> list[Problem]:
    """
    Fetches the entire problemset from Codeforces.
    """
    try:
        params = {}
        if tags:
            params['tags'] = ';'.join(tags)
            
        response = requests.get(PROBLEMSET_URL, params=params)
        response.raise_for_status()
        
        data = response.json()
        if data['status'] != 'OK':
            return None

        # We only care about problems, not statistics
        return data['result']['problems']

    except requests.exceptions.RequestException as e:
        print(f"Error fetching problemset: {e}")
        return None

def generate_mashup_problems(
    username: str, 
    min_rating: int, 
    max_rating: int, 
    num_problems: int
) -> list[Problem] | None:
    """
    The main logic function.
    Generates a list of problems for the mashup.
    """
    
    # Step 1: Get data from Codeforces API
    solved_set = get_solved_problems(username)
    all_problems = get_problemset()

    if solved_set is None or all_problems is None:
        print("Failed to fetch data from Codeforces API")
        return None

    # Step 2: Filter the problems
    eligible_problems = []
    for prob in all_problems:
        # Check if problem has a rating
        if 'rating' not in prob:
            continue
        
        rating = prob['rating']
        unique_id = f"{prob['contestId']}{prob['index']}"

        # Apply our filters
        if (min_rating <= rating <= max_rating) and (unique_id not in solved_set):
            # We use our 'Problem' model to create a clean object
            eligible_problems.append(
                Problem(
                    name=prob['name'],
                    contest_id=prob['contestId'],
                    index=prob['index'],
                    rating=rating
                )
            )

    # Step 3: Check if we have enough problems
    if len(eligible_problems) < num_problems:
        print(f"Not enough problems found. Found {len(eligible_problems)}, needed {num_problems}")
        # We could return what we found, but for now, we'll just fail
        return None

    # Step 4: Randomly select and return
    return random.sample(eligible_problems, num_problems)