from fastapi import APIRouter
from app.services.jokes_client import get_random as get_random_joke
from app.services.jokes_client import get_random_jokes as get_random_jokes
from app.services.jokes_client import get_random_n as get_random_n_service
from app.services.jokes_client import get_type_random as get_type
from app.services.jokes_client import get_by_id as get_by_id

from app.schemas import Joke, JokesList, Error

router = APIRouter(prefix="/jokes", tags=["jokes"])

@router.get("/random/", response_model=Joke)
def get_random():
    return get_random_joke("/random_joke")

@router.get("/ten/", response_model=JokesList)
def get_ten():
    return get_random_jokes("/random_ten")

@router.get("/random/{n}", response_model=JokesList)
def get_random_n_handler(n: int):
    return get_random_n_service(n)

@router.get("/type/{joke_type}/random", response_model=Joke)
def get_random_type_handler(joke_type: str):
    return get_type(f"{joke_type}")

@router.get("/{id}")
def get_by_id_handler(id: int):
    return get_by_id(id)

