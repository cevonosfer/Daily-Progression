import asyncio
import aiohttp
import time 
import argparse

parser = argparse.ArgumentParser(description="recursive web dir brute forcer")
parser.add_argument("-u", "--url", help="base url")
parser.add_argument("-w", "--wordlist", help="wordlist file")
parser.add_argument("-d", "--depth", help="recursiveness depth", type=int, default=1)
args = parser.parse_args()

BASE_URL = "http://scanme.nmap.org"
WORDLIST_FILE = "python\wordlist\web_dir_wordlist.txt"

found_paths = []
visited = set()

def load_paths():
    with open(WORDLIST_FILE, "r") as f:
        paths = []

        for line in f:
            line = line.strip()
            if line:
                paths.append(line)
        return paths

async def check_path(session: aiohttp.ClientSession, url, sem):
    async with sem:
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as r:
                if r.status in [200, 301, 302, 403]: #useful codes 200:ok , 301,302:redirect , 403:exists but denied
                    found_paths.append((url, r.status))
                    return url
                return None
        except (aiohttp.ClientError,asyncio.TimeoutError):
            return None

async def scan(session, base_url, paths, sem, depth):
    if depth == 0 or base_url in visited:
        return
    visited.add(base_url)
    tasks = [check_path(session, f"{base_url}/{p}", sem) for p in paths]
    results = await asyncio.gather(*tasks)
    
    # results is a list like [None, "/admin", None, "/login", None...]
    # filter out the Nones
    found = [r for r in results if r is not None]
    
    # recurse into each found path
    for url in found:
        await scan(session, url, paths, sem, depth - 1)


async def main():
    start = time.perf_counter()
    paths = load_paths()

    print(f"starting scan on {BASE_URL}")
    print(f"loaded {len(paths)} paths\n")

    sem = asyncio.Semaphore(150)

    async with aiohttp.ClientSession() as session:
        await scan(session, BASE_URL, paths, sem, args.depth)

    print(f"Found {len(found_paths)} interesting paths")
    with open("python/web_dir_brute_forcer/saved.txt", "w") as f:
        for url, code in found_paths:
            f.write(f"{code} :: {url}\n")
    
    print(f"\nScan completed in {time.perf_counter() - start:.2f}s")

if __name__ == "__main__":
    asyncio.run(main())