import db
from entities import entities
from services.file_handler import FileHandler


class PantryService:
    def __init__(self):
        self.file_handler = FileHandler()
        self.mock_ingredients = [
            ["ground beef", "400g", "6407840041172"],
            ["macaroni", "400g", "6417700050725"],
        ]

    def get_pantry(self):
        use_db = db.test_database_connection()

        if use_db:
            ingredients = self.get_ingredients_from_db()
        else:
            ingredients = self.get_ingredients_from_text_file()

        pantry = entities.Pantry()
        for ingredient in ingredients:
            entity = entities.Ingredient(ingredient[0], ingredient[1], ingredient[2])
            pantry.add_ingredient(entity)
        return pantry.ingredients

    def get_ingredients_from_text_file(self):
        ingredients = self.file_handler.read_from_csv("pantry.csv")
        if not ingredients:
            self.file_handler.write_to_csv("pantry.csv", self.mock_ingredients)
            ingredients = self.file_handler.read_from_csv("pantry.csv")
        return ingredients

    def get_ingredients_from_db(self):
        ingredients = db.get_all_pantry_ingredients()
        if not ingredients:
            db.insert_ingredient("ground beef", "400g", "6407840041172")
            db.insert_ingredient("macaroni", "400g", "6417700050725")
            ingredients = db.get_all_pantry_ingredients()
        return ingredients