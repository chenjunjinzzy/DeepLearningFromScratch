# Import necessary libraries
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


# Define a simple test function, such as a quadratic function, using two features
def quadratic_function(x):
    return x[0] ** 2 + x[1] ** 2


# Define the gradient of the quadratic function
def gradient_quadratic_function(x):
    return np.array([2 * x[0], 2 * x[1]])
# Define SGD algorithm
def sgd(loss_func, grad_func, initial_x, learning_rate, num_iterations):
    x = initial_x
    x_history = [x]
    for _ in range(num_iterations):
        grad = grad_func(x)
        x = x - learning_rate * grad
        x_history.append(x)
    return x_history


# Define Momentum algorithm
def momentum(loss_func, grad_func, initial_x, learning_rate, momentum_rate, num_iterations):
    x = initial_x
    velocity = np.zeros_like(x)
    x_history = [x]
    for _ in range(num_iterations):
        grad = grad_func(x)
        velocity = momentum_rate * velocity + learning_rate * grad
        x = x - velocity
        x_history.append(x)
    return x_history


# Define Adagrad algorithm
def adagrad(loss_func, grad_func, initial_x, learning_rate, num_iterations):
    x = initial_x
    gradient_squared_sum = np.zeros_like(initial_x)
    x_history = [x]
    for _ in range(num_iterations):
        grad = grad_func(x)
        gradient_squared_sum += grad ** 2
        adagrad_adjusted_gradient = learning_rate * grad / np.sqrt(gradient_squared_sum + 1e-8)
        x = x - adagrad_adjusted_gradient
        x_history.append(x)
    return x_history


# Define Adam algorithm
def adam(loss_func, grad_func, initial_x, learning_rate, beta1, beta2, num_iterations):
    x = initial_x
    m = np.zeros_like(initial_x)  # First moment estimate
    v = np.zeros_like(initial_x)  # Second moment estimate
    t = 0  # Iteration count
    x_history = [x]
    for _ in range(num_iterations):
        t += 1
        grad = grad_func(x)
        m = beta1 * m + (1 - beta1) * grad  # Update first moment
        v = beta2 * v + (1 - beta2) * (grad ** 2)  # Update second moment

        # Compute bias-corrected first moment and second moment estimate
        m_hat = m / (1 - beta1 ** t)
        v_hat = v / (1 - beta2 ** t)

        # Update parameters
        x = x - learning_rate * m_hat / (np.sqrt(v_hat) + 1e-8)
        x_history.append(x)
    return x_history


# Set parameters for the above algorithms
initial_x = np.array([3.0, 3.0])
learning_rate = 0.1
num_iterations = 100
momentum_rate = 0.9
beta1 = 0.9
beta2 = 0.999

# Run different algorithms
x_history_sgd = sgd(quadratic_function, gradient_quadratic_function, initial_x, learning_rate, num_iterations)
x_history_momentum = momentum(quadratic_function, gradient_quadratic_function, initial_x, learning_rate, momentum_rate, num_iterations)
x_history_adagrad = adagrad(quadratic_function, gradient_quadratic_function, initial_x, learning_rate, num_iterations)
x_history_adam = adam(quadratic_function, gradient_quadratic_function, initial_x, learning_rate, beta1, beta2, num_iterations)


# Plot results
plt.figure(figsize=(14, 14))

plt.subplot(2, 2, 1)
plt.plot(np.array(x_history_sgd)[:, 0], np.array(x_history_sgd)[:, 1], label='SGD')
plt.scatter(np.array(x_history_sgd)[:, 0], np.array(x_history_sgd)[:, 1], alpha=0.5)
plt.title('SGD Optimization Path')
plt.xlabel('x1 value')
plt.ylabel('x2 value')
plt.legend()

plt.subplot(2, 2, 2)
plt.plot(np.array(x_history_momentum)[:, 0], np.array(x_history_momentum)[:, 1], label='Momentum')
plt.scatter(np.array(x_history_momentum)[:, 0], np.array(x_history_momentum)[:, 1], alpha=0.5)
plt.title('Momentum Optimization Path')
plt.xlabel('x1 value')
plt.ylabel('x2 value')
plt.legend()

plt.subplot(2, 2, 3)
plt.plot(np.array(x_history_adagrad)[:, 0], np.array(x_history_adagrad)[:, 1], label='Adagrad')
plt.scatter(np.array(x_history_adagrad)[:, 0], np.array(x_history_adagrad)[:, 1], alpha=0.5)
plt.title('Adagrad Optimization Path')
plt.xlabel('x1 value')
plt.ylabel('x2 value')
plt.legend()

plt.subplot(2, 2, 4)
plt.plot(np.array(x_history_adam)[:, 0], np.array(x_history_adam)[:, 1], label='Adam')
plt.scatter(np.array(x_history_adam)[:, 0], np.array(x_history_adam)[:, 1], alpha=0.5)
plt.title('Adam Optimization Path')
plt.xlabel('x1 value')
plt.ylabel('x2 value')
plt.legend()

plt.tight_layout()
plt.show()