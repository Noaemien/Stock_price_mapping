import numpy as np
from flask import Flask, render_template, jsonify, request, json
from nn_module import Neural_Network
app = Flask(__name__)


@app.route("/")
def nn_training():
    return render_template("nn_training.html")

X = np.random.uniform(-1, 5, (1, 500))
Y = X ** 2

nn = Neural_Network(X, Y, [128, 128, 1], optimisation_function="GRADIENTDESCENT")
cost = 0
#Gets called from main.js after a click of the "run" button
@app.route("/nn_iteration/<float:alpha>")
def nn_iteration(alpha):
    global cost
    #print("Success !")
    #print(alpha)
    if alpha != 0:
        cost = nn.train(alpha, 1)
    return json.dumps(cost)


#Resets weights and biases when called from main.js
@app.route("/init_params", methods = ["GET"])
def init_params():
    global nn
    nn = Neural_Network(X, Y, [128, 128, 1], optimisation_function="GRADIENTDESCENT")
    print("Re-initialising !")
    return "None"


if __name__ == "__main__":
    app.run(debug= True)