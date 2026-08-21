from .imports import *


class LoginScreen:
    def __init__(self, app):
        self.app = app
        self.app.add_url_rule("/login", view_func=self.login, methods=["POST"])

        self.db, self.cursor = connect()

    @auto_reconnect
    def login(self):

        # recieve form fields from frontend
        username = request.form["username"]
        password = request.form["password"]

        # check for empty fields
        if not username or not password:
            return jsonify({"error": "Please Complete All Fields"})

        # SQL query to fetch details for login
        self.cursor.execute(
            "SELECT password, salt, user_id FROM Users WHERE username=%s", (username,)
        )
        row = self.cursor.fetchone()

        # check if user exists
        if not row:
            return jsonify({"error": "User Not Found"})

        # define columns in row
        db_password = row[0]
        db_salt = row[1]
        db_user_id = row[2]

        # check if passwords match
        if db_password != hash(password, db_salt):
            return jsonify({"error": "Incorrect Password"})

        # initiate a user session passing the username and id into the session for later use
        session["username"] = username
        session["user_id"] = db_user_id
        return jsonify({"message": "Login Successful"})
