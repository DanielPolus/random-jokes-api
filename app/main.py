from fastapi import FastAPI
from app.routers.health import router as health_router
from app.routers.jokes import router as jokes_router

app = FastAPI(title="Random Joke API")

app.include_router(health_router)
app.include_router(jokes_router)
