"""A wrapper on paho-mqtt; handles connections & publishing messages.

Classes:
    MqttHelper -- A simplified wrapper on paho-mqtt.
"""
import time
import socket
import paho.mqtt.client as mqtt

from src import utils


class MqttHelper:
    """A simplified wrapper on paho-mqtt methods.

    Methods:
        connect    -- Establish an mqtt.Client connection.
        disconnect -- Disconnect the Client created by `connect`.
        publish    -- Exposes paho-mqtt's `Client.publish` method directly.
    """

    def __init__(self,
                 host: str,
                 port: int,
                 mqtt_user: str = None,
                 mqtt_pass: str = None,):
        """Init MqttHelper instance with given host address & port number."""
        # create connection flag for looping
        mqtt.Client.connected_flag = False
        self.__client = mqtt.Client(socket.gethostname())
        # binding client connection callback to above fn
        self.__client.on_connect = self.__on_connect
        self.__mqtt_host = host
        self.__mqtt_port = port

        if mqtt_user is not None and mqtt_pass is not None:
            self.__client.username_pw_set(mqtt_user, mqtt_pass)

    def connect(self) -> 'MqttHelper':
        """Establish an mqtt.Client connection."""
        self.__client.loop_start()
        utils.log(
            "Attempting to establish connection to MQTT Host @ "
            "{mqtt_host}:{mqtt_port}"
            .format(
                mqtt_host=self.__mqtt_host,
                mqtt_port=self.__mqtt_port))

        self.__client.connect(self.__mqtt_host, self.__mqtt_port)
        while not self.__client.connected_flag:
            utils.log("Waiting for connection")
            time.sleep(1)

        return self

    def disconnect(self) -> None:
        """Disconnect the Client created by `connect`."""
        utils.log("Disconnecting MQTT client...")
        self.__client.loop_stop()
        self.__client.disconnect()
        self.__client.connected_flag = False
        utils.log("MQTT client disonnected")

    def publish(self, topic: str, payload: str):
        """Exposes paho-mqtt's `Client.publish` method directly."""
        return self.__client.publish(topic, payload, qos=1, retain=True)

    def will_set(self, topic: str, payload: str):
        """Exposes paho-mqtt's `Client.will_set` method directly."""
        return self.__client.will_set(topic, payload, qos=1, retain=True)

    def __on_connect(self, client, _userdata, _flags, reason_code):
        if reason_code == 0:
            client.connected_flag = True
            utils.log(
                "Connection established to MQTT Host @ "
                "{mqtt_host}:{mqtt_port}"
                .format(
                    mqtt_host=self.__mqtt_host,
                    mqtt_port=self.__mqtt_port))
        else:
            utils.log(
                "Connection failed to MQTT Host @ "
                "{mqtt_host}:{mqtt_port}"
                .format(
                    mqtt_host=self.__mqtt_host,
                    mqtt_port=self.__mqtt_port))

            utils.log(
                "Failure reason code: {reason_code}"
                .format(reason_code=reason_code))
