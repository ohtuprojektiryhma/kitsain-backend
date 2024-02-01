import json
from flask import request, render_template
from app import app, openai_service
import db

# from entities import entities


@app.route("/mock_generate", methods=["POST"])
def mock_generate():
    with open("mock_recipe.json", encoding="utf-8") as file:
        mock_recipe = json.load(file)
    return mock_recipe


def create_pantry():
    # ingredient1 = entities.Ingredient("ground beef", "400 g", "6407840041172")
    # ingredient2 = entities.Ingredient("macaroni", "400 g", "6417700050725")

    # pantry = entities.Pantry()
    # pantry.add_ingredient(ingredient1)
    # pantry.add_ingredient(ingredient2)
    ingredients = db.get_all_pantry_ingredients()
    if not ingredients:
        db.insert_ingredient("ground beef", "400g", "6407840041172")
        db.insert_ingredient("macaroni", "400g", "6417700050725")
        ingredients = db.get_all_pantry_ingredients()

    return ingredients


@app.route("/generate", methods=["POST"])
def generate():
    request_body = request.json
    recipe = openai_service.get_recipe(
        request_body["ingredients"], request_body["recipe_type"]
    )
    return recipe


@app.route("/change", methods=["POST"])
def change():
    request_body = request.json
    recipe = openai_service.change_recipe(request_body["change"])
    return recipe


@app.route("/frontend", methods=["GET", "POST"])
def generate_recipe():
    pantry = create_pantry()
    if request.method == "GET":
        recipe_list = []
        with open("recipes.txt", encoding="utf-8") as f:
            for jsonObj in f:
                recipeDict = json.loads(jsonObj)
                recipeDict["ingredients"] = list(recipeDict["ingredients"].items())
                recipe_list.append(recipeDict)
        return render_template(
            "generate_recipe.html", recipes=recipe_list, pantry=pantry
        )
    if request.method == "POST":
        recipe = request.get_json()
        recipe_string = json.dumps(recipe)
        db.insert_recipe(recipe_string)

        with open("recipes.txt", "a", encoding="utf-8") as recipes_file:
            recipes_file.write(f"{recipe_string}\n")

        return request.json
    return None


@app.route("/recipes", methods=["GET"])
def view_recipes():
    recipe_list = []
    with open("recipes.txt", encoding="utf-8") as f:
        for jsonObj in f:
            recipeDict = json.loads(jsonObj)
            recipeDict["ingredients"] = list(recipeDict["ingredients"].items())
            print(recipeDict)
            recipe_list.append(recipeDict)
    return render_template("view_recipes.html", recipes=recipe_list)


if __name__ == "__main__":
    app.debug = True
    app.run()
