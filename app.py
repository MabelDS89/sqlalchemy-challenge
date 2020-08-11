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
    f"/api/v1.0/startend/<start_date>/<end_date><br/>"      
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
    filter(Measurement.station == "USC00519281").\
    filter(Measurement.date >= '2016-08-23').\
    order_by(Measurement.date.desc()).all()

    session.close()

    # Convert list of tuples into normal list
    mostactivelist = list(np.ravel(USC00519281_12mo))

    return jsonify(USC00519281_12mo)

@app.route("/api/v1.0/start/<start_date>")
def Start(start_date):

    session = Session(engine)

    start_output = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).all()

    session.close()

    startlist = list(np.ravel(start_output))

    return jsonify(startlist)
    
@app.route("/api/v1.0/startend/<start_date>/<end_date>")
def Start_End(start_date, end_date):

    session = Session(engine)

    output = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start_date).\
    filter(Measurement.date <= end_date).all()

    session.close()

    start_endlist = list(np.ravel(output))

    return jsonify(start_endlist)

if __name__ == "__main__":
    app.run(debug=True)