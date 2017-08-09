#Integer constants are suffixed with L.
rectangle_side_a = 10L
rectangle_side_b = 5L
rectangle_area = rectangle_side_a * rectangle_side_b
rectangle_perimeter = 2*(rectangle_side_a + rectangle_side_b)
#The command cat like print can also be used to print the output
#to the command line.
cat("Let there be a rectangle with the sides of lengths:",
    rectangle_side_a, "and", rectangle_side_b, "cm.\n")
cat("Then the area of the rectangle is", rectangle_area, "cm squared.\n")
cat("The perimeter of the rectangle is", rectangle_perimeter, "cm.\n")
