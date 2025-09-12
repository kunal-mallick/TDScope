import os
import yaml
import pickle
import pandas as pd
from sklearn.decomposition import PCA

# load variables from params.yaml
with open("params.yaml", "r") as file:
    params = yaml.safe_load(file)

    n_components = params["feature_engineering"]["n_components"]
    random_state = params["feature_engineering"]["random_state"]

# Load preprocessed data
train_scaled = pd.read_csv("data/processed/train_scaled.csv")
test_scaled = pd.read_csv("data/processed/test_scaled.csv")

# Separate features and target variable
train_data_X = train_scaled.drop(columns=["Tds"])
test_data_X = test_scaled.drop(columns=["Tds"])
train_data_y = train_scaled["Tds"]
test_data_y = test_scaled["Tds"]

# Apply PCA
pca = PCA(n_components=n_components)
train_data_X_pca = pca.fit_transform(train_data_X)
test_data_X_pca = pca.transform(test_data_X)

# Convert PCA results back to DataFrame
train_pca = pd.DataFrame(train_data_X_pca, columns=[f'PC{i+1}' for i in range(train_data_X_pca.shape[1])])
train_pca['Tds'] = train_data_y.values
test_pca = pd.DataFrame(test_data_X_pca, columns=[f'PC{i+1}' for i in range(test_data_X_pca.shape[1])])
test_pca['Tds'] = test_data_y.values

# save PCA model
os.makedirs("models", exist_ok=True)  # Ensure the directory exists
with open("models/pca_model.pkl", "wb") as f:
    pickle.dump(pca, f)

# Save the PCA transformed datasets
os.makedirs("data/features", exist_ok=True)  # Ensure the directory exists
train_pca.to_csv("data/features/train_pca.csv", index=False)
test_pca.to_csv("data/features/test_pca.csv", index=False)