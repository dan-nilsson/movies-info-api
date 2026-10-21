

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from apitools import json_load
from schemas import Movie, MovieUpdate

templates = Jinja2Templates(directory='templates')
app = FastAPI()
movies = json_load()

@app.get('/', include_in_schema=False)
@app.get('/movies', include_in_schema=False)
def home(request: Request) -> None:
    return templates.TemplateResponse(
        request, 'home.html', {'movies': movies, 'title': 'Home'})

@app.get('../api/movies')
def get_movies() -> list:
    return movies



def main():
    print(movies)

if __name__ == '__main__':
    main()