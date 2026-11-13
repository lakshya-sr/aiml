

import numpy as np
import matplotlib.pyplot as plt

from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# Load dataset
data = load_diabetes()
X = data.data
y = data.target

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

models = {
    "Simple Linear Regression": LinearRegression(),
    "Multiple Linear Regression": LinearRegression(),
    "Polynomial Regression": make_pipeline(
        PolynomialFeatures(degree=2, include_bias=False),
        StandardScaler(),
        LinearRegression()
    )
}

predictions = {}
results = {}

for name, model in models.items():

    # Simple regression uses only BMI
    if name == "Simple Linear Regression":
        train = X_train[:, 2:3]
        test = X_test[:, 2:3]
    else:
        train = X_train
        test = X_test

    # Train model
    model.fit(train, y_train)

    # Predict
    y_pred = model.predict(test)
    predictions[name] = y_pred

    # Evaluate
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    results[name] = [mae, mse, rmse, r2]

# Print results
print(f"{'Model':<30} {'MAE':>8} {'MSE':>10} "
      f"{'RMSE':>8} {'R2':>8}")
print("-" * 70)

for name, metrics in results.items():
    print(f"{name:<30} "
          f"{metrics[0]:>8.2f} "
          f"{metrics[1]:>10.2f} "
          f"{metrics[2]:>8.2f} "
          f"{metrics[3]:>8.4f}")

# Actual vs Predicted plots
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

for ax, (name, y_pred) in zip(axes, predictions.items()):
    ax.scatter(y_test, y_pred, alpha=0.6)

    ax.plot(
        [y_test.min(), y_test.max()],
        [y_test.min(), y_test.max()],
        "r--"
    )

    ax.set_title(name)
    ax.set_xlabel("Actual Values")
    ax.set_ylabel("Predicted Values")

plt.tight_layout()
plt.show()

# RMSE comparison
names = list(results.keys())
rmse_values = [results[name][2] for name in names]

plt.figure(figsize=(9, 5))
plt.bar(names, rmse_values)
plt.ylabel("RMSE")
plt.title("Regression Model Performance Comparison")
plt.xticks(rotation=15)
plt.tight_layout()
plt.show()
