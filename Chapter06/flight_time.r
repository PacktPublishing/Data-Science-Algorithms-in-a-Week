flights = data.frame(
    distance = c(365,1462,1285,1096,517,1686,932,1160),
    time = c(1.167,2.333,2.250,2.083,2.250,2.833,1.917,2.167)
)
model = lm(time ~ distance, data = flights)
print(model)
