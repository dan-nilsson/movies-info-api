from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, EmailStr


class MovieBase(BaseModel):
    title: str      = Field(min_length=1, max_length=100)
    director: str   = Field(min_length=1, max_length=100)
    year: int
    runtime: int
    genre: str      = Field(min_length=1, max_length=100)
    rating: float

    poster_art: str | None
    image_path: str | None


class MovieCreate(MovieBase):
    id: int         | None = None
    title: str      | None = None      
    director: str   | None = None
    year: int       | None = None
    runtime: int    | None = None
    genre: str      | None = None
    rating: float   | None = None


class MovieUpdate(BaseModel):
    id: int         | None = Field(default=None, min_length=1, max_length=100)
    title: str      | None = Field(default=None, min_length=1, max_length=100)      
    director: str   | None = Field(default=None)
    year: int       | None = Field(default=None)
    runtime: int    | None = Field(default=None)
    genre: str      | None = Field(default=None)
    rating: float   | None = Field(default=None)


class MovieResponse(MovieBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

    date_added: datetime
    #likes: UserResponse


class UserBase(BaseModel):
    username: str   = Field(min_length=1, max_length=15)
    email: EmailStr = Field(max_length=120) #need pydantic[email] validator WIP


class UserCreate(UserBase):
    pass



class UserUpdate(UserBase):
    pass



class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    profile_art: str | None
    image_path: str | None

    date_joined: datetime
    #liked: MovieResponse
