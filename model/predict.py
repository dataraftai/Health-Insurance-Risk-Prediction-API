import pandas as pd
import joblib

# import the ml model

with open("model/insurance_risk_pipeline.pkl","rb") as f:
    model = joblib.load(f)

#MLflow 
MODEL_VERSION = "1.0.0"
