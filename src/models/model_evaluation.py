import os
import json
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

# save evaluation metrics in json format
metrics = {"test_metrics":
    {'mean_squared_error': mse,
    'r2_score': r2,
    'root_mean_squared_error': rmse}
}

metrics_path = 'reports/evaluation_metrics.json'
os.makedirs(os.path.dirname(metrics_path), exist_ok=True)
with open(metrics_path, 'w') as f:
    json.dump(metrics, f, indent=4)