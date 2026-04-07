def calculate_bmi(user) -> float:
    return user.weight / ((user.height / 100) ** 2)


def interpret_bmi(bmi: float) -> str:
    if bmi < 16.0:
        return "severe thinness"
    elif bmi < 17.0:
        return "moderate thinness"
    elif bmi < 18.5:
        return "underweight"
    elif bmi < 25.0:
        return "normal weight"
    elif bmi < 30.0:
        return "overweight"
    elif bmi < 35.0:
        return "obesity class I"
    elif bmi < 40.0:
        return "obesity class II"
    else:
        return "obesity class III"
