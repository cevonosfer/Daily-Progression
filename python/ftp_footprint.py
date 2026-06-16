import ftplib


ftp = ftplib.FTP()
ftp.connect("127.0.0.1", 21)

try:
    ftp.login("anonymous","password")
    print("anonymous login allowed!")
except ftplib.error_perm:
    print("anonymous login denied") 
except Exception as e:
    print(f"error: {e}")

response = ftp.sendcmd("USER admin")
print(ftp.getwelcome())
print(response)
ftp.quit()