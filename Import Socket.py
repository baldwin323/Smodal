import socket  # Set the target host and port host = 'localhost' port = 8000  # Create a socket object client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  try:     # Connect to the server     client_socket.connect((host, port))     print('Connected to', host, 'on port', port)          # Perform your tasks with the connection     # For example, you can send and receive data      except ConnectionError as e:     print('Connection error:', str(e))  # Close the socket client_socket.close()message_parts = [
    "This script does not work on Python {}.{}".format(*this_python),
    "The minimum supported Python version is {}.{}.".format(*min_version),
    "Please use https://bootstrap.pypa.io/pip/{}.{}/get-pip.py "
    "instead.".format(*this_python),
]
for message_part in message_parts:
    print(message_part)