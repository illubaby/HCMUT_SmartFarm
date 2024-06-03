import serial.tools.list_ports

# List all available ports
ports = serial.tools.list_ports.comports()
for port in ports:
    print(port)
