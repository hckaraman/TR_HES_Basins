import random
import matplotlib.pyplot as plt
import numpy as np

random.seed(1)
n = 10
x = np.random.randint(10, size=10)
y = np.random.randint(10, size=10)

xy = np.array(np.random.random((5, 2)))
plt.scatter(xy[:, 0], xy[:, 1])

i, j = np.where(np.isclose(xy, xy[:, 0].min()))

leftMost = xy[i][0]
index = 2

ll = [x.min(), y.min()]
plt.scatter(leftMost[0], leftMost[1], color='red')

currentVertex = leftMost
plt.scatter(currentVertex[0], currentVertex[1], color='green')
# plt.show()

n = len(xy[:, 0])

nextVertex = xy[0]

plt.plot([currentVertex[0], nextVertex[0]], [currentVertex[1], nextVertex[1]],color = 'red')
checking = xy[index]
plt.plot([currentVertex[0], checking[0]], [currentVertex[1], checking[1]],color ='green')
plt.show()

vector_a = [nextVertex[0], currentVertex[0]], [nextVertex[1], currentVertex[1]]
vector_a = np.asarray(vector_a)
vector_b = [checking[0], currentVertex[0]], [checking[1], currentVertex[1]]
vector_b = np.asarray(vector_b)
cross = np.cross(vector_a, vector_b)
print(cross)
