import torch

# Back propagation:
#   parameters (model weights) are adjusted according to the gradient
#   of the loss function with respect to the given parameter
# computing the gradients in PyTorch has a built in differentiation engine called
# torch.autograd; which supports automatic computation of gradient for any computational graph

# Simplest 1-Layer NN with input: x, params: w & b and some loss func

x = torch.ones(5)
y = torch.zeros(3)
w = torch.randn(5, 3, requires_grad=True)
b = torch.randn(3, requires_grad=True)
z = torch.matmul(x, w)+b
loss = torch.nn.functional.binary_cross_entropy_with_logits(z, y)

print(f"Gradient function for z = {z.grad_fn}")
print(f"Gradient function for loss = {loss.grad_fn}")


# Need to optimize weights of the parameters, we do thusly by computing derivatives
# of the loss function with respect to parameters (w, b) under some fixed values of x & y
# Compute the derivs. with loss.backward()
loss.backward()
print(w.grad)
print(b.grad)

# Can disable gradient tracking (ex: we want to just run a forward computation using input data)
z = torch.matmul(x, w)+b
print(z.requires_grad)

with torch.no_grad():
    z = torch.matmul(x, w)+b
print(z.requires_grad)

# Can do the same with the detach() method
z = torch.matmul(x, w)+b
z_det = z.detach()
print(z_det.requires_grad)

# We'd want to disable grad tracking for:
#   marking some parameters as frozen
#   speed up computations when you're only doing forward pass for efficiency


# Tensor gradients and jacobian products
inp = torch.eye(4, 5, requires_grad=True)
out = (inp+1).pow(2).t()
out.backward(torch.ones_like(out), retain_graph=True)
print(f"First call\n{inp.grad}")
out.backward(torch.ones_like(out), retain_graph=True)
print(f"\nSecond call\n{inp.grad}")
inp.grad.zero_()
out.backward(torch.ones_like(out), retain_graph=True)
print(f"\nCall after zeroing gradients\n{inp.grad}")


# When calling backward a second time with the same arg
# the value of the grad is diff
# this happens because when doing backward propagation pytorch accumulates the grads
# Thus the value of the computed grads is added to the grad property of all DAG leaf nodes.
