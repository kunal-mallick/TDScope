import os
import json
import mlflow
import pickle
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score ,root_mean_squared_error

# load the trained model
model_path = 'models/svr_model.pkl'
with open(model_path, 'rb') as f:
    model = pickle.load(f)

# load the test data
test_data_path = 'data/features/test_pca.csv'
test_data = pd.read_csv(test_data_path)
X_test = test_data.drop(columns=['Tds'])
y_test = test_data['Tds']

# make predictions
y_pred = model.predict(X_test)

# evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
rmse = root_mean_squared_error(y_test, y_pred)

# Set the tracking URI
mlflow.set_tracking_uri("http://127.0.0.1:5000/")

# log metrics to MLflow
mlflow.set_experiment("TDS Prediction Experiment")
with mlflow.start_run():
    mlflow.log_metric("MSE", mse)
    mlflow.log_metric("R2", r2)
    mlflow.log_metric("RMSE", rmse)
    mlflow.sklearn.log_model(model, "model")
    mlflow.log_artifact(test_data_path, artifact_path="test_data")
    mlflow.log_param("model_type", "SVR")
    mlflow.log_param("features", list(X_test.columns))
    mlflow.log_param("target", "Tds")
    mlflow.log_param("test_data_size", len(test_data))
    mlflow.log_param("model_path", model_path)
    mlflow.log_param("test_data_path", test_data_path)
    mlflow.log_param("evaluation_metrics", model.get_params())
    mlflow.end_run()