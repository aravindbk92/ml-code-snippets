import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pathlib

# ---Optimization functions---


def calc_cost(X, y, theta):
    return np.sum(np.power((X @ theta) - y, 2)) / (2 * X.shape[0])


def calc_gradient(X, y, theta):
    grad = ((X @ theta) - y) * X
    return (np.sum(grad, axis=0) / X.shape[0]).reshape(-1, 1)


def gradient_descent(X, y, theta, alpha=0.01, iterations=1000):
    cost = []
    for i in range(iterations):
        theta = theta - alpha * calc_gradient(X, y, theta)
        cost.append(calc_cost(X, y, theta))
    return theta, cost


# ---Get data---
data_file = pathlib.Path(__file__).resolve().parent.parent / \
    'data/andrewng/ex1data1.txt'
data = pd.read_csv(data_file, header=None, names=['Population', 'Profit'])
# print(data.describe())
# data.plot(kind='scatter', x='Population', y='Profit', figsize=(12, 8))

# ---Prepare data---
data.insert(0, 'Ones', 1)
X = data.iloc[:, 0:data.shape[1]-1]
y = data.iloc[:, data.shape[1]-1]
# print(X.head())

X = X.to_numpy()
y = y.to_numpy().reshape(-1, 1)
theta = np.zeros([X.shape[1], 1])


# ---Optimize---
initial_cost = calc_cost(X, y, theta)
final_theta, cost_list = gradient_descent(X, y, theta)
final_cost = calc_cost(X, y, final_theta)
print("Initial cost: {}".format(initial_cost))
print("Final cost: {}".format(final_cost))
print("Final theta: \n{}".format(final_theta))

# ---Plot---
x = np.linspace(data.Population.min(), data.Population.max(), 100)
prediction = final_theta[0] + (final_theta[1] * x)

fig, ax = plt.subplots(1, 2, figsize=(12, 8))
ax[0].plot(x, prediction, 'r', label='Prediction')
ax[0].scatter(data.Population, data.Profit, label='Training Data')
ax[0].legend(loc=2)
ax[0].set_xlabel('Population')
ax[0].set_ylabel('Profit')
ax[0].set_title('Predicted Profit vs. Population Size')

ax[1].plot(cost_list, 'r')
ax[1].set_xlabel('Iteration')
ax[1].set_ylabel('Cost')
ax[1].set_title('Error vs Training Epoch')
plt.show()
