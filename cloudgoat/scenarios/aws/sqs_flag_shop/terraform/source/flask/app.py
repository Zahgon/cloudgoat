from flask import Flask, render_template, request, url_for, redirect
import db
import time
import sqs
import uuid
import json
import os

app = Flask(__name__)


def check_asset():
    cur = db.conn.cursor()
    cur.execute("select asset from asset_table")
    asset = cur.fetchall()
    cur.close()
    return asset[0][0]














@app.route("/", methods=["GET", "POST"])
def index():
    cur = db.conn.cursor()
    db.conn.commit()
    cur.close()
    asset = check_asset()
    return render_template("index.html", asset=asset)


def main():
    app.run(host="0.0.0.0", debug=True)


if __name__ == "__main__":
    main()
