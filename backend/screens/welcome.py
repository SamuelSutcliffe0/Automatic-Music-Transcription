from .imports import *


class Welcome:
    def __init__(self, app):
        self.app = app
        self.app.add_url_rule("/logout", view_func=self.logout, methods=["POST"])
        self.app.add_url_rule("/welcome", view_func=self.welcome, methods=["GET"])

    def logout(self):

        # when logging out, the session's details are removed such that they can't be used by manually routing to other pages after logout 
        session.clear()
        return ""

    def welcome(self):
        
        # gives session name to frontend
        username = session.get("username")
        if not username:
            return jsonify({"error": "Not logged in"}), 401

        return jsonify({"message": username})
