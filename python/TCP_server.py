import socket 
import threading 
import caesar

bind_ip = "0.0.0.0" 
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind((bind_ip, bind_port)) 
server.listen(5) 

print(f"Listening on : {bind_ip} : {bind_port}")                            

def handle(client_socket): 
    request = client_socket.recv(1024)
    decoded = request.decode()
    d_request = caesar.caesar_dec(shift=5,raw_text=decoded) 
    print(f"Recieved: {d_request}") 
    client_socket.send("Ping received".encode()) 
    client_socket.close()

while True: 
    client, addr = server.accept() 
    print(f"Connection from: {addr[0]}:{addr[1]}")
    client_handler = threading.Thread(target=handle, args=(client,))
    client_handler.start()