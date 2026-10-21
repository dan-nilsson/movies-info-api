from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, EmailStr

class MovieBase(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    director: str = Field(min_length=1, max_length=100)
    year: int
    runtime: int
    genre: str
    rating: float

class MovieUpdate(BaseModel):
    id: int         | None = Field(default=None, min_length=1, max_length=100)
    title: str      | None = Field(default=None, min_length=1, max_length=100)      
    director: str   | None = Field(default=None)
    year: int       | None = Field(default=None)
    runtime: int    | None = Field(default=None)
    genre: str      | None = Field(default=None)
    rating: float   | None = Field(default=None)

class MovieCreate(MovieBase):
    id: int         | None = None
    title: str      | None = None      
    director: str   | None = None
    year: int       | None = None
    runtime: int    | None = None
    genre: str      | None = None
    rating: float   | None = None

class MovieUpdate(MovieBase):
    id: int         | None = None
    title: str      | None = None      
    director: str   | None = None
    year: int       | None = None
    runtime: int    | None = None
    genre: str      | None = None
    rating: float   | None = None

class MovieResponse(MovieBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    poster_art: str | None
    poster_art_path: str

    date_added: datetime
    likes: UserResponse

class UserBase(BaseModel):
    username: str = Field(min_length=1, max_length=15)
    # email: EmailStr = Field(max_length=120) #need pydantic[email] validator WIP

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    profile_art: str | None
    profile_art_path: str

    date_joined: datetime
    liked: MovieResponse