# REST API documentation

## POST /generate

Generates a new recipe from given ingredients and conditions.

**Request body:** JSON object with fields:

- ingredients: JSON array of ingredients as strings.
- recipe_type: String of conditions that the recipe must fulfill.

**Returns:** JSON object with fields:

- ingredients: JSON object with format "ingredient": "amount".
- instructions: JSON array of instruction steps in the order they should be completed.
- recipe_name: String, the name of the recipe.

**Example:**

Request

```json
{"ingredients": ["banana", "milk"], "recipe_type": "sweet"}
```

Response

```json
{
  "ingredients": {
    "banana": 2,
    "milk": "2 cups"
  },
  "instructions": [
    "Peel the bananas and slice them into small chunks.",
    "In a blender, add the banana chunks and milk.",
    "Blend until the mixture is smooth and creamy.",
    "Pour the milkshake into glasses and serve immediately."
  ],
  "recipe_name": "Banana Milkshake"
}
```

## POST /change

Changes the previously generated recipe.

**Request body:** JSON object with fields:

- change: String of changes to make to the recipe.

**Returns:** A new recipe in the same format as POST /generate

**Example:**

Request

```json
{"change": "add strawberries"}
```

Response

```json
{
  "ingredients": {
    "banana": 2,
    "milk": "2 cups",
    "strawberries": "1 cup"
  },
  "instructions": [
    "Peel the bananas and slice them into small chunks.",
    "Wash the strawberries and remove the stems.",
    "In a blender, add the banana chunks, strawberries, and milk.",
    "Blend until the mixture is smooth and creamy.",
    "Pour the milkshake into glasses and serve immediately."
  ],
  "recipe_name": "Strawberry Banana Milkshake"
}
```

## GET /frontend

???

## POST /frontend

???