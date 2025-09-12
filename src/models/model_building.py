import yaml
import pickle
import pandas as pd
import numpy as np 
from sklearn.svm import SVR

# Load variables from params.yaml
with open("params.yaml", "r") as file:
    params = yaml.safe_load(file)

    kernel = params["model_building"]["kernel"]
    degree = params["model_building"]["degree"]
    gamma = params["model_building"]["gamma"]
    coef0 = params["model_building"]["coef0"]
    tol = params["model_building"]["tol"]
    C = params["model_building"]["C"]
    epsilon = params["model_building"]["epsilon"]
    shrinking = params["model_building"]["shrinking"]
    cache_size = params["model_building"]["cache_size"]
    verbose = params["model_building"]["verbose"]


# Load feature-engineered training data
train_data = pd.read_csv("data/features/train_pca.csv")
x_train = train_data.drop(columns=["Tds"])
y_train = train_data["Tds"]

# Initialize and train the SVR model
model = SVR(kernel=kernel, degree=degree, gamma=gamma, coef0=coef0, tol=tol, C=C, epsilon=epsilon, shrinking=shrinking, cache_size=cache_size, verbose=verbose)
model.fit(x_train, y_train)

# Save the trained model
with open("models/svr_model.pkl", "wb") as file:
    pickle.dump(model, file)