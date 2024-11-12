import numpy as np
import matplotlib.pyplot as plt

def softmax(x):
    return np.exp(x) / np.sum(np.exp(x))


x = np.array([1, 1, 2])
y = softmax(x)
print(y)
