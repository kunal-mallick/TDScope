import yaml
import pickle
import pandas as pd
import numpy as np 
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV

# Load variables from params.yaml
with open("params.yaml", "r") as file:
    params = yaml.safe_load(file)

    param_grid = params["model_building"]["param_grid"]


# Load feature-engineered training data
train_data = pd.read_csv("data/features/train_pca.csv")
x_train = train_data.drop(columns=["Tds"])
y_train = train_data["Tds"]

# Hyperparameter tuning using GridSearchCV
grid_search = GridSearchCV(SVR(), param_grid, cv=5, n_jobs=-1, verbose=2)
grid_search.fit(x_train, y_train)

# Set up the SVR model with hyperparameter tuning
model = grid_search.best_estimator_

# Train the model
model.fit(x_train, y_train)

# Save the trained model
model_path = "models/svr_model.pkl"
with open(model_path, "wb") as f:
    pickle.dump(model, f)