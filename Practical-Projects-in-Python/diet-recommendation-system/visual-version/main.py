from ..classes.input_handling import *
from tabs.input_tab import *
from tabs.bmi_tab import *
from tabs.bmr_tdee_tab import *
from tabs.macros_tab import *
from tabs.file_handling_tab import *
from tabs.meal_recommendations_tab import *


@st.cache_data
def load_cookbook_cached(filename):
    return create_cookbook(filename)


if __name__ == "__main__":
    st.title("🌱 Healthy Nutrition Assistant")  # application title
    st.write("Welcome to the comprehensive dietary support system.")  # subtitle/first message for the user

    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'filename' not in st.session_state:
        st.session_state.filename = "recipes.csv"

    # Define common tabs for all functionalities
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Data Input", "BMI Calculator",
                                                  "BMR/TDEE Calculator", "Diet Planner",
                                                  "File Handling", "Meal Recommendations"])

    with tab1:
        st.header("Data Input")  # sets the header
        col_z1, col_z2 = st.columns(2)  # divides the screen into columns

        # content of the 1st column (dropdown for gender, numeric fields for age, height, and weight)
        with col_z1:
            gender_val, age_z, height_z, weight_z = st_input_col1()

        # content of the 2nd column (dictionary with activity options and their math formula values, target selection)
        with col_z2:
            activity_val, target_val, lifestyle = st_input_col2()

        # diet types selection list (updated to match English backend logic)
        diet_type = st.multiselect("Diet type", ["gluten-free", "vegetarian",
                                                 "vegan", "standard"], key="z_restr")

        if st.button("Submit entered data", type="primary", key="btn_zuzia"):  # button triggering the code
            try:
                # creating a User class object
                st.session_state.user = User(
                    gender=gender_val,
                    age=int(age_z),
                    weight=weight_z,
                    height=int(height_z),
                    activity=activity_val,
                    diet_type=diet_type,
                    lifestyle=lifestyle,
                    target=target_val
                )  # passing data to the class, checking for errors

            except ValueError as e:
                st.error(f"Data error: {e}")

    with tab2:
        st.header("BMI Calculator")

        if st.session_state.user is not None:
            user = st.session_state.user

            if st.button("Calculate my BMI"):  # creating a button to trigger the next part of the code
                bmi = calculate_bmi(user)

                st.metric(label="Your BMI is", value=f"{bmi:.2f}")
                interpret_bmi(bmi)
        else:
            # This message will only appear if the user hasn't submitted data in tab1
            st.info("First, fill in and submit the data in the 'Data Input' tab")

    with tab3:
        st.header("BMR/TDEE Calculator")

        if st.session_state.user is not None:
            user = st.session_state.user

            if st.button("Calculate BMR and TDEE"):
                bmr_val = calculate_bmr_simple(user)
                tdee_val = calculate_tdee(user)

                st.divider()
                col_res1, col_res2 = st.columns(2)
                col_res1.metric("Basal Metabolic Rate (BMR):", f"{bmr_val:.2f} kcal")
                col_res2.metric("Total Daily Energy Expenditure (TDEE):", f"{tdee_val:.2f} kcal")
        else:
            # This message will only appear if the user hasn't submitted data in tab1
            st.info("First, fill in and submit the data in the 'Data Input' tab")

    with tab4:
        st.header("Diet Planner")

        if st.session_state.user is not None:
            user = st.session_state.user

            if st.button("Diet Planner"):
                tdee_val = calculate_tdee(user)  # calls the tdee calculator function from the User class

                st.markdown("---")  # line separating the form from the results
                st.success(f"🥑 Your energy requirement (TDEE): **{int(tdee_val)} kcal**")  # displays the result

                st.write("Your daily macronutrient requirement:")
                macros_res = macros(user, tdee_val)  # triggers the macros method from the class
                c1, c2, c3 = st.columns(3)  # divides the screen into 3 columns, displaying macro results

                # Matches the English dictionary keys established in the macros() function
                c1.metric("Protein", f"{macros_res['Protein (g)']} g")
                c2.metric("Fats", f"{macros_res['Fats (g)']} g")
                c3.metric("Carbs", f"{macros_res['Carbs (g)']} g")

                st.info(f"💡 Tip: {minerals(user)}")  # displays advice regarding microelements

                with st.expander("See recommended products"):  # creates a dropdown list of recommendations
                    recs_res = recommendations(user)  # fetches the list of recommended products from the class
                    for k, v in recs_res.items():  # loop iterating through the recommendations dictionary
                        st.write(f"**{k}:** {v}")  # prints variables in text (** - bold)
        else:
            # This message will only appear if the user hasn't submitted data in tab1
            st.info("First, fill in and submit the data in the 'Data Input' tab")

    with tab5:
        st.header("File Handling")

        # Handles the file name input through a Streamlit form
        with st.form("file_settings"):
            temp_filename = st.text_input(
                "Enter the name of the CSV file with recipes:",
                value=st.session_state.get('filename', ''),
                help="Enter the name and press Enter or the button below"
            )
            submit_file = st.form_submit_button("Submit file")

        if submit_file:
            # Updates the session state with the provided filename
            st.session_state.filename = temp_filename

        # Manages the logic for loading the cookbook if the filename is valid
        if 'filename' in st.session_state and st.session_state.filename:
            current_file = st.session_state.filename

            # Checks if the cookbook needs to be reloaded from the disk
            if 'cookbook' not in st.session_state or st.session_state.get('last_loaded_file') != current_file:
                with st.spinner(f"Loading recipes from file {current_file}..."):
                    # Populates the cookbook object and updates the tracking variable
                    st.session_state.cookbook = create_cookbook(current_file)
                    st.session_state.last_loaded_file = current_file

            cookbook_data = st.session_state.cookbook
        else:
            st.warning("Please submit the file name to continue.")

        st.subheader("Add a new recipe")
        recipe_to_add = st.text_input("Enter the recipe name (from URL):", key="add_input")

        if st.button("Submit addition"):
            # Triggers the scraping and adding process for a new recipe
            add_recipe_st_version(recipe_to_add, current_file)

        st.subheader("Remove a recipe")
        recipe_slugs = load_recipes_from_file(current_file)

        if recipe_slugs:
            slug_to_remove = st.selectbox("Select a recipe to delete:", options=recipe_slugs)

            if st.button("Confirm removal"):
                # Deletes the specified recipe and reloads the application state
                remove_recipe_from_file(slug_to_remove, current_file)
                st.success(f"Removed: {slug_to_remove}")
                st.rerun()
        else:
            st.info("No recipes in the database to remove.")

        st.subheader("Your recipe list")
        all_slugs = load_recipes_from_file(current_file)

        if all_slugs:
            for slug in all_slugs:
                st.write(f"• {slug}")
        else:
            st.write("The list is currently empty.")

    with tab6:
        st.header("Interactive Day Planner")

        if st.session_state.user is not None:
            current_user = st.session_state.user

            # Verifies if daily plan variables exist in session state, otherwise initializes them
            if 'daily_plan' not in st.session_state:
                st.session_state.daily_plan = []
                st.session_state.temp_exclude = []
                st.session_state.remaining_goals = None
                st.session_state.meals_to_go = 0

            # Renders the initial configuration form for the daily plan
            if st.session_state.meals_to_go == 0:
                num_meals = st.number_input("How many meals to divide the day into?", 2, 10, 3)
                if st.button("Start planning the day"):
                    tdee_value = calculate_tdee(current_user)
                    macro_requirements = macros(current_user, tdee_value)

                    # Establishes the starting nutritional budget based on user data
                    # Uses the updated English keys from the macros() function
                    st.session_state.remaining_goals = {
                        'calories': tdee_value,
                        'carbs': macro_requirements.get("Carbs (g)", 0),
                        'protein': macro_requirements.get("Protein (g)", 0),
                        'fat': macro_requirements.get("Fats (g)", 0),
                        'sugar': macro_requirements.get("Sugar (g)", 50)  # Assuming a 50g baseline
                    }
                    st.session_state.meals_to_go = num_meals
                    st.session_state.daily_plan = []
                    st.rerun()

            # Handles the active meal selection process
            if st.session_state.meals_to_go > 0:
                st.write(f"Meals left to plan: {st.session_state.meals_to_go}")

                # Calculates requirements for the current specific meal slot
                meal_target = {
                    k: v / st.session_state.meals_to_go
                    for k, v in st.session_state.remaining_goals.items()
                }

                # Merges confirmed recipes and temporary skips for the exclusion filter
                exclusion_list = st.session_state.daily_plan + st.session_state.get('temp_exclude', [])

                # Invokes the matching algorithm to suggest the best recipe
                suggested_recipe = find_best_match(
                    st.session_state.cookbook,
                    current_user,
                    goals=meal_target,
                    exclude=exclusion_list
                )

                if suggested_recipe:
                    st.subheader(f"Meal suggestion #{len(st.session_state.daily_plan) + 1}")

                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.markdown(f"### {suggested_recipe.title}")
                        st.write(f"Time: {suggested_recipe.cooking_time} min")
                        st.write("Ingredients:", ", ".join(suggested_recipe.ingredients))
                    with col2:
                        st.write("**Macros (per 100g):**")
                        st.json(suggested_recipe.macro)

                    btn_col1, btn_col2, btn_col3 = st.columns(3)

                    if btn_col1.button("Accept", type="primary", use_container_width=True):
                        # Adds the chosen recipe to the daily plan and updates balance
                        st.session_state.daily_plan.append(suggested_recipe)

                        portion_multiplier = 3.0

                        # Maps your internal keys to the Polish keys used by the web scraper.
                        # These values must stay in Polish to accurately pull from recipe.macro dictionary!
                        mapping_dict = {
                            'calories': 'Kalorie (kcal)',
                            'carbs': 'Węglowodany (g)',
                            'protein': 'Białko (g)',
                            'fat': 'Tłuszcze (g)',
                            'sugar': 'Cukry (g)'
                        }

                        for internal_key, recipe_key in mapping_dict.items():
                            macro_value = float(suggested_recipe.macro.get(recipe_key, 0)) * portion_multiplier
                            # Subtracts the consumed nutrients from the remaining daily allowance
                            st.session_state.remaining_goals[internal_key] -= macro_value

                        st.session_state.temp_exclude = []
                        st.session_state.meals_to_go -= 1
                        st.rerun()

                    if btn_col2.button("Suggest another", use_container_width=True):
                        # Temporarily hides the current recipe from further suggestions
                        st.session_state.temp_exclude.append(suggested_recipe)
                        st.rerun()

                    if btn_col3.button("Reset plan", use_container_width=True):
                        # Clears all progress and returns to the initial state
                        st.session_state.meals_to_go = 0
                        st.session_state.daily_plan = []
                        st.session_state.temp_exclude = []
                        st.rerun()

            # Displays the final summary once all meals are planned
            if st.session_state.meals_to_go == 0 and len(st.session_state.daily_plan) > 0:
                st.success("Your plan for today is ready!")
                for idx, meal in enumerate(st.session_state.daily_plan, 1):
                    st.write(f"{idx}. {meal.title}")

                if st.button("Plan a new day"):
                    st.session_state.daily_plan = []
                    st.rerun()

        else:
            st.info("First, fill in and submit the data in the 'Data Input' tab")