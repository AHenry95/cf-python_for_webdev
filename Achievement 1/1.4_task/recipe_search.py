import pickle

def display_recipe(recipe):
    print('-----------------------------------------------')
    print(f"Name: {recipe['name']}")
    print(f"Cooking Time: {str(recipe['cooking_time'])}")
    print(f"Ingredients: {', '.join(recipe['ingredients'])}")
    print(f"Difficulty: {recipe['difficulty']}")

def search_ingredient(data):
    recipes_to_print = []

    for index, ingredient in enumerate(data['all_ingredients'], 1):
        print(f'{index}. {ingredient}')
    
    while True:
        try:
            ingredient_searched = int(input('Select an ingredient number from the list: ' )) - 1
            ingredient_name = data['all_ingredients'][ingredient_searched]
        except (ValueError, IndexError):
            print('There was an error with your selection, please try again.')
        else:
            break

    for recipe in data['recipes_list']:
        if ingredient_name in recipe['ingredients']:
            recipes_to_print.append(recipe)

    for recipe in recipes_to_print:
        display_recipe(recipe)

while True:
    file = input('What is the name of the file that contains your recipes? ')

    try:
        with open(file, 'rb') as recipe_file:
            data = pickle.load(recipe_file)
    except FileNotFoundError:
        print('The entered file could not be found. Please check that the file and/or pathway are correct.')
    except:
        print('An unexpected error occured. Please try again. ')
    else:
        break

search_ingredient(data)