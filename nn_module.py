import numpy as np


class Neural_Network:
    def __init__(self, X, Y, layer_neurons = [10, 10], hidden_activation = "RELU", end_activation = "RELU", optimisation_function = "ADAM", cost_function = "MSE"):

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

            if self.layer_nbr == i + 1:
                self.params["Act" + layer] = end_activation
            else:
                self.params["Act" + layer] = hidden_activation

    #
    # TO DO
    #
    def activation(self, Z, layer):
        if self.params["Act" + layer] == "RELU":
            out = np.maximum(0, Z)

        return out
    #
    # TO DO
    #
    def d_activation(self, A, layer):
        if self.params["Act" + layer] == "RELU":
            if int(layer) == self.layer_nbr:
                drelu = self.forward_cache["Z" + layer] > 0 #Wrong, needs to be corrected
                out = A * drelu 
            elif layer != "1":
                drelu = self.forward_cache["Z" + str(int(layer) - 1)]
                out = A * drelu 
            else: out = 0
            
        return out
    
    
    #
    # TO DO
    #
    def get_d_cost(self):
        return self.Y
    
    
    #
    # WORKING
    #
    def forward(self):
        self.forward_cache = {}
        
        for i in range(self.layer_nbr):
            layer = str(i + 1)
            if layer == "1":
                self.forward_cache["Z1"] = self.params["W1"].dot(self.X) + self.params["b1"] #Forward pass with 1st layer: W1 * X + b
                self.forward_cache["A1"] = self.activation(self.forward_cache["Z1"], layer) #Activation function
                continue
            #Forward pass with n_st layer: Z_n = W_n * A_n-1 + b_n
            self.forward_cache["Z" + layer] = self.params["W" + layer].dot(self.forward_cache["A" + str(i)]) + self.params["b" + layer] 
            self.forward_cache["A" + layer] = self.activation(self.forward_cache["Z" + layer], layer) #Activation function
    #
    # TO DO
    #       
    def backward(self):
        self.backward_cache = {}
        d_cost = self.get_d_cost()
        for i in reversed(range(self.layer_nbr)):
            layer = str(i + 1)
            print(layer)
            if i + 1 == self.layer_nbr:
                self.backward_cache["dZ" + layer] = self.d_activation(d_cost, layer)
                assert(np.shape(self.backward_cache["dZ" + layer]) == np.shape(self.forward_cache["Z" + layer]))
                
                self.backward_cache["dW" + layer] = self.backward_cache["dZ" + layer].dot(self.forward_cache["A" + str(i)].T)
                assert(np.shape(self.backward_cache["dW" + layer]) == np.shape(self.params["W" + layer]))
                
                
                self.backward_cache["dZ" + str(i)] = self.d_activation(self.params["W" + layer].T.dot(self.forward_cache["dZ" + layer]), layer) #Not working yet
                assert(np.shape(self.backward_cache["dZ" + str(i)]) == np.shape(self.forward_cache["Z" + str(i)]))
                
            else:
                #self.backward_cache["dZ" + layer] = self.d_activation(self.params["W" + layer].T.dot(self.forward_cache["dZ" + str(int(layer) + 1)]), layer) #Not working yet
                
                print(np.shape(self.params["W" + layer]), np.shape(self.forward_cache["Z" + layer]))
                #print(np.shape(self.backward_cache["dZ" + layer]), np.shape(self.forward_cache["Z" + layer]))
                
                #assert(np.shape(self.backward_cache["dZ" + layer]) == np.shape(self.forward_cache["Z" + layer]))
                
                
                
                
                

X = np.random.uniform(0, 1, (10, 100))
Y = np.random.uniform(0, 1, (10, 100))

nn = Neural_Network(X, Y, [512, 515, 511, 513, 10])

for i in range(100):
    nn.forward()
    nn.backward()



