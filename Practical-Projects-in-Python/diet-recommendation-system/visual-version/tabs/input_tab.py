import streamlit as st

def st_input_col1():
    gender_display = st.selectbox("Gender", ["Male", "Female"], key="z_gender")
    gender_val = "m" if gender_display == "Male" else "f"  # refers to the values defined in the class

    age_z = st.number_input("Age", min_value=1, max_value=120, value=25, key="z_age")  # default value: 25

    height_z = st.number_input("Height (cm)", min_value=100, max_value=250, value=170,
                               key="z_height")  # default value: 170
    weight_z = st.number_input("Weight (kg)", min_value=30.0, max_value=300.0, value=65.0,
                               key="z_weight")  # default value: 65

    return gender_val, age_z, height_z, weight_z

def st_input_col2():
    activity_options = {
        "No exercise": 1.2,
        "Light (1-3 days)": 1.375,
        "Moderate (3-5 days)": 1.55,
        "Heavy (6-7 days)": 1.725,
        "Very heavy (professional sports)": 2.4
    }
    act_key = st.selectbox("Activity level", list(activity_options.keys()), key="z_act")  # displays keys from the list
    activity_val = activity_options[act_key]  # extracts the numerical value mapped to the key

    target_options = {"Lose weight": "lose", "Maintain weight": "maintain",
                      "Gain weight": "gain"}  # dictionary mapped to the class
    tar_key = st.selectbox("Target", list(target_options.keys()), key="z_target")  # list for target selection
    target_val = target_options[tar_key]  # extracts the value mapped to the key

    lifestyle = st.selectbox("Work type", ["Office", "Physical", "Mixed"],
                             key="z_work")  # work type selection list

    return activity_val, target_val, lifestyle