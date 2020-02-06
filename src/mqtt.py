import time
import socket
import paho.mqtt.client as mqtt

from src import utils


class MqttHelper:
    def __init__(self, host, port):
        # create connection flag for looping
        mqtt.Client.connected_flag = False
        self._client = mqtt.Client(socket.gethostname())
        # binding client connection callback to above fn
        self._client.on_connect = self._on_connect
        self._MQTT_HOST = host
        self._MQTT_PORT = port

    def connect(self):
        self._client.loop_start()
        utils.log(
            "Attempting to establish connection to MQTT Host @ "
            "{MQTT_HOST}:{MQTT_PORT}"
            .format(
                MQTT_HOST=self._MQTT_HOST,
                MQTT_PORT=self._MQTT_PORT))

        self._client.connect(self._MQTT_HOST, self._MQTT_PORT)
        while not self._client.connected_flag:
            utils.log("Waiting for connection")
            time.sleep(1)

        return self

    def disconnect(self):
        utils.log("Disconnecting MQTT client...")
        self._client.loop_stop()
        self._client.disconnect()
        self._client.connected_flag = False
        utils.log("MQTT client disonnected")

        return self

    def _on_connect(self, client, _userdata, _flags, rc):
        if rc == 0:
            client.connected_flag = True
            utils.log(
                "Connection established to MQTT Host @ "
                "{MQTT_HOST}:{MQTT_PORT}"
                .format(
                    MQTT_HOST=self._MQTT_HOST,
                    MQTT_PORT=self._MQTT_PORT))
        else:
            utils.log(
                "Connection failed to MQTT Host @ "
                "{MQTT_HOST}:{MQTT_PORT}"
                .format(
                    MQTT_HOST=self._MQTT_HOST,
                    MQTT_PORT=self._MQTT_PORT))

            utils.log("Failure reason code: {rc}".format(rc=rc))

    def publish(self, topic: str, payload: str, retain: bool = True):
        return self._client.publish(topic, payload, retain)

    # def __getattr__(self, attr):
    #     return getattr(self._client, attr)
