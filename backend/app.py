from flask import Flask 
import utils
import screens
app = Flask(__name__) 
@app.route("/") 
def home(): 
    return {"message": "Hello from Flask"} 
if __name__ == "__main__": 
    app.run(debug=True) 



import os
from flask import Flask
import mysql.connector
import screens 

class Website: 
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = os.environ.get("SECRET_KEY", "dev_secret")

        self.cursor, self.db = connect()
        self.create_tables()
        self.create_screens()


    def create_tables(self):

        #Users:
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(40) UNIQUE NOT NULL,
            password VARCHAR(40) NOT NULL,
            salt BINARY(4)
        )
        """)

        #Admins:
        self.db.commit()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Admins (
            admin_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(40) UNIQUE NOT NULL,
            password VARCHAR(40) NOT NULL,
            salt BINARY(4)
            )
            """)
        self.db.commit()

        #Tabs:
        self.db.commit()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Tabs (
            tab_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT FOREIGN KEY
            )
            """)
        self.db.commit()

        #Groups:
        self.db.commit()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Groups (
            group_id INT AUTO_INCREMENT PRIMARY KEY,
            group_name VARCHAR(64)
            )
            """)
        self.db.commit()

        #Entries:
        self.db.commit()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Entries ( 
            entry_id INT AUTO_INCREMENT PRIMARY KEY,
            tab_id INT FOREIGN KEY,
            group_id INT FOREIGN KEY
            """)
        self.db.commit()

        #TabNodes:
        self.db.commit()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS TabNodes ( 
            node_id INT AUTO_INCREMENT PRIMARY KEY,
            tab_id INT FOREIGN KEY,
            order_id INT,
            string_number INT,
            fret_number INT 
            """)
        self.db.commit()

    def create_screens(self):

        LoginScreen(self)

    def run(self):
        port = int(os.environ.get("PORT", 5000))
        self.app.run(host="0.0.0.0", port=port)

website = Website()
app = website.app
