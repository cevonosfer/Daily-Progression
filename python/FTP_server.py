import socket

bind_ip = "localhost"
bind_port = 9999

server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen()
print(f"listening on : {bind_ip} : {bind_port}")

client, addr = server.accept()

details = client.recv(1024).decode()
file_name, file_size = details.split("\n")
file_size = int(file_size)
print(file_name, file_size)

file = open(file_name , "wb")

done = False
is_finished = b""

while not done:
    data = client.recv(1024)
    is_finished += data
    if is_finished.endswith(b"<FINISH>"):
        file.write(is_finished)
        done = True

file.close()
client.close()
server.close()
