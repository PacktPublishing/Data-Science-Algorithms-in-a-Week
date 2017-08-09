men = data.frame(
    height = c(180,174,184,168,178),
    weight = c(75,71,83,63,70)
)
model = lm(weight ~ height, data = men)
print(model)
