import warnings

from fastapi import HTTPException, APIRouter

warnings.simplefilter(action='ignore', category=FutureWarning)

diaries_api = APIRouter(prefix='/', tags=['diaries'])