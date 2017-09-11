#!/usr/bin/env python3

"""Basic HTTP Server With Upload.
Acknowledgements:
 *Main logic: https://gist.github.com/UniIsland/3346170
             https://hundredminutehack.blogspot.com.au/2017/03/drag-and-drop-files-with-html5-and-flask.html
 *Changing ports: https://stackoverflow.com/a/29079598
"""

from flask import Flask, request, redirect, jsonify
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"


@app.route("/")
def index():
    return redirect("/static/index.html")


@app.route("/sendfile", methods=["POST"])
def send_file():
    fileob = request.files["file2upload"]
    filename = secure_filename(fileob.filename)
    save_path = "{}/{}".format(app.config["UPLOAD_FOLDER"], filename)
    fileob.save(save_path)

    # open and close to update the access time.
    with open(save_path, "r") as f:
        pass

    return "successful_upload"


@app.route("/filenames", methods=["GET"])
def get_filenames():
    '''
    ** Orders the files by their last_modified date.
    '''
    filenames = os.listdir("uploads/")

    def modify_time_sort(file_name):
        file_path = "uploads/{}".format(file_name)
        file_stats = os.stat(file_path)
        last_access_time = file_stats.st_atime
        return last_access_time

    filenames = sorted(filenames, key=modify_time_sort)
    return_dict = dict(filenames=filenames)
    return jsonify(return_dict)


if __name__ == '__main__':
    app.run(debug=False, host='localhost',port='9393')
