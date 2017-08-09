temperatures = data.frame(
    fahrenheit = c(5,14,23,32,41,50),
    celsius = c(-15,-10,-5,0,5,10)
)
model = lm(celsius ~ fahrenheit, data = temperatures)
print(model)
