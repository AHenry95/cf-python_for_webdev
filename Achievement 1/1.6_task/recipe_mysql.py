import mysql.connector

conn = mysql.connector.connect(
    host = 'localhost',
    user = 'cf-python',
    password = 'password'
)

cursor = conn.cursor()

cursor.execute('CREATE DATABASE IF NOT EXISTS task_database')

cursor.execute('USE task_database')

cursor.execute('''CREATE TABLE IF NOT EXISTS recipes(
               id INT PRIMARY KEY AUTO_INCREMENT,
               name VARCHAR(50),
               ingredients VARCHAR(255),
               cooking_time INT,
               difficulty VARCHAR(20)
               )''')

def calc_difficulty(cooking_time, ingredients):
            num_ingredients = len(ingredients)
            if cooking_time < 10 and num_ingredients <4:
                return 'Easy'
            elif cooking_time < 10 and num_ingredients >= 4:
                return 'Medium'
            elif cooking_time >= 10 and num_ingredients < 4:
                return 'Intermediate'
            else:
                return 'Hard'

def display_all_recipes():
    cursor.execute('SELECT * FROM recipes')
    results = cursor.fetchall()

    if not results:
        print('\nNo recipes found in the database. Please add a recipe and try again!')
        return
    
    print('All Recipes:')
    print('\n' + '='*70)

    for recipe in results:
        recipe_id, name, ingredients, cooking_time, difficulty = recipe
        print(f'ID: {recipe_id}')
        print(f'Name: {name}')
        print(f'Ingredients: {ingredients}')
        print(f'Cooking Time: {cooking_time}')
        print(f'Difficulty: {difficulty}')
        print('-'*70)

