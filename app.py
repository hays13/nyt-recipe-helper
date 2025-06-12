from flask_cors import CORS
from flask import Flask, request, jsonify
import openai
import os
import traceback
import json
import re

app = Flask(__name__)
CORS(app)

# Load your OpenAI API key from environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

# List of major allergens
ALLERGENS = [
    "milk", "eggs", "fish", "shellfish",
    "tree nuts", "peanuts", "wheat", "soy", "sesame"
]

def clean_ingredient_spacing(ingredient):
    spaced = re.sub(r'(?<=\d)(?=[a-zA-Z])', ' ', ingredient)
    return spaced.lower()

@app.route('/detect_allergens', methods=['POST'])
def detect_allergens():
    print("✅ /detect_allergens route was hit")
    try:
        data = request.get_json()
        ingredients = data.get("ingredients", [])

        if not ingredients:
            return jsonify({"error": "No ingredients provided"}), 400

        # Build a prompt for ChatGPT
        prompt = (
            "You are an allergen detection function.\n\n"
            "Given a list of ingredients and a fixed list of 9 allergens, return a JSON object like this:\n"
            "{ \"allergens\": [\"shellfish\", \"peanuts\"] }\n\n"
            "Use this allergen mapping:\n"
            "- shellfish: shrimp, crab, lobster, scallop, oyster, clam\n"
            "- fish: salmon, tuna, cod, halibut, anchovy\n"
            "- peanuts: peanut, peanut butter\n"
            "- tree nuts: almond, walnut, cashew, pecan, pistachio, or other tree nut butters\n"
            "- soy: soy sauce, soybeans, edamame, tofu\n"
            "- wheat: flour, wheat, breadcrumbs, pasta\n"
            "- milk: cheese, yogurt, milk, salted butter, unsalted butter, cream, parmesan\n"
            "- eggs: egg, mayonaise\n"
            "- sesame: sesame seeds, tahini\n\n"
            "Steps:\n"
            "1. Match individual ingredients to any of the allergen keywords above.\n"
            "2. For each match, include the corresponding allergen **once** in the list.\n"
            "3. Only use allergens from this list: milk, eggs, fish, shellfish, tree nuts, peanuts, wheat, soy, sesame\n"
            "4. Do not infer allergens based on typical pairings, common recipes, or associated dishes.\n"
            "5. Only include 'tree nuts' if the ingredient *explicitly* contains one of: almond, walnut, cashew, pecan, pistachio. Do not infer.\n"
            "6. Match allergens if their keyword appears as part of an ingredient (e.g. 'all-purpose flour' matches 'flour'; 'unsalted butter' matches 'butter').\n"
            "7. If none match, return: {\"allergens\": []}\n\n"
            "Ingredients:\n"
            f"{', '.join([clean_ingredient_spacing(i) for i in ingredients])}\n\n"
            "Now return only the JSON object."
        )


        print("\n=== Prompt Sent to OpenAI ===")
        print(prompt)
        print("=============================\n")
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{ "role": "user", "content": prompt }],
            temperature=0
        )
        reply = response.choices[0].message.content.strip()
        print("Raw GPT response:", reply)
        
        # Parse the JSON response
        
        try:
            data = json.loads(reply)
            found = data.get("allergens", [])
        except Exception as e:
            print("Failed to parse JSON reply:", reply)
            traceback.print_exc()
            found = []

        print("Returning allergens:", found)
        return jsonify({"allergens": found})
    

    except Exception as e:
        print("Error:", e)
        traceback.print_exc()
        return jsonify({"error": "Something went wrong with the API call"}), 500

@app.route('/detect_equipment', methods=['POST'])
def detect_equipment():
    print("✅ /detect_equipment route was hit")
    try:
        data = request.get_json()
        instruction_text = data.get("text")

        if not instruction_text:
            print("No text received in request.")
            return jsonify({"error": "No text provided"}), 400

        print("\n=== Received Instructions ===")
        print(instruction_text)
        print("=============================\n")

        prompt = (
            "You are a kitchen equipment extraction function.\n\n"
            "Your job is to extract only **notable or uncommon kitchen equipment** required in a recipe.\n"
            "Ignore common utensils and tools, including: knife, fork, spoon, tongs, whisk, ladle, spatula, grater, peeler, chopsticks, bowl, plate, cutting board, strainer, colander, cup, liquid measuring cup, and dry measuring cup.\n\n"
            "Include only equipment that would be important to know ahead of time, such as:\n"
            "- slow cooker, food processor, Dutch oven, cast iron skillet, stand mixer, rice cooker, large pot, baking dish, roasting pan, 9x13 dish, broiler pan, etc.\n"
            "Be specific about sizes or types when mentioned (e.g., '6-quart slow cooker', '9x13 baking dish').\n\n"
            "Return a JSON object in this format:\n"
            "{ \"equipment\": [\"large pot\", \"Dutch oven\"] }\n\n"
            "Do NOT include duplicates or inferred equipment.\n\n"
            f"Instructions:\n{instruction_text}\n\n"
            "Now return only the JSON object."
        )

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{ "role": "user", "content": prompt }],
            temperature=0
        )

        reply = response.choices[0].message.content.strip()
        print("Raw GPT response:", reply)

        try:
            data = json.loads(reply)
            found = data.get("equipment", [])
        except Exception as e:
            print("Failed to parse JSON reply:", reply)
            traceback.print_exc()
            found = []

        banned_terms = {
            "knife", "fork", "spoon", "tongs", "whisk", "ladle", "spatula", "grater", "peeler",
            "chopsticks", "bowl", "plate", "cutting board", "strainer", "colander", "cup",
            "measuring cup", "liquid measuring cup", "dry measuring cup", "measuring spoon",
            "measuring spoons"
        }

        filtered_equipment = [
            item for item in found
            if not any(banned in item.lower() for banned in banned_terms)
        ]

        print("Returning equipment:", filtered_equipment)
        return jsonify({"equipment": filtered_equipment})

    except Exception as e:
        print("Error:", e)
        traceback.print_exc()
        return jsonify({"error": "Something went wrong with the API call"}), 500

if __name__ == '__main__':
    app.run(debug=True)
