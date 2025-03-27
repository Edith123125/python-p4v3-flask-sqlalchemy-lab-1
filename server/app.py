# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(jsonify(body), 200)


# Task #3: Get earthquake by ID
@app.route('/earthquakes/<int:id>')
def get_earthquake(id):
    earthquake = db.session.get(Earthquake, id)
    if earthquake:
        return make_response(jsonify({
            "id": earthquake.id,
            "location": earthquake.location,
            "magnitude": earthquake.magnitude,
            "year": earthquake.year
        }), 200)
    else:
        return make_response(jsonify({"message": f"Earthquake {id} not found."}), 404)


# Task #4: Get earthquakes by minimum magnitude
@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_magnitude(magnitude):
    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    return make_response(jsonify({
        "count": len(quakes),
        "quakes": [{"id": q.id, "location": q.location, "magnitude": q.magnitude, "year": q.year} for q in quakes]
    }), 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
