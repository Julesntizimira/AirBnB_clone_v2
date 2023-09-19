#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
import os


env_val = os.environ.get('HBNB_TYPE_STORAGE')


class Amenity(BaseModel, Base):
    if env_val == 'db':
        __tablename__ = "amenities"
        name = Column(
                String(128),
                nullable=False)
        place_amenities = relationship(
                "Place",
                secondary="place_amenity",
                back_populates="amenities",
                viewonly=False)
    else:
        name = ""
