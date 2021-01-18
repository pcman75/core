import logging
import sqlalchemy

import datetime

from sqlalchemy import Column, Integer, String, Time, Float
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

_LOGGER = logging.getLogger(__name__)

DOMAIN = "openalpr_scout_service"

ATTR_DATA = "data"
from homeassistant.components.recorder import CONF_DB_URL, DEFAULT_DB_FILE, DEFAULT_URL


class CarPlate(Base):
    __tablename__ = "car_plates"

    uuid = Column(Integer, primary_key=True)
    timestamp = Column(Time)
    camera_id = Column(Integer)
    image_id = Column(String)
    plate = Column(String)
    plate_confidence = Column(Float)
    vehicle_color = Column(String)
    vehicle_color_confidence = Column(Float)
    vehicle_make = Column(String)
    vehicle_make_confidence = Column(Float)
    vehicle_make_model = Column(String)
    vehicle_make_model_confidence = Column(Float)
    vehicle_body_type = Column(String)
    vehicle_body_type_confidence = Column(Float)
    vehicle_year = Column(String)
    vehicle_year_confidence = Column(Float)
    vehicle_year = Column(String)
    vehicle_year_confidence = Column(Float)


def setup(hass, config):
    """Set up is called when Home Assistant is loading our component."""

    def handle_plates_found(call):
        """Handle the service call."""
        data = call.data.get(ATTR_DATA, "")

        _LOGGER.warning("Input data: %s", data)

        try:
            sess = sessmaker()
            plate = CarPlate(
                timestamp=datetime.datetime.now(),
                # camera_id=data["camera_id"],
                # image_id = Column(String)
                # plate = Column(String)
                plate=data["openalpr_webhook"]
                # plate_confidence = Column(Float)
                # vehicle_color = Column(String)
                # vehicle_color_confidence = Column(Float)
                # vehicle_make = Column(String)
                # vehicle_make_confidence = Column(Float)
                # vehicle_make_model = Column(String)
                # vehicle_make_model_confidence = Column(Float)
                # vehicle_body_type = Column(String)
                # vehicle_body_type_confidence = Column(Float)
                # vehicle_year = Column(String)
                # vehicle_year_confidence = Column(Float)
                # vehicle_year = Column(String)
                # vehicle_year_confidence = Column(Float)
            )
            sess.add(plate)
        except sqlalchemy.exc.SQLAlchemyError as err:
            _LOGGER.error("Couldn't connect using %s DB_URL: %s", db_url, err)
            return False
        finally:
            sess.close()

    hass.services.register(DOMAIN, "plates_found", handle_plates_found)

    db_url = config.get(CONF_DB_URL)
    if not db_url:
        db_url = DEFAULT_URL.format(hass_config_path=hass.config.path(DEFAULT_DB_FILE))

    try:
        engine = sqlalchemy.create_engine(db_url)
        sessmaker = scoped_session(sessionmaker(bind=engine))

        # Run a dummy query just to test the db_url
        sess = sessmaker()
        sess.execute("SELECT 1;")

    except sqlalchemy.exc.SQLAlchemyError as err:
        _LOGGER.error("Couldn't connect using %s DB_URL: %s", db_url, err)
        return False
    finally:
        sess.close()

    # Return boolean to indicate that initialization was successfully.
    return True