import streamlit as st
import pandas as pd
import pickle

# Set page title
st.set_page_config(page_title="Calorie Burn Predictor", page_icon="🔥", layout="centered")

# Main Title
st.title("🔥 Calorie Burn Prediction System")
st.write("Enter your exercise details below to estimate calories burned.")
st.markdown("---")

# 1. Load the pre-trained Machine Learning model
@st.cache_resource
def load_model():
    with open("calorie_model.pkl", "rb") as f:
        model = pickle.load(f)
    return model

try:
    model = load_model()
except FileNotFoundError:
    st.error("Error: 'calorie_model.pkl' not found! Please run 'train_model.py' first.")
    st.stop()

# 2. Main Page Input Form
st.subheader("📋 Enter Workout Details")

col1, col2 = st.columns(2)

with col1:
    gender_choice = st.selectbox("Gender", ("Male", "Female"))
    gender = 0 if gender_choice == "Male" else 1
    
    age = st.number_input("Age (years)", min_value=10, max_value=80, value=25)
    height = st.number_input("Height (cm)", min_value=120.0, max_value=220.0, value=170.0)
    weight = st.number_input("Weight (kg)", min_value=30.0, max_value=150.0, value=70.0)

with col2:
    duration = st.number_input("Duration (minutes)", min_value=1.0, max_value=120.0, value=30.0)
    heart_rate = st.number_input("Heart Rate (bpm)", min_value=60.0, max_value=180.0, value=105.0)
    body_temp = st.number_input("Body Temp (°C)", min_value=36.0, max_value=42.0, value=40.0)

st.markdown("---")

# 3. Predict Button & Output
if st.button("🚀 Predict Calories Burned", use_container_width=True):
    # Prepare input data array
    input_data = pd.DataFrame({
        'Gender': [gender],
        'Age': [age],
        'Height': [height],
        'Weight': [weight],
        'Duration': [duration],
        'Heart_Rate': [heart_rate],
        'Body_Temp': [body_temp]
    })

    # Predict using trained model
    prediction = model.predict(input_data)
    calories = round(prediction[0], 2)

    # Display result
    st.success(f"**Estimated Calories Burned:** {calories} kcal")
