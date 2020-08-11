import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def Home():
    return (
    f"HOME<br/>"
    f"Welcome to Step 2 - Climate App section of the SQL Alchemy Homework.<br/>"
    f"Available routes:<br/>"
    f"/api/v1.0/precipitation<br/>"
    f"/api/v1.0/stations<br/>"
    f"/api/v1.0/tobs<br/>"
    f"/api/v1.0/start/<start><br/>"
    f"/api/v1.0/start%20end/<start>/<end><br/>"      
    )

@app.route("/api/v1.0/precipitation")
def Precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation scores for the last 12 months of data (08/23/2016-08/23/2017)"""
    # Query precipitation scores
    prcp_12mo = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= '2016-08-23').\
    filter(Measurement.prcp).\
    order_by(Measurement.date).all()

    session.close()

    # Convert list of tuples into normal list
    prcplist = list(np.ravel(prcp_12mo))

    return jsonify(prcplist)

@app.route("/api/v1.0/stations")
def Stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all stations
    stations = session.query(Station.station, Station.name).\
    order_by(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    stationlist = list(np.ravel(stations))

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def TOBs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all TOBs for USC00519281 station 08/23/2016-08/23/2017"""
    # Query TOBs
    USC00519281_12mo = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.tobs).\
    filter(Measurement.date >= '2016-08-23').\
    order_by(Measurement.date.desc()).all()

    session.close()

    # Convert list of tuples into normal list
    mostactivelist = list(np.ravel(USC00519281_12mo))

    return jsonify(USC00519281_12mo)

# @app.route("/api/v1.0/start/<start>")
# def Start():
#     canonicalized = start.replace(" ", "").lower()
#     for character in justice_league_members:
#         search_term = character["real_name"].replace(" ", "").lower()

#         if search_term == canonicalized:
#             return jsonify(character)

#     return jsonify({"error": f"Character with real_name {real_name} not found."}), 404

if __name__ == "__main__":
    app.run(debug=True)