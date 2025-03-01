# pobranie bibliotek
import numpy as np
import pandas as pd
import sys
from scipy.spatial.distance import cdist



def clusterPam(X,k, metric='euclidean', maxIteration=20):

    # exception handling.

    # 1. checking the type of variable X
    try:
        if not(isinstance(X, (np.ndarray,pd.DataFrame, pd.Series))):
            raise TypeError("Invalid variable type X") 
        if isinstance(X, (pd.DataFrame, pd.Series)):
            X = X.to_numpy()

    except TypeError as e:
        print(f'Error type: __{e}__')
        print(f'!!! X must be one of the following types: numpy.ndarray, pandas.DataFrame, pandas.Series !!!')
        sys.exit(1)

    # 2. checking the type and value of variable k
    try:
        if type(k) is not int:
            raise TypeError("Invalid variable type X")
        if k < 1: 
            raise ValueError('value of k is too small')
        if k > X.shape[0]:
            raise ValueError('value of k is too big')
    except TypeError as e:
        print(f'Error type: __{e}__')
        print(f'!!! X must be an integer !!!')
        sys.exit(1)
    except ValueError as e:
        print(f'Error type: __{e}__')
        print(f'!!! X must be an integer in the range [1, {X.shape[0]}] !!!')
        sys.exit(1)

    # 3. Checking if the data types in X are numeric:
    try:
        if X.dtype == object:
            raise TypeError('X contains categorical variables')
    except TypeError as e:
        print(f'Error type: __{e}__')
        print(f'!!! X must contains only numerical variables !!!')
        sys.exit(1)


    # 4. Checking if X contains missing data:
    try:
        numerOfMissingData = np.isnan(X).sum()
        if numerOfMissingData > 0:
            raise ValueError('missing data in X')
    except ValueError as e:
        print(f'Error type: __{e}__')
        print(f'!!! X must not contain missing data !!!')
        sys.exit(1)


    # 5. Checking if metric is valid

    try:
        if metric not in ('cityblock', 'cosine', 'euclidean', 'mahalanobis', 'minkowski'):
            raise ValueError('Invalid metric')
    except ValueError as e:
        print(f'Error type: __{e}__')
        print(f"!!! metric must be one of the following: 'cityblock', 'cosine', 'euclidean', 'mahalanobis', 'minkowski' !!!")
        sys.exit(1)        



    # Algorithm


    nSamples = X.shape[0]
    distances = computeDistances(X, metric)
    
    # BUILD phase
    medoids = initializeMedoids(X, k)

    for _ in range(maxIteration):

        # Assign points to the closest medoid
        labels, totalCost = assignPointsToMedoidsFast(distances, medoids)

        # SWAP phase
        bestCostReduction = 0
        bestSwap = None

        for medoid in medoids:
            for point in range(nSamples):
                if point not in medoids:
                    # Calculate the cost change for swapping
                    costReduction = calculateCostChangeFast(distances, medoids, labels, medoid, point)

                    if costReduction < bestCostReduction:
                        bestCostReduction = costReduction
                        bestSwap = (medoid, point)

        # Perform the best swap if it reduces the cost
        if bestSwap and bestCostReduction < 0:
            medoids.remove(bestSwap[0])
            medoids.append(bestSwap[1])
        else:
            break  # No improvement, break out

    labels, _ = assignPointsToMedoidsFast(distances, medoids)

    return medoids, pd.DataFrame(labels)

def computeDistances(data, metric):
    """Precompute pairwise distances for all points."""
    distances = cdist(XA=data, XB=data, metric=metric)
    
    return distances

def initializeMedoids(data, k):
    """Initialize k medoids randomly."""
    nSamples = data.shape[0]
    return list(np.random.choice(nSamples, k, replace=False))

def assignPointsToMedoidsFast(distances, medoids):
    """Assign each point to the closest medoid"""
    nSamples = distances.shape[0]
    labels = np.zeros(nSamples, dtype=int)
    totalCost = 0

    for i in range(nSamples):
        distancesToMedoids = [distances[i, medoid] for medoid in medoids]
        closestMedoid = np.argmin(distancesToMedoids)
        labels[i] = closestMedoid
        totalCost += distancesToMedoids[closestMedoid]

    return labels, totalCost

def calculateCostChangeFast(distances, medoids, labels, medoid, point):
    """Calculate the cost change for swapping a medoid with a point"""
    costChange = 0

    for i in range(distances.shape[0]):
        currentDistance = distances[i, medoid]
        newDistance = distances[i, point]

        if labels[i] == medoids.index(medoid):
            costChange += min(newDistance, min(distances[i, m] for m in medoids if m != medoid)) - currentDistance

    return costChange





def main():
    pass


if __name__ == '__main__':
    main()





