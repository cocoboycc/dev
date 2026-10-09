import numpy as np
import matplotlib.pyplot as plt
import scipy

# Dense layer
class Layer_Dense:
    # Layer initialization
    def __init__(self, n_inputs, n_neurons):
        # Initialize weights and biases
        self.weights = 0.01 * np.random.randn(n_inputs, n_neurons)
        self.biases = np.zeros((1, n_neurons))

    # Forward pass
    def forward(self, inputs):
        # Remember input values
        self.inputs = inputs
        # Calculate output values from input ones, weights and biases
        self.output = np.dot(inputs, self.weights) + self.biases

    # Backward pass
    def backward(self, dvalues):
        # Gradients on parameters
        self.dweights = np.dot(self.inputs.T, dvalues)
        self.dbiases = np.sum(dvalues, axis=0, keepdims=True)
        # Gradient on values
        self.dinputs = np.dot(dvalues, self.weights.T)


# ReLU activation
class Activation_ReLU:
    # Forward pass
    def forward(self, inputs):
        # Remember input values
        self.inputs = inputs
        # Calculate output values from inputs
        self.output = np.maximum(0, inputs)

    # Backward pass
    def backward(self, dvalues):
        # Since we need to modify the original variable,
        # let’s make a copy of values first
        self.dinputs = dvalues.copy()
        # Zero gradient where input values were negative
        self.dinputs[self.inputs <= 0] = 0

# Softmax activation
class Activation_Softmax:
 # Forward pass
 def forward(self, inputs):
 # Get unnormalized probabilities
  exp_values = np.exp(inputs - np.max(inputs, axis=1, keepdims=True))
 # Normalize them for each sample
  probabilities = exp_values / np.sum(exp_values, axis=1,keepdims=True)
  self.output = probabilities



# Common loss class
class Loss:
 # Calculates the data and regularization losses
 # given model output and ground truth values
 def calculate(self, output, y):
  # Calculate sample losses
  sample_losses = self.forward(output, y)
  # Calculate mean loss
  data_loss = np.mean(sample_losses)
  # Return loss
  return data_loss


class Loss_CategoricalCrossentropy(Loss):
    # Forward pass
    def forward(self, y_pred, y_true):
        # Number of samples in a batch
        samples = len(y_pred)

        # Clip data to prevent division by 0
        # Clip both sides to not drag mean towards any value
        y_pred_clipped = np.clip(y_pred, 1e-7, 1 - 1e-7)

        # Probabilities for target values -
        # only if categorical labels
        if len(y_true.shape) == 1:
            correct_confidences = y_pred_clipped[
                range(samples),
                y_true
            ]
        # Mask values - only for one-hot encoded labels
        elif len(y_true.shape) == 2:
            correct_confidences = np.sum(
                y_pred_clipped * y_true,
                axis=1
            )

        # Losses
        negative_log_likelihoods = -np.log(correct_confidences)
        return negative_log_likelihoods

    # Backward pass
    def backward(self, dvalues, y_true):
        # Number of samples
        samples = len(dvalues)
        # Number of labels in every sample
        # We'll use the first sample to count them
        labels = len(dvalues[0])

        # If labels are sparse, turn them into one-hot vector
        if len(y_true.shape) == 1:
            y_true = np.eye(labels)[y_true]

        # Calculate gradient
        self.dinputs = -y_true / dvalues
        # Normalize gradient
        self.dinputs = self.dinputs / samples


# Softmax classifier - combined Softmax activation
# and cross-entropy loss for faster backward step
class Activation_Softmax_Loss_CategoricalCrossentropy:
    # Creates activation and loss function objects
    def __init__(self):
        self.activation = Activation_Softmax()
        self.loss = Loss_CategoricalCrossentropy()

    # Forward pass
    def forward(self, inputs, y_true):
        # Output layer's activation function
        self.activation.forward(inputs)
        # Set the output
        self.output = self.activation.output
        # Calculate and return loss value
        return self.loss.calculate(self.output, y_true)

    # Backward pass
    def backward(self, dvalues, y_true):
        # Number of samples
        samples = len(dvalues)
        # If labels are one-hot encoded,
        # turn them into discrete values
        if len(y_true.shape) == 2:
            y_true = np.argmax(y_true, axis=1)
        # Copy so we can safely modify
        self.dinputs = dvalues.copy()
        # Calculate gradient
        self.dinputs[range(samples), y_true] -= 1
        # Normalize gradient
        self.dinputs = self.dinputs / samples

