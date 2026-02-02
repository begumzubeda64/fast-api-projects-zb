from typing import Optional
from pydantic import BaseModel, Field

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed on create.", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(description="Year of publishing book", gt=1999, lt=2031)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Pride and prejudice",
                "author": "Jane austin",
                "description": "A new description",
                "rating": 5,
                "published_date": 2012
            }
        }
    }
