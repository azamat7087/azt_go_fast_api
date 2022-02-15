from pydantic import BaseModel, Field, validator, HttpUrl
from azt_go.models import Links, Categories
from typing import List
from datetime import datetime, timedelta
import validators

''' Categories'''


class CategoriesBase(BaseModel):
    name: str = Field(..., )
    slug: str = Field(..., )
    description: str = Field(..., )
    links: List[int] = Field(None, )

    class Config:
        orm_mode = True
        orm_model = Categories


class CategoriesDB(CategoriesBase):
    id: int
    date_of_add: datetime = Field(None)
    date_of_update: datetime = Field(None)

    class Config:
        orm_mode = True
        orm_model = Categories

        the_schema = {
            "id": 1,
            "name": "test",
            "slug": "test",
            "description": "test",
            "links": ["1", "2"],
            "date_of_add": datetime.now(),
            "date_of_update": datetime.now()
        }


class CategoriesList(BaseModel):
    id: int
    name: str = Field(..., )
    slug: str = Field(..., )

    class Config:
        orm_mode = True
        orm_model = Categories

        the_schema = {
            "id": 1,
            "name": "test",
            "slug": "test",
        }


class CategoriesDetail(BaseModel):
    id: int
    name: str = Field(..., )
    slug: str = Field(..., )
    description: str = Field(..., )
    links: List[Links] = Field(None, )

    class Config:
        orm_mode = True
        orm_model = Categories


''' Links '''


class LinksBase(BaseModel):
    name: str = Field(..., )
    slug: str = Field(..., )
    redirect_url: str = Field(..., )
    category_id: int = Field(None, )

    class Config:
        orm_mode = True
        orm_model = Links


class LinksDB(LinksBase):
    id: int
    date_of_add: datetime = Field(None)
    date_of_update: datetime = Field(None)

    class Config:
        orm_mode = True
        orm_model = Links

        the_schema = {
            "id": 1,
            "name": "test",
            "slug": "test",
            "redirect_url": "test",
            "category_id": 1,
            "date_of_add": datetime.now(),
            "date_of_update": datetime.now()
        }


class LinksList(BaseModel):
    id: int
    name: str = Field(..., )
    slug: str = Field(..., )
    redirect_url: str = Field(..., )

    class Config:
        orm_mode = True
        orm_model = Categories

        the_schema = {
            "id": 1,
            "name": "test",
            "slug": "test",
            "redirect_url": "test"
        }


class LinksDetail(LinksList):
    category_id: int = Field(None, )

    class Config:
        orm_mode = True
        orm_model = Categories

        the_schema = {
            "id": 1,
            "name": "test",
            "slug": "test",
            "redirect_url": "test",
            "category_id": 1,

        }


