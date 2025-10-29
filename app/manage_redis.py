from redis import ConnectionError, from_url
from dotenv import load_dotenv
import os

load_dotenv()

REDIS_URL = os.environ.get("REDIS_URL")
redis_client = from_url(REDIS_URL, decode_responses=True)


def check_connectivity() -> int:
    try:
        redis_client.ping()
    except ConnectionError as error:
        print(f"Redis Error: {error}")
        return 0

    return 1
