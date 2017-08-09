# Constructs a decision tree from data specified in a CSV file.
# Format of a CSV file:
# Each data item is written on one line, with its variables separated
# by a comma. The last variable is used as a decision variable to
# branch a node and construct the decision tree.

import math
# anytree module is used to visualize the decision tree constructed by
# this ID3 algorithm.
from anytree import Node, RenderTree
import sys
sys.path.append('../common')
import common
from common import printfv
import decision_tree

# Program start
if len(sys.argv) < 3:
    sys.exit('Please, input as arguments:\n' +
              '1. the name of the input CSV file.\n' +
              '2. the level of verbosity: 0 or 2\n' +
              '   0 - output only the decision tree,\n' +
              '   1 - also provide some basic information on the ' +
              'construction,' +
              '   2 - in addition provide the explanations of the ' +
              'decision tree construction.\n\n' +
              'Example use:\n' +
              'python construct_decision_tree.py swim.csv 1')

csv_file_name = sys.argv[1]
verbose = int(sys.argv[2])  # verbosity level, 0 - only decision tree

# Define the equired column to be the last one.
# I.e. a column defining the decision variable.
(heading, complete_data, incomplete_data,
 enquired_column) = common.csv_file_to_ordered_data(csv_file_name)

printfv(1, verbose,
        "We construct a decision tree given the following " +
        str(len(complete_data)) + " data items: \n" +
        str(complete_data) + "\n\n")
tree = decision_tree.constuct_decision_tree(
    verbose, heading, complete_data, enquired_column)
printfv(2, verbose, "\n")
printfv(1, verbose, "***Decision tree graph***\n")
decision_tree.display_tree(tree)
