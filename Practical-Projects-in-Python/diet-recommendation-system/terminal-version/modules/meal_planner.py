from classes.aniagotuje_scraping import get_recipe
from modules.file_handling import load_recipes_from_file


def create_cookbook(filename: str = "recipes.csv") -> list:
    recipe_slugs = load_recipes_from_file(filename)
    all_recipes = []

    if not recipe_slugs:
        return all_recipes

    print(f"Loading {len(recipe_slugs)} recipes...")
    for slug in recipe_slugs:
        try:
            recipe_obj = get_recipe(slug)
            all_recipes.append(recipe_obj)
        except Exception as e:
            print(f"Skipped '{slug}': download error ({e})")

    print(f"Loaded {len(all_recipes)} recipes successfully.")
    return all_recipes


def find_best_match(cookbook: list, user, goals: dict, exclude: list = None, multiplier: float = 3.0):
    best_recipe = None
    min_score = float('inf')
    exclude = exclude or []

    mapping = {
        'calories': 'Kalorie (kcal)',
        'protein': 'Białko (g)',
        'fat': 'Tłuszcze (g)',
        'carbs': 'Węglowodany (g)',
        'sugar': 'Cukry (g)'
    }

    weights = {
        'Kalorie (kcal)': 0.1,
        'Węglowodany (g)': 1.0,
        'Białko (g)': 2.0,
        'Tłuszcze (g)': 1.0
    }

    user_diets = [d.lower() for d in (user.diet_type if isinstance(user.diet_type, list) else [user.diet_type])]

    for recipe in cookbook:
        if recipe in exclude:
            continue

        if 'standard' not in user_diets:
            recipe_tags = [d.lower() for d in getattr(recipe, 'diet', [])]
            if not any(diet in recipe_tags for diet in user_diets):
                continue

        score = 0
        found_any_macro = False

        for goal_key, goal_val in goals.items():
            recipe_key = goal_key if goal_key in recipe.macro else mapping.get(goal_key)
            if recipe_key and recipe_key in recipe.macro:
                found_any_macro = True
                actual_val = float(recipe.macro.get(recipe_key, 0)) * multiplier
                w = weights.get(recipe_key, 1.0)
                diff = float(goal_val) - actual_val
                score += (diff ** 2) * w

        if found_any_macro and score < min_score:
            min_score = score
            best_recipe = recipe

    return best_recipe
