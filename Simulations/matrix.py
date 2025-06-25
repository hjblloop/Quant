import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from numpy import random

matrix = np.random.rand(10,10)

plt.imshow(matrix, cmap='viridis', interpolation='nearest')
plt.colorbar(label='Value')
plt.title('matrix')
plt.show()

data = {
    "normal": random.normal(loc=50, scale=7, size=1000),
    "possion1": random.poisson(lam=50, size=1000),
    "possion2": random.poisson(lam=50, size=1000),
    "possion3": random.poisson(lam=50, size=1000),
    "possion4": random.poisson(lam=50, size=1000),
}

sns.displot(data, kind="kde")

plt.show()