from app.config.MySQLConnection import connectToMySQL
from flask import flash
import re


def check(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if(re.fullmatch(regex, email)):
        print("Valid Email")
        return True

    else:
        print("Invalid Email")
        return False


def validateName(str):
    if re.findall("[\d+\W+{2,20}]", str):
        print("Invalid Name")
        return False

    else:
        print("Valid Name")
        return True


def validatePasswd(str):
    validPass = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
    if re.findall(validPass, str):
        print("Valid PassWord")
        return True

    else:
        print("Invalid PassWord")
        return False


class User:
    def __init__(self, data):
        self.user_id = data['user_id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.password = data['password']
        self.email = data['email']
        self.user_location = data['user_location']
        self.fav_food = data['fav_food']
        self.position = data['position']
        self.genre = data['genre']
        self.recipes = []

    @classmethod
    def exists(cls, data):
        # query = "SELECT email, password from users WHERE email = %(email)s"
        query = "SELECT * from users WHERE email = %(email)s"

        result = connectToMySQL("recipes").query_db(query, data)

        if len(result) < 1:
            return False
        print("USER_DB_EXISTS => ", result)
        return cls(result[0])

    @classmethod
    def insert(cls, data):
        query = "INSERT INTO users(first_name,last_name, password, email, user_location, fav_food, position, genre) VALUES(%(first_name)s, %(last_name)s, %(password)s,%(email)s, %(user_location)s, %(fav_food)s, %(position)s, %(genre)s);"

        result = connectToMySQL("recipes").query_db(query, data)
        print("INSERT => ", result)
        return result

    @staticmethod
    def validate_register(data):
        is_valid = True
        # VALIDATING FIRSTNAME
        if not validateName(data['first_name']) or len(data["first_name"]) < 2:
            # if len(data["first_name"]) < 2 or validateName(data['first_name']):
            flash(
                "First Name must be at least 2 characters long and can only has letters (a-Z)", category="register")
            is_valid = False

        # VALIDATING LASTNAME
        if not validateName(data['last_name']) or len(data["last_name"]) < 2:
            # if len(data["last_name"]) < 2 or validateName(data['last_name']):
            flash(
                "Last Name must be at least 2 characters long and can only has letters (a-Z)", "register")
            is_valid = False

        # VALIDATING PASSWORD
        if not validatePasswd(data['password']):
            flash("Your password needs to have at least one upper and lowercase characters, at least one number and at least one special character ('@!$#_-')", "register")
            is_valid = False

        if not check(data['email']):
            flash("You must provide an email in the format example@example.com",
                  "register")
            is_valid = False

        if data.get("location"):
            flash("You must provide a location.")
            is_valid = False
        if len(data["fav_food"]) < 1:
            flash("Your favorite food must be at least 1 characters.",
                  "register")
            is_valid = False
        if not data.get("position"):
            is_valid = False
            flash("You must provide one occupation.",
                  "register")
        if not data.get("genre"):
            is_valid = False
            flash("You must provide your genre.",
                  "register")

        return is_valid

    @classmethod
    def get_all_user_recipes(cls, data):
        query = "SELECT * FROM users JOIN user_recipes ON users.user_id == recipes.user_id WHERE users.user_id = %(id)s;"

        result = connectToMySQL("recipes").query_db(query, data)
        print("USER_RECIPES => ", result)
        return result
