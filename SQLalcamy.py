import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
station = Base.classes.station
measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session=Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

##################################################
@app.route("/api/v1.0/precipitation")
def precipitation ():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitaion by date"""
    # Query all precipitation and date 
    results = session.query(measurement.date, measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data using `date` as the key and `prcp` as the value.
    Prcp_date= []
    for date, precipitation in results:
        prcp_dict = {}
        prcp_dict["Date"] = date
        prcp_dict["Precipitation"] = prcp
        
        Prcp_date.append(prcp_dict)

    return jsonify(Prcp_date)

#################################################
@app.route("/api/v1.0/stations")
def stations ():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations in the data set"""
    # Query all stations in the station data set 
    results = session.query(station.station).all()


    session.close()

    station_names = list(np.ravel(results))

    return jsonify(station_names)
###############################################################
@app.route("/api/v1.0/tobs")
def tobs ():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list dates and tempuratures for 2016-2017 year"""
    # Query the dates and temperature observations of the most active station for the last year of data.
    # Creating the data set 
    sel = [ measurement.date, measurement.prcp,measurement.tobs,  station.station, station.name, station.latitude, station.longitude, station.elevation]
    same_station1 = session.query(*sel).filter(measurement.station == station.station).filter(measurement.date>'2016-08-23').filter (station.station=='USC00519397').all()

    session.close()



    # Create a dictionary from the row data and append to a list of all_passengers
    year_temp= []
    for tobs, date in same_station1:
        tobs_dict = {}
        tobs_dict["Tempurature"] = tobs
        tobs_dict["Date"] = date
        
        year_temp.append(tobs_dict)

    return jsonify(year_temp)
#################################################################################
 # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for the year before a given start 
@app.route("/api/v1.0/<start>")
def start_date_only (start):

    customer_data=input ("What day would you like to start your search? ")
    start_date= date.datetime.strptime( 'customer_data')
    delta = datetime.timedelta(days=365)
    start = start_date-delta
    
    customer_trip_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    trip = list(np.ravel(trip_data))
    return jsonify(trip)
###################################################################################
# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a range 
@app.route("/api/v1.0/<start>/<end>")
def start_end_range (start,end):

   
    Customer_start=input("What day do you want to end your search")
    
    start_date= datetime.strptime("Customer_start")
    end_date= datetime.timedelta (days=7)
    end = start_date + end_date
    trip_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end).all()
    trip = list(np.ravel(trip_data))
    return jsonify(trip)


if __name__ == '__main__':
    app.run(debug=True)


