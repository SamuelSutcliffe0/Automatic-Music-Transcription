from .imports import *


class UploadScreen:
    def __init__(self, app):
        self.app = app
        self.app.add_url_rule("/upload_tab", view_func=self.upload_tab, methods=["POST"])

        self.db, self.cursor = utils.connect()

    @utils.auto_reconnect
    def upload_tab(self):
        audio_file = request.files["file"]
        


            

