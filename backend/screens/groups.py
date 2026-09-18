from .imports import *


class GroupsScreen:
    def __init__(self, app):
        self.app = app
        self.app.add_url_rule("/display_groups", view_func=self.display_groups, methods=["GET"])
        self.app.add_url_rule("/new_group", view_func=self.create_new_group, methods=["POST"])
        self.app.add_url_rule("/add_entry", view_func=self.add_to_group, methods=["POST"])
        self.app.add_url_rule("/remove_entry", view_func=self.remove_from_group, methods=["POST"])

        self.db, self.cursor = utils.connect()

    @utils.auto_reconnect
    def display_groups(self):

        # must return every group 
            
        # select all groups 
        self.cursor.execute("SELECT group_id, group_name FROM UserGroups")
        groups = self.cursor.fetchall()

        # prepare output
        output = []
        for group in groups:
            group_id = group[0]
            group_name = group[1]

            sub_output = []
            sub_output.append(group_name)

            # select all tabs in the group
            self.cursor.execute("""
            SELECT tab_id FROM Entries
            WHERE group_id = %s
            """, (group_id,))

            tabs = self.cursor.fetchall()

            #recreate all tabs in the group
            for tab_id in tabs:
                tab_id = tab_id[0] # remove from tuple 
                head = utils.reconstruct_tabnodes(tab_id)
                sub_output.append({tab_id : utils.convert_to_tablature_form(head)})

            # add group to full output
            output.append({group_id: sub_output})

        return jsonify({"message": output})

    @utils.auto_reconnect
    def create_new_group(self):

        # create new group 
        data = request.get_json()
        if not data["name"]:
            return jsonify({"errror": "Please enter a name"})

        name = data["name"]

        self.cursor.execute("INSERT INTO UserGroups (group_name) VALUES (%s)",
            (name,),
        )
        self.db.commit()
    
    @utils.auto_reconnect
    def add_to_group(self):

        # add new entry into a group 
        data = request.get_json()
        tab_id = data["tab_id"]
        group_id = data["group_id"]

        # check tab not already in group
        self.cursor.execute("""
        SELECT 1 FROM Entries 
        WHERE tab_id = %s
        AND group_id = %s
        """,
            (tab_id, group_id),
        )
        row = self.cursor.fetchone()
        if row:
            return jsonify({"error": "Tab already in group"})

        # add tab to group if not already in
        self.cursor.execute("INSERT INTO Entries (tab_id, group_id) VALUES (%s,%s)",
            (tab_id, group_id),
        )
        self.db.commit()

    @utils.auto_reconnect
    def remove_from_group(self):

        # remove an entry from a group
        data = request.get_json()
        tab_id = data["tab_id"]
        group_id = data["group_id"]

        self.cursor.execute("""
        DELETE FROM Entries 
        WHERE tab_id = %s
        AND group_id = %s
        """,
            (tab_id, group_id),
        )
        self.db.commit()

