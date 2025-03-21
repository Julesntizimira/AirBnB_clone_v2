#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, DateTime


Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(
            DateTime,
            nullable=False,
            default=datetime.utcnow())
    updated_at = Column(
            DateTime,
            nullable=False,
            default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs or kwargs.get('id') is None:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        if kwargs:
            if kwargs.get('created_at') is not None:
                kwargs['created_at'] = datetime.strptime(
                        kwargs['created_at'], '%Y-%m-%dT%H:%M:%S.%f')
            if kwargs.get('updated_at') is not None:
                kwargs['updated_at'] = datetime.strptime(
                        kwargs['updated_at'], '%Y-%m-%dT%H:%M:%S.%f')
            if kwargs.get('__class__') is not None:
                del kwargs['__class__']
            self.__dict__.update(kwargs)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        obj_dict = self.__dict__.copy()
        obj_dict.pop("_sa_instance_state", None)
        return '[{}] ({}) {}'.format(cls, self.id, obj_dict)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        dictionary.pop("_sa_instance_state", None)
        return dictionary

    def delete(self):
        ''' delete the current instance from the storage '''
        models.storage.delete(self)
