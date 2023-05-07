from functools import reduce
from math import sqrt
import math
from random import uniform
import random
import time

MAX_TIME = 60

def euclidian_distance(x1, y1, x2, y2):

    dx = x1 - x2 if x1 > x2 else x2 - x1
    dy = y1 - y2 if y1 > y2 else y2 - y1

    return sqrt((dx * dx) + (dy * dy))

def calculate_clusters(x_axis, y_axis, x_axis_centroid, y_axis_centroid, number_of_clusters):
    return list(
        map(lambda x, y:
            min(
                list(
                    map(lambda xc, yc, c:                            
                        (euclidian_distance(x, y, xc, yc), c)
                    , x_axis_centroid, y_axis_centroid, range(0, number_of_clusters))
                )
            , key = lambda v: v[0])
        , x_axis, y_axis))

def kmeans(x_axis, y_axis, x_axis_centroid, y_axis_centroid, clustered_data, number_of_clusters):

    new_x_axis_centroid = [(0, 0)] * number_of_clusters
    new_y_axis_centroid = [(0, 0)] * number_of_clusters 

    for i in range(0, len(clustered_data)):

        new_x_axis_centroid[clustered_data[i][1]] = (
            new_x_axis_centroid[clustered_data[i][1]][0] + x_axis[i],
            new_x_axis_centroid[clustered_data[i][1]][1] + 1)

        new_y_axis_centroid[clustered_data[i][1]] = (
            new_y_axis_centroid[clustered_data[i][1]][0] + y_axis[i],
            new_y_axis_centroid[clustered_data[i][1]][1] + 1)

    new_x_axis_centroid = list(
        map(
            lambda nx, x: 
                nx[0] / nx[1] if nx[1] > 0 else x
        , new_x_axis_centroid, x_axis_centroid)
    )

    new_y_axis_centroid = list(
        map(
            lambda ny, y: 
                ny[0] / ny[1] if ny[1] > 0 else y
        , new_y_axis_centroid, y_axis_centroid)
    )

    return (new_x_axis_centroid, new_y_axis_centroid)

def calculate_cost(cx, cy):
    
    cost = []

    for i in range(0, len(cx)):

        sum_distances = 0.0

        for j in range(0, len(cx)):

            sum_distances += euclidian_distance(cx[i][0], cy[i][0], cx[j][0], cy[j][0])

        c = (sum_distances, cx[i][1])

        cost.append(c)

    min_cost = min(cost, key = lambda v: v[0])

    return (min_cost)
            
def kmeoids_steps(x_axis, y_axis, clustered_data, number_of_clusters):

    clustered_x_axis = []
    clustered_y_axis = []

    for i in range(0, number_of_clusters):
        clustered_x_axis.append([])
        clustered_y_axis.append([])

    for i in range(0, len(clustered_data)):
        x = (x_axis[i], i)
        y = (y_axis[i], i)
        clustered_x_axis[clustered_data[i][1]].append(x)
        clustered_y_axis[clustered_data[i][1]].append(y)

    cost = list(map(
                lambda cx, cy:
                    calculate_cost(cx, cy)
            , clustered_x_axis, clustered_y_axis))

    x_axis_centroid = list(map(
                                lambda c:
                                    x_axis[c[1]]
                            , cost))
    
    y_axis_centroid = list(map(
                                lambda c:
                                    y_axis[c[1]]
                            , cost))
    
    x_axis_centroid_cost = list(map(
                                lambda c:
                                    c[0]
                            , cost))
    
    y_axis_centroid_cost = list(map(
                                lambda c:
                                    c[0]
                            , cost))

    return (x_axis_centroid, y_axis_centroid, x_axis_centroid_cost, y_axis_centroid_cost)

def kmedoids(x_axis, y_axis, clustered_data, number_of_clusters):    
    
    (x_axis_centroid, y_axis_centroid, x_axis_centroid_cost, y_axis_centroid_cost) = kmeoids_steps(x_axis, y_axis, clustered_data, number_of_clusters)
    test_clustered_data = calculate_clusters(x_axis, y_axis, x_axis_centroid, y_axis_centroid, number_of_clusters)
    (test_x_axis_centroid, test_y_axis_centroid, test_x_axis_centroid_cost, test_y_axis_centroid_cost) = kmeoids_steps(x_axis, y_axis, test_clustered_data, number_of_clusters)

    new_x_axis_centroid = [0] * number_of_clusters
    new_y_axis_centroid = [0] * number_of_clusters

    for i in range(0, number_of_clusters):

            if(x_axis_centroid_cost[i] < test_x_axis_centroid_cost[i]):
                new_x_axis_centroid[i] = x_axis_centroid[i]
            else:
                new_x_axis_centroid[i] = test_x_axis_centroid[i]

            if(y_axis_centroid_cost[i] < test_y_axis_centroid_cost[i]):
                new_y_axis_centroid[i] = y_axis_centroid[i]
            else:
                new_y_axis_centroid[i] = test_y_axis_centroid[i]

    return (new_x_axis_centroid, new_y_axis_centroid)
    

def calculate_error(clustered_data):

    return (reduce(
        lambda a, b:
            a + b
    , list(
        map(
            lambda x: 
                x[0] ** 2
        , clustered_data)
    ))) / len(clustered_data)

def clusterizer(x_axis, y_axis, number_of_clusters=2, method="kmeans"):

    if number_of_clusters < 2 or number_of_clusters > 10:
        return False

    min_x_axis = min(x_axis)
    max_x_axis = max(x_axis)

    min_y_axis = min(y_axis)
    max_y_axis = max(y_axis)

    if(method == "kmeans"):
        x_axis_centroid = list(map(lambda x: uniform(min_x_axis, max_x_axis), range(0, number_of_clusters)))
        y_axis_centroid = list(map(lambda x:  uniform(min_y_axis, max_y_axis), range(0, number_of_clusters)))
    else:
        x_axis_centroid = []
        y_axis_centroid = []

        rnds = []
        for i in range(0, number_of_clusters):
            rnd = random.randint(0, len(x_axis) - 1)

            while(rnds.count(rnd) > 0):
                rnd = random.randint(0, len(x_axis) - 1)

            rnds.append(rnd)
            x_axis_centroid.append(x_axis[rnd])
            y_axis_centroid.append(y_axis[rnd])

    new_x_axis_centroid = range(0, number_of_clusters)
    new_y_axis_centroid = range(0, number_of_clusters)

    x_centroids = x_axis_centroid
    y_centroids = y_axis_centroid

    start_time = time.time()

    while(True):

        clustered_data = calculate_clusters(x_axis, y_axis, x_axis_centroid, y_axis_centroid, number_of_clusters)

        if(method == "kmeans"):            
            (new_x_axis_centroid, new_y_axis_centroid) = kmeans(x_axis, y_axis, x_axis_centroid, y_axis_centroid, clustered_data, number_of_clusters)
        else: 
            (new_x_axis_centroid, new_y_axis_centroid) = kmedoids(x_axis, y_axis, clustered_data, number_of_clusters)

        if((x_axis_centroid == new_x_axis_centroid and y_axis_centroid == new_y_axis_centroid) or time.time() - start_time > MAX_TIME):
            break

        x_axis_centroid = new_x_axis_centroid
        y_axis_centroid = new_y_axis_centroid

        x_centroids.extend(new_x_axis_centroid)
        y_centroids.extend(new_y_axis_centroid)

    error = calculate_error(clustered_data)

    region = list(
        map(
            lambda c: 
                c[1]
        , clustered_data)    
    )

    return (x_axis_centroid, y_axis_centroid, error, region)
    #return (x_centroids, y_centroids, error, region)