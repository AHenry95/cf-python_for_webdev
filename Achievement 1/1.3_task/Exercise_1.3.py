recipes_list = []
ingredients_list = []

def take_recipe():
    name = input('Enter recipe name: ')

    cooking_time = int(input('Enter cooking time in minutes: '))

    ingredients_input = input('Enter each ingredient, separated by a comma: ')
    ingredients = [i.strip() for i in ingredients_input.split(',')]

    recipe = {
        'name': name,
        'cooking_time': cooking_time,
        'ingredients': ingredients
    }

    return recipe

n = int(input('How many recipes would you like to enter? '))

for i in range(n):
    recipe = take_recipe()

    for ingredient in recipe['ingredients']:
        if ingredient not in ingredients_list:
            ingredients_list.append(ingredient)

    recipes_list.append(recipe)

for recipe in recipes_list:
    if recipe['cooking_time'] < 10 and len(recipe['ingredients']) < 4:
        recipe['difficulty'] = 'Easy'

    elif recipe['cooking_time'] < 10 and len(recipe['ingredients']) >= 4:
        recipe['difficulty'] = 'Medium'

    elif recipe['cooking_time'] >= 10 and len(recipe['ingredients']) < 4:
        recipe['difficulty'] = 'Intermediate'
    
    elif recipe['cooking_time'] >= 10 and len(recipe['ingredients']) >= 4:
        recipe['difficulty'] = 'Hard'

    print('\n')
    print('Recipe: ' + recipe['name'])
    print('Cooking Time: ' + str(recipe['cooking_time']))
    print('Ingredients:\n' + '\n'.join(recipe['ingredients']))
    print('Difficulty level: ' + recipe['difficulty'])
    print('\n')

ingredients_list.sort()

print('Ingredients Avilable Across All Recipes')
print('---------------------------------------')
print('\n'.join(ingredients_list))