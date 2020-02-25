import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root1",
  passwd="1122",
  database="book",
  auth_plugin='mysql_native_password'
)
# print(mydb) #<mysql.connector.connection_cext.CMySQLConnection object at 0x0000026F5596BBA8>
mycursor = mydb.cursor()
sql = "SELECT * FROM books WHERE BookID BETWEEN 20 AND 30"
mycursor.execute(sql)
col = mycursor.column_names
myresult = mycursor.fetchall()
for x in myresult:
  print(x)