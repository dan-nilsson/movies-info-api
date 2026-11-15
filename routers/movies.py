import os
from typing import Annotated

from database import getdb
from fastapi import APIRouter, Depends, HTTPException, status
from models import Movie
from schemas import MovieBase, MovieCreate, MovieResponse, MovieUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, selectinload
from starlette.exceptions import HTTPException as StarletteHTTPException

router = APIRouter()

@router.get('', response_model=list[MovieResponse])
def get_movies(db: Annotated[Session, Depends(getdb)]) -> list:
    result = db.execute(select(Movie))
    return result


@router.get('/{movie_id}', response_model=MovieResponse)
def get_movie(movie_id: int, db: Annotated[Session, Depends(getdb)]):
    return find_movie(movie_id)


@router.post('', response_model=MovieResponse, status_code=status.HTTP_201_CREATED)
def create_movie(movie: MovieCreate, db: Annotated[Session, Depends(getdb)]):
    new_movie = {'title': movie.title, 'director': movie.director, 'year': movie.year,
                'runtime': movie.runtime, 'genre': movie.genre, 'rating': movie.rating}
    return new_movie


@router.put('', response_model=MovieResponse, status_code=status.HTTP_201_CREATED)
def replace_movie(movie_id: int, movie: MovieBase, db: Annotated[Session, Depends(getdb)]):
    movie = find_movie(movie_id)
    movie.update({'id': movie.new_id, 'title': movie.title, 'director': movie.director, 'year': movie.year,
                'runtime': movie.runtime, 'genre': movie.genre, 'rating': movie.rating})
    return movie


@router.patch('', response_model=MovieResponse, status_code=status.HTTP_201_CREATED)
def update_movie(movie_id: int, changes: MovieUpdate, db: Annotated[Session, Depends(getdb)]):
    movie = find_movie(movie_id)
    movie.update(changes.model_dump(exclude_unset=True))
    return movie


@router.delete('', response_model=MovieResponse, status_code=status.HTTP_202_ACCEPTED)
def remove_movie(movie_id: int, db: Annotated[Session, Depends(getdb)]) -> None:
    movie = find_movie(movie_id)
    movies.remove(movie)
    return movie


def find_movie(movie_id: int, db: Annotated[Session, Depends(getdb)]) -> MovieResponse:
    result = db.execute(select(Movie).where(Movie.id == movie_id))
    movie = result.scalars().first()
    if movie: return movie
    raise StarletteHTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Movie not found')
