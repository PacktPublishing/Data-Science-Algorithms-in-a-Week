import math

point_a = (1.2, 2.5)
point_b = (5.7, 4.8)
# math.sqrt computes the square root of a float number.
# math.pow computes the power of a float number.
segment_length = math.sqrt(
    math.pow(point_a[0] - point_b[0], 2) +
    math.pow(point_a[1] - point_b[1], 2))
print "Let the point A have the coordinates", point_a, "cm."
print "Let the point B have the coordinates", point_b, "cm."
print "Then the length of the line segment AB is", segment_length, "cm."
