import numpy as np
from matplotlib import pyplot as plt

def class_color(classes):
  colors = ["b", "g", "r", "y", "k", "w", "c", "m"]
  return np.array([colors[c] for c in classes])
  
def color_scatter(X, y, alpha=0.8, s=20):
  plt.scatter(X[:,0], X[:,1], c=class_color(y), alpha=alpha, s=s)
  plt.show()
