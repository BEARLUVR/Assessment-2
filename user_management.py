import sqlite3 as sql
import time
import random
import bcrypt

#user sign up to site,enters thier details into the SQL database
def insertUser(username, password, DoB):
    #convcerts to byte version of password
    byte_password = password.encode('utf-8')
    #hashes byte versionsS
    hash_password = bcrypt.hashpw(byte_password, bcrypt.gensalt())

    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute(
        "INSERT INTO users (username,password,dateOfBirth) VALUES (?,?,?)",
        (username, hash_password, DoB),
    )
    con.commit()
    con.close()

#checks if user exists and checks thier password is corect
def retrieveUsers(username, password):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute(f"SELECT * FROM users WHERE username = '{username}'")
    if cur.fetchone() == None:    #this is checking the sql database if username exist,if not returns false to main
        con.close()
        return False
    else:
        cur.execute(f"Select password FROM users WHERE username = '{username}'") 
        #cur.execute(f"SELECT password FROM users WHERE username = '{username}'")
        savedpassword = cur.fetchone()
        print(savedpassword)
        # Plain text log of visitor count as requested by Unsecure PWA management
        with open("visitor_log.txt", "r") as file:
            number = int(file.read().strip())
            number += 1
        with open("visitor_log.txt", "w") as file:
            file.write(str(number))
        # Simulate response time of heavy app for testing purposes
        time.sleep(random.randint(80, 90) / 1000)
        byte_password = password.encode('utf-8')
        if bcrypt.checkpw(byte_password, savedpassword[0]):
            con.close()
            return False
        else:
            con.close()
            return True


def insertFeedback(feedback):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute(f"INSERT INTO feedback (feedback) VALUES ('{feedback}')")
    con.commit()
    con.close()


def listFeedback():
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    data = cur.execute("SELECT * FROM feedback").fetchall()
    con.close()
    f = open("templates/partials/success_feedback.html", "w")
    for row in data:
        f.write("<p>\n")
        f.write(f"{row[1]}\n")
        f.write("</p>\n")
    f.close()

