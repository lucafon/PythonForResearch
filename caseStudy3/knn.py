import numpy as np
import matplotlib.pyplot as plt
import random
import scipy.stats as ss
from matplotlib.colors import ListedColormap

def majority_vote(votes):
	vote_counts = {}
	for vote in votes:
		vote_counts[vote] = vote_counts.get(vote, 0) + 1
	winners = []
	max_count = max(vote_counts.values())
	for vote, count in vote_counts.items():
		if count == max_count:
			winners.append(vote)
	
	return random.choice(winners)

def distance(p1,p2):
	"""Find the distance between p1 and p2."""
	return np.sqrt(np.sum(np.power(p2 - p1, 2)))
	
def find_nearest_neighbors(p, points, k=5):
	distances = np.zeros(points.shape[0])
	for i in range(len(distances)):
		distances[i] = distance(p, points[i])
	ind = np.argsort(distances)
	return ind[:k]
	
def knn_predict(p, points, outcomes, k=5):
	ind = find_nearest_neighbors(p, points, k)
	return 	majority_vote(outcomes[ind])

def generate_synth_data(n=50):
	points = np.concatenate((ss.norm(0,1).rvs((n,2)), ss.norm(1,1).rvs((n,2))), axis = 0)
	outcomes = np.concatenate((np.repeat(0,n), np.repeat(1,n)))
	return (points, outcomes)
	
def plot_prediction_grid (xx, yy, prediction_grid, filename):
	""" Plot KNN predictions for every point on the grid."""
	background_colormap = ListedColormap (["hotpink","lightskyblue", "yellowgreen"])
	observation_colormap = ListedColormap (["red","blue","green"])
	plt.figure(figsize =(10,10))
	plt.pcolormesh(xx, yy, prediction_grid, cmap = background_colormap, alpha = 0.5)
	plt.scatter(predictors[:,0], predictors [:,1], c = outcomes, cmap = observation_colormap, s = 50)
	plt.xlabel('Variable 1'); plt.ylabel('Variable 2')
	plt.xticks(()); plt.yticks(())
	plt.xlim (np.min(xx), np.max(xx))
	plt.ylim (np.min(yy), np.max(yy))
	plt.savefig(filename)

p = np.array([1.0, 2.7])
n = 20
(points, outcomes) = generate_synth_data(n)
plt.figure()
plt.plot(points[:n,0], points[:n,1], 'ro')
plt.plot(points[n:,0], points[n:,1], 'bo')
plt.plot(p[0],p[1], 'go')
plt.show()

print(knn_predict(p, points, outcomes, k=2))