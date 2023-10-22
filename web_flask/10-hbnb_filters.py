#!/usr/bin/python3
""" script that starts a Flask web application """

from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route("/hbnb_filters")
def cities_list():
    """ """
    states = storage.all(State)
    amenities = storage.all(State)
    return render_template("10-hbnb_filters.html", states=states, amenities=amenities)


@app.teardown_appcontext
def teardown(error):
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
