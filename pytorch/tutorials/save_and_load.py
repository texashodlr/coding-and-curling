import torch
import torchvision.models as models

model = models.vgg16(weights='IMAGENET1K_V1')
torch.save(model.state_dict(), 'model_weights.pth')

# Loading model weights we need to create an instance of the same model first...
# and then load the parameters using load_state_dict() method

model = models.vgg16() # We do not specify ``weights``, i.e. create untrained model
model.load_state_dict(torch.load('model_weights.pth', weights_only=True))
print(model.eval())

torch.save(model, 'model.pth')

model = torch.load('model.pth', weights_only=False)