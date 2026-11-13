
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split

# Load dataset
data = load_diabetes()
X = data.data[:, 2]  # BMI feature
y = data.target

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Simple Linear Regression (Least Squares)
x_mean = np.mean(X_train)
y_mean = np.mean(y_train)

numerator = np.sum((X_train - x_mean) * (y_train - y_mean))
denominator = np.sum((X_train - x_mean) ** 2)

slope = numerator / denominator
intercept = y_mean - slope * x_mean

# Predictions
y_pred = slope * X_test + intercept

# Evaluation metrics (manual)
mae = np.mean(np.abs(y_test - y_pred))
mse = np.mean((y_test - y_pred) ** 2)
rmse = np.sqrt(mse)

ss_res = np.sum((y_test - y_pred) ** 2)
ss_tot = np.sum((y_test - np.mean(y_test)) ** 2)
r2 = 1 - ss_res / ss_tot

# Results
print("Simple Linear Regression Results")
print("--------------------------------")
print(f"Slope     : {slope:.4f}")
print(f"Intercept : {intercept:.4f}")
print(f"MAE       : {mae:.4f}")
print(f"MSE       : {mse:.4f}")
print(f"RMSE      : {rmse:.4f}")
print(f"R2 Score  : {r2:.4f}")

# Visualization
plt.scatter(X_test, y_test, color="blue", label="Actual Data")
plt.plot(
    np.sort(X_test),
    slope * np.sort(X_test) + intercept,
    color="red",
    label="Regression Line"
)

plt.xlabel("BMI (Standardized)")
plt.ylabel("Disease Progression")
plt.title("Simple Linear Regression")
plt.legend()
plt.show()
