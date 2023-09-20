#!/usr/bin/python3
""" Module for testing file storage"""
import os
import unittest
import MySQLdb
from models.base_model import BaseModel
from models import storage
from models.user import User


env_val = os.environ.get('HBNB_TYPE_STORAGE')


@unittest.skipIf(env_val != 'db', 'Not a DB run')
class TestDB(unittest.TestCase):
    """ Class to test the file storage method """
    def test_addition_and_delete(self):
        """
        test if objects are added to db
        """
        one = User(first_name="Sbu", last_name="Ndebele",
                   password="123", email="viet@zoom.com")
        # save to db
        one.save()
        # look for one in saved values
        self.assertTrue(one in storage.all().values())
        # find one in DB
        enginDB = MySQLdb.connect(host=os.environ.get('HBNB_MYSQL_HOST'),
                                  user=os.environ.get("HBNB_MYSQL_USER"),
                                  passwd=os.environ.get("HBNB_MYSQL_PWD"),
                                  port=3306,
                                  db=os.environ.get("HBNB_MYSQL_DB"))
        cursor = enginDB.cursor()
        cursor.execute("SELECT * FROM users WHERE id='{}'".format(one.id))
        info = cursor.fetchone()
        self.assertTrue(info is not None)
        self.assertIn("Sbu", info)
        self.assertIn("Ndebele", info)
        self.assertIn("123", info)
        self.assertIn("viet@zoom.com", info)
        self.assertIn(f"User.{one.id}", storage.all(User).keys())
        # delete
        one.delete()
        self.assertNotIn(f"User.{one.id}", storage.all(User).keys())
        cursor.close()
        enginDB.close()


if __name__ == '__main__':
    unittest.main()
