from .imports import *


class AdminLoginScreen:
    def __init__(self, app):
        self.app = app
        self.app.add_url_rule("/admin_login", view_func=self.admin_login, methods=["POST"])

        self.db, self.cursor = utils.connect()

    @utils.auto_reconnect
    def admin_login(self):

        # recieve form fields from frontend
        data = request.get_json()
        username = data["username"]
        password = data["password"]

        # check for empty fields
        if not username or not password:
            return jsonify({"error": "Please Complete All Fields"})

        # SQL query to fetch details for login
        self.cursor.execute(
            "SELECT password, salt, admin_id FROM Admins WHERE username=%s", (username,)
        )
        row = self.cursor.fetchone()

        # check if user exists
        if not row:
            return jsonify({"error": "User Not Found"})

        # define columns in row
        db_password = row[0]
        db_salt = row[1]
        db_admin_id = row[2]

        # check if passwords match
        if db_password != utils.hash(password, db_salt):
            return jsonify({"error": "Incorrect Password"})

        # initiate a session passing the username and id into the session for later use
        session["username"] = username
        session["admin_id"] = db_admin_id
        return jsonify({"message": "Login Successful"})
