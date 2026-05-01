import socket
import threading
import tqdm

bind_ip = "localhost"
bind_port = 9999

server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen()
print(f"listening on : {bind_ip} : {bind_port}")


def handle_client(client,addr):
    header = client.recv(1024).decode()
    file_name, file_size, _ = header.split("\n", 2)
    file_size = int(file_size)
    print(file_name, file_size)
    bar = tqdm.tqdm(iterable=True, total=int(file_size), unit='B')

    file = open(file_name , "wb")
    done = False
    is_finished = b""

    while not done:
        data = client.recv(1024)
        print(f"received chunk: {data}")  # see exactly what's arriving
        is_finished += data
        bar.update(1024)
        if is_finished.endswith(b"<FINISH>"):
            file.write(is_finished)
            done = True 
    print(f"file received from : {addr[0]} : {addr[1]}")
    client.close()
    file.close()

while True:
    client, addr = server.accept()
    handler = threading.Thread(target=handle_client,args=(client,addr))
    handler.start()
