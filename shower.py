import os
from threading import Thread
from flask import Flask, render_template_string


class ImageShower:

    def __init__(self):
        self.thread = None
        self.app = Flask(__name__, static_folder=".cache/static/")

        @self.app.get("/")
        def index():
            find = False
            file_name = None
            for name in os.listdir(".cache/static"):
                if name[:name.rfind(".")] == "img":
                    file_name = name
                    find = True
            if find:
                temp = "<img src={{ url_for('static', filename='" + file_name + "') }} width='100%'>"
            else:
                temp = "The DM has not sent one picture yet"
            return render_template_string(temp)

    def run(self, port):
        self.thread = Thread(target=self.app.run, kwargs={"host": "0.0.0.0", "port": port}, daemon=True)
        self.thread.start()
