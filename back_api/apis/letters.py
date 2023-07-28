import warnings

from fastapi import HTTPException, APIRouter

warnings.simplefilter(action='ignore', category=FutureWarning)

letters_api = APIRouter(prefix='/', tags=['letters'])