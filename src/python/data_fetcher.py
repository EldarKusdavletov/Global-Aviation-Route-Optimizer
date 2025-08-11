import json
import time
import requests
import logging

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def fetch_airports_data(api_url: str) -> list:
    """
    Fetches the airports data from the provided API URL, handling pagination and rate limits.

    Args: api_url (str): The API URL to start fetching data from.
    Returns: list: A list of all airport data obtained from the API.
    Raises: requests.exceptions.RequestException: If an error occurs during the HTTP request.
    """
    data = []
    logging.info(f"Starting to fetch data from {api_url}.")

    while True:
        try:
            logging.info(f"Sending request to {api_url}.")
            response = requests.get(api_url, timeout=60)

            if response.status_code == 200:
                airports = response.json().get("data", [])
                data.extend(airports)
                logging.info(f"Fetched {len(airports)} airports.")

                prev_link = response.json().get("links", {}).get("last", None)
                next_link = response.json().get("links", {}).get("next", None)

                if not next_link or api_url == prev_link:
                    logging.info("No more pages to fetch.")
                    break
                api_url = next_link
            else:
                logging.error(
                    f"Failed to fetch data: {response.status_code}, {response.text}"
                )
                if response.status_code == 429:
                    logging.warning("Rate limit hit. Retrying in 60 seconds...")
                    time.sleep(60)
                    continue
                else:
                    break
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            break

    logging.info(f"Fetched {len(data)} total airports.")
    return data


def save_airports_data(data: list, file_path: str) -> None:
    """
    Saves the fetched airport data to a JSON file.

    Args:
        data (list): The airport data to save.
        file_path (str): The path to the JSON file where the data will be saved.
    """
    try:
        logging.info(f"Saving data to {file_path}.")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logging.info(f"Data saved to {file_path}.")
    except Exception as e:
        logging.error(f"Failed to save data: {e}")


def refresh_airports_data(api_url: str, file_path: str) -> None:
    """
    Fetches airport data from the API and saves it to a JSON file.

    Args:
        api_url (str): The API URL to fetch data from.
        file_path (str): The file path to save the data.
    """
    logging.info("Starting to refresh airports data...")
    airports_data = fetch_airports_data(api_url)
    if airports_data:
        save_airports_data(airports_data, file_path)
    else:
        logging.warning("No data fetched. The database might not have been updated.")
