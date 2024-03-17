import logging

from dotenv import find_dotenv, load_dotenv

from database_manager import DatabaseManager
from mqtt_connector import MqttConnector

if __name__ == "__main__":
    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())
    # Set the logging level using a variable from .env
    log_level_str = os.getenv("LOG_LEVEL", "DEBUG")
    log_level = getattr(logging, log_level_str.upper())
    # Define the log format string and set the logging level
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=log_level, format=log_fmt)
    # Initialize the database manager
    db_manager = DatabaseManager()
    # Create the table if it doesn't exist
    db_manager.create_table()
    # Initialize the MQTT connector
    mqtt_client = MqttConnector(db_manager)
    # Start fetching data
    mqtt_client.start_fetching()
