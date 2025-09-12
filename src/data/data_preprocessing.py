import os
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Load raw train and test data
train_data = pd.read_csv("data/raw/train.csv")
test_data = pd.read_csv("data/raw/test.csv")

# Drop rows with missing values and unnecessary columns
train_data.dropna(inplace=True)
train_data.drop(columns=["GEMS.Station.Number", "Sample.Date", "Sample.Time"], inplace=True)
test_data.dropna(inplace=True)
test_data.drop(columns=["GEMS.Station.Number", "Sample.Date", "Sample.Time"], inplace=True)

# Separate features and target variable
train_data_X = train_data.drop(columns=["Tds"])
test_data_X = test_data.drop(columns=["Tds"])
train_data_y = train_data["Tds"]
test_data_y = test_data["Tds"]

# Standardize features
scaler = StandardScaler()
train_data_X_scaled = scaler.fit_transform(train_data_X)
test_data_X_scaled = scaler.transform(test_data_X)

# Convert scaled features back to DataFrame
train_scaled = pd.DataFrame(train_data_X_scaled, columns=train_data_X.columns)
train_scaled['Tds'] = train_data_y.values
test_scaled = pd.DataFrame(test_data_X_scaled, columns=test_data_X.columns)
test_scaled['Tds'] = test_data_y.values

# Save the preprocessed datasets
os.makedirs("data/processed", exist_ok=True)  # Ensure the directory exists
train_scaled.to_csv("data/processed/train_scaled.csv", index=False)
test_scaled.to_csv("data/processed/test_scaled.csv", index=False)