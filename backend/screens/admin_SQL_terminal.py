from .imports import *


class AdminSQLTerminalScreen:
    def __init__(self, app):
        self.app = app
        self.app.add_url_rule("/admin_SQL", view_func=self.admin_SQL, methods=["POST"])
        self.app.add_url_rule("/admin_logout", view_func=self.admin_logout, methods=["POST"])
        self.app.add_url_rule("/admin_stats", view_func=self.admin_stats, methods=["GET"])

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
                return jsonify(
                    {
                        "message": "<br>".join(
                            ", ".join(str(item) for item in row) for row in response
                        )
                    }
                )
            except Exception as e:
                return jsonify({"error": f"Unable to send response: {e}"})
        else:
            return jsonify({"message": "No Response"})

    def admin_logout(self):
        # when logging out, the session's details are removed such that they can't be used by manually routing to other pages after logout
        session.clear()
        return ""

    @utils.auto_reconnect
    def admin_stats(self):
        # average number of tabs per user
        average_tabs_per_user = None

        self.cursor.execute("""
        SELECT AVG(COUNT(tab_id)) FROM Users, Tabs
        WHERE Tabs.user_id = Users.user_id
        """)
        average_tabs_per_user = self.cursor.fetchone() 

        #average tab length across all users
        average_tab_length = None
        self.cursor.execute("""
        SELECT AVG(COUNT(order_id)) FROM Users, Tabs, TabNodes
        WHERE Tabs.user_id = Users.user_id
        AND Tabs.tab_id = TabNodes.tab_id
        """)



        

