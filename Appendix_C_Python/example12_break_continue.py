for i in range(0, 10):
    if i % 2 == 1:  # remainder from the division by 2
        continue
    print 'The number', i, 'is divisible by 2.'

for j in range(20, 100):
    print j
    if j > 22:
        break
