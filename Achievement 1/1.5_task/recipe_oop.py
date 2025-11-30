class Recipe:
    all_ingredients = []

    def __init__(self, name):
        self.name = name
        self.ingredients = []
        self.cooking_time = 0
        self.difficulty = None
    
    # Getter Methods
    def get_name(self):
        return self.name
    
    def get_cooking_time(self):
        return self.cooking_time
    
    def get_ingredients(self):
        return self.ingredients
    
    def get_difficulty(self):
        if self.difficulty is None: 
            self.calculate_difficulty()
        return self.difficulty

    # Setter Methods
    def set_name(self, name):
        self.name = name

    def set_cooking_time(self, cooking_time):
        self.cooking_time = cooking_time
        self.calculate_difficulty()

    def add_ingredients(self, *ingredients):
        for ingredient in ingredients:
            self.ingredients.append(ingredient)
        self.update_all_ingredients()
        self.calculate_difficulty()

    def calculate_difficulty(self):
        num_ingredients = len(self.ingredients)

        if self.cooking_time < 10 and num_ingredients < 4:
            self.difficulty = 'Easy'
        elif self.cooking_time < 10 and num_ingredients >= 4:
            self.difficulty = 'Medium'
        elif self.cooking_time >= 10 and num_ingredients < 4:
            self.difficulty = 'Intermediate'
        else:
            self.difficulty = 'Hard'

    # Other Methods
    def search_ingredients(self, ingredient):
        return ingredient in self.ingredients
    
    def update_all_ingredients(self):
        for ingredient in self.ingredients:
            if ingredient not in Recipe.all_ingredients:
                Recipe.all_ingredients.append(ingredient)

    def __str__(self):
        output = 50 * '-'
        output += f'\nRecipe: {self.name}\n'
        output += f'Cooking Time: {self.cooking_time} minutes\n'
        output += f'Ingredients:\n'
        for ingredient in self.ingredients:
            output += f' - {ingredient}\n'
        output += f'Difficulty: {self.difficulty}'
        return output

def recipe_search(data, search_term):
    header = 50 * '='
    header += f'\nRecipes found containing {search_term}:'
    print(header)

    recipes_found = False

    for recipe in data:
        if recipe.search_ingredients(search_term):
            print(recipe)
            recipes_found = True

    if recipes_found == False:
        print(f'No recipes found containing {search_term}! Please try again')

# Main Code

tea = Recipe('Tea')
tea.add_ingredients('Tea Leaves', 'Sugar', 'Water')
tea.set_cooking_time(5)

coffee = Recipe('Coffee')
coffee.add_ingredients('Ground Coffee', 'Water', 'Sugar')
coffee.set_cooking_time(5)

cake = Recipe('Cake')
cake.add_ingredients('Sugar', 'Butter', 'Eggs', 'Vanila Essence', 'Flour', 'Baking Powder', 'Milk')
cake.set_cooking_time(50)

banana_smoothie = Recipe('Banana Smoothie')
banana_smoothie.add_ingredients('Bananas', 'Milk', 'Peanut Butter', 'Sugar', 'Ice Cubes')
banana_smoothie.set_cooking_time(5)

print(tea)
print(coffee)
print(cake)
print(banana_smoothie)

recipes_list = [tea, coffee, cake, banana_smoothie]

recipe_search(recipes_list, 'Water')
recipe_search(recipes_list, 'Sugar')
recipe_search(recipes_list, 'Bananas')