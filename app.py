from flask import Flask, render_template, redirect, request
import sqlite3

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        suffix = request.form.get("suffix")
        longUrl = request.form.get("longUrl")
        with sqlite3.connect("db/urls.db") as db:
            c = db.cursor()
            c.execute('INSERT INTO urls VALUES (?,?,?)', (suffix, longUrl, 0))
        return render_template("success.html", longUrl=longUrl, suffix=request.base_url + suffix)


@app.route("/<suffix>")
def short(suffix):
    with sqlite3.connect("db/urls.db") as db:
        c = db.cursor()
        url = c.execute('SELECT url FROM urls WHERE suffix=(?)', (suffix,))
        if url != None:
            return redirect(url.fetchone()[0])
        else:
            return "something went wrong!"

