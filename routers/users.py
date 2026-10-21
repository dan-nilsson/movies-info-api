from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

import models
from database import get_db
from schemas import MovieResponse, UserCreate, UserResponse, UserUpdate

router = APIRouter()

@router.post('', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Annoted[Session, Depends(getdb)]):
    user_unique, error_type = create_user_validation(user)
    if not user_unique:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{error_type} already exists')
        return user

    new_user = models.User(username=user.username, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('', response_model=list[UserResponse], status_code=status.HTTP_200_OK)
def get_users(db: Annoted[Session, Depends(getdb)]):
    result = db.execute(select(models.User))
    return result


@router.get('/{user_id}', response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user(user_id: int, db: Annoted[Session, Depends(getdb)]):
    result = db.execute(select(models.User).where(models.User.username == user.username))
    user = result.scalars().first()
    if user: return user

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User not found')


def create_user_validation(user: UserCreate) -> bool:
    result = db.execute(select(models.User).where(models.User.username == user.username))
    existing_user = result.scalars().first()
    if existing_user: return False, 'Username'

    result = db.execute(select(models.User).where(models.User.email == user.email))
    existing_user = result.scalars().first()
    if existing_user: return False, 'Email'

    return True, 'Pass'

def find_user(username: str, db: Annoted[Session, Depends(getdb)]) -> UserResponse:
    result = db.execute(select(models.User).where(models.User.username == username))
    user = result.scalars().first()
    if user: return user
    raise StarletteHTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')