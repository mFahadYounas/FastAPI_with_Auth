from redis import Redis, ConnectionError


redis_client = Redis(host="localhost", port=6379, db=0)


def check_connectivity() -> int:
    try:
        redis_client.ping()
    except ConnectionError as error:
        print(f"Redis Error: {error}")
        return 0

    return 1
