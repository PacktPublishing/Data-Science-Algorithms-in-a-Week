# ***Library with common routines and functions***

import random
import csv
import sys

# Increments integer values in a dictionary.


def dic_inc(dic, key):
    if key is None:
        pass
    if dic.get(key, None) is None:
        dic[key] = 1
    else:
        dic[key] = dic[key] + 1


def dic_key_count(dic, key):
    if key is None:
        return 0
    if dic.get(key, None) is None:
        return 0
    else:
        return int(dic[key])

# Returns a dictionary key with the maximal count.


def dic_key_max_count(dic):
    key_max_count = None
    for key, count in dic.items():
        if key is not None and (key_max_count
           is None or count > dic[key_max_count]):
            key_max_count = key
    return key_max_count

# returns a dictionary of 3 lists: 1st with x coordinates,
# 2nd with y coordinates, 3rd with colors with numeric values


def get_x_y_colors(data):
    dic = {}
    dic['x'] = [0] * len(data)
    dic['y'] = [0] * len(data)
    dic['colors'] = [0] * len(data)
    for i in range(0, len(data)):
        dic['x'][i] = data[i][0]
        dic['y'][i] = data[i][1]
        dic['colors'][i] = data[i][2]
    return dic

# Fills the unclassified 2d data with a class name group.


def fill_2d_data(data, x_from, x_to, y_from, y_to, group):
    for y in range(y_from, y_to + 1):
        for x in range(x_from, x_to + 1):
            if data.get((x, y), None) is None:
                data[x, y] = group

# file name should be with the suffix pgm
# img should be in a dictionary format where keys are the coordinates
# of a pixel and the value is the grayscale value
# max_color is the maximum possible color in the grayscale


def save_pgm_img(file_name, img, width, height, max_color):
    f = open(file_name, 'w')
    f.write('P2\n')
    f.write(str(width) + ' ' + str(height) + '\n')
    f.write(str(max_color) + '\n')
    for y in range(0, height):
        for x in range(0, width):
            f.write(str(img.get((x, y), max_color)) + " ")
        f.write('\n')


def load_pgm_img(file_name):
    f = open(file_name, 'r')
    # read header
    header = f.readline()
    if header != 'P2\n':
        raise ValueError(file_name + ' is not a PGM image.')
    dims = (f.readline()).split()
    width = int(dims[0])
    height = int(dims[1])
    max_color = int(f.readline())

    # read the picture
    pixels = (f.read()).split()
    img = {}
    for y in range(0, height):
        for x in range(0, width):
            img[x, y] = pixels[x + y * width]
    return (img, width, height, max_color)


def load_3row_data_to_dic(input_file):
    f = open(input_file, 'r')
    dic = {}
    entries = (f.read()).splitlines()
    for i in range(0, len(entries)):
        values = entries[i].split(' ')
        dic[int(values[0]), int(values[1])] = values[2]
    return dic


def save_3row_data_from_dic(output_file, data):
    f = open(output_file, 'w')
    for key, value in data.items():
        f.write(str(key[0]) + ' ' + str(key[1]) + ' ' + value + '\n')


def load_3row_data_to_list(input_file):
    f = open(input_file, 'r')
    list = []
    entries = (f.read()).splitlines()
    for i in range(0, len(entries)):
        list.append(entries[i].split(' '))
    return list


def csv_file_to_list(csv_file_name):
    with open(csv_file_name, 'rb') as f:
        reader = csv.reader(f)
        data = list(reader)
    return data

# Reads the csv file into the table and then separates the table into
# heading, complete data, incomplete data and then produces also the
# index number for the column that is not complete, i.e. contains a
# question mark.


def csv_file_to_ordered_data(csv_file_name):
    data = csv_file_to_list(csv_file_name)
    return order_csv_data(data)


def is_complete(data_item, pos):
    return data_item[pos] != '?'


def order_csv_data(csv_data):
    # The first row in the CSV file is the heading of the data table.
    heading = csv_data.pop(0)
    complete_data = []
    incomplete_data = []
    # Let enquired_column be the column of the variable which
    # conditional probability should be calculated. Here set that
    # column to be the last one.
    enquired_column = len(heading) - 1
    # Divide the data into the complete and the incomplete data.
    # An incomplete row is the one that has a question mark in the
    # enquired_column. The question mark will be replaced by the
    # calculated Baysian probabilities from the complete data.
    for data_item in csv_data:
        if is_complete(data_item, enquired_column):
            complete_data.append(data_item)
        else:
            incomplete_data.append(data_item)
    return (heading, complete_data, incomplete_data, enquired_column)

# Output utilities


def printf(format, *args):
    sys.stdout.write(format % args)

# Print statement with a verbose parameter.
# The higher the parameter verbose_mode_accepted,
# the more output will be produced.


def printfv(verbose_mode_accepted, verbose_mode_actual, format, *args):
    if verbose_mode_accepted <= verbose_mode_actual:
        printf(format, *args)
