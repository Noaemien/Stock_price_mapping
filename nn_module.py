import numpy as np


class Neural_Network:
    def __init__(self, X, Y, layer_neurons = [10, 10], layer_activations = ["RELU", "LINEAR"], optimisation_function = "ADAM", cost_function = "MSE"):

        self.params = {}
        self.layer_nbr = len(layer_neurons)

        self.features = X.shape[0]

        self.X = X
        self.Y = Y
        
        self.optimisation_function = optimisation_function.upper()
        self.cost_function = cost_function.upper()

        #Initialise parameters
        for i in range(self.layer_nbr):
            layer = str(i + 1)

            #Initialise parameters of first layer.
            if layer == "1":
                self.params["W1"] =  np.random.uniform(-1, 1, (layer_neurons[i], self.features))
                self.params["b1"] = np.random.uniform(-1, 1, (layer_neurons[i], 1))

                self.params["Act1"] = layer_activations[i].upper()

                continue
                
            #Initialise parameters of other layers.
            self.params["W" + layer] =  np.random.uniform(-1, 1, (layer_neurons[i], layer_neurons[i - 1])) * np.sqrt(2/layer_neurons[i - 1])
            self.params["b" + layer] = np.random.uniform(-1, 1, (layer_neurons[i], 1)) * np.sqrt(2/layer_neurons[i - 1])

            self.params["Act" + layer] = layer_activations[i].upper()
        
        self.init_optimisation()



    def init_optimisation(self):
        if self.optimisation_function == "GRADIENTDESCENT":
            pass
        elif self.optimisation_function == "ADAM":
            self.init_adam()
            

    

    def init_adam(self):
        self.V = {}
        
        for i in range(self.layer_nbr):
            layer = str(i + 1)
            self.V["dW" + layer] = np.zeros(np.shape(self.params["W" + layer]))
            self.V["db" + layer] = np.zeros(np.shape(self.params["b" + layer]))

        self.S = self.V.copy()

        

    #
    # TO DO
    #
    def activation(self, Z, layer):
        if self.params["Act" + layer] == "RELU":
            return np.maximum(0, Z)
        elif self.params["Act" + layer] == "LINEAR":
            return Z
        elif self.params["Act" + layer] == "TANH":
            return (np.exp(Z) - np.exp(-Z))/(np.exp(Z) + np.exp(-Z))
        elif self.params["Act" + layer] == "SIGMOID":
            return 1 / ( 1 + np.exp(-Z))
        return 1
    #
    # TO DO
    #
    def d_activation(self, A, layer):
        layer_act = self.params["Act" + layer]
        if layer_act == "RELU":
            drelu = self.forward_cache["Z" + layer] > 0
            out = A * drelu 
        elif layer_act == "LINEAR":
            return A
        elif layer_act == "TANH":
            return 1 - A **2
        elif layer_act == "SIGMOID":
            return A * (1 - A)

        return out
    
    def get_cost(self):
        m = len(self.Y[0])
        if self.cost_function == "MSE":
            return (1/m) * 0.5 * np.sum((self.preds - self.Y) ** 2) #see references for why i multiply by 0.5
    #
    # TO DO
    #
    def get_d_cost(self):
        if self.cost_function == "MSE":
            return (self.preds - self.Y)

        elif self.cost_function == "LOG":
            pass
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
                if int(layer) == self.layer_nbr:
                    self.preds = self.forward_cache["A1"]
                continue
            #Forward pass with n_st layer: Z_n = W_n * A_n-1 + b_n
            self.forward_cache["Z" + layer] = self.params["W" + layer].dot(self.forward_cache["A" + str(i)]) + self.params["b" + layer] 
            self.forward_cache["A" + layer] = self.activation(self.forward_cache["Z" + layer], layer) #Activation function

            if int(layer) == self.layer_nbr:
                self.preds = self.forward_cache["A" + layer] 
    #
    # WORKING BUT NEED TO IMPLEMENT FUNCTIONALITY FOR IF NN IS ONE LAYER LONG
    #       
    def backward(self):
        m = len(self.Y[0])
        self.backward_cache = {}
        d_cost = self.get_d_cost()
        for i in reversed(range(self.layer_nbr)):
            layer = str(i + 1)
            if i + 1 == self.layer_nbr:
                self.backward_cache["dZ" + layer] = self.d_activation(d_cost, layer)
                assert(np.shape(self.backward_cache["dZ" + layer]) == np.shape(self.forward_cache["Z" + layer]))
                
                self.backward_cache["dW" + layer] = (1/m) * (self.backward_cache["dZ" + layer].dot(self.forward_cache["A" + str(i)].T))
                assert(np.shape(self.backward_cache["dW" + layer]) == np.shape(self.params["W" + layer]))

                self.backward_cache["db" + layer] = (1/m) * np.sum(self.backward_cache["dZ" + layer], axis = 1, keepdims = True)
                assert(np.shape(self.backward_cache["db" + layer]) == np.shape(self.params["b" + layer]))
                
                self.backward_cache["dZ" + str(i)] = self.d_activation(self.params["W" + layer].T.dot(self.backward_cache["dZ" + layer]), str(i))
                assert(np.shape(self.backward_cache["dZ" + str(i)]) == np.shape(self.forward_cache["Z" + str(i)]))
                
            else:
                
                
                self.backward_cache["db" + layer] = (1/m) * np.sum(self.backward_cache["dZ" + layer], axis = 1, keepdims = True)
                assert(np.shape(self.backward_cache["db" + layer]) == np.shape(self.params["b" + layer]))

                if layer != "1":
                    self.backward_cache["dW" + layer] = (1/m) * (self.backward_cache["dZ" + layer].dot(self.forward_cache["A" + str(i)].T))
                    assert(np.shape(self.backward_cache["dW" + layer]) == np.shape(self.params["W" + layer])) 

                    self.backward_cache["dZ" + str(i)] = self.d_activation(self.params["W" + layer].T.dot(self.backward_cache["dZ" + layer]), str(i))
                    assert(np.shape(self.backward_cache["dZ" + str(i)]) == np.shape(self.forward_cache["Z" + str(i)]))
                else:
                    self.backward_cache["dW" + layer] = (1/m) * (self.backward_cache["dZ" + layer].dot(self.X.T))
                    assert(np.shape(self.backward_cache["dW" + layer]) == np.shape(self.params["W" + layer]))  
    
    def grad_descent(self, alpha):
        for i in range(self.layer_nbr):
            layer = str(i + 1)
            self.params["W" + layer] -= alpha * self.backward_cache["dW" + layer]
            self.params["b" + layer] -= alpha * self.backward_cache["db" + layer]
            
    def adam(self, alpha, beta1, beta2, it):
        epsilon = 1e-8
        for i in range(self.layer_nbr):
            layer = str(i + 1)
            self.V["dW" + layer] = beta1 * self.V["dW" + layer] + (1 - beta1) * self.backward_cache["dW" + layer]
            self.V["db" + layer] = beta1 * self.V["db" + layer] + (1 - beta1) * self.backward_cache["db" + layer]
            self.S["dW" + layer] = beta2 * self.S["dW" + layer] + (1 - beta2) * self.backward_cache["dW" + layer] **2
            self.S["db" + layer] = beta2 * self.S["db" + layer] + (1 - beta2) * self.backward_cache["db" + layer] **2

            VdW_c = self.V["dW" + layer]/(1 - beta1 ** it)
            SdW_c = self.S["dW" + layer]/(1 - beta2 ** it)  
            Vdb_c = self.V["db" + layer]/(1 - beta1 ** it)
            Sdb_c = self.S["db" + layer]/(1 - beta2 ** it)  


            self.params["W" + layer] -= alpha * (VdW_c/(np.sqrt(SdW_c) + epsilon))
            self.params["b" + layer] -= alpha * (Vdb_c/(np.sqrt(Sdb_c) + epsilon))


    def optimisation(self, alpha, beta1, beta2, it):
        if self.optimisation_function == "GRADIENTDESCENT":
            self.grad_descent(alpha)
        elif self.optimisation_function == "ADAM":
            self.adam(alpha, beta1, beta2, it)
        elif self.optimisation_function == "MOMENTUM":
            pass
        elif self.optimisation_function == "RMSPROP":
            pass


    #
    # WORKING
    #
    def train(self, alpha, it, beta1 = 0.9, beta2 = 0.999):
        self.forward()
        self.backward()
        self.optimisation(alpha, beta1, beta2, it)
        return self.get_cost()
        
                
                
                
                
if __name__ == "__main__":
    X = np.random.uniform(-1, 5, (1, 500))
    Y = X ** 2

    nn = Neural_Network(X, Y, [128, 128, 1], optimisation_function="GRADIENTDESCENT")
    nn.train(0.001, 1)


