from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user

app = FastAPI()

# creates database when it doesn't exist
models.Base.metadata.create_all(engine)



app.include_router(post.router)
app.include_router(user.router)





