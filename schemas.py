from pydantic import BaseModel, ConfigDict, Field

class Movie(BaseModel):
    id: int         | None = None
    title: str
    director: str
    year: int
    runtime: int
    genre: str
    rating: float

class MovieUpdate(BaseModel):
    id: int         | None = None
    title: str      | None = None      
    director: str   | None = None
    year: int       | None = None
    runtime: int    | None = None
    genre: str      | None = None
    rating: float   | None = None