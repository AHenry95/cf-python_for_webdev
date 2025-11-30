def display(file):
    heros = []
    for line in file:
        line = line.rstrip('\n')
        hero_name = line.split(', ')[0]
        first_appearance = line.split(', ')[1]
        heros.append([hero_name, first_appearance])
    heros.sort(key = lambda hero: hero[1])

    for hero in heros:
        print('--------------------------------------')
        print('Superhero: ' + hero[0])
        print('First year of appearance: ' + hero[1])

filename = input('Enter the filename where you have stored your superheroes: ')
try:
    file = open(filename, 'r')
    display(file)
except FileNotFoundError:
    print('File doesn\'t exist - exiting.')
except:
    print('An unexpected error occurred.')
else:
    file.close()
finally:
    print('Goodbye!')