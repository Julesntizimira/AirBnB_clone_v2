#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from models.user import User
from models.city import City
from models.city import Review
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy import Float
from sqlalchemy.orm import relationship
import os


env_val = os.environ.get('HBNB_TYPE_STORAGE')


class Place(BaseModel, Base):
    """ A place to stay """
    if env_val == 'db':
        __tablename__ = "places"
        city_id = Column(
                String(60),
                ForeignKey("cities.id"),
                nullable=False)
        user_id = Column(
                String(60),
                ForeignKey("users.id"),
                nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024))
        number_rooms = Column(
                Integer,
                nullable=False,
                default=0)
        number_bathrooms = Column(
                Integer,
                nullable=False,
                default=0)
        max_guest = Column(
                Integer,
                nullable=False,
                default=0)
        price_by_night = Column(
                Integer,
                nullable=False,
                default=0)
        latitude = Column(Float)
        longitude = Column(Float)
        reviews = relationship("Review", backref="place", cascade='delete')
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self)
        """Returns the list of City instances with
               place_id equals to the current Place.id
        """
        from models.__init__ import storage
        dict_reviews = storage.all(Review)
        reviews_list = []
        for rev in dict_reviews.values():
            if rev.place_id == self.id:
                reviews_list.append(rev)
        return reviews_list
