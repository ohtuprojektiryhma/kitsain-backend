import json

GENERATION_MESSAGE = {
    "role": "system",
    "content": """
You are a tool that generates recipes. You are given the following requirements in JSON form:
{
    "pantry_items": [items available in pantry],
    "required_items": [items that must be used in the recipe],
    "recipe_type": type of recipe to be generated,
    "special_supplies": [special kitchen supplies available],
    "pantry_only": boolean, if true you must not use any extra items not in pantry, even if the recipe would not make sense,
    "language": language of the generated recipe
}
Generate a recipe precisely in the following JSON format:
{
    "recipe_name": name of the generated recipe,
    "ingredients": {dict where key = ingredient name, and value = amount needed for the recipe},
    "instructions": [list of instructions on how to make the recipe]
}
""",
}

CHANGE_MESSAGE = {
    "role": "system",
    "content": "You are a tool that makes changes to recipes. You are given a recipe in a json format and wanted changes to the recipe. Generate the same recipe with given changes in a json form. Provide the fields: recipe_name : name of the generated recipe, ingredients : dict where key = ingredient name, and the value = amount needed for the recipe, instructions : list of instructions on how to make the recipe",  # pylint: disable=C0301
}


class OpenAIService:
    def __init__(self, client):
        self.client = client
        # current chat session
        self.messages = []

    def _send_messages_to_gpt(self):
        # call openai api
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
        )
        response = completion.choices[0].message

        # add response to chat session and return it
        self.messages.append(response)
        return response

    def get_recipe(
        self,
        ingredients: list[str],
        recipe_type: str,
        expiring_soon: list[str],
        supplies: list[str],
        pantry_only: bool,
        language: str,
    ):
        # init chat session
        self.messages.clear()
        self.messages.append(GENERATION_MESSAGE)
        self.messages.append(
            {
                "role": "user",
                "content": f"""
{{
    "pantry_items": {json.dumps(ingredients)},
    "required_items": {json.dumps(expiring_soon)},
    "recipe_type": {json.dumps(recipe_type)},
    "special_supplies": {json.dumps(supplies)},
    "pantry_only": {json.dumps(pantry_only)},
    "language": {json.dumps(language)}
}}
""",
            }
        )

        response = self._send_messages_to_gpt()

        try:
            return json.loads(response.content)
        except json.JSONDecodeError as err:
            print("Error parsing JSON response from GPT. Response:")
            print(response.content)
            raise err

    def change_recipe(
        self,
        details,
        change: str,
        # ingredients: list,
        # recipe_type: str,
        # exp_soon: list,
        # supplies: list,
    ):  # pylint: disable=C0301
        # Messages are cleared, then the CHANGE_MESSAGE is sent to the AI,
        # then we a message where details = details of recipe we want to change
        # and change = the change we want to the recipe
        self.messages.clear()
        print(details)
        print(change)
        self.messages.append(CHANGE_MESSAGE)
        self.messages.append(
            {
                "role": "user",
                "content": f"""{{"details": {json.dumps(details)}, "change": {json.dumps(change)}}}""",
            }
        )

        response = self._send_messages_to_gpt()
        print(response)

        return json.loads(response.content)
