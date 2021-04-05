import numpy as np
from flask import Flask, render_template, jsonify, request, json
from nn_module import Neural_Network
app = Flask(__name__)


@app.route("/")
def nn_training():
    return render_template("nn_training.html")

X = np.random.uniform(-1, 5, (1, 5000))
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
@app.route("/init_params", methods = ["POST"])
def init_params():
    global nn
    
    #Get data from post in "main.js"
    optimisation_f = request.form["optimisation_function"].upper()
    hidden_a = request.form["hidden_activation"].upper()
    out_a = request.form["out_activation"].upper()
    layer_n = json.loads(request.form["layer_neurons"])

    nn = Neural_Network(X, Y, layer_neurons=layer_n, optimisation_function=optimisation_f,hidden_activation=hidden_a, end_activation=out_a)
    print(optimisation_f, hidden_a, out_a, layer_n)
    return "None"


if __name__ == "__main__":
    app.run(debug= True)