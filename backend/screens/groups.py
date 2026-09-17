from .imports import *


class GroupsScreen:
    def __init__(self, app):
        self.app = app
        self.app.add_url_rule("/display_groups", view_func=self.display_groups, methods=["GET"])

        self.db, self.cursor = utils.connect()

    @utils.auto_reconnect
    def display_groups(self):

        # must return every group 
            
        # select all groups 
        self.cursor.execute("SELECT group_id,group_name FROM Groups")
        groups = self.cursor.fetchall()

        # prepare output
        output = None 
        for group in groups:
            group_id = group[0]
            group_name = group[1]

            sub_output = []
            sub_output.append(group_name)

            # select all tabs in the group
            self.cursor.execute("""SELECT tab_id FROM Entries, Groups 
            WHERE Entries.group_id = Groups.group_id
            """)
            tabs = self.cursor.fetchall()

            #recreate all tabs in the group
            for tab_id in tabs:
                head = utils.reconstruct_tabnodes(tab_id)
                sub_output.append(utils.convert_to_tablature_form(head))

            # add group to full output
            output.append(sub_output)

        return jsonify({"message": output})

    @utils.auto_reconnect
    def create_new_group(self):
        pass 
    
    @utils.auto_reconnect
    def add_to_group(self):
        pass 

    @utils.auto_reconnect
    def remove_from_group(self):
        pass 

