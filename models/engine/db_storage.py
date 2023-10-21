#!/usr/bin/python3
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from models.base_model import BaseModel, Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
import os


my_user = os.environ.get('HBNB_MYSQL_USER')
my_password = os.environ.get('HBNB_MYSQL_PWD')
my_host = os.environ.get('HBNB_MYSQL_HOST')
my_db = os.environ.get('HBNB_MYSQL_DB')


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        '''create the engine
           the engine must be linked to the MySQL
           database and user created before

           drop all tables if the environment
           variable HBNB_ENV is equal to test
        '''
        self.__engine = create_engine(
                'mysql+mysqldb://{}:{}@{}/{}'.format(
                    my_user,
                    my_password,
                    my_host,
                    my_db
                    ), pool_pre_ping=True)
        if os.environ.get('HBNB_ENV') == 'test':
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        '''return query on the current database session'''
        obj_dict = {}
        cls_list = [State, City, User, Place, Review, Amenity]
        if cls is None:
            for cl in cls_list:
                for obj in self.__session.query(cl).all():
                    key = cl.__name__ + '.' + obj.id
                    obj_dict[key] = obj
        else:
            if type(cls) == str:
                cls = eval(cls)
            for obj in self.__session.query(cls).all():
                key = cls.__name__ + '.' + obj.id
                obj_dict[key] = obj
        return obj_dict

    def new(self, obj):
        '''add the object to the current database session'''
        self.__session.add(obj)

    def save(self):
        '''commit all changes of the current
           database session
        '''
        self.__session.commit()

    def delete(self, obj=None):
        '''delete from the current database session obj
           if not None
        '''
        if obj is not None:
            self.__session(obj)

    def reload(self):
        '''create all tables in the database
           create the current database session
        '''
        Base.metadata.create_all(bind=self.__engine)
        SessionFactory = sessionmaker(
                bind=self.__engine,
                expire_on_commit=False)
        ScopedSessionFactory = scoped_session(SessionFactory)
        self.__session = ScopedSessionFactory()

    def close(self):
        ''' call remove() method on the private session attribute
            (self.__session) or close() on the class
        '''
        self.__session.close()
