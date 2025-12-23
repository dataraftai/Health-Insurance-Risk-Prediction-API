from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schema.user_input_pydantic import UserInput
from schema.prediction_responce import responce,PredictionResponce
from model.predict import MODEL_VERSION,model
import pandas as pd

app = FastAPI()

@app.get("/")       # for page(for user)
def home():
    return{"project_name": "Health Insurance Risk Prediction API",
        "message":"This project is a Health Insurance Risk Prediction System. It uses Machine Learning (ML) to analyze a person's medical history and lifestyle to determine their insurance risk level."}

@app.get("/health")        # for machine (machine readable)
def health_check():
    return{
        "status":"ok",
        "version":MODEL_VERSION,
        "model_loaded" : model is not None
    }

@app.post("/predict",response_model=responce)
def predict_risk(data:UserInput): 

    user_input =  pd.DataFrame([{
        'age': data.age,
        'income': data.income,
        'household_size': data.household_size,
        'dependents':data.dependents,
        'bmi': data.bmi,
        'visits_last_year' : data.visits_last_year,
        'hospitalizations_last_3yrs' : data.hospitalizations_last_3yrs,
        'days_hospitalized_last_3yrs': data.days_hospitalized_last_3yrs,
        'medication_count': data.medication_count,
        'systolic_bp': data.systolic_bp,
        'diastolic_bp':data.diastolic_bp,
        'ldl': data.ldl,
        'hba1c':data.hba1c,
        'deductible':data.deductible,
        'copay': data.copay,
        'policy_term_years': data.policy_term_years,
        'policy_changes_last_2yrs':data.policy_changes_last_2yrs,
        'provider_quality':data.provider_quality,
        'risk_score':data.risk_score,
        'chronic_count':data.chronic_count,
        'hypertension': data.hypertension,
        'diabetes': data.diabetes,
        'asthma': data.asthma,
        'copd':data.copd,
        'cardiovascular_disease':data.cardiovascular_disease,
        'cancer_history':data.cancer_history,
        'kidney_disease':data.kidney_disease,
        'liver_disease':data.liver_disease,
        'arthritis':data.arthritis,
        'mental_health':data.mental_health,
        'proc_imaging_count':data.proc_imaging_count,
        'proc_surgery_count':data.proc_surgery_count,
        'proc_physio_count':data.proc_physio_count,
        'proc_consult_count':data.proc_consult_count,
        'proc_lab_count': data.proc_lab_count,
        'had_major_procedure':data.had_major_procedure,
        'sex':data.sex,
        'region':data.region,
        'urban_rural':data.urban_rural,
        'education':data.education,
        'marital_status':data.marital_status,
        'employment_status': data.employment_status,
        'smoker':data.smoker,
        'alcohol_freq':data.alcohol_freq,
        'plan_type':data.plan_type,
        'network_tier':data.network_tier
    }])

    try:
        prediction = model.predict(user_input)[0]

        return JSONResponse(status_code=200,content={"predicted_category":int(prediction)})

    except Exception as e:

        return JSONResponse(status_code=500,content=str(e))


@app.post("/predict/high_risk",response_model=PredictionResponce)
def proba_predict_risk(data:UserInput):

    user_input = pd.DataFrame([{
        'age': data.age,
        'income': data.income,
        'household_size': data.household_size,
        'dependents':data.dependents,
        'bmi': data.bmi,
        'visits_last_year' : data.visits_last_year,
        'hospitalizations_last_3yrs' : data.hospitalizations_last_3yrs,
        'days_hospitalized_last_3yrs': data.days_hospitalized_last_3yrs,
        'medication_count': data.medication_count,
        'systolic_bp': data.systolic_bp,
        'diastolic_bp':data.diastolic_bp,
        'ldl': data.ldl,
        'hba1c':data.hba1c,
        'deductible':data.deductible,
        'copay': data.copay,
        'policy_term_years': data.policy_term_years,
        'policy_changes_last_2yrs':data.policy_changes_last_2yrs,
        'provider_quality':data.provider_quality,
        'risk_score':data.risk_score,
        'chronic_count':data.chronic_count,
        'hypertension': data.hypertension,
        'diabetes': data.diabetes,
        'asthma': data.asthma,
        'copd':data.copd,
        'cardiovascular_disease':data.cardiovascular_disease,
        'cancer_history':data.cancer_history,
        'kidney_disease':data.kidney_disease,
        'liver_disease':data.liver_disease,
        'arthritis':data.arthritis,
        'mental_health':data.mental_health,
        'proc_imaging_count':data.proc_imaging_count,
        'proc_surgery_count':data.proc_surgery_count,
        'proc_physio_count':data.proc_physio_count,
        'proc_consult_count':data.proc_consult_count,
        'proc_lab_count': data.proc_lab_count,
        'had_major_procedure':data.had_major_procedure,
        'sex':data.sex,
        'region':data.region,
        'urban_rural':data.urban_rural,
        'education':data.education,
        'marital_status':data.marital_status,
        'employment_status': data.employment_status,
        'smoker':data.smoker,
        'alcohol_freq':data.alcohol_freq,
        'plan_type':data.plan_type,
        'network_tier':data.network_tier
    }])
    
    try:

        prob_high_risk = model.predict_proba(user_input)[0,1]  # with probability defoult threshould
        
        THRESHOLD = 0.30                                                       # with threshould 0.30
        risk_label = "High Risk" if prob_high_risk >= THRESHOLD else "Low Risk"

        return JSONResponse(status_code=200,content={"predicted_category":risk_label,
                                                    "probability_high_risk": float(round(prob_high_risk,4)),
                                                    "threshold_used": THRESHOLD,
                                                })
    except Exception as e:

        return JSONResponse(status_code=500,content=str(e))

