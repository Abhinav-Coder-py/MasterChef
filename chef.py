import sqlite3
import json
import datetime
import random

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

order_rows = cursor.execute("SELECT * FROM MasterChef")
object_list2 = []

for row in order_rows:
    object_list2.append({"Order_ID": row[0], "Customer_Name": row[1],
                        "Order_Recipe": row[2], "Order_Date": row[3]})

order_json = json.loads(json.dumps({"Orders": object_list2}, indent=1))

# username = input("Username: ")

if len(order_json["Orders"]) == 0:
    date = datetime.datetime.now().date()
    recipe = random.choice(recipe_list)
    cursor.execute("INSERT INTO MasterChef VALUES(?, ?, ?, ?)",
                   (1, "Abhinav", recipe, date))
    connection.commit()
    print(recipe)

else:
    order_id = order_json["Orders"][-1]["Order_ID"]
    pos_check = (order_id - 6) >= 0
    if not pos_check:
        date = datetime.datetime.now()
        prev_recs = []
        for order in order_json["Orders"]:
            prev_recs.append(order["Order_Recipe"])

        today_recipe = random.choice([rec for rec in recipe_list if (rec not in prev_recs)])
        cursor.execute("INSERT INTO MasterChef VALUES(?, ?, ?, ?)",
                       (order_id + 1, "Abhinav", today_recipe, date))
        connection.commit()
        print(today_recipe)

    else:
        last_week_recipe = order_json["Orders"][order_id - 6]["Order_Recipe"]
        date = datetime.datetime.now().date()
        prev_recs = []
        for order in order_json["Orders"]:
            if order["Order_ID"] >= order_id - 6:
                prev_recs.append(order["Order_Recipe"])
        today_recipe = random.choice([rec for rec in recipe_list if rec != last_week_recipe
                                      and (rec not in prev_recs)])
        cursor.execute("INSERT INTO MasterChef VALUES(?, ?, ?, ?)",
                       (order_id + 1, "Abhinav", today_recipe, date))
        connection.commit()
        print(today_recipe)
