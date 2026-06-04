import paramiko
import socket
import threading

# ─── credentials (add more to test) ─────────────────────────
VALID_CREDENTIALS = {
    "admin": "admin123",
    "root":  "toor",
    "admin":  "password",
}

HOST = "127.0.0.1"
PORT = 2222

# ─── generate host key (run once, reuse after) ───────────────
HOST_KEY = paramiko.RSAKey.generate(2048)

class SSHHandler(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if VALID_CREDENTIALS.get(username) == password:
            print(f"[+] successful login → {username}:{password}")
            return paramiko.AUTH_SUCCESSFUL
        print(f"[-] failed attempt  → {username}:{password}")
        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        return "password"

def handle_client(client_socket):
    transport = paramiko.Transport(client_socket)
    transport.add_server_key(HOST_KEY)
    handler = SSHHandler()
    try:
        transport.start_server(server=handler)
        channel = transport.accept(timeout=5)
        if channel:
            channel.close()
    except Exception:
        pass
    finally:
        transport.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(100)

    print(f"SSH test server running on {HOST}:{PORT}")
    print(f"Valid credentials: {VALID_CREDENTIALS}\n")

    while True:
        client, addr = server_socket.accept()
        print(f"[*] connection from {addr[0]}:{addr[1]}")
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    main()