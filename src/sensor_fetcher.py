import logging

from dotenv import find_dotenv, load_dotenv

from database_manager import DatabaseManager
from mqtt_connector import MqttConnector

if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=log_fmt)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())
    # Initialize the database manager
    db_manager = DatabaseManager()
    # Create the table if it doesn't exist
    db_manager.create_table()
    # Initialize the MQTT connector
    mqtt_client = MqttConnector(db_manager)
    # Start fetching data
    mqtt_client.start_fetching()
