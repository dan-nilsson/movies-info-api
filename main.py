'''
Movies Info Frontend and API using FastAPI, SQLite
'''
import json
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from apitools import json_load

app = FastAPI()
movies = json_load()

@app.get('/', response_class=HTMLResponse, include_in_schema=False)
@app.get('/movies', response_class=HTMLResponse, include_in_schema=False)
def home() -> None:
    return f'<h1>{movies[0]}</h1>'

@app.get('../api/movies')
def get_movies() -> list:
    return movies



def main():
    print(movies)

if __name__ == '__main__':
    main()