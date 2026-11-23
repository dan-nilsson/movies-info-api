from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, selectinload
from starlette.exceptions import HTTPException as StarletteHTTPException

from database import getdb
from models import Movie, User
from schemas import MovieBase, MovieResponse, UserCreate, UserResponse, UserUpdate

router = APIRouter()


@router.get('', response_model=list[UserResponse], status_code=status.HTTP_200_OK)
def get_users(db: Annotated[Session, Depends(getdb)]):
    result = db.execute(select(User))
    users = result.scalars().all()
    return users


@router.get('/{user_id}', response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user(user_id: int, db: Annotated[Session, Depends(getdb)]):
    result = db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if user: 
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')


@router.post('', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Annotated[Session, Depends(getdb)]
) -> UserResponse:
    user_unique, error_type = create_user_validation(user, db)
    if not user_unique:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{error_type} already exists')

    new_user = User(username=user.username, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def create_user_validation(
        user: UserCreate, 
        db: Annotated[Session, Depends(getdb)]
    ) -> (bool,str):
    result = db.execute(select(User).where(User.username == user.username))
    existing_user = result.scalars().first()
    if existing_user:
        return False, 'Username'
    result = db.execute(select(User).where(User.email == user.email))
    existing_email = result.scalars().first()
    if existing_email: 
        return False, 'Email'
    return True, ''


def find_user(username: str, db: Annotated[Session, Depends(getdb)]) -> UserResponse:
    result = db.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if user: 
        return user
    raise StarletteHTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')