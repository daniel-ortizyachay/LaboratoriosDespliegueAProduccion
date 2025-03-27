# This file is designed based on MlFlow tutorial
# https://mlflow.org/docs/latest/getting-started/intro-quickstart/index.html

import mlflow
from mlflow.models import infer_signature

from utility import pipeline

# Set the MLFlow tracking server URI
uri = "http://127.0.0.1:6001"
mlflow.set_tracking_uri(uri)

# Set experiment name
email = "danielortiz@yachaytech.edu.ec"  # Use a customized experiment name
experiment_name = f"{email}-lab7"
mlflow.set_experiment(experiment_name)

# Generate train and test datasets using `pipeline.data_preprocessing` function
X_train, X_test, y_train, y_test = pipeline.data_preprocessing()

# Define model parameters for Random Forest
params = {
    "n_estimators": 100,
    "max_depth": 10,
    "random_state": 8888,
}

# Train the Random Forest model
trained_model = pipeline.train_random_forest(X_train, y_train, params)

# Evaluate the model
accuracy = pipeline.evaluation(trained_model, X_test, y_test)

# Log model and metrics to the tracking server
run_name = "Random Forest Run"  # Optional: Specify a run name
with mlflow.start_run(run_name=run_name):
    # Log parameters and metrics
    mlflow.log_params(params)
    mlflow.log_metric("accuracy", accuracy)
    mlflow.set_tag("Training Info", "Random Forest model for digits_model data")
    
    # Infer the model signature
    signature = infer_signature(X_train, trained_model.predict(X_train))
    
    # Log the model
    model_info = mlflow.sklearn.log_model(
        sk_model=trained_model,
        artifact_path="random_forest_model",  # Set the artifact path
        signature=signature,
        input_example=X_train,
        registered_model_name="digits_model",  # Static name for the registered model
    )

    print(f"Model registered with accuracy: {accuracy}")
