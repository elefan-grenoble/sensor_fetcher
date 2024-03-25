import json
import logging
import os
import ssl
import sys

import paho.mqtt.client as mqtt


class MqttConnector:
    def __init__(self, db_manager) -> None:
        self.db_manager = db_manager

        # Set up logging
        self.logger = logging.getLogger(__name__)

        # Set MQTT parameters from environment variables
        self.mqtt_username = os.environ.get("MQTT_USERNAME")
        self.mqtt_password = os.environ.get("MQTT_PASSWORD")
        self.mqtt_host = os.environ.get("MQTT_HOST")
        self.mqtt_port = int(os.environ.get("MQTT_PORT", 1883))
        self.mqtt_topics = os.getenv("MQTT_TOPICS")
        if not self.mqtt_topics:
            raise ValueError("MQTT_TOPICS not defined in .env file")

        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
        self.client.on_connect = self.__on_connect
        self.client.on_message = self.__on_message
        self.client.username_pw_set(self.mqtt_username, self.mqtt_password)
        ssl_ctx = ssl.create_default_context()
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE
        self.client.tls_set_context(ssl_ctx)

    def __connect_to_mqtt(self):
        try:
            self.client.connect(self.mqtt_host, self.mqtt_port, 60)
            self.logger.info("Connected to MQTT broker")
        except Exception as e:
            self.logger.error(f"Failed to connect to MQTT broker: {e}")
            sys.exit(1)

    # The callback for when the client receives a CONNACK response.
    def __on_connect(self, client, userdata, flags, reason_code):
        if reason_code == 0:
            # Subscribe to multiple topics specified in MQTT_TOPICS
            topics = self.mqtt_topics.split(',')
            for topic in topics:
                client.subscribe(topic.strip())
            self.logger.info("Subscribed to topics: %s", topics)
        else:
            self.logger.error(
                "Failed to connect to MQTT broker with reason code "
                f"{reason_code}"
            )

    # The callback for when a PUBLISH message is received from the server.
    def __on_message(self, client, userdata, msg):
        self.logger.debug(f"Received message: {msg.topic} {str(msg.payload)}")
        try:
            payload = json.loads(msg.payload.decode("utf-8"))
            if "object" in payload:
                obj = payload["object"]
                self.db_manager.add_entry(
                    payload["deviceName"],
                    obj.get("battery"),
                    obj.get("light"),
                    obj.get("pressure"),
                    obj.get("temperature"),
                )
            else:
                self.logger.debug("Payload does not contain required data.")
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")

    def start_fetching(self):
        self.logger.info("Starting MQTT message fetching...")
        self.__connect_to_mqtt()
        self.client.loop_forever()  # Start the MQTT client loop
