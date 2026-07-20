class LoginScreen:
    def __init__(self, website):
        self.website = website
        self.app = website.app
        self.db, self.cursor = website.initiate_db()
        self.app.add_url_rule("/login", view_func=self.login, methods=["POST"])

    @auto_reconnect
    def login(self):

        username = request.form["username"]
        password = hash(request.form["password"])

        if not username or not password:
            return jsonify({"error": "Please Enter a Username and Password"})

        self.cursor.execute("SELECT password FROM users WHERE username=%s", (username,))
        row = self.cursor.fetchone()

        if not row:
            return jsonify({"error": "User Not Found"})

        if row[0] != password:
            return jsonify({"error": "Incorrect Password"})


        session["username"] = username
        self.cursor.execute("SELECT id FROM users WHERE username=%s", (username,))
        return_id = self.cursor.fetchone()
        session["user_id"] = int(return_id[0])

        return jsonify({"message": "Login Successful"})

