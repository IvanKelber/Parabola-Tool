import os
import math

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp

from parabolas import find_general_parabola

"""App configuration copy-and-pasted from Harvard CS50 problem set 8 distribution ("finance")"""

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#set dimensions of grid
WIDTH, HEIGHT = 200, 100

@app.route("/", methods=["GET", "POST"])
def index():
    cells = []
    for i in range(HEIGHT):
        row = []
        for j in range(WIDTH):
            row.append(str(i * WIDTH + j))
        cells.append(row)
    if request.method == "POST":
        p1, p2, p3 = str(request.form.get("point_0"))[4:], str(request.form.get("point_1"))[4:], str(request.form.get("point_2"))[4:]
        p1x, p1y, p2x, p2y, p3x, p3y = int(p1) % WIDTH, (int(p1) - (int(p1) % WIDTH)) / WIDTH, int(p2) % WIDTH, (int(p2) - (int(p2) % WIDTH)) / WIDTH, int(p3) % WIDTH, (int(p3) - (int(p3) % WIDTH)) / WIDTH
        points = [[p1x,p1y],[p2x,p2y],[p3x,p3y]]
        ang = float(request.form.get("angle")) * 2 * math.pi / 360
        cfs = find_general_parabola(points, ang)
        for entry in cfs:
            entry *= 10
        message = ""

        #change cells in cells array to black if they're on the parabola:
        if len(cfs) == 6:
            for i in range(HEIGHT):
                for j in range(WIDTH):
                    val = (j**2 * cfs[0]) + (j * i * cfs[1]) + (i**2 * cfs[2]) + (j * cfs[3]) + (i * cfs[4]) + cfs[5]
                    if ang != 0:
                        if val < 10 and val > -10:
                            cells[i][j] = "black"
                    else:
                        if val < 1 and val > -1:
                            cells[i][j] = "black"
        else:
            message = "points do not form a valid parabola"
        return render_template("parabolas.html", cells=cells, message=message)
    else:
        message = ""
        return render_template("parabolas.html", cells=cells, message=message)