from nnfs.datasets import spiral_data
import nnfs

"""
X,y = spiral_data(100, classes=3)
dense1= Layer_Dense(2,3)
activation1= Activation_ReLU()
dense2= Layer_Dense(3,3)
loss_activation= Activation_Softmax_Loss_CategoricalCrossentropy()
dense1.forward(X)
activation1.forward(dense1.output)
dense2.forward(activation1.output)
loss = loss_activation.forward(dense2.output, y)


# Let’s see output of the first few samples:
print(loss_activation.output[:5])
# Print loss value
print('loss:', loss)
# Calculate accuracy from output of activation2 and targets
# calculate values along first axis
predictions = np.argmax(loss_activation.output, axis=1)
if len(y.shape) == 2:
 y = np.argmax(y, axis=1)
accuracy = np.mean(predictions == y)
# Print accuracy
print('acc:', accuracy)
# Backward pass
loss_activation.backward(loss_activation.output, y)
dense2.backward(loss_activation.dinputs)
activation1.backward(dense2.dinputs)
dense1.backward(activation1.dinputs)
# Print gradients
print(dense1.dweights)
print(dense1.dbiases)
print(dense2.dweights)
print(dense2.dbiases)
"""
class Optimizer_GD: 
    def __init__(self, learning_rate=1):
      self.learning_rate= learning_rate

    def update_params(self, layer): 
       layer.weights+= -self.learning_rate * layer.dweights
       layer.biases+= -self.learning_rate * layer.dbiases

class Optimizer_SGD: 
    def __init__(self, learning_rate=1., decay=0., momentum=0. ):
        self.learning_rate= learning_rate
        self.current_learning_rate= learning_rate
        self.decay= decay
        self.iterations=0
        self.momentum= momentum

    def pre_update_params(self): 
        if self.decay: 
           self.current_learning_rate= self.learning_rate* (1/(1+ self.decay*self.iterations))

    def update_params(self, layer):

        if self.momentum: 
            if not hasattr(layer, 'weight_momentums'):
               layer.weight_momentums= np.zeros_like(layer.weights)
               layer.bias_momentums= np.zeros_like(layer.biases)

            weight_updates= self.momentum * layer.weight_momentums - self.current_learning_rate* layer.dweights
            layer.weight_momentums= weight_updates

            bias_updates= self.momentum* layer.bias_momentums- self.current_learning_rate*layer.dbiases
            layer.bias_momentums= bias_updates
           
        else: 
           weight_updates= -self.current_learning_rate* layer.dweights
           bias_updates= -self.current_learning_rate* layer.dbiases

        layer.weights+= -self.current_learning_rate * layer.dweights
        layer.biases+= -self.current_learning_rate * layer.dbiases

    def post_update_params(self):
       self.iterations+=1 
#Gradient Descent with Back and Forward Propagation

