## Ignore SQLITE warnings related to Decimal numbers in the hawaii database
import warnings
warnings.filterwarnings('ignore')

## Dependencies
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.types import Date
from sqlalchemy.orm import Session, scoped_session, sessionmaker
import datetime as dt


## Establish Base for which classes will be constructed
Base = declarative_base()


## Create Measurements and Stations classes
# Measurements
class Measurements(Base):
    __tablename__ = "measurement"
    id = Column(Integer, primary_key = True)
    station = Column(String(255))
    date = Column(Date)
    prcp = Column(Float)
    tobs = Column(Float)

# Stations
class Stations(Base):
    __tablename__ = "station"
    id = Column(Integer, primary_key = True)
    station = Column(String(255))
    name = Column(String(255))
    latitude = Column(Float)
    longtitude = Column(Float)
    elevation = Column(Float)



## Create and establish database connection
engine = create_engine("sqlite:///Resources/hawaii.sqlite")     # Create
conn = engine.connect()                                         # Establish


# Create both the Measurements and Stations tables within the datase
Base.meta.creation_all(conn)


## Create our session (link) from Python to the DB
session = Session(bind = engine)
#======================================================================================
#======================================================================================


#======================================================================================
## Create Climate App
app = Flask(__name__)

@app.route("/")
def home():
    print("Server received request for 'Climate App'")
    return (
        f"Welcome to Climate App!<br/>"
        f"Available Routes:<br/>"
        f"Rain measurement for last 12 months: /api/v1.0/precipitation<br/>"
        f"Stations and respective numbers: /api/v1.0/stations<br>"
        f"Temperature observations from the most active station (Heewii) for last 12 months: /api/v1.0/tobs<br/>"
        f"Temperature info (min, max, ave) for dates you specify (yyy-mm-dd): /api/v1.0/<start><br/>"
        f"Temperature info (min, max, ave) for date range you specify (start and end, yyy-mm-dd): /api/v1.0/<start>/<end>"
        )
# List all routes here



## Define next route: ***precipitation***
# Rain measurement for last 12 months (all stations)
@app.route("/api/v1.0/precipitation")
def precipitation():
    print(f"Rain measurement for last 12 months (all stations)")
    sel = [Measurements.date, Measurements.prcp]
    date = dt.datetime(2017, 8, 23) - dt.timedelta(days=365)

    prcp_12mnth = session.query(*sel).\
        order_by(Measurements.date.asc()).\
            filter(Measurements.date >= date).all()

    session.close()

    # Convert result into a dict (date as key, prcp as value)
    prcp_12mnth_dict = dict(prcp_12mnth)
    
    # Return dict, jsonified
    return jsonify(prcp_12mnth_dict)



## Define next route: ***stations***
# Stations and respective numbers
app.route("/api/v1.0/stations")
def stations_list():
    print(f"Stations and respective numbers")
    stations_list = session.query(Stations.name, Stations.station).all()

    session.close()

    # Convert result into a dict (date as key, prcp as value)
    stations_list_dict = dict(stations_list)
    
    # Return dict, jsonified.
    return jsonify(stations_list_dict)



## Define next route: ***temp observations***
# Temperature observations from the most active station (Heewii, USC00519281) for last 12 months
@app.route("/api/v1.0/tobs")
def tobs():
    print(f"Temperature observations from the most active station (Heewii, USC00519281) for last 12 months")
    date2 = dt.datetime(2017, 8, 23) - dt.timedelta(days=365)
    
    station_9281 = session.query(Measurements.date, Measurements.tobs).\
    filter(Measurements.station == 'USC00519281').\
        filter(Measurements.date >= date2).\
            order_by(Measurements.date.asc()).all()

    session.close()

    # Convert results into dict
    station_9281_dict = dict(station_9281)

    # Return dict, jsonified.
    return jsonify{station_9281_dict}



## Define next route: query based on start date
# Temperature info (min, max, ave) for dates you specify (yyy-mm-dd)
@app.route("/api/v1.0/<start>")
def start():
    print("Temperature info (min, max, ave) for dates you specify (yyy-mm-dd)")
    
    # Firstly, join 2 tables together
    sel1 = [Measurements.station, Measurements.date, Measurements.prcp, Measurements.tobs, Stations.station, Stations.name, Stations.latitude, Stations.longitude, Stations.elevation]
    same_station = session.query(*sel1).filter(Measurements.station == Stations.station).all()
    same_station
    
    # Run query
    temp_all = session.query(Measurements.station, func.min(Measurements.tobs), func.max(Measurements.tobs), func.avg(Measurements.tobs)).\
        filter(Measurements.station == 'USC00519281').all()

    session.close()

    # Convert results into dict
     = dict()

    # Return dict, jsonified.
    return jsonify{}

# Define next route: query based on start and end date
@app.route("/api/v1.0/<start>/<end>")
def startandend():
    print("Server received request for querying based on start and end date")
    return "Welcome to the temperature observation data page, where you can query date ranges!"



if __name__ == "__main__":
    app.run(debug=True)