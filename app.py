import os

from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

app = Flask(__name__)

AZURE_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")

print("Endpoint:", AZURE_ENDPOINT)
print("Deployment:", AZURE_DEPLOYMENT)
print("API Key Loaded:", bool(AZURE_API_KEY))

client = AzureOpenAI(
    api_key=AZURE_API_KEY,
    azure_endpoint=AZURE_ENDPOINT,
    api_version="2024-02-01"
)

print("KEY:", bool(AZURE_API_KEY))
print("ENDPOINT:", AZURE_ENDPOINT)
print("DEPLOYMENT:", AZURE_DEPLOYMENT)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate_recipe", methods=["POST"])
def generate_recipe():

    try:

        data = request.get_json()

        recipe_type = data.get("recipe_type")
        ingredients = data.get("ingredients")
        prep_time = data.get("prep_time")

        prompt = f"""
        Create a detailed recipe.

        Recipe Type:
        {recipe_type}

        Available Ingredients:
        {ingredients}

        Maximum Preparation Time:
        {prep_time} minutes

        Return:

        Recipe Name

        Preparation Time

        Servings

        Ingredients Used

        Step-by-Step Instructions

        Chef Tips
        """

        response = client.chat.completions.create(
            model=AZURE_DEPLOYMENT,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional chef who creates "
                        "easy-to-follow recipes using only the "
                        "ingredients provided."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=1000
        )

        recipe = response.choices[0].message.content

        return jsonify({
            "success": True,
            "recipe": recipe
        })

    except Exception as e:

        print("ERROR:", str(e))

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)