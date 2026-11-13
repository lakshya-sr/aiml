Name: Lakshya Shrivastav


# 1. Simple Linear Regression Implementation

## Code

```python


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
```


## Output

```

Simple Linear Regression Results
--------------------------------
Slope     : 998.5777
Intercept : 152.0034
MAE       : 52.2600
MSE       : 4061.8259
RMSE      : 63.7325
R2 Score  : 0.2334
```

# 2. Simple, Multiple, Polynomial Regression Using Scikit Learn

## Code

```python



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
```


## Output

```

Model                               MAE        MSE     RMSE       R2
----------------------------------------------------------------------
Simple Linear Regression          52.26    4061.83    63.73   0.2334
Multiple Linear Regression        42.79    2900.19    53.85   0.4526
Polynomial Regression             43.59    3102.75    55.70   0.4144
```


# 3. Gradient Descent

## Code

```python



import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Load dataset (BMI feature)
data = load_diabetes()
X = data.data[:, 2]
y = data.target

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Standardize using training statistics
mean, std = X_train.mean(), X_train.std()
X_train = (X_train - mean) / std
X_test = (X_test - mean) / std


# Gradient Descent implementation
def gradient_descent(X, y, lr=0.01, epochs=1000):
    m = 0.0
    b = 0.0
    n = len(X)
    losses = []

    for _ in range(epochs):
        y_pred = m * X + b
        error = y_pred - y

        # Gradients of MSE
        dm = (2 / n) * np.sum(error * X)
        db = (2 / n) * np.sum(error)

        # Update parameters
        m -= lr * dm
        b -= lr * db

        # Record loss
        loss = np.mean((m * X + b - y) ** 2)
        losses.append(loss)

    return m, b, losses


# Compare learning rates
learning_rates = [0.001, 0.01, 0.1]
results = {}

print(f"{'Learning Rate':<16} {'MSE':>12} {'R2':>10}")
print("-" * 40)

for lr in learning_rates:
    m, b, losses = gradient_descent(
        X_train, y_train, lr=lr, epochs=1000
    )

    y_pred = m * X_test + b

    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    results[lr] = (m, b, losses, mse, r2)

    print(f"{lr:<16} {mse:>12.2f} {r2:>10.4f}")


# Plot convergence for different learning rates
plt.figure(figsize=(8, 5))

for lr, (_, _, losses, _, _) in results.items():
    plt.plot(losses, label=f"lr = {lr}")

plt.xlabel("Epochs")
plt.ylabel("Mean Squared Error (Training)")
plt.title("Gradient Descent Convergence")
plt.legend()
plt.grid(True)
plt.show()


# Plot regression line for best model
best_lr = min(results, key=lambda lr: results[lr][3])
m, b, _, mse, r2 = results[best_lr]

x_line = np.linspace(X_test.min(), X_test.max(), 100)
y_line = m * x_line + b

plt.figure(figsize=(8, 5))
plt.scatter(X_test, y_test, alpha=0.6, label="Actual Data")
plt.plot(x_line, y_line, color="red", label="Regression Line")

plt.xlabel("Standardized BMI")
plt.ylabel("Disease Progression")
plt.title(f"Linear Regression (Learning Rate = {best_lr})")
plt.legend()
plt.grid(True)
plt.show()

print(f"\nBest Learning Rate: {best_lr}")
print(f"Slope: {m:.4f}")
print(f"Intercept: {b:.4f}")
print(f"Test MSE: {mse:.2f}")
print(f"Test R2: {r2:.4f}")
```


## Output

```

 
Learning Rate             MSE         R2
----------------------------------------
0.001                 4366.16     0.1759
0.01                  4061.83     0.2334
0.1                   4061.83     0.2334

Best Learning Rate: 0.01
Slope: 47.1411
Intercept: 153.7365
Test MSE: 4061.83
Test R2: 0.2334
```


