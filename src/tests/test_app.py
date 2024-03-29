from os import getenv, path
from collections import deque
from dotenv import load_dotenv
from unittest import TestCase
from unittest.mock import patch
from app import app
from tests.mock_openai import OpenAI

dirname = path.dirname(__file__)

try:
    load_dotenv(dotenv_path=path.join(dirname, "../..", ".env"))
except FileNotFoundError:
    pass


class TestApp(TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
        self.client = app.test_client()

    # Inject mock OpenAI object into the service class.
    @patch("app.openai_service.client", OpenAI(api_key="mock api key"))
    def test_generate_recipe(self):
        data = {"pantry": ["Water", "Salt"], "recipe_type": "Soup"}

        response = self.client.post("/generate", json=data)

        self.assertEqual(response.status_code, 200)

        response_data = response.json
        self.assertEqual(
            response_data,
            {
                "recipe_name": "Mock Soup",
                "ingredients": {"Water": "1 cup", "Salt": "1 tsp"},
                "instructions": ["Boil water", "Add salt"],
            },
        )

    # Inject mock OpenAI object into the service class.
    @patch("app.openai_service.client", OpenAI(api_key="mock api key"))
    def test_change_recipe(self):
        data = {
            "recipe": {
                "recipe_name": "Mock Soup",
                "ingredients": {"Water": "1 cup", "Salt": "1 tsp"},
                "instructions": ["Boil water", "Add salt"],
            },
            "change": "Add pepper",
        }

        response = self.client.post("/change", json=data)

        self.assertEqual(response.status_code, 200)

        response_data = response.json
        self.assertEqual(
            response_data,
            {
                "recipe_name": "Improved Mock Soup",
                "ingredients": {"Water": "1 cup", "Salt": "1 tsp", "Pepper": "1 tsp"},
                "instructions": ["Boil water", "Add salt", "Add pepper"],
            },
        )

    # Patching REQUEST_QUEUE to be empty before this test
    @patch("routes.REQUEST_QUEUE", deque())
    def test_rate_limit(self):

        # First 500 requests should return success
        for _ in range(0, 500):
            response = self.client.post("/test_route")
            self.assertEqual(response.status_code, 204)

        # Request 501 should return trigger the rate limiter
        response = self.client.post("/test_route")
        self.assertEqual(response.status_code, 429)
