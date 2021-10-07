from app.config.MySQLConnection import connectToMySQL
from flask import flash, request
import re


def validateStr(str):
    if re.findall("[\d+\W+{3,n}]", str):
        print("Invalid Str")
        return False

    else:
        print("Valid Str")
        return True


class Recipe:
    def __init__(self, data):
        self.recipe_id = data['recipe_id']
        self.recipe_name = data['recipe_name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date = data['date']
        self.under_time = data['under_time']
        self.user_id = data['user_id']

    @ classmethod
    def insert(cls, data):
        query = "INSERT INTO users_recipes(recipe_name, description, instructions, date, under_time, user_id) VALUES(%(recipe_name)s, %(description)s, %(instructions)s, %(date)s, %(under_time)s, %(user_id)s);"

        result = connectToMySQL("recipes").query_db(query, data)
        print("INSERT_RECIPE => ", result)
        return result

    @ classmethod
    def get(cls, data):
        query = "SELECT * FROM users_recipes WHERE users_recipes.recipe_id = %(id)s;"

        result = connectToMySQL("recipes").query_db(query, data)
        print("GET_RECIPE => ", result)

        if len(result) < 1:
            return False
        return cls(result[0])

    @ classmethod
    def delete(cls, data):
        query = "DELETE FROM users_recipes WHERE users_recipes.recipe_id = %(id)s;"

        result = connectToMySQL("recipes").query_db(query, data)
        print("RECIPE_DELETED => ", result)
        return result

    @ classmethod
    def get_all(cls):
        query = "SELECT * FROM users_recipes;"
        results = connectToMySQL("recipes").query_db(query)
        print("GET_ALL_RECIPES => ", results)
        recipes = []
        for result in results:
            recipes.append(cls(result))
        return recipes

    @classmethod
    def update(cls, data):
        query = "UPDATE users_recipes SET recipe_name = %(recipe_name)s, description = %(description)s, instructions = %(instructions)s, date = %(date)s, under_time=%(under_time)s WHERE  users_recipes.recipe_id = %(recipe_id)s;"
        result = connectToMySQL("recipes").query_db(query, data)
        print("UPDATE_RECIPE => ", result)
        return result

    @classmethod
    def validate_recipe(cls, data):
        is_valid = True
        if not validateStr(data['recipe_name']) or len(data['recipe_name']) < 3:
            is_valid = False
            flash("The recipe name must be at least 3 characters long.",
                  "recipe_edition")
        if not validateStr(data['description']) or len(data['description']) < 3:
            is_valid = False
            flash("The description must be at least 3 characters long.",
                  "create_recipe")
        if not validateStr(data['instructions']) or len(data['instructions']) < 3:
            is_valid = False
            flash("The instructions must be at least 3 characters long.",
                  "create_recipe")

        if not data.get('date'):
            is_valid = False
            flash("You must provide the date field", "create_recipe")

        if not data.get('under_time'):
            is_valid = False
            flash("You must provide the under 30 minutes field", "create_recipe")
        return is_valid
