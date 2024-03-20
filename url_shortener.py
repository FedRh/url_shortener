import argparse
import os
import string
import random
from datetime import datetime, timedelta

from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient

load_dotenv()  # Load environment variables from .env file

MONGODB_URI = os.getenv("MONGODB_URI")

# Create a new client and connect to the server
client = MongoClient(MONGODB_URI)
db = client["url_shortener"]
collection = db["urls"]

BASE_URL = "https://myurlshortener.com/"
CHARACTERS = string.ascii_lowercase + string.digits + string.ascii_uppercase
DEFAULT_EXPIRATION_TIME = 604800  # 7 days in seconds


def shorten_url(original_url: str) -> str:
    existing_url = collection.find_one({"original_url": original_url})
    if existing_url and existing_url["expiration_time"] > datetime.utcnow():
        return existing_url["short_url"]  # Existing URL not expired

    while True:
        short_code = ''.join(random.choices(CHARACTERS, k=5))  # Generate random 5-character code
        short_url = BASE_URL + short_code  # Construct the full shortened URL
        if not collection.find_one({"short_url": short_url}):
            break

    expiration_time = datetime.utcnow() + timedelta(seconds=DEFAULT_EXPIRATION_TIME)
    collection.insert_one({"original_url": original_url, "short_url": short_url, "expiration_time": expiration_time})
    return short_url


def expand_url(short_url: str) -> str:
    url_data = collection.find_one({"short_url": short_url})
    if url_data:
        if url_data["expiration_time"] > datetime.utcnow():
            return url_data["original_url"]
        else:
            collection.delete_one({"short_url": short_url})
            return "The link has expired."
    else:
        return "Invalid link."


def main():
    parser = argparse.ArgumentParser(description="URL shortener")
    parser.add_argument("--minify", type=str, help="Shorten a URL")
    parser.add_argument("--expand", type=str, help="Expand a shortened URL")

    args = parser.parse_args()

    if args.minify:
        try:
            short_url = shorten_url(args.minify)
            print(f"Shortened URL: {short_url}")
        except Exception as e:
            print(f"Error shortening URL: {e}")
    elif args.expand:
        try:
            original_url = expand_url(args.expand)
            print(f"Original URL: {original_url}")
        except Exception as e:
            print(f"Error expanding URL: {e}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()