import os
from typing import Annotated

from database import Base, engine, getdb, sqlite_connect
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from models import Movie, User
from routers import movies, users
from schemas import MovieResponse, MovieUpdate, UserCreate, UserResponse
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException as StarletteHTTPException

base_dir = os.path.dirname(__file__)
static_path = os.path.join(base_dir, 'static/')
media_path = os.path.join(base_dir, 'media/')

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount('/media', StaticFiles(directory=media_path), name='media')
app.mount('/static', StaticFiles(directory=static_path), name='static')
templates = Jinja2Templates(directory='templates')

app.include_router(users.router, prefix='/api/users', tags=['users'])
app.include_router(movies.router, prefix='/api/movies', tags=['movies'])

conn = sqlite_connect()

@app.get('/', include_in_schema=False)
@app.get('/movies', include_in_schema=False)
def home(request: Request, db: Annotated[Session, Depends(getdb)]) -> None:
    result = db.execute(select(Movie))
    movies = result.scalars().all()
    return templates.TemplateResponse(
        request, 'home.html', {'movies': movies, 'title': 'Home'})


@app.get('/movies/{movie_id}', include_in_schema=False)
def movie_page(request: Request, movie_id: int, db: Annotated[Session, Depends(getdb)]):
    movie = find_movie(movie_id, db)
    print(movie.title, movie.director)
    return templates.TemplateResponse(request, 'movie.html', {'movie': movie, 'title': movie.title})


@app.exception_handler(StarletteHTTPException)
def http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = ( exception.detail if exception else 
                'An error occured. Please check ther request and try again.')
    if request.url.path.startswith('/api'):
        return JSONResponse(status_code=exception.status_code, content={'detail': message})
    return templates.TemplateResponse(
        request,
        'error.html',
        {'status_code': exception.status_code, 'title': exception.status_code, 'message': message},
        status_code=exception.status_code)


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith('/api'):
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, content={'detail': exception.errors()})
    return templates.TemplateResponse(
        request,
        'error.html',
        {'status_code': status.HTTP_422_UNPROCESSABLE_CONTENT,
        'title': status.HTTP_422_UNPROCESSABLE_CONTENT,
        'message': 'Invalid request. Please check the input and try again.'},
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT)


def find_movie(movie_id: int, db: Annotated[Session, Depends(getdb)]) -> MovieResponse:
    result = db.execute(select(Movie).where(Movie.id == movie_id))
    movie = result.scalars().first()
    if movie: return movie
    raise StarletteHTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Movie not found')


def find_user(username: str, db: Annotated[Session, Depends(getdb)]) -> UserResponse:
    result = db.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if user: return user
    raise StarletteHTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')