import math
import random
import sys
sys.path.append('../common')
import common  # noqa
import decision_tree  # noqa
from common import printfv  # noqa


def sample_with_replacement(population, size):
    sample = []
    for i in range(0, size):
        sample.append(population[random.randint(0, len(population) - 1)])
    return sample


def construct_random_forest(verbose, heading, complete_data,
                            enquired_column, m, tree_count):
    printfv(2, verbose, "*** Random Forest construction ***\n")
    printfv(2, verbose, "We construct a random forest that will " +
            "consist of %d random decision trees.\n", tree_count)
    random_forest = []
    for i in range(0, tree_count):
        printfv(2, verbose, "\nConstruction of a random " +
                "decision tree number %d:\n", i)
        random_forest.append(construct_random_decision_tree(
            verbose, heading, complete_data, enquired_column, m))
    printfv(2, verbose, "\nTherefore we have completed the " +
            "construction of the random forest consisting of %d " +
            "random decision trees.\n", tree_count)
    return random_forest


def construct_random_decision_tree(verbose, heading, complete_data,
                                   enquired_column, m):
    sample = sample_with_replacement(complete_data, len(complete_data))
    printfv(2, verbose, "We are given %d features as the input data. " +
            "Out of these, we choose randomly %d features with the " +
            "replacement that we will use for the construction of " +
            "this particular random decision tree:\n" +
            str(sample) + "\n", len(complete_data),
            len(complete_data))
    return decision_tree.construct_general_tree(verbose, heading,
                                                sample,
                                                enquired_column, m)


def display_forest(verbose, forest):
    if verbose > 0:
        print "\n***Random forest graph***"
        for i in range(0, len(forest)):
            print "\nTree " + str(i) + ":"
            decision_tree.display_tree(forest[i])

# M is the given number of the decision variables, i.e. properties
# of one feature.


def choose_m(verbose, M):
    m = int(min(M, math.ceil(2 * math.sqrt(M))))
    printfv(2, verbose, "We are given M=" + str(M) +
            " variables according to which a feature can be " +
            "classified. ")
    printfv(3, verbose, "In random forest algorithm we usually do " +
            "not use all " + str(M) + " variables to form tree " +
            "branches at each node. ")
    printfv(3, verbose, "We use only m variables out of M. ")
    printfv(3, verbose, "So we choose m such that m is less than or " +
            "equal to M. ")
    printfv(3, verbose, "The greater m is, a stronger classifier an " +
            "individual tree constructed is. However, it is more " +
            "susceptible to a bias as more of the data is considered. " +
            "Since we in the end use multiple trees, even if each may " +
            "be a weak classifier, their combined classification " +
            "accuracy is strong. Therefore as we want to reduce a " +
            "bias in a random forest, we may want to consider to " +
            "choose a parameter m to be slightly less than M.\n")
    printfv(2, verbose, "Thus we choose the maximum number of the " +
            "variables considered at the node to be " +
            "m=min(M,math.ceil(2*math.sqrt(M)))" +
            "=min(M,math.ceil(2*math.sqrt(%d)))=%d.\n", M, m)
    return m


def display_classification(verbose, random_forest, heading,
                           enquired_column, incomplete_data):
    printfv(0, verbose, "\n***Classification***\n")
    printfv(3, verbose, "Since for the construction of a random " +
            "decision tree we use only a subset of the original data," +
            " we may not have enough features to form a full tree " +
            "that is able to classify every feature. In such a case" +
            " a tree will not return any class for a particular " +
            "feature that should be classified. Thus we will only " +
            "consider trees that actually classify a feature to " +
            "some specific class.")
    if len(incomplete_data) == 0:
        printfv(0, verbose, "No data to classify.\n")
    else:
        for incomplete_feature in incomplete_data:
            printfv(0, verbose, "\nFeature: " +
                    str(incomplete_feature) + "\n")
            display_classification_for_feature(
                verbose, random_forest, heading,
                enquired_column, incomplete_feature)


def display_classification_for_feature(verbose, random_forest, heading,
                                       enquired_column, feature):
    classification = {}
    for i in range(0, len(random_forest)):
        group = decision_tree.classify_by_tree(
            random_forest[i], heading, enquired_column, feature)
        common.dic_inc(classification, group)
        printfv(0, verbose, "Tree " + str(i) +
                " votes for the class: " + str(group) + "\n")
    printfv(0, verbose, "The class with the maximum number of votes " +
            "is '" + str(common.dic_key_max_count(classification)) +
            "'. Thus the constructed random forest classifies the " +
            "feature " + str(feature) + " into the class '" +
            str(common.dic_key_max_count(classification)) + "'.\n")

# Program start
if len(sys.argv) < 4:
    sys.exit('Please, input as arguments:\n' +
             '1. the name of the input CSV file,\n' +
             '2. the number of the trees in the random forest to be ' +
             'constructed,\n' +
             '3. output verbosity level:\n' +
             '\t0 for the least output - result of the classification,\n' +
             '\t1 includes in addition the output of the trees constructed ' +
             'and the result of the classification,\n' +
             '\t2 includes in addition brief explanations of the tree ' +
             'construction and classification,\n' +
             '\t3 includes detailed explanations of the algorithm.\n')

csv_file_name = sys.argv[1]
tree_count = int(sys.argv[2])
verbose = int(sys.argv[3])

(heading, complete_data, incomplete_data,
 enquired_column) = common.csv_file_to_ordered_data(csv_file_name)
m = choose_m(verbose, len(heading))
printfv(2, verbose, "We are given the following features:\n" +
        str(complete_data) + "\n When constructing a random " +
        "decision tree as a part of a random forest, we will choose " +
        "only a subset out of them in a random way with the " +
        "replacement.\n\n")

random_forest = construct_random_forest(
    verbose, heading, complete_data, enquired_column, m, tree_count)
display_forest(verbose, random_forest)
printfv(2, verbose, "\n")
printfv(0, verbose, "Total number of trees in the random forest=%d.\n",
        len(random_forest))
printfv(0, verbose, "The maximum number of the variables considered " +
        "at the node is m=%d.\n", m)
display_classification(verbose, random_forest, heading,
                       enquired_column, incomplete_data)
