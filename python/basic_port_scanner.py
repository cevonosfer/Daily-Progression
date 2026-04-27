import argparse
import socket 
from threading import Lock,Thread
import nvdlib

parser = argparse.ArgumentParser(description = "basic tool")
parser.add_argument("target" , help="ip or hostname")
parser.add_argument("-p" ,"--ports" , nargs="+" , type=int , default=[80])
args = parser.parse_args()

lock = Lock()

def iterator(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(3)
            s.connect((host,port))
            s.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
            banner = s.recv(1024).decode()  
            print(f"open : {port} -- {banner}")
            cve_lookup(banner)
    except (socket.timeout , ConnectionRefusedError , ConnectionResetError , OSError):
        print(f"closed : {port}")

def cve_lookup(banner):
    keyword = banner.replace("/", " ").replace("-"," ").replace("_", " ").split("\r\n")[0][:50]
    
    try:
        r = nvdlib.searchCVE(keywordSearch=keyword , limit=3)
        for eachCVE in r:
            print(eachCVE.id, str(eachCVE.score[0]), eachCVE.url, eachCVE.cpe)
        if not r: 
            print (f"no CVE found for {keyword}")

    except Exception as e:    
        print(f"failed {e}")
        
threads = []

for port in args.ports:
    t = Thread(target = iterator , args=(args.target , port))
    threads.append(t)
    t.start()

for t in threads:
    t.join()