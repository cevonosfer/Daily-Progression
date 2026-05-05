import socket
import caesar

target_host = '127.0.0.1'
target_port = 9999

while True:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect((target_host, target_port))

    message = input("your message")
    encrypted = caesar.caesar_enc(shift=5,raw_text=message)
    client.send(encrypted.encode())

    response = client.recv(1024)

    print(response.decode())
