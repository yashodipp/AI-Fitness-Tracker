

# ==========================================================
# AI FITNESS PREDICTION DASHBOARD
# ==========================================================

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import joblib
import os
import time
import plotly.express as px
from streamlit_option_menu import option_menu

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="AI Fitness Dashboard",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp{
    background: linear-gradient(
        135deg,
        #0f172a,
        #111827,
        #1e293b,
        #0f172a
    );
    background-size:400% 400%;
    animation: gradient 15s ease infinite;
}

@keyframes gradient{
    0%{background-position:0% 50%;}
    50%{background-position:100% 50%;}
    100%{background-position:0% 50%;}
}

.hero{
    padding:40px;
    border-radius:25px;
    background:rgba(255,255,255,0.08);
    backdrop-filter:blur(20px);
    text-align:center;
    box-shadow:0px 8px 32px rgba(0,0,0,.4);
}

.hero h1{
    color:white;
    font-size:52px;
}

.hero p{
    color:#d1d5db;
    font-size:18px;
}

.glass{
    background:rgba(255,255,255,0.08);
    backdrop-filter:blur(15px);
    border-radius:20px;
    padding:20px;
    box-shadow:0px 8px 32px rgba(0,0,0,.3);
}

.result-card{
    background:linear-gradient(
        135deg,
        #00F5A0,
        #00D9F5
    );

    color:black;
    padding:30px;
    border-radius:20px;
    text-align:center;
    font-size:28px;
    font-weight:bold;
    animation:fadein 1s ease;
}

@keyframes fadein{
    from{
        opacity:0;
        transform:translateY(20px);
    }
    to{
        opacity:1;
        transform:translateY(0px);
    }
}

.stButton > button{
    width:100%;
    border:none;
    border-radius:15px;
    background:linear-gradient(
        90deg,
        #00F5A0,
        #00D9F5
    );
    color:black;
    font-weight:700;
    font-size:18px;
    padding:14px;
}

.stButton > button:hover{
    transform:scale(1.02);
    box-shadow:0px 0px 20px cyan;
}

