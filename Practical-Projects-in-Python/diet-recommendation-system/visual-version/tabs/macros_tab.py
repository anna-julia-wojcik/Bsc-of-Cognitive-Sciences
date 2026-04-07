# defines macronutrient proportions depending on the target
def macros(user, tdee_value):
    if user.target == "lose":
        p_ratio, f_ratio, c_ratio = 0.30, 0.25, 0.45
    elif user.target == "gain":
        p_ratio, f_ratio, c_ratio = 0.20, 0.20, 0.60
    else:
        p_ratio, f_ratio, c_ratio = 0.20, 0.30, 0.50

    # calculates the requirement for a specific weight (grams) of macronutrients
    proteins = (tdee_value * p_ratio) / 4
    fats = (tdee_value * f_ratio) / 9
    carbs = (tdee_value * c_ratio) / 4
    return {
        "Protein (g)": round(proteins),
        "Fats (g)": round(fats),
        "Carbs (g)": round(carbs)
    }


# function returns micronutrient recommendations depending on the selected target
def minerals(user):
    if user.target == "lose":
        return "Monitor magnesium, B vitamins, iron, and iodine levels due to the caloric deficit."
    elif user.target == "gain":
        return "Monitor zinc, calcium, vitamin D, potassium, and sodium."
    else:
        return "For a healthy diet, monitor magnesium, potassium, vitamins B and D, and OMEGA-3 fatty acids."


# function recommends specific products particularly rich in given macronutrients
def recommendations(user):
    protein_list = ["chicken", "turkey", "lean beef", "fish", "eggs", "cottage cheese", "Greek yogurt",
                    "lentils", "quinoa", "beans", "chickpeas", "tofu"]
    fat_list = ["olive oil", "nuts (almonds, walnuts)", "avocado", "chia seeds", "pumpkin seeds", "marine fish"]
    carb_list = ["groats", "brown rice", "oats", "whole wheat bread", "whole wheat pasta", "potatoes",
                 "sweet potatoes", "fruits", "vegetables"]

    # dietary restrictions - depending on the user's choice, removes intolerable products from the recommendation list
    if "vegan" in user.diet_type:
        forbidden = ["chicken", "turkey", "lean beef", "fish", "eggs", "cottage cheese", "Greek yogurt",
                     "marine fish"]
        protein_list = [p for p in protein_list if p not in forbidden]
        fat_list = [p for p in fat_list if p not in forbidden]
    elif "vegetarian" in user.diet_type:
        forbidden = ["chicken", "turkey", "lean beef", "fish", "marine fish"]
        protein_list = [p for p in protein_list if p not in forbidden]
        fat_list = [p for p in fat_list if p not in forbidden]

    if "gluten-free" in user.diet_type:
        gluten = ["oats", "whole wheat bread", "whole wheat pasta"]
        carb_list = [p for p in carb_list if p not in gluten]
        carb_list.extend(["gluten-free bread", "corn/rice pasta", "millet flakes"])

    return {"Proteins": ", ".join(protein_list), "Fats": ", ".join(fat_list),
            "Carbs": ", ".join(carb_list)}