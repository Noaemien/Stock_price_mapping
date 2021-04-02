import numpy as np
from flask import Flask, render_template
from nn_module import Neural_Network


app = Flask(__name__)


@app.route("/")
def nn_training():
    return render_template("nn_training.html")

X = np.random.uniform(-1, 5, (1, 500))
Y = X ** 2

nn = Neural_Network(X, Y, [128, 128, 1], optimisation_function="GRADIENTDESCENT")
#nn.train(0.001, 500)

if __name__ == "__main__":
    app.run(debug= True)