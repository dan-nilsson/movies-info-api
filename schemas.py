from pydantic import BaseModel, ConfigDict, Field

class MovieBase(BaseModel):
    id: int   
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

class MovieResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    director: str
    year: int
    runtime: int
    genre: str
    rating: float