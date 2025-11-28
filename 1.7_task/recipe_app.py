import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, or_
from sqlalchemy.orm import sessionmaker, declarative_base

# load paramaters from .env
load_dotenv()
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST', 'localhost')
db_name = os.getenv('DB_NAME')

engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}')

Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

class Recipe(Base):
    __tablename__ = 'final_recipes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    def __repr__(self):
        return f'<Recipe ID: {self.id} - {self.name}, Difficulty: {self.difficulty}>'

    def __str__(self):
        border = '=' * 50
        label_width = 15

        return(
            f'{border}\n'
            f"{'Recipe ID:':<{label_width}} {self.id}\n"
            f"{'Recipe:':<{label_width}} {self.name}\n"
            f"{'Cooking Time:':<{label_width}} {self.cooking_time} minutes\n"
            f"{'Difficulty:':<{label_width}} {self.difficulty}\n"
            f"{'Ingredients:':<{label_width}} {self.ingredients}"
        )

    def calculate_difficulty(self):
        num_ingredients = len(self.return_ingredients_as_list())

        if self.cooking_time < 10 and num_ingredients <4:
            self.difficulty = 'Easy'
        elif self.cooking_time < 10 and num_ingredients >= 4:
            self.difficulty = 'Medium'
        elif self.cooking_time >= 10 and num_ingredients < 4:
            self.difficulty = 'Intermediate'
        else:
            self.difficulty = 'Hard'
        
    def return_ingredients_as_list(self):
        if not self.ingredients:
            return []
        return [ingredient.strip() for ingredient in self.ingredients.split(',') if ingredient.strip()]

Base.metadata.create_all(engine)

def get_name():
    while True:
        name = input('\nEnter the name of the recipe (50 characters max): ').strip()
        if not name:
            print('Recipe name cannot be empty, please try again.')
            continue
        elif len(name) > 50:
            print('Recipe name cannot exceed 50 characters.')
            continue
        else:
            return name

def get_cooking_time():
    while True:
        cooking_time = input ('Enter cooking time in minutes: ').strip()
        if not cooking_time.isnumeric():
            print('Cooking time must be a number, please try again.')
            continue
        
        cooking_time = int(cooking_time)
        if cooking_time == 0:
            print('Cooking time cannot be 0, please try again.')
            continue
        else:
            return cooking_time

def get_ingredients():
    while True:
        try:
            ingredient_num = int(input('How many ingredients does your recipe need: ').strip())
            if ingredient_num <= 0:
                print('Number of ingredients must be a positive number, please try again.')
                continue
        except ValueError:
            print('Please try again and enter a numerical character.')
            continue
        
        ingredients = []

        for i in range(ingredient_num):
            while True:
                ingredient = input(f'Enter ingredient number {i + 1}: ').strip()
                if not ingredient:
                    print('Ingredients can not be empty, please try again.')

                elif ',' in ingredient:
                    print('Please only enter a single ingredient as a time.')
                    continue
                else:
                    ingredient = ' '.join(ingredient.split()).lower().capitalize()
                    ingredients.append(ingredient)
                    break
        ingredients_str = ', '.join(ingredients)

        if len(ingredients_str) > 255:
            print('Unfortunately your list of ingredients exceeds the maximum number of characters (255). Please try again with a shorter ingredients list.')
            continue

        return ingredients_str

def create_recipe():
    name = get_name()
    cooking_time = get_cooking_time()
    ingredients = get_ingredients()

        
    recipe_entry = Recipe(
        name = name,
        ingredients = ingredients,
        cooking_time = cooking_time
    )
    recipe_entry.calculate_difficulty()
    
    try: 
        session.add(recipe_entry)
        session.commit()
        print(f'\nRecipe {name} added successfully!')
    except Exception as e:
        session.rollback()
        print(f'Error saving recipe: {e}')
        print('Please try again later\n')
        return None

def view_all_recipes():
    recipes_list = session.query(Recipe).all()
    if len(recipes_list) == 0:
        print('\n\t---- No recipes found ----')
        return None
    
    print('=' * 50)
    print('\t   --- All Recipes ----')
    for recipe in recipes_list:
        print(recipe.__str__())
    print('=' * 50)
    
def search_by_ingredients():
    if session.query(Recipe).count() == 0:
        print('\n\t---- No recipes found ----')
        return None
    
    results = session.query(Recipe.ingredients).all()

    all_ingredients_set = set()

    for i in results:
        all_ingredients_set.update(ing.strip().lower() for ing in i[0].split(','))

    all_ingredients = sorted(list(all_ingredients_set))

    print('\n---- List of Ingredients ----')
    print()
    for position, name in enumerate(all_ingredients, 1):
        print(f'{position}. {name.capitalize()}')

    while True:
        try:
            user_input = input('Enter the numbers of the ingredients you would like to search for, separated by spaces: ').split()
            if not user_input:
                print("Please try again and enter at least one ingredient number.")
                continue

            try:
                search_numbers = list(map(int, user_input))
            except ValueError:
                print('Please enter only numbers, no other character types.')
                continue

            for i in search_numbers:
                if i <= 0 or i > len(all_ingredients):
                    raise ValueError('Please pick a number from the list')
            break
        except ValueError as e:
            print(f'\n{e}')

    search_ingredients = []
    for i in search_numbers:
        search_ingredients.append(all_ingredients[i - 1])

    conditions = []

    for i in search_ingredients:
        conditions.append(Recipe.ingredients.like(f'%{i}%'))
    
    results = session.query(Recipe).filter(or_(*conditions)).all()
    print
    print(f'       ---- Recipes ----')
    for result in results:
        print(result.__str__())

