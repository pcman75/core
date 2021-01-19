import logging
import sqlalchemy

import datetime

from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

_LOGGER = logging.getLogger(__name__)

DOMAIN = "openalpr_scout_service"

ATTR_DATA = "data"
CONF_DB_URL = "db_url"


class CarPlate(Base):
    __tablename__ = "car_plates"

    uuid = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    camera_id = Column(Integer)
    image_id = Column(String(64))
    plate = Column(String(10))
    plate_confidence = Column(Float)
    vehicle_color = Column(String(20))
    vehicle_color_confidence = Column(Float)
    vehicle_make = Column(String(20))
    vehicle_make_confidence = Column(Float)
    vehicle_make_model = Column(String(20))
    vehicle_make_model_confidence = Column(Float)
    vehicle_body_type = Column(String(20))
    vehicle_body_type_confidence = Column(Float)
    vehicle_year = Column(String(20))
    vehicle_year_confidence = Column(Float)
    vehicle_year = Column(String(20))
    vehicle_year_confidence = Column(Float)


def setup(hass, config):
    """Set up is called when Home Assistant is loading our component."""

    def handle_plates_found(call):
        """Handle the service call."""
        data = call.data.get(ATTR_DATA, "")

        _LOGGER.debug("Input data: %s", data)

        try:
            sess = sessmaker()
            plate = CarPlate(
                timestamp=datetime.datetime.fromtimestamp(data["epoch_start"] / 1000),
                camera_id=data["camera_id"],
                image_id=data["best_uuid"],
                plate=data["best_plate_number"],
                plate_confidence=data["best_confidence"],
                vehicle_color=data["vehicle"]["color"][0]["name"],
                vehicle_color_confidence=data["vehicle"]["color"][0]["confidence"],
                vehicle_make=data["vehicle"]["make"][0]["name"],
                vehicle_make_confidence=data["vehicle"]["make"][0]["confidence"],
                vehicle_make_model=data["vehicle"]["make_model"][0]["name"],
                vehicle_make_model_confidence=data["vehicle"]["make_model"][0][
                    "confidence"
                ],
                vehicle_body_type=data["vehicle"]["body_type"][0]["name"],
                vehicle_body_type_confidence=data["vehicle"]["body_type"][0][
                    "confidence"
                ],
                vehicle_year=data["vehicle"]["year"][0]["name"],
                vehicle_year_confidence=data["vehicle"]["year"][0]["confidence"],
            )
            sess.add(plate)
            sess.commit()
        except sqlalchemy.exc.SQLAlchemyError as err:
            _LOGGER.error("Couldn't connect using %s DB_URL: %s", db_url, err)
            return False
        finally:
            sess.close()

    hass.services.register(DOMAIN, "plates_found", handle_plates_found)

    db_url = config[DOMAIN][CONF_DB_URL]

    _LOGGER.debug("DB_URL: %s", db_url)

    try:
        engine = sqlalchemy.create_engine(db_url)
        sessmaker = sessionmaker(bind=engine)

        # create all necessary tables
        sess = sessmaker()
        Base.metadata.create_all(engine)

    except sqlalchemy.exc.SQLAlchemyError as err:
        _LOGGER.error("Couldn't connect using %s DB_URL: %s", db_url, err)
        return False
    finally:
        sess.close()

    # Return boolean to indicate that initialization was successfully.
    return True