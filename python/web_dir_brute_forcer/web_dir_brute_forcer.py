import requests
from concurrent.futures import ThreadPoolExecutor


BASE_URL = "http://127.0.0.1:8000"
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

def check_path(path):
    url = f"{BASE_URL}/{path}"

    try:
        r = requests.get(url, timeout=2)

        if r.status_code in [200, 301, 302, 403]: #useful codes 200:ok , 301,302:redirect , 403:exists but denied
            print(f"{r.status_code} :: {url}")
            found_paths.append((url, r.status_code))

        else:
            print(f"{r.status_code} :: {url}")

    except requests.RequestException:
        print(f"error :: {url}")

def main():
    words = load_words()

    print(f"starting scan on {BASE_URL}")
    print(f"loaded {len(words)} paths\n")

    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(check_path, words)

    print(f"Found {len(found_paths)} interesting paths")
    print(f"found URLs : {found_paths}")

if __name__ == "__main__":
    main()