from fastapi import APIRouter
from app.services.jokes_client import get_random as get_random_joke
from app.services.jokes_client import get_random_jokes as get_random_jokes

from app.schemas import Joke, JokesList, Error

router = APIRouter(prefix="/jokes", tags=["jokes"])

@router.get("/random/", response_model=Joke)
def get_random():
    return get_random_joke("/random_joke")

@router.get("/ten/", response_model=JokesList)
def get_ten():
    return get_random_jokes("/random_ten")

@router.get("/random/{n}")
def get_random_n():
    return {"random_n": "ok"}

@router.get("/type/{n}/random")
def get_random_joke_type():
    return {"random_type_joke": "ok"}

@router.get("/{id}")
def get_joke_id():
    return {"id": "ok"}
