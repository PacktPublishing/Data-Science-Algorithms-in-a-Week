# ***Library implementing knn algorihtm***
import math
import sys
sys.path.append('../common')
import sort  # noqa
import common  # noqa


def euclidean_metric_2d((x1, y1), (x2, y2)):
    return math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))


def manhattan_metric_2d((x1, y1), (x2, y2)):
    return abs(x1 - x2) + abs(y1 - y2)

# Reset the counts for the neighbors and the classes(groups) of a data
# point in question.


def info_reset(info):
    info['nbhd_count'] = 0
    info['class_count'] = {}

# Find the class of a neighbor with the coordinates x,y.
# If the class is known count that neighbor.


def info_add(info, data, x, y):
    group = data.get((x, y), None)
    common.dic_inc(info['class_count'], group)
    info['nbhd_count'] += int(group is not None)

# Apply knn algorithm to the 2d data using the k-nearest neighbors with
# the Manhattan distance.
# The dictionary data comes in the form with keys being 2d coordinates
# and the values being the class.
# x,y are integer coordinates for the 2d data with the range
# [x_from,x_to] x [y_from,y_to].


def knn_to_2d_data(data, x_from, x_to, y_from, y_to, k):
    new_data = {}
    info = {}
    # Go through every point in an integer coordinate system.
    for y in range(y_from, y_to + 1):
        for x in range(x_from, x_to + 1):
            info_reset(info)
            # Count the number of neighbors for each class group for
            # every distance dist starting at 0 until at least k
            # neighbors with known classes are found.
            for dist in range(0, x_to - x_from + y_to - y_from):
                # Count all neighbors that are distanced dist from
                # the point [x,y].
                if dist == 0:
                    info_add(info, data, x, y)
                else:
                    for i in range(0, dist + 1):
                        info_add(info, data, x - i, y + dist - i)
                        info_add(info, data, x + dist - i, y - i)
                    for i in range(1, dist):
                        info_add(info, data, x + i, y + dist - i)
                        info_add(info, data, x - dist + i, y - i)
                # There could be more than k-closest neighbors if the
                # distance of more of them is the same from the point
                # [x,y]. But immediately when we have at least k of
                # them, we break from the loop.
                if info['nbhd_count'] >= k:
                    break
            class_max_count = None
            # Choose the class with the highest count of the neighbors
            # from among the k-closest neighbors.
            for group, count in info['class_count'].items():
                if group is not None and (class_max_count is None or
                   count > info['class_count'][class_max_count]):
                    class_max_count = group
            new_data[x, y] = class_max_count
    return new_data

# Distance Buffer - a buffer keeping the calculated distances in
# sorted order.


class DistBuffer:

    # metric takes two 2d points and returns a distance between them.
    def __init__(self, metric):
        self.metric = metric
        self.dist_list = [(0, 0, 0)]
        self.pos = 0
        self.max_covered_dist = 0

    def reset(self):
        self.pos = 0

    def next(self):
        if self.pos < len(self.dist_list):
            (x, y, dist) = self.dist_list[self.pos]
            if dist <= self.max_covered_dist:
                self.pos += 1
                return (x, y)
        self.__loadNext()
        return self.next()

    # Loads more items into the buffer so that more of them are avaiable
    # for the method next().
    def __loadNext(self):
        self.max_covered_dist += 1
        for x in range(-self.max_covered_dist, self.max_covered_dist + 1):
            self.__append(x, -self.max_covered_dist)
            self.__append(x, self.max_covered_dist)
        for y in range(-self.max_covered_dist + 1, self.max_covered_dist):
            self.__append(-self.max_covered_dist, y)
            self.__append(self.max_covered_dist, y)
        self.__sortList()

    def __append(self, x, y):
        self.dist_list.append((x, y, self.metric((0, 0), (x, y))))

# Assuming that the sorting algorithm does not change the order of the
# initial already sorted elements. This is so that next() does not skip
# some elements and returns a different element instead.
    def __sortList(self):
        self.dist_list.sort(key=proj_to_3rd)

    def printList(self):
        print self.dist_list


def proj_to_3rd((x, y, d)):
    return d


def less_than_on_3rd((x1, y1, d1), (x2, y2, d2)):
    return d1 < d2

# lookup_limit specifies at how many neighbors at most the algorithm
# should look at. In case it fails to find a class within that number
# of neighbors, the classification defaults to the value default.


def knn_to_2d_data_with_metric(data, x_from, x_to, y_from, y_to, k,
                               metric, lookup_limit, default):
    new_data = {}
    info = {}
    db = DistBuffer(metric)
    # Go through every point in an integer coordinate system.
    for y in range(y_from, y_to + 1):
        for x in range(x_from, x_to + 1):
            info_reset(info)
            db.reset()
            # Count the number of neighbors for each class group for
            # every distance dist starting at 0 until at least k
            # neighbors with known classes are found.
            lookup_count = 0
            while info['nbhd_count'] < k and lookup_count < lookup_limit:
                (x0, y0) = db.next()
                xn = x + x0
                yn = y + y0
                if x_from <= xn and xn <= x_to and y_from <= yn and yn <= y_to:
                    info_add(info, data, xn, yn)
                lookup_count += 1

            # Choose the class with the highest count of the neighbors
            # from among the k-closest neighbors.
            result = common.dic_key_max_count(info['class_count'])
            if result is None:
                new_data[x, y] = default
            else:
                new_data[x, y] = result
    return new_data
