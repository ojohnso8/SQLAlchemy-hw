import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/") 
def welcome():

    return(
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/start <br/>"
        f"/api/v1.0/start/end <br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    start_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precip_results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= start_date).all()

    
    # Create a dictionary from the row data and append to a list of prcp_data
    prcp_data = []
    for date, prcp in precip_results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_data.append(prcp_dict)
    return jsonify(prcp_data) 

@app.route("/api/v1.0/stations")
def station_list():
    station_list = session.query(Station.station).all()
    all_stations= list(np.ravel(station_list))
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def temp_year():
    start_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    temp_results = session.query(Measurement.date, Measurement.tobs).\
       filter(Measurement.date >= start_date).all()

    # Create a dictionary from the row data and append to a list of prcp_data
    temp_data = []
    for date, tobs in temp_results:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["tobs"] = tobs
        temp_data.append(temp_dict)
    return jsonify(temp_data) 

@app.route("/api/v1.0/<start>")
def start_temp(start):
    # get the min/avg/max
    
    start_date = dt.datetime.strptime(start, '%Y-%m-%d').date()
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),\
        func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()

# dictionary
    temp_data = []
    for tmin, tavg, tmax in results:
        temp_dict = {}
        temp_dict["TMIN"] = tmin
        temp_dict["TAVG"] = tavg
        temp_dict["TMAX"] = tmax
        temp_data.append(temp_dict)

    return jsonify(temp_data)

@app.route("/api/v1.0/<start>/<end>")
def range_temp(start, end):
 # get the min/avg/max
 
    start_date = dt.datetime.strptime(start, '%Y-%m-%d').date()
    end_date = dt.datetime.strptime(end, '%Y-%m-%d').date()
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),\
        func.max(Measurement.tobs)).\
        filter(Measurement.date >= start, Measurement.date <= end).all()
    
# dictionary
    temp_data_range = []
    for tmin, tavg, tmax in results:
        temp_dict_range = {}
        temp_dict_range["TMIN"] = tmin
        temp_dict_range["TAVG"] = tavg
        temp_dict_range["TMAX"] = tmax
        temp_data_range.append(temp_dict_range)
    return jsonify(temp_data_range)

if __name__ == '__main__':
    app.run(debug=True)

