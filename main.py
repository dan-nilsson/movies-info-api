import os
from typing import Annotated

from fastapi import FastAPI, Request, HTTPException, status, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Movie, User
from database import Base, engine, get_db, sqlite_connect
from schemas import MovieBase, MovieUpdate, MovieResponse, UserCreate, UserResponse
from routers import users, movies

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
def home(request: Request, db: Annoted[Session, Depends(getdb)]) -> None:
    movies = get_all_movies_sqlite()
    # movies = db.execute(select(models.Movie))
    return templates.TemplateResponse(
        request, 'home.html', {'movies': movies, 'title': 'Home'})


@app.get('/movies/{movie_id}', include_in_schema=False)
def movie_page(request: Request, movie_id: int, db: Annoted[Session, Depends(getdb)]):
    movie = find_movie(movie_id, db)
    return templates.TemplateResponse(request, 'movie.html', {'movie': movie, 'title': movie['title']})


@app.exception_handler(StarletteHTTPException)
def http_exception_handler(request: Request, exception: StarletteHTTPException) -> json:
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
def validation_exception_handler(request: Request, exception: RequestValidationError) -> json:
    if request.url.path.startswith('/api'):
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, content={'detail': exception.errors()})
    return templates.TemplateResponse(
        request,
        'error.html',
        {'status_code': status.HTTP_422_UNPROCESSABLE_CONTENT,
        'title': status.HTTP_422_UNPROCESSABLE_CONTENT,
        'message': 'Invalid request. Please check the input and try again.'},
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT)


def find_movie(movie_id: int, db: Annoted[Session, Depends(getdb)]) -> MovieResponse:
    result = db.execute(select(models.Movie).where(models.Movie.id == movie_id))
    movie = result.scalars().first()
    if movie: return movie
    raise StarletteHTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Movie not found')


def find_user(username: str, db: Annoted[Session, Depends(getdb)]) -> UserResponse:
    result = db.execute(select(models.User).where(models.User.username == username))
    user = result.scalars().first()
    if user: return user
    raise StarletteHTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')


def get_all_movies_sqlite() -> list[dict]:
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM movies')
    rows = cursor.fetchall()
    movies = [row_to_dict(row, cursor) for row in rows]
    print(movies)
    return movies

def row_to_dict(row, cursor):
    columns = [column[0] for column in cursor.description]
    return dict(zip(columns, row))