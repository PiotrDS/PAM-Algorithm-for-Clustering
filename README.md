# :bar_chart: PAM Algorithm for Clustering :bar_chart:
The goal of this project was to implement an algorithm based on the PAM (Partitioning Around Medoids) algorithm (L. Kaufman, P.J. Rousseeuw; 1987), which is used for the k-medoids clustering method. K-medoids is a clustering algorithm similar to k-means, but instead of using the mean of the data points as the cluster center, it selects actual data points as the cluster centers, called medoids. This approach makes k-medoids more interpretable and robust to noise and outliers. Additionally, it can work with any dissimilarity measure, unlike k-means, which typically relies on Euclidean distance. The algorithm divides a dataset into k clusters (with the number of clusters specified beforehand) and minimizes the sum of dissimilarities within each cluster. K-medoids is often preferred when the data contains outliers or when non-Euclidean distance metrics are required.

Brief Description of the PAM Algorithm

1. (BUILD phase) Initialize: greedily select k of the n data points as the medoids to minimize the cost.

2. Associate each data point with the closest medoid.

3. (SWAP phase) While the cost of the configuration decreases:

4. For each medoid m, and for each non-medoid data point o:

5. Consider swapping m and o, and compute the change in cost.

6. If the cost change is the current best, remember this m and o combination.

7. Perform the best swap of $m_{best}$ and $o_{best}$, if it decreases the cost function. Otherwise, the algorithm terminates.
