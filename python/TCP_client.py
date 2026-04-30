import socket

target_host = '127.0.0.1'
target_port = 9999

while True:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect((target_host, target_port))

    message = input("your message")
    client.send(message.encode())

    response = client.recv(1024)

    print(response.decode())
