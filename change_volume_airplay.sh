#!/bin/bash

# Check if an argument is provided
if [ -z "$1" ]; then
    echo "Error: No volume argument provided."
    exit 1
fi

# Get the input volume from the first argument
input_volume="$1"

# Special case: If the input is -144, set volume to 0
if [ "$input_volume" == "-144" ]; then
    volume=0
else
    # Validate that the input is a number
    if ! [[ "$input_volume" =~ ^-?[0-9]+(\.[0-9]+)?$ ]]; then
        logger -p user.warning "Error: Volume argument must be a number between -30 and 0, or -144, received $input_volume"
        exit 1
    fi

    # Check if the input is between -30 and 0
    if (( $(echo "$input_volume < -30" | bc -l) )) || (( $(echo "$input_volume > 0" | bc -l) )); then
        logger -p user.warning "Warning: Volume argument must be between -30 and 0, or -144, received $input_volume"
        exit 1
    fi

    # Calculate the volume using linear mapping
    # volume = (input_volume + 30) * (65 / 30)
    volume=$(echo "scale=2; (($input_volume + 30) * (65 / 30))" | bc)

    # Round the volume to the nearest whole number
    volume=$(printf "%.0f" "$volume")
fi

# Send the message to /dev/ttyUSB0
echo "(VOL $volume)" > /dev/ttyUSB0
