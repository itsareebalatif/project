from fastapi import FastAPI
from app.database import engine, Base
from app.routers import auth
from app.routers import users
from app.routers import posts
from app.routers import comments
import logging
#for logger (extra)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


# 1. Create all database tables automatically based on our models
Base.metadata.create_all(bind=engine)

# 2. Initialize the FastAPI application
app = FastAPI(
    title="Project OF FAST API",
    description="FastAPI application auth and sec",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Practice Project  of FAST API! Server is running successfully...."}