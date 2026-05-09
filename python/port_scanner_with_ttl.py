import argparse
import socket 
from threading import Lock,Thread
import nvdlib
from scapy.all import *

parser = argparse.ArgumentParser(description = "basic tool")
parser.add_argument("target" , help="ip or hostname")
parser.add_argument("-p" ,"--ports" , nargs="+" , type=int)
args = parser.parse_args()

lock = Lock()

def iterator(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            if s.connect_ex((host,port)) == 0:
                print(f"open : {port}")
                packet = sr1(IP(dst=args.target)/TCP(dport=(port),flags="S"),verbose=0,timeout=1)
                if packet:
                    print(f"TTL: {packet.ttl}")
                
                #cve_lookup(banner)
    except (socket.timeout , ConnectionRefusedError , ConnectionResetError , OSError):
        pass


# def cve_lookup(banner):
#    keyword = banner.replace("/", " ").replace("-"," ").replace("_", " ").split("\r\n")[0][:50]
#
#    try:
#        r = nvdlib.searchCVE(keywordSearch=keyword , limit=3)
#        for eachCVE in r:
#            print(eachCVE.id, str(eachCVE.score[0]), eachCVE.url, eachCVE.cpe)
#        if not r: 
#            print (f"no CVE found for {keyword}")
#
#    except Exception as e:    
#        print(f"failed {e}")
        
threads = []

for port in args.ports:
    t = Thread(target = iterator , args=(args.target , port))
    threads.append(t)
    t.start()

for t in threads:
    t.join()