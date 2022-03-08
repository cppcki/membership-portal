import json
from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/users")
def users():
  return jsonify({
    "users": [
      {
        "name": "bob",
        "email": "bob@bobble.com"
      }    
    ]
  })

app.run(debug = True)