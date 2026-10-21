
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException

from apitools import json_load
from schemas import MovieBase, MovieUpdate, MovieResponse

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

@app.get('/api/movies', response_model=list[MovieResponse])
def get_movies() -> list:
    return movies

@app.get('/api/movies/{movie_id}', response_model=MovieResponse)
def get_movie(movie_id: int):
    return find_movie(movie_id)

@app.post('/api/movies', response_model=MovieResponse, status_code=status.HTTP_201_CREATED)
def create_movie(movie: MovieBase) -> json:
    new_id = max(m['id'] for m in movies) + 1 if movies else 1
    new_movie = {'id': new_id, 'title': movie.title, 'director': movie.director, 'year': movie.year,
                'runtime': movie.runtime, 'genre': movie.genre, 'rating': movie.rating}
    movies.append(new_movie)
    return new_movie

@app.put('/api/movies', response_model=MovieResponse, status_code=status.HTTP_201_CREATED)
def replace_movie(movie_id: int, movie: MovieBase) -> json:
    movie = find_movie(movie_id)
    movie.update({'id': new_id, 'title': movie.title, 'director': movie.director, 'year': movie.year,
                'runtime': movie.runtime, 'genre': movie.genre, 'rating': movie.rating})
    return movie

@app.patch('/api/movies', response_model=MovieResponse, status_code=status.HTTP_201_CREATED)
def update_movie(movie_id: int, changes: MovieUpdate) -> json:
    movie = find_movie(movie_id)
    movie.update(changes.model_dump(exclude_unset=True))
    return movie

@app.delete('/api/movies', response_model=MovieResponse, status_code=status.HTTP_202_ACCEPTED)
def remove_movie(movie_id: int) -> None:
    movie = find_movie(movie_id)
    movies.remove(movie)
    return movie

def find_movie(movie_id: int) -> MovieBase:
    for movie in movies:
        if movie['id'] == movie_id:
            return movie
    raise StarletteHTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Movie not found')

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



def main():
    print(movies)

if __name__ == '__main__':
    main()