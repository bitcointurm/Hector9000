import sqlite3 as lite
from datetime import datetime
from time import *


class Database:
    con = None
    cur = None

    def __init__(self, db_name):
        self.con = lite.connect(db_name + ".db")
        self.cur = self.con.cursor()

    def create_tables_if_not_exist(self):
        self.cur.execute(
            "CREATE TABLE if not exists DrinksLog("
            "ID Integer primary key, "
            "name TEXT, "
            "date timestamp)"
        )
        self.cur.execute(
            "CREATE TABLE if not exists IngredientsLog("
            "ID Integer primary key, "
            "ingredient TEXT, "
            "ml integer, "
            "date timestamp)"
        )
        self.con.commit()
    
    def count_up_drink(self, drink):
        self.cur.execute(
            "INSERT INTO DrinksLog (name, date) VALUES (?, ?)",
            (drink, datetime.now())
        )
        self.con.commit()
    
    def count_up_ingredient(self, ingredient, ml):
        self.cur.execute(
            "INSERT INTO IngredientsLog (ingredient, ml, date) VALUES (?, ?, ?)",
            (ingredient, ml, datetime.now())
        )
        self.con.commit()

    def get_made_drinks(self, start, end):
        self.cur.execute(
            "SELECT name, COUNT(*) as times_made FROM DrinksLog WHERE date BETWEEN ? AND ? GROUP BY name ORDER BY times_made DESC", (start, end)
        )
        result = self.cur.fetchall()
        return result
    
    def get_used_ingredients(self, start, end):
        self.cur.execute(
            "SELECT ingredient, SUM(ml) as Total_ml FROM IngredientsLog WHERE date BETWEEN ? and ? GROUP BY ingredient ORDER BY Total_ml DESC", (start, end)
        )
        result = self.cur.fetchall()
        return result
    
    def __del__(self):
        self.con.commit()
        self.con.close()