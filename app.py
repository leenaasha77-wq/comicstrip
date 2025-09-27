import os
import requests
import base64
import ast
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Load API keys from environment variables
HUGGING_FACE_TOKEN = os.getenv("HUGGING_FACE_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_KEY")

# Initialize the Groq client
client = Groq(api_key=GROQ_API_KEY)

# Hugging Face API URL for text-to-image
# Using a common text-to-image model from Hugging Face
HF_IMAGE_API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
HEADERS_IMAGE = {"Authorization": f"Bearer {HUGGING_FACE_TOKEN}"}


def query_groq(prompt):
    """Sends a request to the Groq API to generate the comic script."""
    if not GROQ_API_KEY:
        raise ValueError("Missing Groq API key.")

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            # Use a model that is available on Groq's platform
            model="openai/gpt-oss-20b",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        raise requests.exceptions.RequestException(f"Groq API request failed: {e}")


def generate_image_huggingface(prompt_text):
    """Sends a request to the Hugging Face API to generate an image."""
    if not HUGGING_FACE_TOKEN:
        raise ValueError("Missing Hugging Face API token.")

    payload = {"inputs": prompt_text}
    response = requests.post(HF_IMAGE_API_URL, headers=HEADERS_IMAGE, json=payload)
    
    if response.status_code == 200:
        # The API returns binary image data. Convert it to base64.
        base64_image = base64.b64encode(response.content).decode("utf-8")
        return base64_image
    else:
        # Raise an exception with the error message from the API
        try:
            error_message = response.json().get("error", "Unknown error")
        except json.JSONDecodeError:
            error_message = response.text
        raise requests.exceptions.HTTPError(f"Hugging Face API: {response.status_code} - {error_message}")


@app.route('/')
def index():
    """Renders the main page."""
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate_comic():
    """Main endpoint to generate the comic strip."""
    try:
        data = request.get_json()
        story_idea = data.get('story_idea')
        tone = data.get('tone', 'funny')

        if not story_idea:
            return jsonify({'error': 'Story idea is required.'}), 400

        prompt = f"""
        You are a creative comic strip writer. Your task is to generate a 4-panel comic strip script based on a user's idea and a specific tone.

        **Story Idea:** "{story_idea}"
        **Tone:** {tone}

        For each of the 4 panels, provide:
        1. A short "caption" which is the dialogue or narration for that panel.
        2. A detailed "description" for an AI image generator. The description should be a visual scene, focusing on characters, actions, setting, and emotions. Do not mention the panel number in the description.

        Provide the output ONLY as a valid Python list of dictionaries, with no other text before or after it.
        Example format:
        [
            {{"panel": 1, "caption": "Caption for panel 1.", "description": "A detailed visual description for panel 1."}},
            {{"panel": 2, "caption": "Caption for panel 2.", "description": "A detailed visual description for panel 2."}},
            {{"panel": 3, "caption": "Caption for panel 3.", "description": "A detailed visual description for panel 3."}},
            {{"panel": 4, "caption": "Caption for panel 4.", "description": "A detailed visual description for panel 4."}}
        ]
        """
        generated_text = query_groq(prompt)

        start_index = generated_text.find('[')
        if start_index == -1:
            return jsonify({'error': 'Failed to parse the script from the text model.'}), 500

        script_str = generated_text[start_index:]

        try:
            panel_scripts = ast.literal_eval(script_str)
        except (SyntaxError, ValueError) as e:
            return jsonify({'error': f'Failed to parse the generated script. Details: {e}'}), 500

        comic_panels_data = []
        for panel in panel_scripts:
            image_prompt = panel['description']
            image_b64 = generate_image_huggingface(image_prompt)

            comic_panels_data.append({
                'caption': panel['caption'],
                'image': image_b64
            })

        return jsonify(comic_panels_data)

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'API request failed: {e}'}), 500
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {e}'}), 500


if __name__ == '__main__':
    app.run(debug=True)