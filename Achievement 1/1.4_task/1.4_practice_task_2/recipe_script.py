import pickle

with open('recipe_pickle.bin', 'rb') as my_file:
    tea_recipe = pickle.load(my_file)

print('Recipe:', tea_recipe['name'])
print('Ingredients:',  ', '.join(tea_recipe['ingredients']))
print('Cooking Time:', tea_recipe['cooking_time'], 'minutes')
print('Difficulty:', tea_recipe['difficulty'])