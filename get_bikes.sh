#!/bin/bash
#*/10 * * * * /home/pi/bikes/./get_bikes.sh

/usr/bin/wget -q https://shared-mobility.ethz.ch/api/live -O /home/pi/bikes/data/$(date -d "today" +"%Y%m%d_%H%M%S").geojson
