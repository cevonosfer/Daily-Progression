from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import os

authorizer = DummyAuthorizer()

# Test account
authorizer.add_user(
    "admin",
    "password",
    os.getcwd(),
    perm="elradfmwMT"
)

handler = FTPHandler
handler.authorizer = authorizer

server = FTPServer(("127.0.0.1", 21), handler)

print("FTP server running on port 21")
print("Username: admin")
print("Password: password")

server.serve_forever()