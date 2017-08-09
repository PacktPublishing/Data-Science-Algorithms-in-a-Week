# write to the file with the name "test.txt"
file = open("test.txt", "w")
file.write("first line\n")
file.write("second line")
file.close()

# read the file
file = open("test.txt", "r")
print file.read()
