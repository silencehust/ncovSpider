from flask import Flask
from flask import render_template
import utils
from flask import jsonify
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("main.html")

@app.route("/time")
def get_time():
    return utils.get_time()

@app.route("/c1")
def get_c1_data():
    data=utils.get_c1_data()
    d=jsonify({"confirm":int(data[0]), "suspect": int(data[1]), "heal": int(data[2]), "dead": int(data[3])})
    return d

if __name__ == '__main__':
    app.run()
