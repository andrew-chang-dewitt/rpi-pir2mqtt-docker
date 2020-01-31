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
2. A compatible power supply for the Raspberry Pi ([RaspberryPi.org recommends 5V & 2.5A]
(https://www.raspberrypi.org/documentation/hardware/raspberrypi/power/README.md))
2. A 16GB or larger micro SD card ([more here]
(https://www.raspberrypi.org/documentation/installation/sd-cards.md))
3. A USB network adapter, either USB to Ethernet (such as [this low-power one from MonoPrice]
(https://www.monoprice.com/product?c_id=&cp_id=&cs_id=&p_id=9466&sep=1&format=2)), or a 
similar wifi adapter.
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

Lastly, if you want a setup that's really easy to place the raspberry pi, you can always look into Power Over 
Ethernet or using a Pi Zero W.
