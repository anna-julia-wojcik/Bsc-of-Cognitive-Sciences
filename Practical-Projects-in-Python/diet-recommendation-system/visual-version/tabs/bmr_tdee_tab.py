# function - Basal Metabolic Rate (BMR) calculator
def calculate_bmr_simple(user):
    if user.gender == "f":
        return 10 * user.weight + 6.25 * user.height - 5 * user.age - 161
    return 10 * user.weight + 6.25 * user.height - 5 * user.age + 5

def calculate_tdee(user):
    return calculate_bmr_simple(user) * user.activity# function - Basal Metabolic Rate (BMR) calculator