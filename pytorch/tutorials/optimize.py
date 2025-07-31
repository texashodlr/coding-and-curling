import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor

training_data = datasets.FashionMNIST(
        root="data",
        train=True,
        download=True,
        transform=ToTensor()
)

test_data = datasets.FashionMNIST(
        root="data",
        train=False,
        download=True,
        transform=ToTensor()
)

train_dataloader = DataLoader(training_data, batch_size=64)
test_dataloader  = DataLoader(test_data, batch_size=64)

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

model = NeuralNetwork()

# Hyper parameters!
#   Adjustable parameters that let you control the model optimization process,
#   different hyperparameter values can impact model training and convergence rates
# Hyper Definitions:
#   Number of Epochs: number of times to iterate over the dataset
#   Batch Size: number of data samples propagated through the network before the parameters are updated
#   Learning Rate: how much to update models parameters at each batch/epoch smaller values yield slow learning speed, while large may result in unpred' behaviour during training

learning_rate = 1e-3
batch_size    = 64
epochs        = 5

# Optimization Loop
# Once we set our hyperparameters we cna then trian and optimize the model with an optimization loop
#   Each iteration of the optimization loop is called an epoch
#   Epoch consists of: Train loop- iterate over the training dataset and try to converge to optimal params
#                      Validation/Test Loop-iterate over the test dataset to check if model perf is improving

# Loss Function
# Measures (the function that is) the degree of dissimilarity of obtained result to the traget value and it is the loss function that we want to minimize during trianing
# TO calculate the loss we make a prediction using the inputs of our given data sample and compare it against the true data label value

    # Init
# Cross Entropy Loss recieves our model's output logits and then normalizes the logits and compute the prediction error.

# Optimizer (SGD basically)

# Full training loop
def train_loop (dataloader, model, loss_fn, optimizer):
    size = len(dataloader.dataset)
    model.train()
    for batch, (X, y) in enumerate(dataloader):
        pred = model(X)
        loss = loss_fn(pred, y)

        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        if batch % 100 == 0:
            loss, current = loss.item(), batch * batch_size + len(X)
            print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")

def test_loop(dataloader, model, loss_fn):
    model.eval()
    size=len(dataloader.dataset)
    num_batches = len(dataloader)
    test_loss, correct = 0, 0

    with torch.no_grad():
        for X, y in dataloader:
            pred = model(X)
            test_loss += loss_fn(pred, y).item()
            correct   += (pred.argmax(1) == y).type(torch.float).sum().item()

    test_loss /= num_batches
    correct /= size
    print(f"Test Error: \n Accuracy: {(100*correct):>0.1f}%, Avg loss: {test_loss:>8f} \n")


loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

epochs = 10
for t in range(epochs):
    print(f"Epoch {t+1}\n-------------------------------")
    train_loop(train_dataloader, model, loss_fn, optimizer)
    test_loop(test_dataloader, model, loss_fn)
print("Done!")
