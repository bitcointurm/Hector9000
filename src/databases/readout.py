from database import Database
from pprint import pprint
import random

DATE_FROM = "2023-08-20 12:00:00"
DATE_TO = "2023-08-20 23:00:00"

db = Database("h9k")
drinks_made = db.get_made_drinks(DATE_FROM, DATE_TO)
used_ingredients = db.get_used_ingredients(DATE_FROM, DATE_TO)

print('\nDrinks:')
for name, number in drinks_made:
    print(f'{name}: {number}')

print('\nIngredients:')
for ingredient, ml in used_ingredients:
    print(f'{ingredient}: {ml}')