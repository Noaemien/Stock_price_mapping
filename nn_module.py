import numpy as np


class Neural_Network:
    def __init__(self, X, Y, layer_neurons, hidden_activation, end_activation, optimisation_function):

        self.params = {}
        self.layer_nbr = len(layer_neurons)

        self.features = X.shape[0]

        self.X = X
        self.Y = Y
        

        end_activation = end_activation.upper()
        hidden_activation = hidden_activation.upper()

        #Initialise parameters
        for i in range(self.layer_nbr):
            layer = str(i + 1)

            #Initialise parameters of first layer.
            if layer == "1":
                self.params["W1"] =  np.random.rand(layer_neurons[i], self.features) - 0.5
                self.params["b1"] = np.random.rand(layer_neurons[i], 1) - 0.5

                #Set activation of first layer to end activation if number of layers is equals to 1
                if len(layer_neurons) == 1:
                    self.params["Act1"] = end_activation
                else:
                    self.params["Act1"] = hidden_activation

                continue
                
            #Initialise parameters of other layers.
            self.params["W" + layer] =  np.random.rand(layer_neurons[i], layer_neurons[i - 1]) - 0.5
            self.params["b" + layer] = np.random.rand(layer_neurons[i], 1) - 0.5

            if len(layer_neurons) == i + 1:
                self.params["Act" + layer] = end_activation
            else:
                self.params["Act" + layer] = hidden_activation

    def activation(self, Z, layer):
        if self.params["Act" + layer] == "RELU":
            out = relu(Z)

        return out


    def forward(self):
        self.forward_cache = {}
        
        for i in range(self.layer_nbr):
            layer = str(i + 1)
            if layer == "1":
                self.forward_cache["Z1"] = self.params["W1"].dot(self.X) + self.params["b1"] #Forward pass with 1st layer: W1 * X + b
                self.forward_cache["A1"] = self.activation(self.forward_cache["Z1"], layer)



def relu(Z):
    return np.maximum(0, Z)




