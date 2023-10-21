#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.city import City
import os


env_val = os.environ.get('HBNB_TYPE_STORAGE')


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship(
            "City",
            cascade="all, delete-orphan",
            backref="state")
    if env_val != 'db':
        @property
        def cities(self):
            """Returns the list of City instances with
               state_id equals to the current State.id
            """
            from models.__init__ import storage
            dict_cities = storage.all(City)
            cities_list = []
            for city in dict_cities.values():
                if city.state_id == self.id:
                    cities_list.append(city)
            return cities_list
