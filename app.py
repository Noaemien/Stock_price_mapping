import numpy as np
from flask import Flask, render_template, jsonify, request, json
from nn_module import Neural_Network
app = Flask(__name__)


@app.route("/")
def nn_training():
    return render_template("nn_training.html")

X = np.random.uniform(-1, 5, (1, 5000))
Y = X ** 2

nn = Neural_Network(X, Y, [128,  1], optimisation_function="GRADIENTDESCENT")
#Gets called from main.js after a click of the "run" button
@app.route("/nn_iteration", methods = ["POST"])
def nn_iteration():
    cost = 0
    
    alpha = float(request.form["alpha"])
    it = int(request.form["iteration"])
    beta1 = float(request.form["beta1"])
    beta2 = float(request.form["beta2"])
    print(alpha, it, beta1, beta2)
    if alpha != 0:
        cost = nn.train(alpha, it, beta1=beta1, beta2 = beta2)
        print(cost)
    return json.dumps(cost)


#Resets weights and biases when called from main.js
@app.route("/init_params", methods = ["POST"])
def init_params():
    global nn
    
    #Get data from post in "main.js"
    optimisation_f = request.form["optimisation_function"].upper()
    activation_f = json.loads(request.form["layer_activations"])
    layer_n = json.loads(request.form["layer_neurons"])

    nn = Neural_Network(X, Y, layer_neurons=layer_n, optimisation_function=optimisation_f, layer_activations= activation_f)
    print(optimisation_f, activation_f, layer_n)
    return "None"


if __name__ == "__main__":
    app.run(debug= True)