import argparse
import socket
import os

#usage: python file.py -t {ip or hostname} -p {port(s)} -m {message} -f {filename} 

parser = argparse.ArgumentParser(description="netcat")
target = parser.add_argument("-t", "--target", default="127.0.0.1",  help="ip or hostname")
ports = parser.add_argument("-p", "--ports", nargs="+", type=int)
files = parser.add_argument("-f", "--files", nargs="+", type=str)
messages = parser.add_argument("-m", "--message", nargs="+", type=str)
parser.add_argument("-l", "--listen", action="store_true", help="initiates a listener(TCP)")
parser.add_argument("-zv", "--scan", help="port scanner")
args = parser.parse_args()



def scanner(target,ports):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((target,ports))
            s.send(b"HEAD / HTTP/1.0\r\n\r\n")
            banner = s.recv(1024).decode()
            print(f"open : {ports} -- {banner}")
    except(socket.timeout, ConnectionRefusedError, ConnectionResetError):
        print(f"closed {ports}")

def listener(target,ports):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((target, ports))
        s.listen(10)
        print(f"Listening on : {target} : {ports}")
    
        client, addr = s.accept()
        request = client.recv(1024)
        decoded = request.decode()
        if decoded.startswith("FILE"):
            __, file_name, file_size, _ = decoded.split("\n", 3)
            file_size = int(file_size)
            print(file_name, file_size)

            file = open(file_name , "wb")
            done = False
            is_finished = b""

            while not done:
                data = client.recv(1024)
                print(f"received chunk: {data}")  # see exactly what's arriving
                is_finished += data
                if is_finished.endswith(b"<FINISH>"):
                    file.write(is_finished[:-8])
                    done = True 
            client.send("Ping received".encode())
            print(f"file received from : {addr[0]} : {addr[1]}")
            print(f"Connection from : {addr[0]} : {addr[1]}")
            print(f"Recieved: {decoded}") 
            client.close()
            s.close()
            file.close()

        
        print(f"Connection from : {addr[0]} : {addr[1]}")
        print(f"Recieved: {decoded}") 
        client.close()
        s.close()

def file_sender(target,ports,files):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
        c.connect((target,ports))
        
        location = "text.txt"
        file_obj = open(location, "rb")
        size = os.path.getsize(location)
        name = os.path.basename(location)

        header = f"FILE:\n{name}\n{size}\n"
        c.send(header.encode())


        data = file_obj.read()
        c.sendall(data)
        c.send(b"<FINISH>")

        response = c.recv(1024)
        print(response.decode())
        file_obj.close()
        c.close()

def message_sender(target,ports,messages):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
        c.connect((target,ports))
        message = messages
        c.send(message.encode())
        response = c.recv(1024)
        print(response.decode())

def main():
    if args.scan:
        for port in args.ports:
            scanner(args.target,port)
    elif args.listen:
        listener(args.target,args.ports[0])
    elif args.files:
        file_sender(args.target,args.ports[0],args.files[0])
    else:
        message_sender(args.target,args.ports[0],args.message[0])
if __name__ == "__main__": 
    main()
