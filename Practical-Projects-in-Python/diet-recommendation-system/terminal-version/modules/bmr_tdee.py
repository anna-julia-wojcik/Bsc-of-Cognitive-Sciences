def calculate_bmr(user) -> float:
    if user.gender == "f":
        return 10 * user.weight + 6.25 * user.height - 5 * user.age - 161
    return 10 * user.weight + 6.25 * user.height - 5 * user.age + 5


def calculate_tdee(user) -> float:
    return calculate_bmr(user) * user.activity
