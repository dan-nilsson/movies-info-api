

from fastapi import FastAPI, Request, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException

from apitools import json_load
from schemas import Movie, MovieUpdate

app = FastAPI()
templates = Jinja2Templates(directory='templates')
app.mount('/static', StaticFiles(directory='static'), name='static')

movies = json_load()

@app.get('/', include_in_schema=False)
@app.get('/movies', include_in_schema=False)
def home(request: Request) -> None:
    return templates.TemplateResponse(
        request, 'home.html', {'movies': movies, 'title': 'Home'})

@app.get('/movies/{movie_id}', include_in_schema=False)
def movie_page(request: Request, movie_id: int):
    movie = find_movie(movie_id)
    return templates.TemplateResponse(request, 'movie.html', {'movie': movie, 'title': movie['title']})

@app.get('/api/movies')
def get_movies() -> list:
    return movies

@app.get('/api/movies/{movie_id}')
def get_movie(movie_id: int):
    return find_movie(movie_id)

def find_movie(movie_id: int) -> Movie:
    for movie in movies:
        if movie['id'] == movie_id:
            return movie
    raise StarletteHTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Movie not found')

@app.exception_handler(StarletteHTTPException)
def http_exception_handler(request: Request, exception: StarletteHTTPException) -> None:
    message = ( exception.detail if exception else 
                'An error occured. Please check ther request and try again.')
    if request.url.path.startswith('/api'):
        return JSONResponse(status_code=exception.status_code, content={'detail': message})
    return templates.TemplateResponse(
        request,
        'error.html',
        {'status_code': exception.status_code, 'title': exception.status_code, 'message': message},
        status_code=exception.status_code)

def main():
    print(movies)

if __name__ == '__main__':
    main()