import pickle

def calc_difficulty(cooking_time, ingredients):
    num_ingredients = len(ingredients)
    if cooking_time < 10 and num_ingredients < 4:
        return 'Easy'
    elif cooking_time < 10 and num_ingredients >= 4:
        return 'Medium'
    elif cooking_time >= 10 and num_ingredients < 4:
        return 'Intermediate'
    else:
        return 'Hard' 

def take_recipe():
    while True:
        name = input('Enter recipe name: ').strip()
        if name == '':
            print('Recipe name cannot be empty. Please try again')
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
            print('Invalid input! Please enter a number.')
    
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

    difficulty = calc_difficulty(cooking_time, ingredients)

    recipe = {
        'name': name,
        'cooking_time': cooking_time,
        'ingredients': ingredients,
        'difficulty': difficulty
    }

    return recipe

while True: 
    file = input('Enter the name of the file where your recipes are stored: ')
    if file.strip() == '':
        print('Filename cannot be empty. Please enter a name and try again.')
        continue
    break

while True:
    try:
        recipe_file = open(file, 'rb')
        data = pickle.load(recipe_file)
    except FileNotFoundError:
        print('The entered file could not be found. A file with the entered name will be created to save your recipes!')
        data = {
            'recipes_list': [],
            'all_ingredients': []
        }
        break
    except:
        print('An unexpected error occurred with your entry. Please try again.')
        continue
    else:
        recipe_file.close()
        break

recipes_list = data['recipes_list']
all_ingredients = data['all_ingredients']

while True:
    try: 
        n = int(input('How many recipes would you like to enter? '))
        if n <= 0:
            print('Please enter a positive number.')
            continue
        break
    except ValueError:
        print('Please enter a number, not another data type.')

for i in range(n):
    recipe_to_add = take_recipe()
    recipes_list.append(recipe_to_add)

    for ingredient in recipe_to_add['ingredients']:
        if ingredient not in all_ingredients:
            all_ingredients.append(ingredient)

data = {
    'recipes_list': recipes_list,
    'all_ingredients': all_ingredients
}

with open(file, 'wb') as recipe_file:
    pickle.dump(data, recipe_file)