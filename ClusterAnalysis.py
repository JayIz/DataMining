import random
from sklearn import datasets
import pandas as pd
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# 正规化数据集 X
def normalize(X, axis=-1, p=2):
    lp_norm = np.atleast_1d(np.linalg.norm(X, p, axis))
    lp_norm[lp_norm == 0] = 1
    return X / np.expand_dims(lp_norm, axis)


# 计算一个样本与数据集中所有样本的欧氏距离的平方
def euclidean_distance(one_sample, X):
    one_sample = one_sample.reshape(1, -1)
    X = X.reshape(X.shape[0], -1)
    distances = np.power(np.tile(one_sample, (X.shape[0], 1)) - X, 2).sum(axis=1)
    return distances


class Kmeans():

    def __init__(self, k=3, max_iterations=500, varepsilon=0.0001):
        self.k = k
        self.max_iterations = max_iterations
        self.varepsilon = varepsilon

    # 从所有样本中随机选取self.k样本作为初始的聚类中心
    def init_random_centroids(self, X):
        n_samples, n_features = np.shape(X)
        centroids = np.zeros((self.k, n_features))
        for i in range(self.k):
            centroid = X[np.random.choice(range(n_samples))]
            centroids[i] = centroid
        return centroids

    # 返回距离该样本最近的一个中心索引[0, self.k)
    def _closest_centroid(self, sample, centroids):
        distances = euclidean_distance(sample, centroids)
        closest_i = np.argmin(distances)
        return closest_i

    # 将所有样本进行归类，归类规则就是将该样本归类到与其最近的中心
    def create_clusters(self, centroids, X):
        n_samples = np.shape(X)[0]
        clusters = [[] for _ in range(self.k)]
        for sample_i, sample in enumerate(X):
            centroid_i = self._closest_centroid(sample, centroids)
            clusters[centroid_i].append(sample_i)
        return clusters

    # 对中心进行更新
    def update_centroids(self, clusters, X):
        n_features = np.shape(X)[1]
        centroids = np.zeros((self.k, n_features))
        for i, cluster in enumerate(clusters):
            centroid = np.mean(X[cluster], axis=0)
            centroids[i] = centroid
        return centroids
        print (centroids)

    # 将所有样本进行归类，其所在的类别的索引就是其类别标签
    def get_cluster_labels(self, clusters, X):
        y_pred = np.zeros(np.shape(X)[0])
        for cluster_i, cluster in enumerate(clusters):
            for sample_i in cluster:
                y_pred[sample_i] = cluster_i
        return y_pred

    # 对整个数据集X进行Kmeans聚类，返回其聚类的标签
    def predict(self, X):
        # 从所有样本中随机选取self.k样本作为初始的聚类中心
        centroids = self.init_random_centroids(X)

        # 迭代，直到算法收敛(上一次的聚类中心和这一次的聚类中心几乎重合)或者达到最大迭代次数
        for _ in range(self.max_iterations):
            # 将所有进行归类，归类规则就是将该样本归类到与其最近的中心
            clusters = self.create_clusters(centroids, X)
            former_centroids = centroids

            # 计算新的聚类中心
            centroids = self.update_centroids(clusters, X)

            # 如果聚类中心几乎没有变化，说明算法已经收敛，退出迭代
            diff = centroids - former_centroids
            if diff.any() < self.varepsilon:
                break
        print (centroids)
        return self.get_cluster_labels(clusters, X)


def main():
    # Load the dataset

    # 读取用于聚类的数据，并创建数据表
    loan_data = pd.DataFrame(pd.read_csv('ClusterAnalysis.csv', header=0))


    # 查看表中的各列的名称
    print (loan_data.columns)

    # 设置要聚类的字段
    X = np.array(loan_data[['x','y','z']])

    # 用Kmeans算法进行聚类
    clf = Kmeans(k=3)
    #k为聚类数
    y_pred = clf.predict(X)
    print (y_pred)

    #对聚类完成后的标签进行计数
    s = 0
    for i in y_pred:
        if i==0:
            s+=1
        else:
            s0 = s
    print (s0)
    a = 0
    for i in y_pred:
        if i == 1:
            a += 1
        else:
            s1 = a
    print (s1)
    b=0
    for i in y_pred:
        if i == 2:
            b += 1
        else:
            s2 = b
    print (s2)


    # new a figure and set it into 3d
    ax1 = plt.subplot(111, projection='3d')  # 创建一个三维的绘图工程

    # draw the figure, the color is r = read
    figure1 = ax1.scatter(X[y_pred == 0][:, 0], X[y_pred == 0][:, 1], X[y_pred == 0][:, 2], c='r')
    figure2 = ax1.scatter(X[y_pred == 1][:, 0], X[y_pred == 1][:, 1], X[y_pred == 1][:, 2],c='g')
    figure3 = ax1.scatter(X[y_pred == 2][:, 0], X[y_pred == 2][:, 1], X[y_pred == 2][:, 2], c='b')

    ax1.set_zlabel('x')  # 坐标轴
    ax1.set_ylabel('y')
    ax1.set_xlabel('z')
    plt.show()

if __name__ == "__main__":
    main()
