import argparse
import socket 

parser = argparse.ArgumentParser(description = "basic tool")
parser.add_argument("target" , help="ip or hostname")
parser.add_argument("-p" ,"--ports" , nargs="+" , type=int , default=[80])
args = parser.parse_args()


def iterator(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(3)
            s.connect((host,port))
            s.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
            banner = s.recv(1024)    
            print(f"open : {port} -- {banner[:80][:22]}")
    except (socket.timeout , ConnectionRefusedError , ConnectionResetError , OSError):
        print(f"closed : {port}")

for port in args.ports:
    iterator(args.target , port)

