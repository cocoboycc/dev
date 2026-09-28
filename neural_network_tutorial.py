import numpy as np
import matplotlib.pyplot as plt
import scipy


class Layer_Dense:
    def __init__(self, n_inputs, n_neurons):
        self.weights = 0.10 * np.random.randn(n_inputs, n_neurons)
        self.biases = np.zeros((1, n_neurons))

    def forward(self, inputs):
        self.output = np.dot(inputs, self.weights) + self.biases

layer= Layer_Dense(3,3)
layer.forward([[1,2,3]])
print(layer.output)


def RELU(input): 
    return np.maximum(0,input)  
print (RELU(-2))

total_values= [1,2,3]
weights_1=[0.2, 0.8, -0.5]
weights_2=[0.5, -0.91, 0.26]
weights_3=[-0.26, -0.27, 0.17]
total_weights= [weights_1, weights_2, weights_3]


bias_1= 2
bias_2=3
bias_3=0.5
total_biases=[bias_1, bias_2, bias_3]
total_biases= np.sum(total_biases)
output_layers=[0,0,0]

output_layers= np.dot(total_weights, total_values) + total_biases
#print (np.sum(output_layers))

