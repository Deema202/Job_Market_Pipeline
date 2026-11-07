import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Retrieve API Credentials securely from environment variables
APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")
SAMPLE_FILE = "sample_response.json"


def fetch_jobs(what_query="Data Engineer", country="gb", page=1, results_per_page=5):
    """
    Fetches job market data from the Adzuna REST API based on search query criteria.

    Parameters:
        what_query (str): Job title or keyword to search for (default: "Data Engineer").
        country (str): Two-letter country code (default: "gb").
        page (int): Page number for pagination (default: 1).
        results_per_page (int): Number of job records to return per request (default: 5).

    Returns:
        dict: Parsed JSON response containing job results if successful, otherwise None.
    """
    url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/{page}"
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "what": what_query,
        "results_per_page": results_per_page,
    }
    try:
        response = requests.get(url, params=params, timeout=30)
        print("Status Code:", response.status_code)
        # Raise an exception for HTTP error responses (4xx or 5xx)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None


def save_sample(data, path=SAMPLE_FILE):
    """
    Saves the API JSON response payload to a local JSON file for sample inspection/caching.

    Parameters:
        data (dict): The dictionary/JSON data to be saved.
        path (str): File path where the JSON file will be written.
    """
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Saved to {path}")


def load_sample(path=SAMPLE_FILE):
    """
    Loads and returns stored sample job data from a local JSON file.

    Parameters:
        path (str): Path to the local JSON file.

    Returns:
        dict: Content of the JSON file as a Python dictionary.
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    # Entry point for testing extraction logic independently
    data = fetch_jobs()
    if data:
        print("Total results found:", data.get("count"))
        save_sample(data)