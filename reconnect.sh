#!/bin/bash

#Reiniciar la conexion a internet

ifdown wlan0
ip a flush wlan0
ifup wlan0
dhclient wlan0
iwconfig

