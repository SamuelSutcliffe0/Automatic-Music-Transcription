from .imports import *


class SignUpScreen:
    def __init__(self, app):
        self.app = app
        self.app.add_url_rule("/signup", view_func=self.signup, methods=["POST"])

        self.db, self.cursor = utils.connect()

    @utils.auto_reconnect
    def signup(self):

        # generate unique user salt of 4 byte binary
        salt = os.urandom(4)

        # recieve form fields from frontend
        data = request.get_json()
        username = data["username"]
        password = utils.hash(data["password"], salt)
        confirm_password = utils.hash(data["confirm_password"], salt)

        # check for empty fields
        if not username or not password or not confirm_password:
            return jsonify({"error": "Please Complete All Fields"})

        # check password matches the confirm password section
        if password != confirm_password:
            return jsonify({"error": "Passwords Don't Match"})

        # SQL query to check username not taken
        self.cursor.execute(
            "SELECT 1 FROM Users WHERE username=%s LIMIT 1", (username,)
        )
        row = self.cursor.fetchone()
        if row:
            return jsonify({"error": "Username Already Taken"})

        # SQL to add the new user to database
        self.cursor.execute(
            "INSERT INTO Users (username, password, salt) VALUES (%s, %s, %s)",
            (username, password, salt),
        )
        self.db.commit()
        return jsonify({"message": "Signup Successful"})
