

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
