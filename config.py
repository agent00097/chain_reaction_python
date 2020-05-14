import mysql.connector

mysql_username="root"
mysql_paswword="root"

mydb = mysql.connector.connect(
  host="localhost",
  user=mysql_username,
  passwd=mysql_paswword
)
mycursor = mydb.cursor()
#mycursor.execute("CREATE DATABASE gameserver;")
mycursor.execute("SHOW DATABASES;")
flag=1
for x in mycursor:
    if x[0] == "gameserver":
        flag = 0

if flag == 1:
    mycursor.execute("CREATE DATABASE gameserver;")

mydb.commit()


mydb = mysql.connector.connect(
  host="localhost",
  user=mysql_username,
  passwd=mysql_paswword ,
  database="gameserver"
)

mycursor = mydb.cursor()
mycursor.execute("DROP TABLE IF EXISTS user;")
mycursor.execute("DROP TABLE IF EXISTS games;")
mycursor.execute("CREATE TABLE user (name VARCHAR(255) PRIMARY KEY, password VARCHAR(255), win INT, loss INT, draw INT);")
mycursor.execute("CREATE TABLE games (id INT AUTO_INCREMENT PRIMARY KEY, player1 VARCHAR(255) , player2 VARCHAR(255), move1 TEXT, move2 TEXT);")
mydb.commit()

