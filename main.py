from fastapi import FastAPI
from dotenv import load_dotenv
import uvicorn

app = FastAPI()

load_dotenv()  # load environment variables


def main():
    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
