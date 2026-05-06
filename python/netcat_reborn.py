import argparse
import socket

parser = argparse.ArgumentParser(description="netcat")
host = parser.add_argument("host", help="ip or hostname")
ports = parser.add_argument("-p", "--ports", nargs="+", type=int)
parser.add_argument("-l", help="initiates a listener(TCP)")
parser.add_argument("-lu", help="initiates a listener(UDP)")
parser.add_argument("-zv", help="port scanner")
args = parser.parse_args()



def scanner(host,ports):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host,ports))
            s.send()
            banner = s.recv(1024).decode()
            print(f"open : {ports} -- {banner}")
    except(socket.timeout, ConnectionRefusedError, ConnectionResetError):
        print(f"closed{ports}")

def listener(host,ports):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        bind_ip = host
        bind_port = ports
        s.bind((bind_ip, bind_port))
        s.listen(10)

def listenerUDP(host,ports):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        bind_ip = host
        bind_port = ports
        s.bind((bind_ip, bind_port))
        s.listen(10)

def sender(): #client for sending messages and files#

def main(): #main for the argument conditions and functions#