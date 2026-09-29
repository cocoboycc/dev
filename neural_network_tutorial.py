import numpy as np
import matplotlib.pyplot as plt
import scipy


class Layer_Dense:
    def __init__(self, n_inputs, n_neurons):
        self.weights = 0.10 * np.random.randn(n_inputs, n_neurons)
        self.biases = np.zeros((1, n_neurons))

    def forward(self, inputs):
        self.output = np.dot(inputs, self.weights) + self.biases

class Activation_RELU: 
    def forward(self, inputs): 
        self.output=np.maximum(0, inputs)

class Activation_Softmax:
    def forward(self, inputs):
        exp_values = np.exp(inputs - np.max(inputs, axis=1, keepdims=True))
        probabilities = exp_values / np.sum(exp_values, axis=1, keepdims=True)
        self.output = probabilities

class Loss: 
    def calculate(self, output, y):
        sample_losses = self.forward(output, y)
        data_loss = np.mean(sample_losses)
        return data_loss

class Loss_CategoricalCrossentropy(Loss):
    def forward(self, y_pred, y_true):
        samples = len(y_pred)
        y_pred_clipped = np.clip(y_pred, 1e-7, 1 - 1e-7)
        if len(y_true.shape) == 1:
            correct_confidences = y_pred_clipped[range(samples), y_true]
        elif len(y_true.shape) == 2:
            correct_confidences = np.sum(y_pred_clipped * y_true, axis=1)
        negative_log_likelihoods = -np.log(correct_confidences)
        return negative_log_likelihoods

def accuracy(pred, y):
    predictions= np.argmax(pred, axis=1)
    if len(y.shape)==2:
        y= np.argmax(y, axis=1)
    accuracy= np.mean(predictions==y)
    return accuracy
class_targets = np.array([0, 1, 1])

min_loss=1
layer1= Layer_Dense(2,3)
inputs= [[1,2],
        [4,5],
        [7,8]]

layer2= Layer_Dense(3,3)

for i in range(100000):
    layer1.weights += 0.05 *np.random.randn(2,3) 
    layer2.weights += 0.05*np.random.randn(3,3) 
    layer1.biases += 0.05* np.random.randn(1,3) 
    layer2.biases += 0.05* np.random.randn(1,3) 

    layer1.forward(inputs)
    relu_step= Activation_RELU()
    relu_step.forward(layer1.output)
    layer2.forward(relu_step.output)
    softmax_step= Activation_Softmax()
    softmax_step.forward(layer2.output)
    Losses= Loss_CategoricalCrossentropy()
    loss= Losses.calculate(softmax_step.output, class_targets)
    curr_min_loss= loss

    if curr_min_loss<min_loss: 
        min_loss= curr_min_loss
        print (f"Iteration:{i}: Min_Loss: {min_loss}")
        best_weights_1 = layer1.weights
        best_weights_2 = layer2.weights
        best_biases_1 = layer1.biases
        best_biases_2 = layer2.biases
        best_output = softmax_step.output.copy()

print (min_loss)
print(best_weights_1, best_weights_2, best_biases_1, best_biases_2)
print (best_output)