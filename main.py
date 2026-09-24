from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import numpy as np
import joblib
import tensorflow as tf


# ============================================================
# CREATE FASTAPI APP
# ============================================================

app = FastAPI(
    title="Telecom Customer Churn Prediction API",
    description="Deep Learning based Telecom Customer Churn Prediction",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# LOAD MODEL / SCALER / FEATURE NAMES
# ============================================================

MODEL_PATH = "churn_ann.keras"
SCALER_PATH = "scaler.pkl"
FEATURE_NAMES_PATH = "feature_names.pkl"


model = tf.keras.models.load_model(MODEL_PATH)

scaler = joblib.load(SCALER_PATH)

feature_names = joblib.load(FEATURE_NAMES_PATH)


print("Model loaded successfully")
print("Number of features:", len(feature_names))
print("Features:", feature_names)


# ============================================================
# PYDANTIC REQUEST MODEL
# ============================================================

class CustomerData(BaseModel):

    SeniorCitizen: int = Field(
        ...,
        ge=0,
        le=1,
        description="0 = No, 1 = Yes"
    )

    tenure: float = Field(
        ...,
        ge=0,
        le=100
    )

    MonthlyCharges: float = Field(
        ...,
        ge=0
    )

    TotalCharges: float = Field(
        ...,
        ge=0
    )

    gender: str

    Partner: str

    Dependents: str

    PhoneService: str

    MultipleLines: str

    InternetService: str

    OnlineSecurity: str

    OnlineBackup: str

    DeviceProtection: str

    TechSupport: str

    StreamingTV: str

    StreamingMovies: str

    Contract: str

    PaperlessBilling: str

    PaymentMethod: str


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/")
def home():

    return {
        "message": "Telecom Churn Prediction API is running",
        "docs": "/docs"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "scaler_loaded": scaler is not None,
        "features": len(feature_names)
    }


# ============================================================
# CREATE MODEL INPUT
# ============================================================

def create_feature_vector(data: CustomerData):

    # Start with all features as 0
    features = {
        feature: 0
        for feature in feature_names
    }

    # --------------------------------------------------------
    # NUMERICAL FEATURES
    # --------------------------------------------------------

    features["SeniorCitizen"] = data.SeniorCitizen
    features["tenure"] = data.tenure
    features["MonthlyCharges"] = data.MonthlyCharges
    features["TotalCharges"] = data.TotalCharges


    # --------------------------------------------------------
    # GENDER
    # --------------------------------------------------------

    if data.gender == "Male":
        features["gender_Male"] = 1


    # --------------------------------------------------------
    # PARTNER
    # --------------------------------------------------------

    if data.Partner == "Yes":
        features["Partner_Yes"] = 1


    # --------------------------------------------------------
    # DEPENDENTS
    # --------------------------------------------------------

    if data.Dependents == "Yes":
        features["Dependents_Yes"] = 1


    # --------------------------------------------------------
    # PHONE SERVICE
    # --------------------------------------------------------

    if data.PhoneService == "Yes":
        features["PhoneService_Yes"] = 1


    # --------------------------------------------------------
    # MULTIPLE LINES
    # --------------------------------------------------------

    if data.MultipleLines == "No phone service":

        features["MultipleLines_No phone service"] = 1

    elif data.MultipleLines == "Yes":

        features["MultipleLines_Yes"] = 1


    # --------------------------------------------------------
    # INTERNET SERVICE
    # --------------------------------------------------------

    if data.InternetService == "Fiber optic":

        features["InternetService_Fiber optic"] = 1

    elif data.InternetService == "No":

        features["InternetService_No"] = 1


    # --------------------------------------------------------
    # ONLINE SECURITY
    # --------------------------------------------------------

    if data.OnlineSecurity == "No internet service":

        features["OnlineSecurity_No internet service"] = 1

    elif data.OnlineSecurity == "Yes":

        features["OnlineSecurity_Yes"] = 1


    # --------------------------------------------------------
    # ONLINE BACKUP
    # --------------------------------------------------------

    if data.OnlineBackup == "No internet service":

        features["OnlineBackup_No internet service"] = 1

    elif data.OnlineBackup == "Yes":

        features["OnlineBackup_Yes"] = 1


    # --------------------------------------------------------
    # DEVICE PROTECTION
    # --------------------------------------------------------

    if data.DeviceProtection == "No internet service":

        features["DeviceProtection_No internet service"] = 1

    elif data.DeviceProtection == "Yes":

        features["DeviceProtection_Yes"] = 1


    # --------------------------------------------------------
    # TECH SUPPORT
    # --------------------------------------------------------

    if data.TechSupport == "No internet service":

        features["TechSupport_No internet service"] = 1

    elif data.TechSupport == "Yes":

        features["TechSupport_Yes"] = 1


    # --------------------------------------------------------
    # STREAMING TV
    # --------------------------------------------------------

    if data.StreamingTV == "No internet service":

        features["StreamingTV_No internet service"] = 1

    elif data.StreamingTV == "Yes":

        features["StreamingTV_Yes"] = 1


    # --------------------------------------------------------
    # STREAMING MOVIES
    # --------------------------------------------------------

    if data.StreamingMovies == "No internet service":

        features["StreamingMovies_No internet service"] = 1

    elif data.StreamingMovies == "Yes":

        features["StreamingMovies_Yes"] = 1


    # --------------------------------------------------------
    # CONTRACT
    # --------------------------------------------------------

    if data.Contract == "One year":

        features["Contract_One year"] = 1

    elif data.Contract == "Two year":

        features["Contract_Two year"] = 1


    # --------------------------------------------------------
    # PAPERLESS BILLING
    # --------------------------------------------------------

    if data.PaperlessBilling == "Yes":

        features["PaperlessBilling_Yes"] = 1


    # --------------------------------------------------------
    # PAYMENT METHOD
    # --------------------------------------------------------

    if data.PaymentMethod == "Credit card (automatic)":

        features["PaymentMethod_Credit card (automatic)"] = 1

    elif data.PaymentMethod == "Electronic check":

        features["PaymentMethod_Electronic check"] = 1

    elif data.PaymentMethod == "Mailed check":

        features["PaymentMethod_Mailed check"] = 1


    # --------------------------------------------------------
    # CONVERT TO ARRAY IN EXACT MODEL ORDER
    # --------------------------------------------------------

    vector = np.array(
        [
            features[feature]
            for feature in feature_names
        ],
        dtype=np.float32
    ).reshape(1, -1)

    return vector


# ============================================================
# PREDICTION ENDPOINT
# ============================================================

@app.post("/predict")
def predict(data: CustomerData):

    try:

        # Create 30-feature vector
        input_data = create_feature_vector(data)

        # Scale
        scaled_data = scaler.transform(input_data)

        # Deep learning prediction
        prediction_probability = model.predict(
            scaled_data,
            verbose=0
        )

        # Convert probability to float
        probability = float(
            np.asarray(prediction_probability).reshape(-1)[0]
        )

        # Convert to percentage
        probability_percentage = probability * 100

        # Classification threshold
        prediction = 1 if probability >= 0.5 else 0

        if prediction == 1:

            result = "Customer likely to churn"
            status = "HIGH RISK"

        else:

            result = "Customer likely to stay"
            status = "LOW RISK"


        return {

            "success": True,

            "prediction": prediction,

            "result": result,

            "status": status,

            "churn_probability": round(
                probability,
                4
            ),

            "churn_percentage": round(
                probability_percentage,
                2
            )

        }

    except Exception as e:

        return {

            "success": False,

            "error": str(e)

        }
