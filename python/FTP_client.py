import os
import socket

client = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
client.connect(("localhost", 9999))

file = open("python/text.txt" , "rb")
size = os.path.getsize("python/text.txt")

details = f"received_text.txt\n{size}"
client.send(details.encode())

data = file.read()
client.sendall(data)
client.send(b"<FINISH>")
file.close()
client.close()



