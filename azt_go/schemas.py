from pydantic import BaseModel, Field, validator, HttpUrl
from azt_go.models import Links, Categories
from typing import List, Optional
from datetime import datetime, timedelta
import validators

''' Categories'''


class CategoriesPaginated(BaseModel):
    count: int
    page: str
    results: List["CategoriesList"] = []


class CategoriesBase(BaseModel):
    name: str = Field(..., )
    description: str = Field(..., )
    links: Optional[List[int]] = Field(None, )

    class Config:
        orm_mode = True
        orm_model = Categories


class CategoriesDB(CategoriesBase):
    id: int
    slug: str = Field(..., )
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
    links: Optional[List["LinksList"]] = Field(None, )

    class Config:
        orm_mode = True
        orm_model = Categories


''' Links '''


class LinksPaginated(BaseModel):
    count: int
    page: str
    results: List["LinksList"] = []


class LinksBase(BaseModel):
    name: str = Field(..., description="Name of link (AzatAI GitHub)")
    redirect_url: str = Field(..., description="Redirecting url (https://github.com/AzatAI)")
    category_id: Optional[int] = Field(None, description="Category id (1)")

    @validator('redirect_url')
    def validate_redirect_url(cls, value):
        if not validators.url(value):
            raise ValueError('Use valid redirect url')

        return value

    @validator('category_id')
    def validate_category_id(cls, value):
        if value:
            if value <= 0:
                raise ValueError('Use valid category id')

        return value

    class Config:
        orm_mode = True
        orm_model = Links

        schema_extra = {
            "example": {
                "name": "AzatAI GitHub",
                "redirect_url": "https://github.com/AzatAI",
                "category_id": 1
            }
        }


class LinksDB(LinksBase):
    id: int = Field(None)
    slug: str = Field(..., )
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
            "category_id": None,
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
    category_id: Optional[int] = Field(None, )

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


