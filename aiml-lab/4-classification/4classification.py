

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    log_loss,
    ConfusionMatrixDisplay
)

# Load dataset
data = load_breast_cancer()
X, y = data.data, data.target

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Classification models
models = {
    "SVM": make_pipeline(
        StandardScaler(), SVC(probability=True, random_state=42)
    ),
    "Decision Tree": DecisionTreeClassifier(
        max_depth=5, random_state=42
    ),
    "KNN": make_pipeline(
        StandardScaler(), KNeighborsClassifier(n_neighbors=5)
    ),
    "Naive Bayes": GaussianNB()
}

results = []
predictions = {}

# Train and evaluate
for name, model in models.items():
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)

    predictions[name] = y_pred

    results.append({
        "Model": name,
        "Accuracy": accuracy_score(y_test, y_pred),
        "Precision": precision_score(y_test, y_pred, average="weighted"),
        "Recall": recall_score(y_test, y_pred, average="weighted"),
        "F1 Score": f1_score(y_test, y_pred, average="weighted"),
        "Log Loss": log_loss(y_test, y_prob, labels=model.classes_)
    })

# Display results
df = pd.DataFrame(results)
print("\nClassification Performance Comparison")
print(df.round(4).to_string(index=False))

# Bar chart comparison
metrics = ["Accuracy", "Precision", "Recall", "F1 Score"]

df.set_index("Model")[metrics].plot(
    kind="bar", figsize=(10, 5), ylim=(0, 1)
)

plt.title("Classification Model Comparison")
plt.ylabel("Score")
plt.xticks(rotation=0)
plt.legend(loc="lower right")
plt.tight_layout()
plt.show()

# Log loss comparison
plt.figure(figsize=(8, 4))
plt.bar(df["Model"], df["Log Loss"])
plt.title("Log Loss Comparison")
plt.ylabel("Log Loss (Lower is Better)")
plt.tight_layout()
plt.show()

# Confusion matrices
fig, axes = plt.subplots(2, 2, figsize=(10, 8))

for ax, (name, y_pred) in zip(axes.flat, predictions.items()):
    ConfusionMatrixDisplay.from_predictions(
        y_test, y_pred,
        display_labels=data.target_names,
        ax=ax,
        colorbar=False
    )
    ax.set_title(name)

plt.tight_layout()
plt.show()

# Best model by F1 score
best = df.loc[df["F1 Score"].idxmax()]
print(f"\nBest Model (F1 Score): {best['Model']}")
print(f"F1 Score: {best['F1 Score']:.4f}")
