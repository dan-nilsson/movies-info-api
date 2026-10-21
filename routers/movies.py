import os

# from .. models import models
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database import get_db
from schemas import MovieResponse, MovieCreate, MovieUpdate

router = APIRouter()

@router.get('', response_model=list[MovieResponse])
def get_movies(db: Annoted[Session, Depends(getdb)]) -> list:
    result = db.execute(select(models.Movie))
    return result


@router.get('/{movie_id}', response_model=MovieResponse)
def get_movie(movie_id: int, db: Annoted[Session, Depends(getdb)]):
    return find_movie(movie_id)


@router.post('', response_model=MovieResponse, status_code=status.HTTP_201_CREATED)
def create_movie(movie: MovieCreate, db: Annoted[Session, Depends(getdb)]) -> json:
    new_movie = {'title': movie.title, 'director': movie.director, 'year': movie.year,
                'runtime': movie.runtime, 'genre': movie.genre, 'rating': movie.rating}
    return new_movie


@router.put('', response_model=MovieResponse, status_code=status.HTTP_201_CREATED)
def replace_movie(movie_id: int, movie: MovieBase, db: Annoted[Session, Depends(getdb)]) -> json:
    movie = find_movie(movie_id)
    movie.update({'id': new_id, 'title': movie.title, 'director': movie.director, 'year': movie.year,
                'runtime': movie.runtime, 'genre': movie.genre, 'rating': movie.rating})
    return movie


@router.patch('', response_model=MovieResponse, status_code=status.HTTP_201_CREATED)
def update_movie(movie_id: int, changes: MovieUpdate, db: Annoted[Session, Depends(getdb)]) -> json:
    movie = find_movie(movie_id)
    movie.update(changes.model_dump(exclude_unset=True))
    return movie


@router.delete('', response_model=MovieResponse, status_code=status.HTTP_202_ACCEPTED)
def remove_movie(movie_id: int, db: Annoted[Session, Depends(getdb)]) -> None:
    movie = find_movie(movie_id)
    movies.remove(movie)
    return movie


def find_movie(movie_id: int, db: Annoted[Session, Depends(getdb)]) -> MovieResponse:
    result = db.execute(select(models.Movie).where(models.Movie.id == movie_id))
    movie = result.scalars().first()
    if movie: return movie
    raise StarletteHTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Movie not found')
