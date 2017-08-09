# Applies the knn algorithm to the input data.
# The input text file is assumed to be of the format with one line per
# every data entry consisting of the temperature in degrees Celsius,
# wind speed and then the classification cold/warm.

import sys
sys.path.append('..')
sys.path.append('../../common')
import knn  # noqa
import common  # noqa

# Start of the program
if len(sys.argv) < 8:
    sys.exit(
        'Please, input as arguments:\n' +
        '1. the name of the data file with the 2d coordinates of the' +
        'points be applied on the knn algorithm.\n' +
        '2. the name of the output file where the classification of' +
        'the neighbours should be recorded.\n' +
        '3. the number of k-neighbors to consider in the' +
        'classification.\n' +
        '4-7. the coordinates of the rectangle in which the class of' +
        'the neighbors should be determined:\n' +
        '4. x coordinate of the bottom left point of the ' +
        'rectangle,\n' +
        '5. x coordinate of the top right point of the ' +
        'rectangle,\n' +
        '6. y coordinate of the bottom left point of the ' +
        'rectangle,\n' +
        '7. y coordinate of the top right point of the ' +
        'rectangle.\n\n' +
        'Example use:\n' +
        'python knn_to_data.py mary_and_temperature_preferences.data' +
        ' mary_and_temperature_preferences_completed.data' +
        ' 1 5 30 0 10')

# E.g. "mary_and_temperature_preferences.data"
input_file = sys.argv[1]
# E.g. "mary_and_temperature_preferences_completed.data"
output_file = sys.argv[2]

k = int(sys.argv[3])
x_from = int(sys.argv[4])
x_to = int(sys.argv[5])
y_from = int(sys.argv[6])
y_to = int(sys.argv[7])

data = common.load_3row_data_to_dic(input_file)
new_data = knn.knn_to_2d_data(data, x_from, x_to, y_from, y_to, k)
common.save_3row_data_from_dic(output_file, new_data)
