from flask import Flask, render_template, request, session, redirect, flash
from app import app
from app.models.Recipe import Recipe


@app.route("/create", methods=['GET'])
def create_recipe():
    if 'user' in session:
        return render_template("create.html")


@app.route("/create/new", methods=['POST'])
def add_new():
    if 'user' in session:
        print(session)
        if not Recipe.validate_recipe(request.form):
            return redirect("/create")
        data = {
            "recipe_name": request.form['recipe_name'],
            "description": request.form['description'],
            "instructions": request.form['instructions'],
            "date": request.form["date"],
            "under_time": request.form["under_time"],
            "user_id": session['user']['id']
        }

        result = Recipe.insert(data)
        return redirect("/dashboard")
    return redirect("/")


@app.route("/recipe/<id>", methods=['GET'])
def show_recipe(id):
    if 'user' in session:
        data = {"id": id}
        recipe = Recipe.get(data)
        print(session)
        return render_template("recipe.html", recipe=recipe)
    return redirect("/")


@app.route("/delete/<id>", methods=['GET'])
def delete_recipe(id):
    if 'user' in session:
        data = {"id": id}
        result = Recipe.delete(data)
        return redirect("/dashboard")
    return redirect("/")


@app.route("/edit/<id>", methods=['GET'])
def edit_recipe(id):
    if 'user' in session:
        data = {"id": id}
        recipe = Recipe.get(data)
        print("RECIPE_IN_EDITION => ", recipe.description, recipe.instructions)
        return render_template("edit.html", recipe=recipe)
    return redirect("/")


@app.route("/update/<id>", methods=['POST'])
def update_recipe(id):
    if 'user' in session:
        data = {
            "recipe_name": request.form['recipe_name'],
            "description": request.form['description'],
            "instructions": request.form['instructions'],
            "date": request.form['date'],
            "under_time": request.form['under_time'],
            "recipe_id": id
        }

        Recipe.update(data)
        return redirect("/dashboard")
    return redirect("/")
