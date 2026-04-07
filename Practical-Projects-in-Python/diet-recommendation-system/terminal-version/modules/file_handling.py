import os
import csv
import requests
from classes.aniagotuje_scraping import create_soup


def load_recipes_from_file(filename: str = "recipes.csv") -> list:
    recipes = []
    if not os.path.exists(filename):
        return recipes
    try:
        with open(filename, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    recipes.append(row[0].strip())
    except Exception as e:
        print(f"Unexpected error while loading the file: {e}")
    return recipes


def add_recipe_to_file(recipe_url_name: str, filename: str = "recipes.csv") -> str:
    recipe_url_name = recipe_url_name.strip().lower()

    if recipe_url_name in load_recipes_from_file(filename):
        return "Recipe already exists in the database"

    try:
        create_soup(recipe_url_name)
        with open(filename, 'a', encoding='utf-8', newline='') as f:
            csv.writer(f).writerow([recipe_url_name])
        return "SUCCESS"
    except requests.exceptions.HTTPError:
        raise Exception("Error: The page for your recipe does not exist.")
    except requests.exceptions.ConnectionError:
        raise Exception("Error: Internet connection problem.")
    except Exception as e:
        raise Exception(f"Unexpected error: {e}")


def remove_recipe_from_file(recipe_url_name: str, filename: str = "recipes.csv") -> None:
    recipe_url_name = recipe_url_name.strip().lower()
    recipes = load_recipes_from_file(filename)

    if recipe_url_name not in recipes:
        print(f"Not found: {recipe_url_name}")
        return

    recipes.remove(recipe_url_name)
    with open(filename, "w", encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        for recipe in recipes:
            writer.writerow([recipe])
    print(f"Removed: {recipe_url_name}")