def edit_recipe():
    if session.query(Recipe).count() == 0:
        print('\nNo recipes found! Please add one and try again.')
        return None
        
    results = session.query(Recipe.id, Recipe.name).all()
    recipe_ids = [recipe_id for recipe_id, _ in results]

    print('\nAvailable Recipes:')
    for recipe_id, recipe_name in results:
        print(f'{recipe_id}. {recipe_name}')

    while True:
        user_choice = input('Enter the number of the recipe you would like to edit: ').strip()
        try:
            chosen_id = int(user_choice)
        except ValueError:
            print('Please enter a number and not another type of character and try again')
            continue

        if chosen_id not in recipe_ids:
            print("Please enter a recipe number from the list.")
            continue
        break

    recipe_to_edit = session.query(Recipe).filter(Recipe.id == chosen_id).one()

    print(f'\n ---- Edit {recipe_to_edit.name} ----')
    print('-' * 50)
    print(f'1. Name: {recipe_to_edit.name}')
    print(f'2. Cooking Time: {recipe_to_edit.cooking_time}')
    print(f'3. Ingredients: {recipe_to_edit.ingredients}')
    print()

    while True:
        try:
            choice = int(input('Enter the number of the field you would like to edit, or enter 4 to cancel: '))
            if choice not in [1, 2, 3, 4]:
                print('Please enter one of the valid options from above, or 4 to cancel.')
                continue
            break
        except ValueError:
            print('Please enter a number and try again.')
            continue
    
    if choice == 1:
        new_name = get_name()
        recipe_to_edit.name = new_name

    elif choice == 2:
        new_cooking_time = get_cooking_time()
        recipe_to_edit.cooking_time = new_cooking_time

    elif choice == 3:
        new_ingredients = get_ingredients()
        recipe_to_edit.ingredients = new_ingredients

    elif choice == 4:
        print('Editing cancelled, returning to main menu.')
        return None

    if choice in (2, 3):
        recipe_to_edit.calculate_difficulty()

    try:
        session.commit()
        print('\nThe recipe has been updated successfully!\n')
        print(recipe_to_edit)
        print('=' * 50 + '\n')

    except Exception as e:
        session.rollback()
        print(f'Error updating the recipe: {e}')
        print('Changes not saved, please try again later.')

def delete_recipe():
    if session.query(Recipe).count() == 0:
        print('\nNo recipes found! Please add one and try again.')
        return None
    
    results = session.query(Recipe.id, Recipe.name).all()
    recipe_ids = [recipe_id for recipe_id, _ in results]

    print('\n Available Recipes:')
    for recipe_id, recipe_name in results:
        print(f'{recipe_id}. {recipe_name}')
    
    while True:
        user_choice = input('Enter the number of the recipe you would like to delete: ').strip()
        try:
            chosen_id = int(user_choice)
        except ValueError:
            print('Please enter a number and not another type of character and try again')
            continue

        if chosen_id not in recipe_ids:
            print("Please enter a recipe number from the list.")
            continue
        break

    recipe_to_delete = session.query(Recipe).filter(Recipe.id == chosen_id).one()

    while True:
        user_verification = input("Are you sure you want to delete this recipe? (y/n): ").strip().lower()
        if user_verification == 'y':
            try:
                session.delete(recipe_to_delete)
                session.commit()
                print('The recipe has been successfully deleted.')
                break
            except Exception as e:
                session.rollback()
                print(f'There was an error deleting the recipe: {e}')
                print('No changes have been saved, please try again later.')
                return None
        elif user_verification == 'n':
            session.rollback()
            print(f'The recipe {recipe_to_delete.name} has not been deleted.')
            return None
        else:
            print('Please enter either "y" or "n" to confirm if you would like the recipe to be deleted or not.')
            continue

def main_menu():
    choice = ''

    while choice != 'quit':
        print('\n       ---- Main Menu ----')
        print('=' * 50)
        print('What would you like to do: ')
        print("\n1. Create a new recipe")
        print("\n2. View all recipes")
        print("\n3. Search for a recipe by ingredient")
        print("\n4. Edit a recipe")
        print("\n5. Delete a recipe")
        print("\nType 'quit' to exit the program.")
        print('=' * 50)
    
        choice = input('\nEnter the number of your choice: ').strip().lower()
        if choice == "1":
            create_recipe()

        elif choice == "2":
            view_all_recipes()

        elif choice == "3":
            search_by_ingredients()

        elif choice == "4":
            edit_recipe()

        elif choice == "5":
            delete_recipe()

        elif choice != "quit":
            print("\nPlease select one of the options above, or type quite to exit")

        elif choice == "quit":
            print('Thank you for using the Recipe App. Goodbye!')
            session.close()
            engine.dispose()

main_menu()
