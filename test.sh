#!/usr/bin/bash
watch -n1 'vcgencmd measure_temp; cat /sys/devices/platform/cooling_fan/hwmon/*/fan1_input'