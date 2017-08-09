bills = data.frame(
    month = c(1,2,3,4,5),
    bill = c(120.0,131.2,142.1,152.9,164.3)
)
model = lm(bill ~ month, data = bills)
print(model)
