# A program that reads the CSV file with the data and returns
# the Bayesian probability for the unknown value denoted by ? to
# belong to a certain class.
# An input CSV file should be of the following format:
# 1. items in a row should be separated by a comma ','
# 2. the first row should be a heading - should contain a name for each
# column of the data.
# 3. the remaining rows should contain the data itself - rows with
# complete and rows with the incomplete data.
# A row with complete data is the row that has a non-empty and
# non-question mark value for each column. A row with incomplete data is
# the row that has the last column with the value of a question mark ?.
# Please, run this file on the example chess.csv to understand this help
# better:
# $ python naive_bayes.py chess.csv

import imp
import sys
sys.path.append('../common')
import common  # noqa

# Calculates the Baysian probability for the rows of incomplete data and
# returns them completed by the Bayesian probabilities. complete_data
# are the rows with the data that is complete and are used to calculate
# the conditional probabilities to complete the incomplete data.


def bayes_probability(heading, complete_data, incomplete_data,
                      enquired_column):
    conditional_counts = {}
    enquired_column_classes = {}
    for data_item in complete_data:
        common.dic_inc(enquired_column_classes,
                       data_item[enquired_column])
        for i in range(0, len(heading)):
            if i != enquired_column:
                common.dic_inc(
                    conditional_counts, (
                        heading[i], data_item[i],
                        data_item[enquired_column]))

    completed_items = []
    for incomplete_item in incomplete_data:
        partial_probs = {}
        complete_probs = {}
        probs_sum = 0
        for enquired_group in enquired_column_classes.items():
            # For each class in the of the enquired variable A calculate
            # the probability P(A)*P(B1|A)*P(B2|A)*...*P(Bn|A) where
            # B1,...,Bn are the remaining variables.
            probability = float(common.dic_key_count(
                enquired_column_classes,
                enquired_group[0])) / len(complete_data)
            for i in range(0, len(heading)):
                if i != enquired_column:
                    probability = probability * (float(
                        common.dic_key_count(
                            conditional_counts, (
                                heading[i], incomplete_item[i],
                                enquired_group[0]))) / (
                        common.dic_key_count(enquired_column_classes,
                                             enquired_group[0])))
            partial_probs[enquired_group[0]] = probability
            probs_sum += probability

        for enquired_group in enquired_column_classes.items():
            complete_probs[enquired_group[0]
                           ] = partial_probs[enquired_group[0]
                                             ] / probs_sum
        incomplete_item[enquired_column] = complete_probs
        completed_items.append(incomplete_item)
    return completed_items

# Program start
if len(sys.argv) < 2:
    sys.exit('Please, input as an argument the name of the CSV file.')

(heading, complete_data, incomplete_data,
 enquired_column) = common.csv_file_to_ordered_data(sys.argv[1])

# Calculate the Bayesian probability for the incomplete data
# and output it.
completed_data = bayes_probability(
    heading, complete_data, incomplete_data, enquired_column)
print completed_data
