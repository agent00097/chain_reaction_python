import mysql.connector
import hashlib,os,binascii

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="gameserver"
)
def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 10)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'),salt.encode('ascii'),10)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

mycursor = mydb.cursor()
mycursor.execute("DROP TABLE IF EXISTS user;")
mycursor.execute("DROP TABLE IF EXISTS games;")
mycursor.execute("CREATE TABLE user (name VARCHAR(255) PRIMARY KEY, password VARCHAR(255), win INT, loss INT, draw INT);")
mycursor.execute("CREATE TABLE games (id INT AUTO_INCREMENT PRIMARY KEY, player1 VARCHAR(255) , player2 VARCHAR(255), move1 TEXT, move2 TEXT);")
mycursor.execute("SELECT * FROM user;")
x = mycursor.fetchone()
if x is None:
    print("o")
data=hash_password("dasdas")
val_recv=("dasdas",data,0,0,0)
sql="INSERT INTO user (name, password,win,loss,draw) VALUES (%s, %s,%s, %s, %s);"
mycursor.execute(sql, val_recv)
#mycursor.execute("SELECT * FROM user;")

mycursor.execute("SELECT * FROM user WHERE name = %s;",("dasdas",))
x = mycursor.fetchone()
if x is None:
    print("o")
print(x[1])



#SELECT * FROM games WHERE player1=%s OR player2=%s;
#myresult = mycursor.fetchall()


#print(mydb)
