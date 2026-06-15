import joblib

model = joblib.load("models/best_model.pkl")

print(type(model))
print(model)