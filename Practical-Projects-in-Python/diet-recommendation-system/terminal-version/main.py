from classes.input_handling import User
from modules.bmi import calculate_bmi, interpret_bmi
from modules.bmr_tdee import calculate_bmr, calculate_tdee
from modules.macros import macros, minerals, recommendations
from modules.file_handling import load_recipes_from_file, add_recipe_to_file, remove_recipe_from_file
from modules.meal_planner import create_cookbook, find_best_match


def prompt_int(prompt: str, min_val: int, max_val: int) -> int:
    while True:
        try:
            val = int(input(prompt))
            if min_val <= val <= max_val:
                return val
            print(f"  Please enter a value between {min_val} and {max_val}.")
        except ValueError:
            print("  Invalid input — please enter a whole number.")


def prompt_float(prompt: str, min_val: float, max_val: float) -> float:
    while True:
        try:
            val = float(input(prompt))
            if min_val <= val <= max_val:
                return val
            print(f"  Please enter a value between {min_val} and {max_val}.")
        except ValueError:
            print("  Invalid input — please enter a number.")


def prompt_choice(prompt: str, options: list[str]) -> str:
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")
    while True:
        try:
            idx = int(input(prompt)) - 1
            if 0 <= idx < len(options):
                return options[idx]
            print(f"  Please enter a number between 1 and {len(options)}.")
        except ValueError:
            print("  Invalid input.")


def divider():
    print("\n" + "─" * 50 + "\n")


def collect_user_data() -> User:
    divider()
    print("📋  DATA INPUT")

    print("\nGender:")
    gender_display = prompt_choice("Select: ", ["Male", "Female"])
    gender_val = "m" if gender_display == "Male" else "f"

    age = prompt_int("Age: ", 1, 120)
    height = prompt_int("Height (cm): ", 50, 300)
    weight = prompt_float("Weight (kg): ", 0.1, 600)

    activity_options = {
        "No exercise": 1.2,
        "Light (1-3 days/week)": 1.375,
        "Moderate (3-5 days/week)": 1.55,
        "Heavy (6-7 days/week)": 1.725,
        "Very heavy (professional sports)": 2.4
    }
    print("\nActivity level:")
    act_key = prompt_choice("Select: ", list(activity_options.keys()))
    activity_val = activity_options[act_key]

    target_options = {"Lose weight": "lose", "Maintain weight": "maintain", "Gain weight": "gain"}
    print("\nTarget:")
    tar_key = prompt_choice("Select: ", list(target_options.keys()))
    target_val = target_options[tar_key]

    print("\nWork type:")
    lifestyle = prompt_choice("Select: ", ["Office", "Physical", "Mixed"])

    print("\nDiet type (enter numbers separated by commas, e.g. 1,3):")
    diet_options = ["gluten-free", "vegetarian", "vegan", "standard"]
    for i, d in enumerate(diet_options, 1):
        print(f"  {i}. {d}")
    while True:
        raw = input("Select: ").strip()
        try:
            indices = [int(x.strip()) - 1 for x in raw.split(",")]
            if all(0 <= i < len(diet_options) for i in indices):
                diet_type = [diet_options[i] for i in indices]
                break
            print("  Invalid selection — please use numbers from the list.")
        except ValueError:
            print("  Invalid input.")

    try:
        user = User(
            gender=gender_val,
            age=age,
            weight=weight,
            height=height,
            activity=activity_val,
            diet_type=diet_type,
            lifestyle=lifestyle,
            target=target_val
        )
        print("\n✅  Profile saved successfully.")
        return user
    except ValueError as e:
        print(f"\n❌  Error: {e}")
        return collect_user_data()


def show_bmi(user: User):
    divider()
    print("📊  BMI CALCULATOR")
    bmi = calculate_bmi(user)
    interpretation = interpret_bmi(bmi)
    print(f"\n  Your BMI:       {bmi:.2f}")
    print(f"  Interpretation: {interpretation}")


def show_bmr_tdee(user: User):
    divider()
    print("🔥  BMR / TDEE CALCULATOR")
    bmr = calculate_bmr(user)
    tdee = calculate_tdee(user)
    print(f"\n  Basal Metabolic Rate (BMR):            {bmr:.2f} kcal")
    print(f"  Total Daily Energy Expenditure (TDEE): {tdee:.2f} kcal")


def show_diet_planner(user: User):
    divider()
    print("🥑  DIET PLANNER")
    tdee = calculate_tdee(user)
    macro_res = macros(user, tdee)

    print(f"\n  Your energy requirement (TDEE): {int(tdee)} kcal")
    print("\n  Daily macronutrient requirements:")
    for k, v in macro_res.items():
        print(f"    {k}: {v} g")

    print(f"\n  💡 Tip: {minerals(user)}")

    show_recs = input("\n  Show recommended products? (y/n): ").strip().lower()
    if show_recs == "y":
        recs = recommendations(user)
        print()
        for k, v in recs.items():
            print(f"    {k}: {v}")


