import os
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

device = torch.accelerator.current_accelerator().type if torch.accelerator.is_available() else "cpu"
print(f"Using {device} device")

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

# Do not call model.forward() directly!
X = torch.rand(1, 28, 28, device=device)
logits = model(X)
pred_probab = nn.Softmax(dim=1)(logits)
y_pred = pred_probab.argmax(1)
print(f"Predicted class: {y_pred}")

# Model Layers
input_image = torch.rand(3,28,28)
print(input_image.size())

# Flattening the images into 784 px arrays
flatten = nn.Flatten()
flat_image = flatten(input_image)
print(flat_image.size())

# nn.linear applies the linear transformation the input using its stored weights and biases
layer1 = nn.Linear(in_features=28*28, out_features=20)
hidden1 = layer1(flat_image)
print(hidden1.size())

# ReLU! Non-linear activations are what create the complex mappings between the models inputs and outputs
# Theyre applied after linear transofmraitons to introduce nonlinearity helping nns learn a wide array of phenomena

print(f"Before ReLU: {hidden1}\n\n")
hidden1 = nn.ReLU()(hidden1)
print(f"After ReLU: {hidden1}")


# Sequential, is an ordered container of modules. The data is pass through all the modules int he same order as defined you can use sequential containers to put together a quick network like seq_modules.

seq_modules = nn.Sequential(
        flatten,
        layer1,
        nn.ReLU(),
        nn.Linear(20, 10)
)
input_image = torch.rand(3,28,28)
logits = seq_modules(input_image)

# Softmax: last linear layer of the nn returns logits whch are raw values in the -inf to +inf range which ar passed to the 
# Softmax module the logits are scaled values [0, 1] rep'ng the models predid' probs for each class
# Dim param indicates the dimension along which the values must sum to 1

softmax = nn.Softmax(dim=1)
pred_probab = softmax(logits)

# Model Params
print(f"Model Structure: {model}\n\n")

for name, param in model.named_parameters():
    print(f"Layer: {name} | Size: {param.size()} | Values : {param[:2]}\n")
