# rpi-security-gpio2mqtt

A docker image for reading GPIO input from wired home security sensors & 
publishing a message via MQTT on a sensor detection event. Intended to be used 
on a Raspberry Pi with the 40-pin GPIO header & containerized to Docker for 
easy installation & management.

Getting up and running is fairly simple, but it does have a few hardware & software 
requirements. Also, some basic circuitry wiring is neccessary. Requirements & 
basic instructions are included below.

## Requirements

The software requirements are a much simpler than the hardware, thanks to Docker.

### Software:

Docker on a Linux distribution (tested with Debian-based varities (Ubuntu & Raspbian) 
as well as Alpine, but may work with others).

### Hardware:

At minimum, the following hardware is needed: 

1. Raspberry Pi with a 40-pin GPIO header (tested on a Raspberry Pi Zero v1.3, but
should work just as well on any version from the 1B+ through the newest 4B as well
as the Zero W)
2. A compatible power supply for the Raspberry Pi ([RaspberryPi.org recommends 5V & 2.5A](https://www.raspberrypi.org/documentation/hardware/raspberrypi/power/README.md))
2. A 16GB or larger micro SD card ([more here](https://www.raspberrypi.org/documentation/installation/sd-cards.md))
3. A USB network adapter, either USB to Ethernet (such as [this low-power one from MonoPrice](https://www.monoprice.com/product?c_id=&cp_id=&cs_id=&p_id=9466&sep=1&format=2)),
or a similar wifi adapter.
2. Sensors - So far this can be any of the following types

  - PIR Motion (tested with the HC-SR501)
  - Form A (Normally Open, SPST) Reed Switch (tested with the Honeywell 951WG & the 
  Honeywell 944TRE, but should work with any basic Form A switch)

3. Resistors (anything between 1k & 5k Ohms should work)
3. Wires

For a more complete/complicated setup, it's advisable to have the following:

1. A prototyping board for wiring the sensors to the GPIO pins & building simple circuits
2. Screw terminals to solder to the prototyping board for easier configuration of sensors
3. Both solid-core & stranded core wiring (solid core is easier for use on a breadboard & 
prototyping board, but doesn't work as well for longer runs to sensor installation 
locations due to it's liklihood to break inside the insulation)

Lastly, if you want a setup that's really easy to place the raspberry pi, you can always look 
into Power Over Ethernet or using a Pi Zero W.

## Installation


### Software

The easist path to get the application up & running is to use DockerHub. On a compatible Raspberry Pi 
running Docker on Linux (see requirements above), pull the latest image with

```
$ docker pull rpi-security-gpio2mqtt
```

then run using

```
$ docker run -itd \
    --name rpi-security
    --restart always
    --privileged \
    -v /rpi-security2mqtt/configuration.yaml:/src/configuration.yaml \
    rpi-security-gpio2mqtt
```

This command runs the image in privilaged mode (required for GPIO access) & sets the restart parameter to 
always for better uptime & easier management. It also maps the configuration file to a root folder for the 
application (any location can be used, just change the part after `-v ` to the path of your choosing like 
this `-v SOME/PATH/FILE.yaml:/src/configuration.yaml`). Mapping the configuration file to a volume allows 
for editing of the file & restarting the container to implement changes.

Lastly, you'll need to edit the host copy (located at the first half of the volume declaration you specified
at `docker run ... -v`). The first part to change is your MQTT settings; you'll need to tell the application 
your MQTT host address & port number, the MQTT username & password (if using), & (optionally) the root topic 
you want all the sensor's data to be published on.

```
mqtt_host: "host.address.here"    # must be a string, defaults to 127.0.0.1, or localhost
mqtt_port: 1111                   # must be a number, defaults to 1883
mqtt_user: "username"             # string, defaults to not being set
mqtt_pass: "password"             # string, defaults to not being set
root_topic: "/some/topic/"        # string, the last '/' is required, defaults to /security/sensors/
```

In addition to MQTT configuration, you'll need to set up the sensors. They are organized by group, like this:

```
sensor_groups:
    a_group:
        # ... sensors go here
    another_group:
        # ... more sensors here
```

which will cause them to broadcast on a sub topic specific to their group, (e.g. `/security/sensors/a_group` 
or `/security/sensors/another_group` in the example above). Then individual sensors are added to the groups 
as a sequence, like this:

```
    a_group:
      - name: "sensor_name"
        type: # ... can be any of the supported types (see the Sensor Types section near the end of this README)
        pin: # an integer corresponding the the GPIO input the sensor will be wired to
      - name: "another_sensor"
        type: # ...
        pin: 11
        # ... and continues like above for each sensor
```

### Hardware

Of course, having the application running in Docker on the Pi is useless without having the sensors wired up. 
Instructions for each currently supported type is below.
