import numpy as np
from matplotlib import pyplot as plt

def class_color(classes):
  colors = ["b", "g", "r", "y", "k", "w", "c", "m"]
  return np.array([colors[c] for c in classes])
  
def plot_data(X, y):
  plt.scatter(X[:,0], X[:,1], c=class_color(y))
