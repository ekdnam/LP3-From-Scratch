import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib import style
style.use('ggplot')

x = np.array([[1, 2], [1.5, 1.8], [2, 4], [9, 8], [8, 8], [9, 8.7]])

plt.scatter(x[:, :-1], x[:, -1])
plt.show()

class KMeans:
  def __init__(self, k=2, tol=0.001, max_iter=300):
    self.k = k
    self.tol = tol
    self.max_iter = max_iter

  def fit(self, data):
    self.centroids = {}

    for i in range(self.k):
      self.centroids[i] = data[i]

    for i in range(self.max_iter):
      self.classifications = {}
      for i in range(self.k):
        self.classifications[i] = []

      for featureset in data:
        distances = [np.linalg.norm(featureset-self.centroids[centroid]) for centroid in self.centroids]
        classification = distances.index(min(distances))
        self.classifications[classification].append(featureset)

      prev_centroids = dict(self.centroids)

      for classification in self.classifications:
        self.centroids[classification] = np.average(self.classifications[classification], axis=0)

      optimized = True

      for c in self.centroids:
        original_centroid = prev_centroids[c]
        current_centroid = self.centroids[c]

        if np.sum((current_centroid-original_centroid)/original_centroid*100.0) > self.tol:
          print(np.sum((current_centroid-original_centroid)/original_centroid*100.0))
          optimized = False
        
        if optimized:
          break
      
      def predict(self, data):
        distances = [np.linalg.norm(featureset - self.centroids[centroid]) for centroid in self.centroids]
        classification = distances.index(min(distances))
        return classification

model = KMeans()
model.fit(x)

for centroid in model.centroids:
  # print(centroid)
  plt.scatter(model.centroids[centroid][0], model.centroids[centroid][1], marker='o', color='k', s=10, linewidth=5)

colors = ['blue', 'green']
i = 0

for classification in model.classifications:
  color = colors[i]
  i += 1
  for featureset in model.classifications[classification]:
    plt.scatter(featureset[0], featureset[1], color=color, s=15, linewidth=5, marker='x')
plt.plot()