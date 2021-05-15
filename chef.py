import sqlite3
import json
import datetime

connection = sqlite3.connect("recipes.db")
cursor = connection.cursor()

rows = cursor.execute("SELECT * FROM Recipes")
object_list = []
recipe_list = []

for row in rows:
    object_list.append({"Recipe_ID": row[0], "Recipe_Name": row[1],
                        "Recipe_Desc": row[2]})

recipe_json = json.loads(json.dumps({"Recipes": object_list}, indent=1))

for recipe in recipe_json["Recipes"]:
    recipe_list.append(recipe["Recipe_Name"])
