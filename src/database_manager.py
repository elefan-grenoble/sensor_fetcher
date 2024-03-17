import logging
import os
import sys

from sqlalchemy import Column, DateTime, Float, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

Base = declarative_base()


class DatabaseManager:
    # Define the table schema
    class SensorTable(Base):
        __tablename__ = os.getenv("DB_TABLE", "data")
        id = Column(Integer, primary_key=True)
        device_name = Column(String(255), nullable=False)
        created_at = Column(DateTime(timezone=True), server_default=func.now())
        battery = Column(Float, nullable=True)
        light = Column(Float, nullable=True)
        pressure = Column(Float, nullable=True)
        temperature = Column(Float, nullable=True)

    def __init__(self):
        # Set up logging
        self.logger = logging.getLogger(__name__)

        # Retrieve connection parameters from environment variables
        self.db_user = os.getenv("DB_USERNAME")
        self.db_password = os.getenv("DB_PASSWORD")
        self.db_host = os.getenv("DB_HOST")
        self.db_port = os.getenv("DB_PORT", "3306")  # Default port is 3306
        self.db_database = os.getenv("DB_DATABASE")

        # Build connection string
        self.connection_string = (
            f"mysql+pymysql://{self.db_user}:{self.db_password}@"
            f"{self.db_host}:{self.db_port}/{self.db_database}?charset=utf8mb4"
        )

        # Create engine and session
        try:
            self.engine = create_engine(self.connection_string)
            self.Session = sessionmaker(bind=self.engine)
            self.logger.info("Database connection established successfully.")
        except Exception as e:
            self.logger.error(f"Error connecting to the database: {str(e)}")
            sys.exit(1)

    def create_table(self):
        try:
            # Create the table in the database
            Base.metadata.create_all(self.engine)
            self.logger.info("Table created successfully.")
        except Exception as e:
            self.logger.error(f"Error creating table: {str(e)}")
            sys.exit(1)

    def add_entry(self, device_name, battery, light, pressure, temperature):
        if (
            battery is None
            and light is None
            and pressure is None
            and temperature is None
        ):
            self.logger.debug(
                f"Empty data for sensor {device_name}. SKipping..."
            )
            return
        try:
            # Create a session
            session = self.Session()
            # Create a new entry
            new_entry = self.SensorTable(
                device_name=device_name,
                battery=battery,
                light=light,
                pressure=pressure,
                temperature=temperature,
            )
            # Add the new entry to the session
            session.add(new_entry)
            # Commit the transaction
            session.commit()
            self.logger.debug(
                f"New entry for sensor {device_name} added successfully."
            )
        except Exception as e:
            self.logger.error(f"Error adding entry: {str(e)}")
        finally:
            # Close the session
            session.close()
