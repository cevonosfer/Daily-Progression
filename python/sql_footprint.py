import pymysql

conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="")
cursor = conn.cursor()
cursor.execute("SELECT VERSION()")
print(cursor.fetchone())

cursor.execute("SELECT user, host FROM mysql.user")
print(cursor.fetchall())

cursor.execute("SELECT user FROM mysql.user WHERE authentication_string = ''")

cursor.execute("SHOW DATABASES")
print(cursor.fetchall())