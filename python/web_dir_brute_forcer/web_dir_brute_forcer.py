import requests
from concurrent.futures import ThreadPoolExecutor
import asyncio
import aiohttp
import time 


BASE_URL = "http://scanme.nmap.org"
WORDLIST_FILE = "python\web_dir_brute_forcer\wordlist.txt"

found_paths = []

def load_words():
    with open(WORDLIST_FILE, "r") as f:
        words = []

        for line in f:
            line = line.strip()
            if line:
                words.append(line)
        return words

async def check_path(session: aiohttp.ClientSession, path, sem):
    url = f"{BASE_URL}/{path}"
    async with sem:
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as r:

                if r.status in [200, 301, 302, 403]: #useful codes 200:ok , 301,302:redirect , 403:exists but denied
                    print(f"{r.status} :: {url}")
                    found_paths.append((url, r.status))

        except requests.RequestException:
            print(f"error :: {url}")

async def main():
    start = time.perf_counter()
    words = load_words()

    print(f"starting scan on {BASE_URL}")
    print(f"loaded {len(words)} paths\n")

    sem = asyncio.Semaphore(100)

    async with aiohttp.ClientSession() as session:
        tasks = [check_path(session, word, sem) for word in words]
        await asyncio.gather(*tasks)

    print(f"Found {len(found_paths)} interesting paths")
    for url, code in found_paths:
        if code != 404:
            print(f"{code} :: {url}")
    print(f"\nScan completed in {time.perf_counter() - start:.2f}s")

if __name__ == "__main__":
    asyncio.run(main())