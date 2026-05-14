import argparse
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
import socket
import re
import nvdlib
from scapy.all import IP,TCP,sr1

parser = argparse.ArgumentParser(description = "basic tool")
parser.add_argument("-t", "--target", help="ip or hostname" )
parser.add_argument("-p", "--port", help="port(s)")
parser.add_argument("-o", "--detect", action="store_true", help="enable os detection")
parser.add_argument("-c", "--cve", action="store_true", help="enable cve lookup")
parser.add_argument("-b", "--banner", action="store_true", help="enable banner grab")
args = parser.parse_args()

lock = Lock()

PROBES = { #for ports that requires a request
    80: b"HEAD / HTTP/1.0\r\n\r\n",
    #port
    #port
    #port
    #...
}

def port_range(port):

    ports = []

    if "-" in port:

        start,end = map(int,port.split("-"))
        ports.extend(range(start,end+1) )
    elif " " in port:
        ports.extend(map(int, port.split(",")))
    else:
        ports.append(int(port))
    if start < 1 or end > 65535:
        raise ValueError("invalid port range")

    return ports

def port_scan(host,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.settimeout(2)
        if s.connect_ex((host,port)) == 0:
            return True
        else:
            return False
    except (socket.timeout , ConnectionRefusedError , ConnectionResetError , OSError):
        return False

def banner_grab(host,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    patterns = [
        r"(openssh[_\- ]\d+[\w\.]*)",
        r"(apache/?[\d\.]+)",
        r"(nginx/?[\d\.]+)",
        r"(vsftpd[\d\.]*)",
        r"(proftpd[\d\.]*)",
    ]
    
    try:
        s.settimeout(2)
        s.connect((host, port))
        if port in PROBES:
            s.send(PROBES.get(port))
        
        raw_banner = s.recv(1024)
        banner = raw_banner.decode(errors="ignore").strip()
        banner = banner.lower()
        s.close()
        if banner is None:
            return None
        else:
            for p in patterns:
                match = re.search(p, banner)
                if match:
                    return match.group(0)
            return banner.split()[0][:50]
        
    except (socket.timeout , ConnectionRefusedError , ConnectionResetError , OSError):
        return None 

def TTL_time(port):
    packet = sr1(IP(dst=args.target)/TCP(dport=(port),flags="S"),verbose=0,timeout=1)
    if packet and packet.haslayer(IP):
        return packet[IP].ttl
    else:
        return None   

def cve_lookup(banner):
    try:
        if banner == None:
            return ["no banner found, skipping CVE lookup"]
        else:
            r = nvdlib.searchCVE(keywordSearch=banner , limit=3)
            for eachCVE in r:
                return[f"CVEs found for {banner}, {eachCVE.id}, {str(eachCVE.score[0])}, {eachCVE.url}, {eachCVE.cpe}"]
            if not r: 
                return [f"no CVE found for {banner}"]

    except Exception as e:   
        return ["CVE lookup failed"]

#def alerts():
#def utils():
#These will be for transforming this to a discord bot

def pseudo_main(host,port):
    output = {
        "port": port,
        "state": "closed",
        "banner": None,
        "ttl": None,
        "os": None,
        "cves": []
    }

    if port_scan(host,port) == True:
        output["state"] = "open"
        if args.banner:
            banner = banner_grab(host, port)
            if banner:
                output["banner"] = banner
            else:
                output["banner"] = "N/A"
        if args.detect:
            ttl = TTL_time(port)
            output["ttl"] = ttl
            if ttl is None:
                output["ttl"] = "N/A"
            elif ttl <= 64:
                output["os"] = "linux"
            elif ttl <= 128:
                output["os"] = "windows"
            else:
                output["os"] = "network device"
        if args.cve:
            output["cves"] = cve_lookup(output["banner"])
    return output

def main():
    ports = port_range(args.port)
    with ThreadPoolExecutor(max_workers=10) as executor:
        output = list(executor.map(pseudo_main,
                     [args.target] * len(ports),
                     ports))
    for r in output:
        if r["state"] == "open":

            print(f"\nPort: {r['port']}")
            print(f"State: {r['state']}")

            if args.banner:
                print(f"Banner: {r['banner']}")

            if args.detect:
                print(f"TTL: {r['ttl']}")
                print(f"OS Guess: {r['os']}")

            if args.cve:
                print("CVEs:")

                for cve in r["cves"]:
                    print(f"  {cve}")

            print("-" * 40)

if __name__ == "__main__": 
    main()