import argparse
import asyncio
import socket
import re
import nvdlib
from scapy.all import IP,TCP,sr1,ICMP,send
import time 

parser = argparse.ArgumentParser(description = "basic tool")
parser.add_argument("-t", "--target", help="ip or hostname" )
parser.add_argument("-p", "--port", help="port(s)")
parser.add_argument("-o", "--detect", action="store_true", help="enable os detection")
parser.add_argument("-c", "--cve", action="store_true", help="enable cve lookup")
parser.add_argument("-b", "--banner", action="store_true", help="enable banner grab")
parser.add_argument("-s", "--threads", help="thread count", type=int, default=20)
args = parser.parse_args()

PROBES = { #for ports that requires a request
    80: b"HEAD / HTTP/1.0\r\n\r\n",
    21: b"USER anonymous\r\n",
    25: b"EHLO example.com\r\n",
    143: b"A001 CAPABILITY\r\n",
    6379: b"PING\r\n",
    "generic": b"\r\n",
}

def port_range(port):

    ports = []

    if "-" in port:
        start,end = map(int,port.split("-"))
        ports.extend(range(start,end+1) )
    elif "," in port:
        ports.extend(map(int, port.split(",")))
    else:
        ports.append(int(port))
    for p in ports:
        if p < 1 or p > 65535:
            raise ValueError("invalid port")
    return ports

def is_host_up(host):
    packet = sr1(IP(dst=host)/ICMP(),timeout=0.5) #ping the host to see its up 
    if packet == None:
        return {"host": "down"}
    else:
        return {"host": "up"}

async def port_scan(host,port):
    try:
        packet = await asyncio.to_thread(sr1, IP(dst=host)/TCP(dport=port, flags="S"),timeout=1,verbose=0)
        if packet is None:
            return {"state": "filtered"}
        if packet.haslayer(TCP):
            flags = packet[TCP].flags
            if flags == 0x12: #SYN-ACK
                await asyncio.to_thread(send, IP(dst=host) /TCP(dport=port, flags="R"),verbose=0) # send RST to close half open ports
                return {"state": "open"}
            elif flags == 0x14: #RST-ACK 
                return {"state": " closed"}
        return {"state": "unknown"}
    except (socket.timeout , ConnectionRefusedError , ConnectionResetError , OSError):
        return {"state": "closed"}

async def banner_grab(host,port):
    def grab():
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
            else:
                s.send(PROBES.get("generic"))
            
            raw_banner = s.recv(1024)
            banner = raw_banner.decode(errors="ignore").strip()
            banner = banner.lower()
            s.close()
            if not banner:
                return None
            else:
                for p in patterns:
                    match = re.search(p, banner)
                    if match:
                        return {"banner": match.group(0)}
                return {"banner": banner.split()[0][:50]}
            
        except (socket.timeout , ConnectionRefusedError , ConnectionResetError , OSError):
            return None 
    return await asyncio.to_thread(grab)

async def TTL_time(port):
    packet = await asyncio.to_thread(sr1, IP(dst=args.target)/TCP(dport=(port),flags="S"),verbose=0,timeout=1)
    if packet and packet.haslayer(IP):
        return {"ttl": packet[IP].ttl}
    else:
        return None  

async def cve_lookup(banner):
    try:
        if banner == None:
            return {"cves": "no banner found, skipping CVE lookup"}
        else:
            r = nvdlib.searchCVE(keywordSearch=banner , limit=3)
            for eachCVE in r:
                return {"cves": f"CVEs found for {banner}, {eachCVE.id}, {str(eachCVE.score[0])}, {eachCVE.url}, {eachCVE.cpe}"}
            if not r: 
                return {"cves": f"no CVE found for {banner}"}

    except Exception as e:   
        return {"cves": "CVE lookup failed"}

#def alerts():
#def utils():
#These will be for transforming this to a discord bot

async def pseudo_main(host,port,sem):
    output = {
        "host": host,
        "port": port,
        "state": "closed",
        "banner": None,
        "ttl": None,
        "os": None,
        "cves": []
    }
    
    async with sem:
        port_result = await port_scan(host,port)
        output.update(port_result)

        if output["state"] == "open":
            if args.banner:
                banner_result = await banner_grab(host, port)
                if banner_result:
                    output.update(banner_result)
                else:
                    output["banner"] = "N/A"
            if args.detect:
                ttl_result = await TTL_time(port)
                output.update(ttl_result)
                ttl = output["ttl"]
                if ttl == None:
                    output["ttl"] = "N/A"
                elif ttl <= 64:
                    output["os"] = "linux"
                elif ttl <= 128:
                    output["os"] = "windows"
                else:
                    output["os"] = "network device"
            if args.cve:
                cve_result = await cve_lookup(output["banner"])
                output.update(cve_result)
    return output

async def main():
    start = time.perf_counter()
    ports = port_range(args.port)
    sem = asyncio.Semaphore(args.threads)
    tasks = [pseudo_main(args.target, p, sem) for p in ports]
    output = await asyncio.gather(*tasks)

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
                print(r["cves"])

            print("-" * 40)
    print(f"\nScan completed in {time.perf_counter() - start:.2f}s")

if __name__ == "__main__": 
    asyncio.run(main())