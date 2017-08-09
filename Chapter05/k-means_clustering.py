import math
import imp
import sys
import matplotlib.pyplot as plt
import matplotlib
import sys
sys.path.append('../common')
import common  # noqa
matplotlib.style.use('ggplot')


def printf(format, *args):
    sys.stdout.write(format % args)

# Returns k initial centroids for the given points.


def choose_init_centroids(points, k):
    centroids = []
    centroids.append(points[0])
    while len(centroids) < k:
        # Find the centroid that with the greatest possible distance
        # to the closest already chosen centroid.
        candidate = points[0]
        candidate_dist = min_dist(points[0], centroids)
        for point in points:
            dist = min_dist(point, centroids)
            if dist > candidate_dist:
                candidate = point
                candidate_dist = dist
        centroids.append(candidate)
    return centroids


# Returns the distance of a point from the closest point in points.
def min_dist(point, points):
    min_dist = euclidean_dist(point, points[0])
    for point2 in points:
        dist = euclidean_dist(point, point2)
        if dist < min_dist:
            min_dist = dist
    return min_dist

# Returns an Euclidean distance of two 2-dimensional points.


def euclidean_dist((x1, y1), (x2, y2)):
    return math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))

# Converts string 2d tuples into the numberical 2d points.


def data_to_points(data):
    points = []
    for (x, y) in data:
        points.append((float(x), float(y)))
    return points

# PointGroup is a tuple that contains in the first coordinate a 2d point
# and in the second coordinate a group which a point is classified to.


def choose_centroids(point_groups, k):
    centroid_xs = [0] * k
    centroid_ys = [0] * k
    group_counts = [0] * k
    for ((x, y), group) in point_groups:
        centroid_xs[group] += x
        centroid_ys[group] += y
        group_counts[group] += 1
    centroids = []
    for group in range(0, k):
        centroids.append((
            float(centroid_xs[group]) / group_counts[group],
            float(centroid_ys[group]) / group_counts[group]))
    return centroids

# Returns the number of the centroid which is closest to the point.
# This number of the centroid is the number of the group where
# the point belongs to.


def closest_group(point, centroids):
    selected_group = 0
    selected_dist = euclidean_dist(point, centroids[0])
    for i in range(1, len(centroids)):
        dist = euclidean_dist(point, centroids[i])
        if dist < selected_dist:
            selected_group = i
            selected_dist = dist
    return selected_group

# Reassigns the groups to the points according to which centroid
# a point is closest to.


def assign_groups(point_groups, centroids):
    new_point_groups = []
    for (point, group) in point_groups:
        new_point_groups.append(
            (point, closest_group(point, centroids)))
    return new_point_groups

# Returns a list of pointgroups given a list of points.


def points_to_point_groups(points):
    point_groups = []
    for point in points:
        point_groups.append((point, 0))
    return point_groups

# Clusters points into the k groups adding every stage
# of the algorithm to the history which is returned.


def cluster_with_history(points, k):
    history = []
    centroids = choose_init_centroids(points, k)
    point_groups = points_to_point_groups(points)
    while True:
        point_groups = assign_groups(point_groups, centroids)
        history.append((point_groups, centroids))
        new_centroids = choose_centroids(point_groups, k)
        done = True
        for i in range(0, len(centroids)):
            if centroids[i] != new_centroids[i]:
                done = False
                break
        if done:
            return history
        centroids = new_centroids

# Returns a tuple where the first argument is a list of the final
# pointgroups and the second argument is a list of the final centroids.


def cluster(points, k):
    history = cluster_with_history(points, k)
    return history[len(history) - 1]

# Returns a textual output of the clustering history.


def print_cluster_history(history):
    i = 0
    for (point_groups, centroids) in history:
        print "Step number " + str(i) + ":"
        print_point_groups(point_groups)
        print "centroids =", centroids
        i += 1


# Returns a color for the n-th group out of the k groups.
number_to_color_list = ['blue', 'red', 'green',
                        'magenta', 'gray', 'black',
                        'white', 'yellow', 'cyan']


def number_to_color(n, k):
    if k >= len(number_to_color_list):
        return n
    return number_to_color_list[n]

# Draws the points and centroids. If they belong to the same group,
# then it colors them with the same color. Points are drawn as filled
# circles. Centroids are drawn as filled squares.


def draw(point_groups, centroids):
    xs = []
    ys = []
    colors = []
    for ((x, y), group) in point_groups:
        xs.append(x)
        ys.append(y)
        colors.append(number_to_color(group, len(centroids)))

    centroids_xs = []
    centroids_ys = []
    centroids_colors = []
    group = 0
    for (x, y) in centroids:
        centroids_xs.append(x)
        centroids_ys.append(y)
        centroids_colors.append(number_to_color(group, len(centroids)))
        group += 1

    plt.title('Centroids and points classified according to them')
    plt.scatter(xs, ys, c=colors, s=[50] * len(point_groups))
    plt.scatter(centroids_xs, centroids_ys, c=centroids_colors,
                s=[100] * len(centroids), marker='s')
    plt.show()


def print_point_groups(points_groups):
    max_group = 0
    group_lists = {}
    point_count = 0
    for (point, group) in point_groups:
        if group > max_group:
            max_group = group
        if group_lists.get(group, None) is None:
            group_lists[group] = []
        point_count += 1
        group_lists[group].append((point_count, point))
    for group in range(0, max_group + 1):
        printf("Cluster " + str(group) + ": ")
        print group_lists[group]


# Program start
if len(sys.argv) < 3:
    sys.exit('Please, input as arguments:\n' +
             '1. the name of the CSV file with the 2d coordinates of the' +
             ' points to be clustered.\n' +
             '2. the number of the clusters to be created from the points.\n' +
             '3. the number of the step of the algorithm starting from 0 to ' +
             'be shown or "last" for displaying the last step and the number' +
             ' of the steps.')

csv_file = sys.argv[1]
k = int(sys.argv[2])
everything = False
if sys.argv[3] == "last":
    everything = True
else:
    step = int(sys.argv[3])

data = common.csv_file_to_list(csv_file)
points = data_to_points(data)
history = cluster_with_history(points, k)
if everything:
    print "The total number of steps:", len(history)
    print "The history of the algorithm:"
    (point_groups, centroids) = history[len(history) - 1]
    # Print all the history.
    print_cluster_history(history)
    # But display the situation graphically at the last step only.
    draw(point_groups, centroids)
else:
    (point_groups, centroids) = history[step]
    print "Data for the step number", step, ":"
    print point_groups, centroids
    draw(point_groups, centroids)
