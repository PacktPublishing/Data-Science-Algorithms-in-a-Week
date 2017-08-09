# ***Decision Tree library ***
# Used to construct a decision tree and a random forest.
import math
import random
import common
from anytree import Node, RenderTree
from common import printfv

# Node for the construction of a decision tree.


class TreeNode:

    def __init__(self, var=None, val=None):
        self.children = []
        self.var = var
        self.val = val

    def add_child(self, child):
        self.children.append(child)

    def get_children(self):
        return self.children

    def get_var(self):
        return self.var

    def get_val(self):
        return self.val

    def is_root(self):
        return self.var is None and self.val is None

    def is_leaf(self):
        return len(self.children) == 0

    def name(self):
        if self.is_root():
            return "[root]"
        return "[" + self.var + "=" + self.val + "]"

# Classifies the feature to the class decided by the decision tree.


def classify_by_tree(tree, heading, enquired_column, feature):
    var_to_index = {}
    for index in range(0, len(heading)):
        var_to_index[heading[index]] = index
    return classify_by_tree_main(tree, var_to_index, feature)


def classify_by_tree_main(tree, var_to_index, feature):
    if tree.is_leaf():
        return tree.get_val()
    else:
        for child in tree.get_children():
            if child.is_leaf():
                return child.get_val()
            if child.get_val() == feature[
               var_to_index.get(child.get_var())]:
                return classify_by_tree_main(
                       child, var_to_index, feature)
        return None

# Constructs a decision tree where heading is the heading of the table
# with the data, i.e. the names of the attributes.
# complete_data are data samples with a known value for every attribute.
# enquired_column is the index of the column (starting from zero) which
# holds the classifying attribute.


def constuct_decision_tree(verbose, heading, complete_data, enquired_column):
    return construct_general_tree(verbose, heading, complete_data,
                                  enquired_column, len(heading))

# m is the number of the classifying variables that should be at most
# considered at each node. m needed only for a random forest.


def construct_general_tree(verbose, heading, complete_data,
                           enquired_column, m):
    available_columns = []
    for col in range(0, len(heading)):
        if col != enquired_column:
            available_columns.append(col)
    tree = TreeNode()
    printfv(2, verbose, "We start the construction with the root node" +
                        " to create the first node of the tree.\n")
    add_children_to_node(verbose, tree, heading, complete_data,
                         available_columns, enquired_column, m)
    return tree

# Splits the data samples into the groups with each having a different
# value for the attribute at the column col.


def split_data_by_col(data, col):
    data_groups = {}
    for data_item in data:
        if data_groups.get(data_item[col]) is None:
            data_groups[data_item[col]] = []
        data_groups[data_item[col]].append(data_item)
    return data_groups

# Adds a leaf node to node.


def add_leaf(verbose, node, heading, complete_data, enquired_column):
    leaf_node = TreeNode(heading[enquired_column],
                         complete_data[0][enquired_column])
    printfv(2, verbose,
            "We add the leaf node " + leaf_node.name() + ".\n")
    node.add_child(leaf_node)

# Adds all the descendants to the node.


def add_children_to_node(verbose, node, heading, complete_data,
                         available_columns, enquired_column, m):
    if len(available_columns) == 0:
        printfv(2, verbose, "We do not have any available variables " +
                "on which we could split the node further, therefore " +
                "we add a leaf node to the current branch of the tree. ")
        add_leaf(verbose, node, heading, complete_data, enquired_column)
        return -1

    printfv(2, verbose, "We would like to add children to the node " +
            node.name() + ".\n")

    selected_col = select_col(
        verbose, heading, complete_data, available_columns,
        enquired_column, m)
    for i in range(0, len(available_columns)):
        if available_columns[i] == selected_col:
            available_columns.pop(i)
            break

    data_groups = split_data_by_col(complete_data, selected_col)
    if (len(data_groups.items()) == 1):
        printfv(2, verbose, "For the chosen variable " +
                heading[selected_col] +
                " all the remaining features have the same value " +
                complete_data[0][selected_col] + ". " +
                "Thus we close the branch with a leaf node. ")
        add_leaf(verbose, node, heading, complete_data, enquired_column)
        return -1

    if verbose >= 2:
        printfv(2, verbose, "Using the variable " +
                heading[selected_col] +
                " we partition the data in the current node, where" +
                " each partition of the data will be for one of the " +
                "new branches from the current node " + node.name() +
                ". " + "We have the following partitions:\n")
        for child_group, child_data in data_groups.items():
            printfv(2, verbose, "Partition for " +
                    str(heading[selected_col]) + "=" +
                    str(child_data[0][selected_col]) + ": " +
                    str(child_data) + "\n")
        printfv(
            2, verbose, "Now, given the partitions, let us form the " +
                        "branches and the child nodes.\n")
    for child_group, child_data in data_groups.items():
        child = TreeNode(heading[selected_col], child_group)
        printfv(2, verbose, "\nWe add a child node " + child.name() +
                " to the node " + node.name() + ". " +
                "This branch classifies %d feature(s): " +
                str(child_data) + "\n", len(child_data))
        add_children_to_node(verbose, child, heading, child_data, list(
            available_columns), enquired_column, m)
        node.add_child(child)
    printfv(2, verbose,
            "\nNow, we have added all the children nodes for the " +
            "node " + node.name() + ".\n")

