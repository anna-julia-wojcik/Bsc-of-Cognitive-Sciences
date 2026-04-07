# Diet System Recommendation: Terminal Version

The project is an interactive command-line application for personalized dietary support. It takes user biometric and lifestyle data through step-by-step prompts, calculates BMI, BMR, and TDEE, generates macronutrient and micronutrient recommendations, and provides an interactive daily meal planner. Recipes are sourced in real time by scraping the [aniagotuje.pl](https://aniagotuje.pl) website, and users can manage their personal recipe database through a CSV file.

## My Contribution

My specific responsibility covered the scraping backend and the meal recommendation system. I implemented `aniagotuje_scraping.py` in full — the `recipe` class, `create_soup`, `get_recipe_info`, `get_recipe_ingredients`, `get_recipe_title`, and `get_recipe` — as well as `meal_planner.py`, including `create_cookbook` and `find_best_match` (the weighted least-squares recipe matching algorithm). I also made the `file_handling.py`, `main.py` and `__init__.py` files. I also refractored all the code to make it terminal-friendly in this version.

## Project Stages

- Collecting user biometric and lifestyle data through interactive terminal prompts (gender, age, height, weight, activity level, dietary preferences, and goal).
- Calculating BMI, BMR, and TDEE based on the submitted profile using standard nutritional formulas.
- Generating personalized macronutrient targets (protein, fats, carbohydrates) and micronutrient tips tailored to the user's goal and dietary restrictions.
- Managing a personal recipe database stored in a CSV file — listing, adding, and removing recipes sourced from aniagotuje.pl.
- Scraping recipe data (title, macros, ingredients, cooking time, diet tags) in real time from aniagotuje.pl based on URL slugs.
- Running an interactive daily meal planner that splits the user's nutritional budget across a chosen number of meals and suggests the best-matching recipe for each slot using a weighted least-squares algorithm.

## Installation and Requirements

The project requires Python ≥ 3.10. Install all dependencies with:

```bash
pip install -r requirements.txt
```

## Running the App

```bash
python main.py
```

The app opens with a numbered main menu. Start with option **1 (Data Input)** — all other sections except Recipe Database require a submitted user profile to function.

```
MAIN MENU
  1. Data Input
  2. BMI Calculator
  3. BMR / TDEE Calculator
  4. Diet Planner
  5. Recipe Database
  6. Meal Planner
  7. Exit
```

---

# Module Descriptions

## `classes/input_handling.py` — User Data Model

### Class: `User`

Stores and validates all user biometric and lifestyle data. Every attribute is protected by a property setter that raises a `ValueError` on invalid input.

| Attribute | Type | Validation |
|---|---|---|
| `gender` | `str` | Must be `"m"` or `"f"` |
| `age` | `int` | 1–120 |
| `weight` | `float` | 0–600 kg |
| `height` | `int` | 50–300 cm |
| `activity` | `float` | Numeric multiplier (set from prompt) |
| `diet_type` | `list[str]` | Lowercased list of dietary tags |
| `lifestyle` | `str` | Office / Physical / Mixed |
| `target` | `str` | `"lose"`, `"gain"`, or `"maintain"` |

---

## `classes/aniagotuje_scraping.py` — Web Scraper

Scrapes recipe data from `https://aniagotuje.pl/przepis/<slug>`.

### Class: `recipe`
Stores a single recipe's data: `title`, `macro` (dict), `cooking_time`, `number_of_portions`, `diet` (list), `ingredients` (list). Implements `__eq__` for identity comparison used by the meal planner's exclusion logic.

### Functions:

**`create_soup(recipe_name)`**
Sends an HTTP GET request to aniagotuje.pl and returns a parsed `BeautifulSoup` object. Raises `HTTPError` if the recipe page does not exist.

**`get_recipe_info(soup)`**
Extracts portions, diet type, cooking time, and macronutrients from the parsed page using Schema.org `itemprop` attributes. Returns a tuple `(portions, diet, cooking_time, macros)`. Handles comma-decimal formatting and hour-to-minute conversion for cooking time.

**`get_recipe_ingredients(soup)`**
Extracts the full ingredients list using `itemprop="recipeIngredient"` tags.

**`get_recipe_title(soup)`**
Extracts the recipe title from the `h1` tag with `itemprop="name"`, falling back to a generic `h1` if needed.

**`get_recipe(recipe_name)`**
Orchestrates the full scraping pipeline and returns a populated `recipe` object.

---

## `modules/bmi.py` — BMI Calculator

**`calculate_bmi(user)`**
Computes BMI as `weight / (height_m)²`.

**`interpret_bmi(bmi)`**
Maps the result to one of eight categories from severe thinness to obesity class III and returns the interpretation as a string.

---

## `modules/bmr_tdee.py` — BMR and TDEE Calculator

**`calculate_bmr(user)`**
Applies the Mifflin–St Jeor formula, branching on gender.

**`calculate_tdee(user)`**
Multiplies BMR by the user's activity level multiplier.

---

## `modules/macros.py` — Diet Planner

**`macros(user, tdee_value)`**
Calculates daily protein, fat, and carbohydrate targets in grams based on calorie ratios that vary by goal (`lose` / `gain` / `maintain`). Returns a dict with keys `"Protein (g)"`, `"Fats (g)"`, `"Carbs (g)"`.

**`minerals(user)`**
Returns a string tip about micronutrients to monitor, tailored to the user's target.

**`recommendations(user)`**
Returns a dict of recommended food sources for protein, fats, and carbs. Filters out incompatible items based on `diet_type` (vegan, vegetarian, gluten-free).

---

## `modules/file_handling.py` — Recipe Database Management

Manages the CSV file that stores recipe slugs (URL identifiers from aniagotuje.pl).

**`load_recipes_from_file(filename)`**
Reads the CSV line by line and returns a list of slug strings. Returns an empty list if the file does not exist.

**`add_recipe_to_file(recipe_url_name, filename)`**
Validates uniqueness, calls `create_soup` to confirm the recipe page exists, then appends the slug to the CSV. Returns `"SUCCESS"` or raises a descriptive exception.

**`remove_recipe_from_file(recipe_url_name, filename)`**
Removes the slug from the in-memory list and rewrites the full CSV file.

---

## `modules/meal_planner.py` — Meal Planner

**`create_cookbook(filename)`**
Reads all slugs from the CSV file, calls `get_recipe` for each one, and returns a list of `recipe` objects. Skips slugs that fail to download without stopping the whole process.

**`find_best_match(cookbook, user, goals, exclude, multiplier)`**
Finds the recipe that best satisfies the user's current meal-slot nutritional goals using a weighted squared-error score. Filters by diet type compatibility, skips recipes in the `exclude` list, scales 100g macro values to a portion (default 300g via `multiplier=3.0`), and prioritizes protein matches through a higher weight coefficient. Returns the `recipe` object with the lowest score, or `None` if no valid match is found.

---

## `main.py` — Entry Point

Defines all terminal UI functions and the main menu loop. Input validation is handled by three helper functions — `prompt_int`, `prompt_float`, and `prompt_choice` — which re-prompt on invalid input rather than crashing. The meal planner loop works identically to the Streamlit version: the user specifies the number of meals, the app calculates a starting nutritional budget from TDEE and macros, and for each meal slot it suggests a recipe and lets the user accept, skip (suggest another), or reset the full plan.

---

## `recipes.csv`

A plain-text CSV file containing one aniagotuje.pl recipe slug per line (e.g. `zupa-dyniowa-z-curry`). This file serves as the default recipe database and can be extended or modified through option **5 (Recipe Database)** in the main menu.
