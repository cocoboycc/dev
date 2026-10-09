import numpy as np
import matplotlib.pyplot as plt
import os
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from nnfs.datasets import spiral_data
import nnfs

device = torch.accelerator.current_accelerator().type if torch.accelerator.is_available() else "cpu"

class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(28*28, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 10),
        )

    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits


model = NeuralNetwork().to(device)
print(model)

X = torch.rand(1, 28, 28, device=device)
logits = model(X)
pred_probab = nn.Softmax(dim=1)(logits)
y_pred = pred_probab.argmax(1)
print(f"Predicted class: {y_pred}")

#input_image = torch.rand(3,28,28)
X, y = spiral_data(samples=100, classes=3)
X = torch.from_numpy(X).float()
y = torch.from_numpy(y).long()
layer1 = nn.Linear(in_features=2, out_features=20)
flatten= nn.Flatten()
seq_modules = nn.Sequential(
    flatten,
    layer1,
    nn.ReLU(),
    nn.Linear(20, 10)
)
logits = seq_modules(X)
softmax = nn.Softmax(dim=1)
pred_probab = softmax(logits)
#testing data and printing result
X_test, y_test = spiral_data(samples=100, classes=3)
X_test = torch.from_numpy(X_test).float()
y_test = torch.from_numpy(y_test).long()
logits_test = seq_modules(X_test)
pred_probab_test = softmax(logits_test)
y_pred_test = pred_probab_test.argmax(1)
print(f"Predicted classes for test data: {y_pred_test}")
plt.figure()
plt.scatter(X_test[:, 0], X_test[:, 1], c=y_pred_test, cmap="brg")
plt.show()