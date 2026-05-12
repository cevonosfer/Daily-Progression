import argparse
import socket
import re
import nvdlib
from scapy.all import IP,TCP,sr1




parser = argparse.ArgumentParser(description = "basic tool")
parser.add_argument("-t", "--target", help="ip or hostname" )
parser.add_argument("-p", "--port", nargs="+", type=int, help="port(s)")
parser.add_argument("-o", "--detect", action="store_true", help="enable os detection")
parser.add_argument("-c", "--cve", action="store_true", help="enable cve lookup")
parser.add_argument("-b", "--banner", action="store_true", help="enable banner grab")
args = parser.parse_args()



PROBES = { #for ports that requires a request
    80: b"HEAD / HTTP/1.0\r\n\r\n",
    #port
    #port
    #port
    #...
}

def port_scan(host,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.settimeout(2)
        if s.connect_ex((host,port)) == 0:
                print(f"Open: {port}")
        else:
                print(f"Closed: {port}")
        s.close()
    except (socket.timeout , ConnectionRefusedError , ConnectionResetError , OSError):
        pass

def banner_grab(host,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.settimeout(2)
        s.connect((host, port))
        if port in PROBES:
            s.send(PROBES.get(port))
        
        banner = s.recv(1024)
        s.close()
        return banner.decode(errors="ignore").strip()
    except (socket.timeout , ConnectionRefusedError , ConnectionResetError , OSError):
        return None 

def banner_extract(banner):
    if banner is None:
        return None
    banner = banner.lower()
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
        
    return banner.split()[0][:50]

def TTL_time(port):
    packet = sr1(IP(dst=args.target)/TCP(dport=(port),flags="S"),verbose=0,timeout=1)
    if packet and packet.haslayer(IP):
        return packet[IP].ttl
    else:
        return None
    
def os_guess(ttl):
    
        if ttl is None:
            print("TTL not found")
        elif ttl <= 64:
            print(f"TTL: {ttl} //Likely Linux/Unix")
        elif ttl <= 128:
            print(f"TTL: {ttl} //Likely Windows")
        else:
            print(f"TTL: {ttl} //Likely network device")  

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

#def alerts():
#def utils():
#These will be for transforming this to a discord bot


def main():
    for port in args.port:
        port_scan(args.target,port)
        raw_banner = banner_grab(args.target, port)
        if raw_banner:
            banner = banner_extract(raw_banner)
        else:
            banner = None
        if args.banner:
            if banner:
                    print(banner)
            else:
                    print("banner not found")
        if args.detect:
            os_guess(TTL_time(port))
        if args.cve:
            cve_lookup(banner)

if __name__ == "__main__": 
    main()