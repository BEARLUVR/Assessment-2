import sqlite3 as sql
import time
import random
import bcrypt

  #
  #  cur = con.cursor()
    #cur.execute(
     ##  (username, password, DoB),
    #)
    #con.commit()
   # con.close()

def insertUser(username, password, DoB):
    #convcerts to byte version of password
    byte_password = password.encode('utf-8')
    #hashes byte versionsS
    hash_password = bcrypt.hashpw(byte_password, bcrypt.gensalt())

    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    sqlQ = "SELECT * FROM users WHERE username = ?"
    cur.execute(sqlQ,(username,)) #now it leaves login as just as
    if cur.fetchone() == None:
        if username == password: #only messages inside the console,need to add prompt to user
         print("They can't be the same")
        else:
         cur.execute(
        "INSERT INTO users (username,password,dateOfBirth) VALUES (?,?,?)",
        (username, hash_password, DoB),
        )
        con.commit()
        con.close()
    else:
     print("username aleady exists")

    

def retrieveUsers(username, password):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    
    sqlQ = "SELECT * FROM users WHERE username = ?"
    #cur.execute(f"SELECT * FROM users WHERE username = '{username}'") original string
    #cur.execute(sql, "SELECT * From ? WHERE ?  )
    cur.execute(sqlQ,(username,)) #now it leaves login as just as
    if cur.fetchone() == None: 
        con.close()
        return False


    else:
        cur.execute(sqlQ,(password,))
        #cur.execute(f"SELECT * FROM users WHERE password = '{password}'")  original line
        # Plain text log of visitor count as requested by Unsecure PWA management
        savedpassword = cur.fetchone()
        print('this is the hashed version of password')
        with open("visitor_log.txt", "r") as file:
            number = int(file.read().strip())
            number += 1
        with open("visitor_log.txt", "w") as file:
            file.write(str(number))
        # Simulate response time of heavy app for testing purposes
        time.sleep(random.randint(80, 90) / 1000)
        byte_password = password.encode('utf-8')
        if bcrypt.checkpw(byte_password, savedpassword[0]):
        
         if cur.fetchone() == None:
            con.close()
            return False
        else:
            con.close()
            return True

def insertFeedback(feedback):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    #cur.execute("INSERT INTO FEEDBACK (feedback) VALUES ('{feedback}')") #original string
    sqlQ =  ("INSERT INTO feedback (?) VALUES ('{?}')")
    cur.execute(sqlQ,(feedback,))
    con.commit()
    con.close()


def listFeedback():
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    data = cur.execute("SELECT * FROM feedback").fetchall() #original line
    con.close()
    f = open("templates/partials/success_feedback.html", "w")
    for row in data:
        f.write("<p>\n")
        f.write(f"{row[1]}\n")
        f.write("</p>\n")
    f.close()