def show_file_handling(filename: str) -> str:
    divider()
    print("📁  RECIPE DATABASE")

    while True:
        print("\n  1. List all recipes")
        print("  2. Add a recipe")
        print("  3. Remove a recipe")
        print("  4. Back to main menu")

        choice = input("\nSelect: ").strip()

        if choice == "1":
            recipes = load_recipes_from_file(filename)
            if recipes:
                print(f"\n  Recipes in '{filename}':")
                for r in recipes:
                    print(f"    • {r}")
            else:
                print("  The list is currently empty.")

        elif choice == "2":
            slug = input("  Enter recipe name (from aniagotuje.pl URL): ").strip()
            try:
                result = add_recipe_to_file(slug, filename)
                if result == "SUCCESS":
                    print("  ✅  Recipe added successfully.")
                else:
                    print(f"  ⚠️   {result}")
            except Exception as e:
                print(f"  ❌  {e}")

        elif choice == "3":
            recipes = load_recipes_from_file(filename)
            if not recipes:
                print("  No recipes to remove.")
                continue
            print("\n  Recipes:")
            for i, r in enumerate(recipes, 1):
                print(f"    {i}. {r}")
            try:
                idx = int(input("  Select number to remove: ")) - 1
                if 0 <= idx < len(recipes):
                    remove_recipe_from_file(recipes[idx], filename)
                    print("  ✅  Recipe removed.")
                else:
                    print("  Invalid selection.")
            except ValueError:
                print("  Invalid input.")

        elif choice == "4":
            break

    return filename


def show_meal_planner(user: User, filename: str):
    divider()
    print("🍽️   INTERACTIVE DAY PLANNER")

    cookbook = create_cookbook(filename)
    if not cookbook:
        print("  No recipes available. Please add recipes in the Recipe Database section.")
        return

    num_meals = prompt_int("\nHow many meals to divide the day into? (2-10): ", 2, 10)

    tdee = calculate_tdee(user)
    macro_req = macros(user, tdee)

    remaining_goals = {
        'calories': tdee,
        'carbs': macro_req.get("Carbs (g)", 0),
        'protein': macro_req.get("Protein (g)", 0),
        'fat': macro_req.get("Fats (g)", 0),
        'sugar': 50.0
    }

    daily_plan = []
    temp_exclude = []
    meals_to_go = num_meals

    mapping_dict = {
        'calories': 'Kalorie (kcal)',
        'carbs': 'Węglowodany (g)',
        'protein': 'Białko (g)',
        'fat': 'Tłuszcze (g)',
        'sugar': 'Cukry (g)'
    }

    while meals_to_go > 0:
        divider()
        print(f"  Meals left to plan: {meals_to_go}")

        meal_target = {k: v / meals_to_go for k, v in remaining_goals.items()}
        exclusion_list = daily_plan + temp_exclude

        suggested = find_best_match(cookbook, user, goals=meal_target, exclude=exclusion_list)

        if not suggested:
            print("  No matching recipe found. Try adjusting your diet settings.")
            break

        print(f"\n  🍴  Meal suggestion #{len(daily_plan) + 1}: {suggested.title}")
        print(f"  Cooking time: {suggested.cooking_time} min")
        print(f"  Ingredients:  {', '.join(suggested.ingredients)}")
        print("  Macros (per 100g):")
        for k, v in suggested.macro.items():
            print(f"    {k}: {v}")

        print("\n  1. Accept")
        print("  2. Suggest another")
        print("  3. Reset plan")
        action = input("Select: ").strip()

        if action == "1":
            daily_plan.append(suggested)
            portion_multiplier = 3.0
            for internal_key, recipe_key in mapping_dict.items():
                macro_value = float(suggested.macro.get(recipe_key, 0)) * portion_multiplier
                remaining_goals[internal_key] -= macro_value
            temp_exclude = []
            meals_to_go -= 1

        elif action == "2":
            temp_exclude.append(suggested)

        elif action == "3":
            print("  Plan reset.")
            daily_plan = []
            temp_exclude = []
            remaining_goals = {
                'calories': tdee,
                'carbs': macro_req.get("Carbs (g)", 0),
                'protein': macro_req.get("Protein (g)", 0),
                'fat': macro_req.get("Fats (g)", 0),
                'sugar': 50.0
            }
            meals_to_go = num_meals

    if daily_plan:
        divider()
        print("✅  Your plan for today:")
        for idx, meal in enumerate(daily_plan, 1):
            print(f"  {idx}. {meal.title}")


def main():
    print("=" * 50)
    print("       🌱  HEALTHY NUTRITION ASSISTANT")
    print("=" * 50)
    print("Welcome to the comprehensive dietary support system.")

    user = None
    filename = "recipes.csv"

    while True:
        divider()
        print("MAIN MENU")
        print("  1. Data Input")
        print("  2. BMI Calculator")
        print("  3. BMR / TDEE Calculator")
        print("  4. Diet Planner")
        print("  5. Recipe Database")
        print("  6. Meal Planner")
        print("  7. Exit")

        choice = input("\nSelect: ").strip()

        if choice == "1":
            user = collect_user_data()

        elif choice in ("2", "3", "4", "6"):
            if user is None:
                print("\n  ⚠️   Please complete Data Input (option 1) first.")
                continue
            if choice == "2":
                show_bmi(user)
            elif choice == "3":
                show_bmr_tdee(user)
            elif choice == "4":
                show_diet_planner(user)
            elif choice == "6":
                show_meal_planner(user, filename)

        elif choice == "5":
            filename = show_file_handling(filename)

        elif choice == "7":
            print("\nGoodbye! 👋")
            break

        else:
            print("  Invalid choice — please enter a number from 1 to 7.")


if __name__ == "__main__":
    main()
