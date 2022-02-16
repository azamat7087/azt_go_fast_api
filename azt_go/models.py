import datetime
from core.db import Base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class Categories(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String(length=70), nullable=False, unique=True)
    slug = Column(String(length=100), unique=True, nullable=False)
    description = Column(String(length=300), default="")
    date_of_add = Column('date_of_add', DateTime, default=datetime.datetime.now, nullable=False)
    date_of_update = Column('date_of_update', DateTime, default=datetime.datetime.now,
                            onupdate=datetime.datetime.now, nullable=False)

    links = relationship("Links", back_populates="category")


class Links(Base):

    __tablename__ = "links"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String(length=70), nullable=False, unique=True)
    slug = Column(String(length=100), unique=True, nullable=False)
    redirect_url = Column(String(length=300), nullable=False, unique=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    date_of_add = Column('date_of_add', DateTime, default=datetime.datetime.now, nullable=False)
    date_of_update = Column('date_of_update', DateTime, default=datetime.datetime.now,
                            onupdate=datetime.datetime.now, nullable=False)

    category = relationship("Categories", back_populates="links")
