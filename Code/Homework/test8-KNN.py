from numpy import *

dataSet = array([[1.0, 0.9], [1.0, 1.0], [0.1, 0.2], [0.0, 0.1]])
labels = ['A','A','B','B']
print(dataSet)
print(labels)

numSamples = dataSet.shape[0]
new_t = array([0.2,0.7])

diff = tile(new_t,(numSamples,1))-dataSet
squreDiff = diff**2
squreDist = sum(squreDiff, axis=1)
distance = squreDist ** 0.5
print(distance)

sortedDistIndices = argsort(distance)

print(sortedDistIndices)
classCount = {}
K = 4
for i in range(K):
    voteLabel = labels[sortedDistIndices[i]]
    print(voteLabel)
    classCount[voteLabel] = classCount.get(voteLabel, 0) + 1
print(classCount)

maxCount = 0
for k, v in classCount.items():
    if v > maxCount:
        maxCount = v
        maxIndex = k

print("Your input is:", new_t, "and classified to class: ", maxIndex)
