import numpy as np
import matplotlib.pyplot as plt



img = plt.imread('хр.jpg')
fig, ax = plt.subplots()
ax.imshow(img, extent=[-5, 80, -5, 30])

plt.show()