.footer{
    text-align:center;
    color:#cbd5e1;
    padding:20px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# MODEL LOADING
# ==========================================================

MODEL_PATH = "linear_model.pkl"

@st.cache_resource
def load_model():

    if not os.path.exists(MODEL_PATH):
        return None

    try:
        return joblib.load(MODEL_PATH)
    except:
        pass

    try:
        with open(MODEL_PATH, "rb") as f:
            return pickle.load(f)
    except:
        return None

model = load_model()

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    selected = option_menu(
        menu_title="AI FITNESS",
        options=[
            "Home",
            "Prediction",
            "Analytics",
            "About Model",
            "Contact"
        ],
        icons=[
            "house",
            "cpu",
            "bar-chart",
            "info-circle",
            "envelope"
        ],
        default_index=0
    )

# ==========================================================
# HOME
# ==========================================================

if selected == "Home":

    st.markdown("""
    <div class="hero">
        <h1>🏋️ AI Fitness Dashboard</h1>
        <p>
        Machine Learning Powered Fitness Prediction System
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Features", "17")
    c2.metric("Model", "Loaded" if model else "Not Found")
    c3.metric("Analytics", "Active")
    c4.metric("Version", "2.0")

    st.write("")

    st.markdown("""
    <div class='glass'>
    <h3>🚀 AI Fitness Intelligence</h3>

    Predict fitness-related outcomes using advanced
    machine learning algorithms and health metrics.

    </div>
    """, unsafe_allow_html=True)

# ==========================================================
# PREDICTION
# ==========================================================

elif selected == "Prediction":

    st.title("🔮 Fitness Prediction")

    if model is None:
        st.error("Model not loaded. Place linear_model.pkl in project folder.")
        st.stop()

    col1,col2,col3 = st.columns(3)

    with col1:

        age = st.slider("Age",10,100,25)

        gender = st.selectbox(
            "Gender",
            ["Male","Female"]
        )

        weight = st.number_input(
            "Weight (kg)",
            value=70.0
        )

        height = st.number_input(
            "Height (m)",
            value=1.75
        )

        max_bpm = st.number_input(
            "Max_BPM",
            value=180
        )

        avg_bpm = st.number_input(
            "Avg_BPM",
            value=120
        )

    with col2:

        resting_bpm = st.number_input(
            "Resting_BPM",
            value=70
        )

        session_duration = st.number_input(
            "Session_Duration (hours)",
            value=1.5
        )

        fat_percentage = st.number_input(
            "Fat_Percentage",
            value=20.0
        )

        water_intake = st.number_input(
            "Water_Intake (liters)",
            value=3.0
        )

        workout_frequency = st.number_input(
            "Workout_Frequency",
            value=4
        )

        experience_level = st.selectbox(
            "Experience_Level",
            [1,2,3]
        )

    with col3:

        bmi = st.number_input(
            "BMI",
            value=22.0
        )

        workout_type = st.selectbox(
            "Workout Type",
            [
                "Cardio",
                "HIIT",
                "Strength",
                "Yoga"
            ]
        )

    if st.button("🚀 Predict"):

        try:

            gender_value = 1 if gender=="Male" else 0

            cardio = 1 if workout_type=="Cardio" else 0
            hiit = 1 if workout_type=="HIIT" else 0
            strength = 1 if workout_type=="Strength" else 0
            yoga = 1 if workout_type=="Yoga" else 0

            input_data = {

                "Age": age,
                "Gender": gender_value,
                "Weight (kg)": weight,
                "Height (m)": height,
                "Max_BPM": max_bpm,
                "Avg_BPM": avg_bpm,
                "Resting_BPM": resting_bpm,
                "Session_Duration (hours)": session_duration,
                "Fat_Percentage": fat_percentage,
                "Water_Intake (liters)": water_intake,
                "Workout_Frequency (days/week)": workout_frequency,
                "Experience_Level": experience_level,
                "BMI": bmi,
                "Workout_Type_Cardio": cardio,
                "Workout_Type_HIIT": hiit,
                "Workout_Type_Strength": strength,
                "Workout_Type_Yoga": yoga
            }

            if hasattr(model, "feature_names_in_"):

                ordered_data = {}

                for col in model.feature_names_in_:
                    ordered_data[col] = input_data.get(col, 0)

                input_df = pd.DataFrame([ordered_data])

            else:
                input_df = pd.DataFrame([input_data])

            with st.spinner("AI Processing..."):
                time.sleep(2)
                prediction = model.predict(input_df)

            st.markdown(
                f"""
                <div class="result-card">
                Prediction Result<br><br>
                {prediction[0]:,.2f}
                </div>
                """,
                unsafe_allow_html=True
            )

        except Exception as e:
            st.error(f"Prediction Error: {e}")

# ==========================================================
# ANALYTICS
# ==========================================================

elif selected == "Analytics":

    st.title("📊 Fitness Analytics")

    analytics_df = pd.DataFrame({
        "Month":["Jan","Feb","Mar","Apr","May","Jun"],
        "Calories":[450,580,620,700,830,910],
        "Workout Hours":[12,15,18,22,26,30],
        "BMI":[24,23.8,23.4,23.1,22.8,22.5]
    })

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Calories", "4,090")
    c2.metric("Workout Hrs", "123")
    c3.metric("Avg BMI", "23.3")
    c4.metric("Fitness Score", "92%")

    col1,col2 = st.columns(2)

    with col1:

        donut = px.pie(
            analytics_df,
            names="Month",
            values="Calories",
            hole=0.6,
            title="Calories Distribution"
        )

        donut.update_layout(template="plotly_dark")

        st.plotly_chart(
            donut,
            use_container_width=True
        )

    with col2:

        violin = px.violin(
            analytics_df,
            y="Calories",
            box=True,
            points="all",
            title="Calories Violin Plot"
        )

        violin.update_layout(template="plotly_dark")

        st.plotly_chart(
            violin,
            use_container_width=True
        )

    area = px.area(
        analytics_df,
        x="Month",
        y="Calories",
        title="Calories Trend"
    )

    area.update_layout(template="plotly_dark")

    st.plotly_chart(
        area,
        use_container_width=True
    )

    line = px.line(
        analytics_df,
        x="Month",
        y="Workout Hours",
        markers=True,
        title="Workout Progress"
    )

    line.update_layout(template="plotly_dark")

    st.plotly_chart(
        line,
        use_container_width=True
    )

    bmi_chart = px.bar(
        analytics_df,
        x="Month",
        y="BMI",
        title="BMI Trend"
    )

    bmi_chart.update_layout(template="plotly_dark")

    st.plotly_chart(
        bmi_chart,
        use_container_width=True
    )

# ==========================================================
# ABOUT MODEL
# ==========================================================

elif selected == "About Model":

    st.title("🤖 About Linear Regression Model")

    st.markdown("""
    ### Linear Regression

    Linear Regression is a supervised machine learning algorithm used
    to predict continuous numerical values.

    It finds the best-fit relationship between independent variables
    and a target variable.

    ### Formula
    """)

    st.latex(
        r"Y = \beta_0 + \beta_1X_1 + \beta_2X_2 + ... + \beta_nX_n"
    )

    st.markdown("""
    ### Features Used

    - Age
    - Gender
    - Weight
    - Height
    - BMI
    - Max BPM
    - Avg BPM
    - Resting BPM
    - Session Duration
    - Water Intake
    - Workout Frequency
    - Experience Level
    - Workout Type

    ### Advantages

    ✅ Fast

    ✅ Interpretable

    ✅ Lightweight

    ✅ Accurate for Numerical Prediction
    """)

# ==========================================================
# CONTACT
# ==========================================================

elif selected == "Contact":

    st.title("📩 Contact")

    with st.form("contact_form"):

        name = st.text_input("Name")

        email = st.text_input("Email")

        message = st.text_area("Message")

        submit = st.form_submit_button("Send")

        if submit:
            st.success(
                "Message submitted successfully!"
            )

# ==========================================================
# FOOTER
# ==========================================================

st.markdown("---")

st.markdown("""
<div class='footer'>

© 2026 AI Fitness Prediction Dashboard

<br><br>

👨‍💻 Developed with Streamlit python & Machine Learning

</div>
""", unsafe_allow_html=True)