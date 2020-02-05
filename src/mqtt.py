import time
import socket
import paho.mqtt.client as mqtt

import utils

class MqttHelper:
    def __init__(self, host, port):
        mqtt.Client.connected_flag = False # creates connection flag for looping
        self._client = mqtt.Client(socket.gethostname())
        self._client.on_connect = self._on_connect # binding client connection callback to above fn
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

    def __getattr__(self, attr):
        return getattr(self._client, attr)
