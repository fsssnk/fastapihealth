from fastapi import FastAPI

app = FastAPI()


@app.post("/post")
def post():
    return post