def main_menu(conn, cursor):

    def create_recipe(conn, cursor):

        while True:
            name = input('Enter the name of the recipe: ').strip()
            if name == '':
                print('Recipe name cannot be empty. Please try again!')
                continue
            break

        while True:
            try:
                cooking_time = int(input('Enter the cooking time in minutes: '))
                if cooking_time <= 0:
                    print('Cooking time must be a positive number. Please try again.')
                    continue
                break
            except ValueError:
                print('Invalid input. Please enter a number')

        while True:
            ingredients_input = input('Enter each ingredient, separated by a comma: ')
            ingredients = [i.strip().lower() for i in ingredients_input.split(',')]
            ingredients = [ing for ing in ingredients if ing != '']

            ingredients_set = set(ingredients)
            ingredients = sorted(ingredients_set)

            if len(ingredients) == 0:
                print('You must enter at least one ingredient. Please try again.')
                continue
            break

        ingredients_string = ', '.join(ingredients)
        if len(ingredients_string) > 255:
            print('The ingredients list is too long! Please enter a shorter list of ingredients.')
            return
            
        difficulty = calc_difficulty(cooking_time, ingredients)

        try:    
            sql = 'INSERT INTO recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)'
            val = (name, ingredients_string, cooking_time, difficulty)
            
            cursor.execute(sql, val) 
            conn.commit()

            print(f'\n{name} created successfully!')
        except mysql.connector.Error as err:
            print(f'\n Error creating recipe: {err}')
            conn.rollback()


    def search_recipe(conn, cursor):
        
        cursor.execute('SELECT ingredients FROM recipes')
        results = cursor.fetchall()

        if not results:
            print('No ingredients found, please add some recipes and try again.')
            return
        
        all_ingredients = []

        for row in results:
            ingredients_string = row[0]
            ingredients_list = ingredients_string.split(',')
            
            for ingredient in ingredients_list:
                ingredient = ingredient.strip()
                if ingredient not in all_ingredients:
                    all_ingredients.append(ingredient)


        print('=' * 50)
        print('Available Ingredients:')
        for index, ingredient in enumerate(all_ingredients, 1):
            print(f'{index}. {ingredient}')
        print('=' * 50)

        while True:
            try:
                choice = int(input('\nEnter the number of the ingredients you would like to search for: '))

                if 1 <= choice <= len(all_ingredients):
                    search_ingredient = all_ingredients[choice -1]
                    break
                else:
                    print(f'Please enter a number between 1 and {len(all_ingredients)}')
            except ValueError:
                print('Invalid input, please enter a number.')
        
        sql = 'SELECT * FROM recipes WHERE ingredients LIKE %s'
        val =f'%{search_ingredient}%'
        cursor.execute(sql, (val,))
        matching_recipes = cursor.fetchall()

        if not matching_recipes:
            print(f'No recipes found containing {search_ingredient}')
        else:
            print('-' * 50)
            for recipe in matching_recipes:
                print('ID:', recipe[0])
                print('Name:', recipe[1])
                print('Ingredients:', recipe[2])
                print('Cooking Time:', recipe[3], 'minutes')
                print('Difficulty:', recipe[4])
                print('-' * 50) 

    def update_recipe(conn, cursor):
        display_all_recipes()
        
        while True:
            try:
                selected_id = int(input('Enter the ID number of the recipe you would like to update: '))

                cursor.execute('SELECT * FROM recipes WHERE id = %s', (selected_id,))
                selected_recipe = cursor.fetchone()

                if selected_recipe:
                    break
                else:
                    print(f'No recipe with ID {selected_id} found. Please try again.')
            except ValueError:
                print('Invalid input. Please enter a number.')

        recipe_id, name, ingredients, cooking_time, difficulty = selected_recipe
        print('Selected Recipe:')
        print(f'ID: {recipe_id}',)
        print(f'Name: {name}')
        print(f'Ingredients: {ingredients}')
        print(f'Cooking Time: {cooking_time}')
        print(f'Difficulty: {difficulty}')
        print('-' * 50)
        print('1. Name')
        print('2. Ingredients')
        print('3. Cooking Time')

        while True:
            try:
                column_choice = int(input('Which column number would you like to update: '))
                if 1 <= column_choice <= 3:
                    break
                else:
                    print('Please enter 1, 2, or 3')
            except ValueError:
                print('Invalid input. Please enter a number.')

        if column_choice == 1:
            while True:
                new_name = input('Please enter the new name for the recipe: ').strip()
                if new_name == '':
                    print('Name cannot be empty. Please try again.')
                    continue
                break

            sql = 'UPDATE recipes SET name = %s WHERE id = %s'
            val = (new_name, selected_id)
            cursor.execute(sql, val)
            conn.commit()
            print(f'Recipe No. {selected_id} updated to {new_name} successfully!')
        
        elif column_choice == 2:
            while True:
                ingredients_input = input('Enter the new ingredients, separated by a comma: ')
                new_ingredients_list = [i.strip().lower() for i in ingredients_input.split(',')]
                new_ingredients_list = [ing for ing in new_ingredients_list if ing != '']

                new_ingredients_set = set(new_ingredients_list)
                new_ingredients_list = sorted(new_ingredients_set)

                if len(new_ingredients_list) == 0:
                    print('You must enter at least one ingredient. Please try again')
                    continue
                break

            new_ingredients_string = ', '.join(new_ingredients_list)

            new_difficulty = calc_difficulty(cooking_time, new_ingredients_list)

            sql = 'UPDATE recipes SET ingredients = %s, difficulty = %s WHERE id = %s'
            val = (new_ingredients_string, new_difficulty, selected_id)
            cursor.execute(sql, val)
            conn.commit()
            print('Ingredients updated successfully!')
        
        elif column_choice == 3:
            while True:
                try: 
                    new_cooking_time = int(input('\nEnter the new cooking time (in minutes): '))
                    if new_cooking_time <= 0:
                        print('Cooking time must be a positive number. Please try again.')
                        continue
                    break
                except ValueError:
                    print('Invalid input. Please enter a number.')

            ingredients_list = ingredients.split(',')
            ingredients_list = [ing.strip() for ing in ingredients_list]
            new_difficulty = calc_difficulty(new_cooking_time, ingredients_list)

            sql = 'UPDATE recipes SET cooking_time = %s, difficulty = %s WHERE id = %s'
            val = (new_cooking_time, new_difficulty, selected_id)
            cursor.execute(sql, val)
            conn.commit()
            print(f'Cooking time updated to {new_cooking_time} minutes!')

    def delete_recipe(conn, cursor):
        display_all_recipes()

        while True:
            try:
                selected_id = int(input('\nEnter the ID number of the recipe you would like to delete: '))

                cursor.execute('SELECT * FROM recipes WHERE id = %s', (selected_id,))
                selected_recipe = cursor.fetchone()

                if selected_recipe:
                    break
                else:
                    print(f'Recipe with ID {selected_id} not found. Please try again.')
            except ValueError:
                print('Invalid input. Please try again.')
        
        recipe_id, name, ingredients, cooking_time, difficulty = selected_recipe
        print('\nYou are about to delete this recipe:')
        print(f'ID: {recipe_id}')
        print(f'Name: {name}')
        print(f'Ingredients: {ingredients}')
        print(f'Cooking Time: {cooking_time} minutes')
        print(f'Difficulty: {difficulty}')

        while True:
            confirm = input('\nAre you sure you would like to delete this recipe? (y/n): ').lower().strip()
            if confirm == 'y':
                cursor.execute('DELETE FROM recipes WHERE id = %s', (selected_id,))
                conn.commit()

                print(f'The {name} recipe has been deleted.')
                break
            elif confirm == 'n':
                print('Deletion cancelled.')
                break
            else:
                print('Please enter y or n to confirm your choice.')
            
    choice = ''

    while (choice != 'quit'):
        print('Main Menu')
        print('=' * 60)
        print('What would you like to do? Pick a choice:')
        print('1. Create a new recipe')
        print('2. Search for a recipe by ingredient')
        print('3. Update an exisiting recipe')
        print('4. Delete a recipe')
        print('Type "quit" to exit the program.')
        choice = input('Your choice: ').strip().lower()

        if choice == '1':
            create_recipe(conn, cursor)
        
        elif choice == '2':
            search_recipe(conn, cursor)

        elif choice == '3':
            update_recipe(conn, cursor)
        
        elif choice == '4':
            delete_recipe(conn, cursor)

        elif choice == 'quit':
            print('Thank you for using this script to manage your recipes. Goodbye!')

        else:
            print('\nInvalid entry. Please enter 1, 2, 3, 4, or "quit"')

# Main Code Section
try:
    main_menu(conn, cursor)
except KeyboardInterrupt:
    print('\n\nProgram interrupted. Exiting program now.')
except mysql.connector.Error as err:
    print(f'\nDatabase error: {err}')
finally:
    cursor.close()
    conn.close()
    print('Database connection closed.')