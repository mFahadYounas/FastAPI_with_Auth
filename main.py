from fastapi import FastAPI
import uvicorn

app = FastAPI()


def main():
    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