# Selects an available column/attribute with the highest information
# gain.


def select_col(verbose, heading, complete_data, available_columns,
               enquired_column, m):
    # Consider only a subset of the available columns of size m.
    printfv(2, verbose,
            "The available variables that we have still left are " +
            str(numbers_to_strings(available_columns, heading)) + ". ")
    if len(available_columns) < m:
        printfv(
            2, verbose, "As there are fewer of them than the " +
                        "parameter m=%d, we consider all of them. ", m)
        sample_columns = available_columns
    else:
        sample_columns = random.sample(available_columns, m)
        printfv(2, verbose,
                "We choose a subset of them of size m to be " +
                str(numbers_to_strings(available_columns, heading)) +
                ".")

    selected_col = -1
    selected_col_information_gain = -1
    for col in sample_columns:
        current_information_gain = col_information_gain(
            complete_data, col, enquired_column)
        # print len(complete_data),col,current_information_gain
        if current_information_gain > selected_col_information_gain:
            selected_col = col
            selected_col_information_gain = current_information_gain
    printfv(2, verbose,
            "Out of these variables, the variable with " +
            "the highest information gain is the variable " +
            heading[selected_col] +
            ". Thus we will branch the node further on this " +
            "variable. " +
            "We also remove this variable from the list of the " +
            "available variables for the children of the current node. ")
    return selected_col

# Converts each number in a list numbers into the string in the
# list strings with that index.


def numbers_to_strings(numbers, strings):
    string_list = []
    for n in numbers:
        string_list.append(strings[n])
    return string_list

# Calculates the information gain when partitioning complete_data
# according to the attribute at the column col and classifying by the
# attribute at enquired_column.


def col_information_gain(complete_data, col, enquired_column):
    data_groups = split_data_by_col(complete_data, col)
    information_gain = entropy(complete_data, enquired_column)
    for _, data_group in data_groups.items():
        information_gain -= (float(len(data_group)) / len(complete_data)
                             ) * entropy(data_group, enquired_column)
    return information_gain

# Calculates the entropy of the data classified by the attribute
# at the enquired_column.


def entropy(data, enquired_column):
    value_counts = {}
    for data_item in data:
        if value_counts.get(data_item[enquired_column]) is None:
            value_counts[data_item[enquired_column]] = 0
        value_counts[data_item[enquired_column]] += 1
    entropy = 0
    for _, count in value_counts.items():
        probability = float(count) / len(data)
        entropy -= probability * math.log(probability, 2)
    return entropy

# A visual output of a tree using the text characters.


def display_tree(tree):
    anytree = convert_tree_to_anytree(tree)
    for pre, fill, node in RenderTree(anytree):
        pre = pre.encode(encoding='UTF-8', errors='strict')
        print("%s%s" % (pre, node.name))

# A simple textual output of a tree without the visualization.


def display_tree_simple(tree):
    print('***Tree structure***')
    display_node(tree)
    sys.stdout.flush()

# A simple textual output of a node in a tree.


def display_node(node):
    if node.is_leaf():
        print('The node ' + node.name() + ' is a leaf node.')
        return
    sys.stdout.write('The node ' + node.name() + ' has children: ')
    for child in node.get_children():
        sys.stdout.write(child.name() + ' ')
    print('')
    for child in node.get_children():
        display_node(child)

# Convert a decision tree into the anytree module tree format to make
# it ready for rendering.


def convert_tree_to_anytree(tree):
    anytree = Node("Root")
    attach_children(tree, anytree)
    return anytree

# Attach the children from the decision tree into the anytree
# tree format.


def attach_children(parent_node, parent_anytree_node):
    for child_node in parent_node.get_children():
        child_anytree_node = Node(
            child_node.name(), parent=parent_anytree_node)
        attach_children(child_node, child_anytree_node)
