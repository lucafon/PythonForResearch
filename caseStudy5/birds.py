import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

birddata = pd.read_csv('bird_tracking.csv')
print(birddata.head(), birddata.info())


plt.figure(figsize=(7,7))
bird_names = pd.unique(birddata.bird_name)
for bird_name in bird_names:
	ix = birddata.bird_name == bird_name
	x, y = birddata.longitude[ix], birddata.latitude[ix]
	plt.plot(x,y, '.', label = bird_name)
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.legend(loc='lower right')
plt.show()