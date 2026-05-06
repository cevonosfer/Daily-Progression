import argparse
import socket
import os

parser = argparse.ArgumentParser(description="netcat")
target = parser.add_argument("-t", help="ip or hostname")
ports = parser.add_argument("-p", "--ports", nargs="+", type=int)
files = parser.add_argument("-f", "--files", nargs="+", type=str)
messages = parser.add_argument("-m", "--message", nargs="+", type=str)
parser.add_argument("-l", action="store_true", help="initiates a listener(TCP)")
parser.add_argument("-zv", help="port scanner")
args = parser.parse_args()



def scanner(target,ports):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((target,ports))
            s.send(b"HEAD / HTTP/1.0\r\n\r\n")
            banner = s.recv(1024).decode()
            print(f"open : {ports} -- {banner}")
    except(socket.timeout, ConnectionRefusedError, ConnectionResetError):
        print(f"closed{ports}")

def listener(target,ports):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((target, ports))
        s.listen(10)
        print(f"Listening on : {target} : {ports}")

    while True:     
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
                    file.write(is_finished)
                    done = True 
            print(f"file received from : {addr[0]} : {addr[1]}")
            client.close()
            file.close()

        print(f"Connection from : {addr[0]} : {addr[1]}")
        print(f"Recieved: {decoded}") 
        client.send("Ping received".encode()) 
        client.close()

def sender(target,ports,files,messages):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
        c.connect((target,ports))

        if files:
            location = os.path.abspath(files)
            files = open(location, "rb")
            size = os.path.getsize(files)
            name = files

            header = f"{name}\n{size}\n"
            c.send(header.encode())

            data = files.read()
            c.sendall(data)
            c.send(b"<FINISH>")
            files.close()
            c.close()

        message = messages
        c.send(message.encode())
        response = c.recv(1024)
        print(response.decode())


def main(): #main for the argument conditions and functions#