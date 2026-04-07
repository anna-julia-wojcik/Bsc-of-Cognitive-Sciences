import os
import csv
import streamlit as st

from ..classes.aniagotuje_scraping import *


def load_recipes_from_file(filename="recipes.csv") -> list:
    """
    Loads recipe list from the CSV file. If the file doesn't exist, returns an empty list.

    Args:
        filename: name of the file with recipes, by default it should be 'recipes.csv' (pre-made recipe list)

    Returns:
        list:  list of all the recipes that the file contains
    """
    recipes = []

    # Checks if the path to a file exists, if not - then returns an empty list
    if not os.path.exists(filename):
        return recipes

    try:
        with open(filename, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                # Checks if a line in the file is not empty
                if row:
                    # Gets the first value in the row and adds it to the list
                    recipes.append(row[0].strip())
    except Exception as e:
        print(f"Unexpected error while loading the file: {e}")

    return recipes


def add_recipe_to_file(recipe_url_name: str, filename='recipes.csv') -> str | None:
    """
    Adds recipe to the CSV file. If the file doesn't exist, returns an empty list.

    Args:
        recipe_url_name: name of the recipe taken from aniagotuje url, that user tries to add to the file
        filename: name of the file with recipes, by default it should be 'recipes.csv' (pre-made recipe list)

    Returns:
        str | None: function returns a string message if the recipe already is in the file, or "SUCCESS",
                or raises an error
    """
    recipe_url_name = recipe_url_name.strip().lower()

    # Checks if the user's recipe already exists in the csv file
    if recipe_url_name in load_recipes_from_file(filename):
        print(f"Entry '{recipe_url_name}' already exists in the file.")
        return "Recipe already exists in the database"

    try:
        # If create_soup() raises an error, recipe won't be added to the csv file
        soup = create_soup(recipe_url_name)

        # Appends recipe name to the csv file
        with open(filename, 'a', encoding='utf-8', newline='') as f:
            csv.writer(f).writerow([recipe_url_name])

        return "SUCCESS"

    # Handles the errors raised by create_soup()
    except requests.exceptions.HTTPError:
        raise Exception("Error: The page for your recipe does not exist.")
    except requests.exceptions.ConnectionError:
        raise Exception("Error: Internet connection problem.")
    except Exception as e:
        raise Exception(f"Unexpected error: {e}")


def remove_recipe_from_file(recipe_url_name: str, filename='recipes.csv') -> None:
    """
    Removes recipe from the CSV file. If the file doesn't exist, returns an empty list.

    Args:
        recipe_url_name: name of the recipe taken from aniagotuje url, that user tries to remove from the file
        filename: name of the file with recipes, by default it should be 'recipes.csv' (pre-made recipe list)

    Returns:
        None: function doesn't return a value, but it prints out a success message or an error message
    """
    recipe_url_name = recipe_url_name.strip().lower()
    recipes = load_recipes_from_file(filename)

    if recipe_url_name in recipes:
        soup = create_soup(recipe_url_name)
        title = get_recipe_title(soup)

        # Removes the user's recipe from the recipe list
        recipes.remove(recipe_url_name)
        # Clears the file and writes down modificated recipe list (there's no an easier way to do this)
        with open(filename, "w", encoding="utf-8", newline='') as f:
            writer = csv.writer(f)
            for recipe in recipes:
                writer.writerow([recipe])

        print(f"Removed {title}")
    else:
        print(f"Not found: {recipe_url_name}")


def add_recipe_st_version(new_recipe_name: str, file: str) -> None:
    """
    Adds a recipe to the file and handles the Streamlit user interface updates.

    Args:
        new_recipe_name: name of the recipe taken from aniagotuje url, that user tries to add to the file
        file: name of the file with recipes (e.g., 'recipes.csv')

    Returns:
        None: function doesn't return a value, but it displays a success, warning, or error message in the Streamlit app and reruns it upon success
    """
    if new_recipe_name:
        try:
            # Try to add the recipe
            result = add_recipe_to_file(new_recipe_name, file)

            if result == "SUCCESS":
                st.success("Recipe added successfully!")
                st.rerun()  # Refresh the list only on success
            else:
                # This handles the case when the recipe already exists
                st.warning(result)

        except Exception as e:
            # Here Streamlit will display the error from AniaGotuje in red
            st.error(str(e))
    else:
        st.error("Please enter a recipe name!")