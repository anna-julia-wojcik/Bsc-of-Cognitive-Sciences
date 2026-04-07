import requests
from bs4 import BeautifulSoup


class recipe:
    def __init__(self, title: str, macro: dict, cooking_time: float, number_of_portions: str, diet: list[str],
                 ingredients: list[str]):
        self.title = title
        self.macro = macro
        self.cooking_time = cooking_time
        self.number_of_portions = str(number_of_portions)
        self.diet = diet
        self.ingredients = ingredients

    def __repr__(self) -> str:
        return (f"{self.title}:\nMacro: {self.macro}\nCooking time: {self.cooking_time} min\n"
                f"Portions: {self.number_of_portions}\nDiet: {', '.join(self.diet)}\n"
                f"Ingredients: {', '.join(self.ingredients)}")

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.__dict__ == other.__dict__


def create_soup(recipe_name: str) -> BeautifulSoup:
    aniagotuje_url = "https://aniagotuje.pl/przepis/"
    response = requests.get(aniagotuje_url + recipe_name)
    response.raise_for_status()
    return BeautifulSoup(response.content, 'html.parser')


def get_recipe_info(soup: BeautifulSoup) -> tuple | str:
    recipe_info = soup.find('p', class_='recipe-info')
    if not recipe_info:
        return "Recipe info not found"

    full_text = recipe_info.get_text(" ", strip=True)

    results = {
        "portions": "Not provided",
        "diet": [],
        "cooking_time": 0,
        "macros": {}
    }

    if "Czas przygotowania:" in full_text:
        time_raw = full_text.split("Czas przygotowania:")[1].split("Liczba porcji:")[0].strip()
        parts = time_raw.split()
        if parts[0].isdigit():
            val = int(parts[0])
            results["cooking_time"] = val * 60 if "godz" in time_raw else val

    if "Liczba porcji:" in full_text:
        results["portions"] = full_text.split("Liczba porcji:")[1].split("W 100")[0].strip()

    if "Dieta:" in full_text:
        diet_val = full_text.split("Dieta:")[1].strip()
        results["diet"] = [d.strip().lower() for d in diet_val.split(',') if d.strip()] if diet_val else ["standardowa"]
    else:
        results["diet"] = ["standardowa"]

    macro_map = {
        'calories': 'Kalorie (kcal)',
        'carbohydrateContent': 'Węglowodany (g)',
        'sugarContent': 'Cukry (g)',
        'proteinContent': 'Białko (g)',
        'fatContent': 'Tłuszcze (g)'
    }

    for item_prop, label in macro_map.items():
        element = soup.find(attrs={"itemprop": item_prop})
        if element:
            raw_text = element.get_text(strip=True)
            parts = raw_text.split(" ")
            if parts:
                first_part = parts[0].replace(",", ".")
                try:
                    results["macros"][label] = float(first_part)
                except ValueError:
                    results["macros"][label] = 0

    return results["portions"], results["diet"], results["cooking_time"], results["macros"]


def get_recipe_ingredients(soup: BeautifulSoup) -> str | list[str]:
    items = soup.find_all(attrs={"itemprop": "recipeIngredient"})
    if not items:
        return "Ingredients not found"
    return [item.get_text(" ", strip=True) for item in items]


def get_recipe_title(soup: BeautifulSoup) -> str | None:
    title_tag = soup.find('h1', attrs={'itemprop': 'name'})
    if not title_tag:
        title_tag = soup.find('h1')
        if not title_tag:
            return "Title not found"
    return title_tag.get_text(strip=True)


def get_recipe(recipe_name: str) -> recipe:
    soup = create_soup(recipe_name)
    number_of_portions, diet, cooking_time, macro = get_recipe_info(soup)
    ingredients = get_recipe_ingredients(soup)
    title = get_recipe_title(soup)
    return recipe(title, macro, cooking_time, number_of_portions, diet, ingredients)
