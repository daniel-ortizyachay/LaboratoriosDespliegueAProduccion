import mlflow
import numpy as np
import pandas as pd

# Set the MLFlow server URI
uri = "http://127.0.0.1:6001"
mlflow.set_tracking_uri(uri=uri)

# Provide the model path/url
logged_model = "runs:/485a1dffa0104cdea493bdccc78d0192/logistic_regression_model"

# Load model as a PyFuncModel
loaded_model = mlflow.sklearn.load_model(logged_model)

# Input a random datapoint
np.random.seed(42)
data = np.random.rand(1, 64)  # Example input with 64 features

# Predict the output for the data
# Convert the numpy array to a pandas DataFrame
data_df = pd.DataFrame(data, columns=[f"feature_{i}" for i in range(data.shape[1])])

# Convert DataFrame back to numpy array to avoid warnings
prediction = loaded_model.predict(data_df.values)

# Print out prediction result
print("Prediction:", prediction)
