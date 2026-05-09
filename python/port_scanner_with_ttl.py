import argparse
import socket 
from threading import Lock,Thread
import nvdlib
from scapy.all import *
import re

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
                s.send(b"HEAD / HTTP/1.0\r\n\r\n")
                banner = s.recv(1024)
                banner_decoded = banner.decode(errors="ignore").strip()
                fingerprint = extract_banner(banner_decoded)
                packet = sr1(IP(dst=args.target)/TCP(dport=(port),flags="S"),verbose=0,timeout=1)
                if packet:
                    with lock:
                        cve_lookup(fingerprint)
                        print(f"open : {port}")
                        print(f"TTL: {packet.ttl}")
                        print()
    except (socket.timeout , ConnectionRefusedError , ConnectionResetError , OSError):
        pass

def extract_banner(banner: str):
    banner = banner.lower()
    if not banner:
        return None
    patterns = [
        r"(openssh[_\- ]\d+[\w\.]*)",
        r"(apache/?[\d\.]+)",
        r"(nginx/?[\d\.]+)",
        r"(vsftpd[\d\.]*)",
        r"(proftpd[\d\.]*)",
    ]

    for p in patterns:
        match = re.search(p, banner)
        if match:
            return match.group(0)
        else:
            return banner.split()[0][:50]

def cve_lookup(banner):

    try: 
        if banner == None:
            print("no banner found, skipping CVE lookup")
        else:
            r = nvdlib.searchCVE(keywordSearch=banner , limit=3)
            for eachCVE in r:
                print(f"CVEs found for {banner}, {eachCVE.id}, {str(eachCVE.score[0])}, {eachCVE.url}, {eachCVE.cpe}")
            if not r: 
                print (f"no CVE found for {banner}")

    except Exception as e:    
        print(f"failed {e}")

def main():    
    threads = []

    for port in args.ports:
        t = Thread(target = iterator , args=(args.target , port))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
if __name__ == "__main__":    
    main()