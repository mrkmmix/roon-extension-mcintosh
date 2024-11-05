#!/usr/bin/env python3

import serial
import time

def main():
    serial_port = '/dev/ttyUSB1'
    baud_rate = 9600

    try:
        ser = serial.Serial(
            port=serial_port,
            baudrate=baud_rate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=2,          # Read timeout in seconds
            write_timeout=2,    # Write timeout in seconds
            xonxoff=False,      # Disable software flow control
            rtscts=False,       # Disable hardware flow control
            dsrdtr=False        # Disable hardware flow control
        )

        # Clear buffers to remove any residual data
        ser.reset_input_buffer()
        ser.reset_output_buffer()

        # Send 'GET_SYS_MODE' command with proper line terminator
        ser.write(b'GET_SYS_MODE\r\n')
        ser.flush()  # Ensure command is sent

        # Read echoed command
        echoed_command = ser.readline().decode('ascii', errors='replace').strip()
        print(f"Echoed command: {echoed_command}")

        # Read actual response
        response = ser.readline().decode('ascii', errors='replace').strip()
        print(f"Device response: {response}")

        # Check if the response is the expected one
        if response == "NORMAL_MODE!":
            # Send the next command
            ser.write(b'SET_XLR_NA_RCA_MONO\r\n')
            ser.flush()
            print("Sent command: SET_XLR_NA_RCA_MONO")

            # Optionally, read echoed command and response
            echoed_command = ser.read_all().decode('ascii', errors='replace').strip()
            print(f"Received: {echoed_command}")
        else:
            print("Unexpected response from device.")

    except serial.SerialException as e:
        print(f"Serial communication error: {e}")
    finally:
        ser.close()

if __name__ == '__main__':
    main()
