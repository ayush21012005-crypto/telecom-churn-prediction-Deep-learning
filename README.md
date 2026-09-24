# Telecom Customer Churn Prediction using Deep Learning

A deep learning-based web application that predicts whether a telecom customer is likely to churn.

## 🚀 Project Overview

This project uses an Artificial Neural Network (ANN) to predict customer churn based on customer demographic, service, contract and billing information.

The trained model is exposed through a FastAPI backend and connected to an interactive frontend built using HTML, CSS and JavaScript.

## 🛠️ Technologies Used

- Python
- TensorFlow / Keras
- Scikit-learn
- Pandas
- NumPy
- FastAPI
- Uvicorn
- HTML5
- CSS3
- JavaScript
- Git
- GitHub

## 🧠 Machine Learning

The model uses 30 engineered features including:

- Senior Citizen
- Tenure
- Monthly Charges
- Total Charges
- Gender
- Partner
- Dependents
- Phone Service
- Multiple Lines
- Internet Service
- Online Security
- Online Backup
- Device Protection
- Tech Support
- Streaming TV
- Streaming Movies
- Contract
- Paperless Billing
- Payment Method

## 📁 Project Structure

```text
telecom-churn-prediction/
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── model/
│   ├── churn_ann.keras
│   ├── scaler.pkl
│   └── feature_names.pkl
│
└── frontend/
    ├── index.html
    ├── style.css
    └── script.js
