import mysql.connector
import re
connection= mysql.connector.connect(
    host= 'localhost',
    user= 'root',
    password= 'adminadmin',
    database= "vocab"
)

cursor= connection.cursor()
cursor.execute("SHOW DATABASES")
found=False 
for db in cursor:
    pattern= "[(,')]"
    db_string = re.sub(pattern,"", str(db))
    if(db_string=='vocab'):
        found=True
        print("database vocab exists")
if (not found):
    cursor.execute("CREATE DATABASE vocab")

sql="DROP TABLE IF EXISTS vocab_table"
cursor.execute(sql)
sql="CREATE TABLE vocab_table(word VARCHAR(255), definition VARCHAR(255))"
cursor.execute(sql)

filehandle = open("Vocabulary_list.csv", 'r')


wordlist=filehandle.readlines()

wordlist.pop(0)

vocab_list=[]

for rawstring in wordlist:
    word,definition= rawstring.split(',',1)
    definition=definition.rstrip()
    vocab_list.append({word,definition})
    sql= "INSERT INTO vocab_table(word, definition) VALUES(%s,%s)"
    values = (word, definition)
    cursor.execute(sql,values)

    connection.commit()
    print("Inserted"+ str(cursor.rowcount)+ "row into vocab_table")

sql= "SELECT * from vocab_table WHERE word = %s"

value= ('boisterous',)
cursor.execute(sql,value)

result=cursor.fetchall()

for row in result:
    print(row)

sql = "UPDATE vocab_table SET definition= %s WHERE word =%s"
value=('sprited:lively', 'boisterous')
cursor.execute(sql,value)

connection.commit()
print("number of modified rows: ", cursor.rowcount)
sql="SELECT * FROM vocab_table WHERE word=%s"
value =('boisterous',)
cursor.execute(sql, value)
result = cursor.fetchall()

for row in result:
    print(row)
#update the definition for boisterois
#escape the values to prevent sql injection
#print(vocab_list)
