import streamlit as st

def calculate_bmi(user):
    # formula to calculate BMI
    return user.weight / ((user.height / 100) ** 2)

def interpret_bmi(bmi):
    if bmi < 16.0:  # checks if BMI is less than 16 and assigns the appropriate interpretation
        interpretation = "severe thinness"
        color = "error"  # sets the color flag to "error", which in Streamlit means red
    elif bmi < 17.0:  # if the above condition is not met, checks if BMI is greater than or equal to 16 but less than 17 and assigns the appropriate interpretation
        interpretation = "moderate thinness"
        color = "warning"  # sets the color flag to "warning", which in Streamlit means orange
    elif bmi < 18.5:  # if the above condition is not met, checks if BMI is greater than or equal to 17 but less than 18.5 and assigns the appropriate interpretation
        interpretation = "underweight"
        color = "warning"  # sets the color flag to "warning", which in Streamlit means orange
    elif bmi < 25.0:  # if the above condition is not met, checks if BMI is greater than or equal to 18.5 but less than 25 and assigns the appropriate interpretation
        interpretation = "normal weight"
        color = "success"  # sets the color flag to "success", which in Streamlit means green
    elif bmi < 30.0:  # if the above condition is not met, checks if BMI is greater than or equal to 25 but less than 30 and assigns the appropriate interpretation
        interpretation = "overweight"
        color = "warning"  # sets the color flag to "warning", which in Streamlit means orange
    elif bmi < 35.0:  # if the above condition is not met, checks if BMI is greater than or equal to 30 but less than 35 and assigns the appropriate interpretation
        interpretation = "obesity class I"
        color = "error"  # sets the color flag to "error", which in Streamlit means red
    elif bmi < 40.0:  # if the above condition is not met, checks if BMI is greater than or equal to 35 but less than 40 and assigns the appropriate interpretation
        interpretation = "obesity class II"
        color = "error"  # sets the color flag to "error", which in Streamlit means red
    else:  # if the above condition is not met, else handles all cases where BMI is greater than or equal to 40
        interpretation = "obesity class III"
        color = "error"  # sets the color flag to "error", which in Streamlit means red

    if color == "success":  # displays a green "success" banner with the interpretation text
        st.success(f"Interpretation: {interpretation}")
    elif color == "warning":  # displays an orange "warning" banner with the interpretation text
        st.warning(f"Interpretation: {interpretation}")
    else:  # displays a red "error" banner with the interpretation text
        st.error(f"Interpretation: {interpretation}")