#Predicting profit based on the year
business_profits = data.frame(
    year = c(2011,2012,2013,2014,2015,2016,2017),
    profit = c(40,43,45,50,54,57,59)
)
model = lm(profit ~ year, data = business_profits)
print(model)
