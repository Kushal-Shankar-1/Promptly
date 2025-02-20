import os
import pandas as pd
from fairlearn.reductions import EqualizedOdds, ExponentiatedGradient
from fairlearn.metrics import selection_rate
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Load text data
data_file = os.path.abspath("data/Kushal_Resume.pdf.txt")

if not os.path.exists(data_file):
    print(f"Error: {data_file} not found! Run extract_text.py first.")
    exit(1)

# Load text into a Pandas DataFrame
with open(data_file, "r") as file:
    text_data = file.readlines()

df = pd.DataFrame({"text": text_data})

# Simulate demographic labels (replace with real categorical labels if available)
df["category"] = ["A"] * (len(df) // 2) + ["B"] * (len(df) - len(df) // 2)

# Encode text data into numerical values (since Fairlearn needs numerical features)
df["encoded_text"] = df["text"].factorize()[0]

# Encode categorical labels
label_encoder = LabelEncoder()
df["category_encoded"] = label_encoder.fit_transform(df["category"])

# Split data
X_train, X_test, y_train, y_test, sensitive_train, sensitive_test = train_test_split(
    df["encoded_text"].values.reshape(-1, 1),
    df["category_encoded"],
    df["category_encoded"],  # Passing sensitive attributes
    test_size=0.2,
    random_state=42,
)

# Train a simple Logistic Regression model
predictor = LogisticRegression()
predictor.fit(X_train, y_train)

# ✅ Check for bias before running mitigation
print("Selection Rate by Group Before Mitigation:")
print(df.groupby("category")["encoded_text"].count() / len(df))  # Measures bias in dataset

# ✅ Apply Fairlearn Bias Mitigation using EqualizedOdds
mitigator = ExponentiatedGradient(predictor, constraints=EqualizedOdds())

try:
    mitigator.fit(X_train, y_train, sensitive_features=sensitive_train)  # ✅ Pass sensitive attributes

    # ✅ Check if Fairlearn generated any predictors
    if len(mitigator.predictors_) > 0:
        best_model = mitigator.predictors_[-1]  # Take the last predictor as the best one
        fairness_violation = best_model.predict(X_test)
        print("Fairness Constraint Violation Predictions:", fairness_violation)

        # ✅ Measure selection rate after mitigation
        print("Selection Rate by Group After Mitigation:")
        mitigated_predictions = mitigator.predict(X_test)
        print(pd.DataFrame({"category": sensitive_test, "predictions": mitigated_predictions}).groupby("category")["predictions"].mean())

    else:
        print("⚠️ Fairlearn did not generate any predictors. Model may already be fair or dataset is too small.")

except Exception as e:
    print(f"⚠️ Fairlearn bias mitigation failed: {e}")

print("✅ Bias detection completed.")
