from .imports import *


class TabsScreen:
    def __init__(self, app):
        self.app = app
        self.app.add_url_rule("/display_tabs", view_func=self.display_tabs, methods=["GET"])

        self.db, self.cursor = utils.connect()

    @utils.auto_reconnect
    def display_tabs(self):

        # must return every tab for the user currently logged in

        # check if the user's session exists
        if not session["username"] and not session["user_id"]:
            return jsonify({"error": "Login Error, please try relogging in"})
            
        # take all the tab_ids that match with the user_id
        user_id = session["user_id"]
        self.cursor.execute(
            "SELECT tab_id FROM Tabs WHERE user_id=%s ORDER BY tab_id", (user_id,)
        )
        row = self.cursor.fetchall()


        # for each tab_id, recreate the tab and add it to the output
        output = []
        for tab_id in row:
            head = utils.reconstruct_tabnodes(tab_id)
            output.append({tab_id : utils.convert_to_tablature_form(head)})

        return jsonify({"message": output})

    @utils.auto_reconnect
    def add_tab(self):
        data = request.get_json()
        audio = data["audio"]

