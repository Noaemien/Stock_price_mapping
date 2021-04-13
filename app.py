import numpy as np
from flask import Flask, render_template, jsonify, request, json
from nn_module import Neural_Network
from io import BytesIO
import pandas as pd
app = Flask(__name__)


@app.route("/")
def nn_training():
    return render_template("nn_training.html")

X = np.random.uniform(-1, 5, (1, 8670))
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
    cost_f = request.form["cost_function"].upper()
    activation_f = json.loads(request.form["layer_activations"])
    layer_n = json.loads(request.form["layer_neurons"])

    nn = Neural_Network(X, Y, layer_neurons=layer_n, optimisation_function=optimisation_f, layer_activations= activation_f, cost_function=cost_f)
    print(optimisation_f, cost_f, activation_f, layer_n)
    return "None"

@app.route("/get_dims", methods=["POST"])
def getDatasetDims():
    global X
    file_n = request.files["file"]
    file_r = file_n.stream.read()
    df_file = pd.read_csv(BytesIO(file_r))
    X = df_file.to_numpy()

    if len(X) != min(len(X), len(X[0])):
        X = X.T

    #
    # NEED TO ADD DATASET FORM DETECTION ( REMOVE INDEX LAYER IF IT EXISTS AND REMOVE LAYERS WITH NAN VALUES )
    #

    X = np.delete(X, 0, axis = 0)

    data = {
        "size_x": len(df_file),
        "size_y": len(df_file.columns)
    }
    return json.dumps(data)

@app.route("/checkYDataset", methods=["POST"])
def checkYDataset():
    global Y, X
    file_n = request.files["file"]
    file_r = file_n.stream.read()
    df_file = pd.read_csv(BytesIO(file_r))
    Y = df_file.to_numpy()

    if len(Y) == len(X[0]):
        Y = Y.T
    elif len(Y[0]) == len(X[0]):
        pass
    else:
        return json.dumps({
            "isSuccess": "0",  #Send that the datasets are incompatible
            "size_y": 0
        })
         
    
    print(Y)

    return json.dumps({
            "isSuccess": "1",  #Send that the datasets are compatible
            "size_y": len(Y)
        })



if __name__ == "__main__":
    app.run(debug= True)