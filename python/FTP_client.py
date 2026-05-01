import os
import socket

client = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
client.connect(("localhost", 9999))

file = open("python/text.txt", "rb")
size = os.path.getsize("python/text.txt")
name = "sent_file.txt"

header = f"{name}\n{size}\n"
client.send(header.encode())

data = file.read()
client.sendall(data)
client.send(b"<FINISH>")
file.close()
client.close()



