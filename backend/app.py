from flask import Flask
import utils
import screens
import os
import pymysql
from flask_cors import CORS


class Website:
    def __init__(self):
        # Create Flask app backend
        self.app = Flask(__name__)
        self.app.secret_key = os.environ.get("SECRET_KEY", "dev_secret")

        # Handle session keys
        self.app.config["SESSION_PERMANENT"] = False
        self.app.config["SESSION_TYPE"] = "filesystem"

        # Change Cross‑Origin Resource Sharing to allow cookies to be shared
        CORS(self.app, supports_credentials=True)

        # Setup database and screens
        self.db, self.cursor = utils.connect()
        self.create_tables()
        self.create_screens()

    def create_tables(self):

        # Users:
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(40) UNIQUE NOT NULL,
            password VARCHAR(64) NOT NULL,
            salt BINARY(4)
        )
        """)
        self.db.commit()

        # Admins:
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Admins (
            admin_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(40) UNIQUE NOT NULL,
            password VARCHAR(64) NOT NULL,
            salt BINARY(4)
            )
            """)
        self.db.commit()

        # Tabs:
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Tabs (
            tab_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            FOREIGN KEY (user_id) REFERENCES Users(user_id)
            )
            """)
        self.db.commit()

        # Groups:
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS UserGroups (
            group_id INT AUTO_INCREMENT PRIMARY KEY,
            group_name VARCHAR(64)
            )
            """)
        self.db.commit()

        # Entries:
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Entries ( 
            entry_id INT AUTO_INCREMENT PRIMARY KEY,
            tab_id INT,
            group_id INT,
            FOREIGN KEY (tab_id) REFERENCES Tabs(tab_id),
            FOREIGN KEY (group_id) REFERENCES UserGroups(group_id)
            )
            """)
        self.db.commit()

        # TabNodes:
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS TabNodes ( 
            node_id INT AUTO_INCREMENT PRIMARY KEY,
            tab_id INT, 
            order_id INT,
            string_number INT,
            fret_number INT,
            FOREIGN KEY (tab_id) REFERENCES Tabs(tab_id)
            )
            """)
        self.db.commit()

    def create_screens(self):
        screens.LoginScreen(self.app)
        screens.SignUpScreen(self.app)
        screens.Welcome(self.app)

    def run(self):
        port = int(5000)
        self.app.run(host="0.0.0.0", port=port)


website = Website()
website.run()
