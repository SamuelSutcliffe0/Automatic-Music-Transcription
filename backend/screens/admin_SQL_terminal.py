from .imports import *


class AdminSQLTerminalScreen:
    def __init__(self, app):
        self.app = app
        self.app.add_url_rule("/admin_SQL", view_func=self.admin_SQL, methods=["POST"])
        self.app.add_url_rule("/admin_logout", view_func=self.admin_logout, methods=["POST"])

        self.db, self.cursor = utils.connect()

    @utils.auto_reconnect
    def admin_SQL(self):

        # recieve form fields from frontend
        data = request.get_json()
        query = data["query"]

        # try executing the providided SQL
        try:
            self.cursor.execute(query)
            response = self.cursor.fetchall()
            self.db.commit()

        # return error 
        except Exception as e: 
            return jsonify({"error": f"Inncorrect SQL: {e}"})

        # return SQL result if relevant
        if response:
            try:
                return jsonify({"message": "<br>".join(", ".join(str(item) for item in row) for row in response)})
            except Exception as e:
                return jsonify({"error": f"Unable to send response: {e}"})
        else: 
            return jsonify({"message": "No Response"})


    def admin_logout(self):
        # when logging out, the session's details are removed such that they can't be used by manually routing to other pages after logout
        session.clear()
        return ""
            
