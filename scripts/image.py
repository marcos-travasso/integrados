import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('output_f2.csv')

image = data.reshape(60, 60).T

plt.imshow(image, cmap='gray', interpolation='nearest')
plt.colorbar()
plt.title("60x60 Image Plot")
plt.show()
