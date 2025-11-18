import requests
import random
import logging
from ..models.models import Problem

logger = logging.getLogger(__name__)

USER_STATUS_URL = "https://codeforces.com/api/user.status"
PROBLEMSET_URL = "https://codeforces.com/api/problemset.problems"
REQUEST_TIMEOUT = 10


def get_solved_problems(username: str) -> set | None:
    """
    Fetches all unique solved problems for a given user.
    """
    try:
        params = {"handle": username}
        response = requests.get(USER_STATUS_URL, params=params, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()

        data = response.json()
        if data['status'] != 'OK':
            return None

        solved_problems = set()
        for sub in data['result']:
            if sub['verdict'] == 'OK':
                problem = sub['problem']
                solved_problems.add(f"{problem['contestId']}{problem['index']}")

        return solved_problems

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching solved problems for {username}: {e}")
        return None


def get_problemset(tags: list = None) -> list | None:
    """
    Fetches the entire problemset from Codeforces.
    """
    try:
        params = {}
        if tags:
            params['tags'] = ';'.join(tags)

        response = requests.get(PROBLEMSET_URL, params=params, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()

        data = response.json()
        if data['status'] != 'OK':
            return None

        return data['result']['problems']

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching problemset: {e}")
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
    solved_set = get_solved_problems(username)
    all_problems = get_problemset()

    if solved_set is None or all_problems is None:
        logger.error("Failed to fetch data from Codeforces API")
        return None

    eligible_problems = []
    for prob in all_problems:
        if 'rating' not in prob:
            continue

        rating = prob['rating']
        unique_id = f"{prob['contestId']}{prob['index']}"

        if (min_rating <= rating <= max_rating) and (unique_id not in solved_set):
            eligible_problems.append(
                Problem(
                    name=prob['name'],
                    contest_id=prob['contestId'],
                    index=prob['index'],
                    rating=rating
                )
            )

    if len(eligible_problems) < num_problems:
        logger.warning(
            f"Not enough problems found. Found {len(eligible_problems)}, needed {num_problems}"
        )
        return None

    return random.sample(eligible_problems, num_problems)