import sys
import os
from flask import Flask, render_template, request

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "grundbau")))

from erddruck import AktiverErddruckbeiwert, Erddruckkraft

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/calculate", methods=["POST"])
def calculate():
    phi_k = float(request.form["phi_k"])
    alpha = float(request.form["alpha"])
    beta = float(request.form["beta"])
    delta_a = float(request.form["delta_a"])

    objekt_1 = AktiverErddruckbeiwert(phi_k, alpha, beta, delta_a)
    result = objekt_1.K_a_g

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