class Optimizer_Adam:
    # Initialize optimizer - set settings
    def __init__(self, learning_rate=0.001, decay=0., epsilon=1e-7, beta_1=0.9, beta_2=0.999):
        self.learning_rate = learning_rate
        self.current_learning_rate = learning_rate
        self.decay = decay
        self.iterations = 0
        self.epsilon = epsilon
        self.beta_1 = beta_1
        self.beta_2 = beta_2

    # Call once before any parameter updates
    def pre_update_params(self):
        if self.decay:
            self.current_learning_rate = self.learning_rate * (1. / (1. + self.decay * self.iterations))

    # Update parameters
    def update_params(self, layer):
        # If layer does not contain cache arrays, create them filled with zeros
        if not hasattr(layer, 'weight_cache'):
            layer.weight_momentums = np.zeros_like(layer.weights)
            layer.weight_cache = np.zeros_like(layer.weights)
            layer.bias_momentums = np.zeros_like(layer.biases)
            layer.bias_cache = np.zeros_like(layer.biases)

        # Update momentum with current gradients
        layer.weight_momentums = self.beta_1 * layer.weight_momentums + (1 - self.beta_1) * layer.dweights
        layer.bias_momentums = self.beta_1 * layer.bias_momentums + (1 - self.beta_1) * layer.dbiases

        # Get corrected momentum
        # self.iteration is 0 at first pass and we need to start with 1 here
        weight_momentums_corrected = layer.weight_momentums / (1 - self.beta_1 ** (self.iterations + 1))
        bias_momentums_corrected = layer.bias_momentums / (1 - self.beta_1 ** (self.iterations + 1))

        # Update cache with squared current gradients
        layer.weight_cache = self.beta_2 * layer.weight_cache + (1 - self.beta_2) * layer.dweights**2
        layer.bias_cache = self.beta_2 * layer.bias_cache + (1 - self.beta_2) * layer.dbiases**2

        # Get corrected cache
        weight_cache_corrected = layer.weight_cache / (1 - self.beta_2 ** (self.iterations + 1))
        bias_cache_corrected = layer.bias_cache / (1 - self.beta_2 ** (self.iterations + 1))

        # Vanilla SGD parameter update + normalization with square rooted cache
        layer.weights += -self.current_learning_rate * weight_momentums_corrected / (np.sqrt(weight_cache_corrected) + self.epsilon)
        layer.biases += -self.current_learning_rate * bias_momentums_corrected / (np.sqrt(bias_cache_corrected) + self.epsilon)

    # Call once after any parameter updates
    def post_update_params(self):
        self.iterations += 1

class Layer_Dropout: 

    def __init__(self, rate):
        self.rate = 1-rate

    def forward(self, inputs):
        self.inputs=inputs
        self.binary_mask= np.random.binomial(1,self.rate, size=inputs.shape)/ self.rate
        self.output = inputs * self.binary_mask

    def backward(self, dvalues): 
        self.dinputs= dvalues* self.binary_mask


X,y= spiral_data(100, classes=3)
plt.scatter(X[:,0],X[:,1], c=y, cmap="brg")
plt.show()
dense1= Layer_Dense(2,64)
activation1= Activation_ReLU()
dropout1= Layer_Dropout(0.1)
dense2= Layer_Dense(64,3)
loss_activation= Activation_Softmax_Loss_CategoricalCrossentropy()
optimizer= Optimizer_Adam(decay=1e-3)

for epoch in range(40001):

    dense1.forward(X)
    activation1.forward(dense1.output)
    dropout1.forward(activation1.output)
    dense2.forward(activation1.output)
    loss = loss_activation.forward(dense2.output,y)
    predictions= np.argmax(loss_activation.output, axis=1)
    if len(y.shape)==2:
       y=np.argmax(y,axis=1)
    accuracy= np.mean(predictions==y)

    if not epoch %100:
       print (f'epoch={epoch},' + f'acc: {accuracy}' + f'loss: {loss}')

    #Backward pass
    loss_activation.backward(loss_activation.output, y)
    dense2.backward(loss_activation.dinputs)
    dropout1.backward(dense2.dinputs)
    activation1.backward(dense2.dinputs)
    dense1.backward(activation1.dinputs)
    optimizer.pre_update_params()
    optimizer.update_params(dense1)
    optimizer.update_params(dense2)
    optimizer.post_update_params()

X,y= spiral_data(100, classes=3)
##predicting the colors with the trained model
dense1.forward(X)
activation1.forward(dense1.output)
dense2.forward(activation1.output)
predictions= np.argmax(dense2.output, axis=1)
##printing the predicted colors
plt.scatter(X[:,0],X[:,1], c=predictions, cmap="brg")
accuracy = np.mean(predictions == y)
print (f"Final accuracy:{accuracy}")
plt.show()