# 🎨 AI Comic Strip Generator

This project generates a 4-panel comic strip (text + images) based on a user-provided story idea and tone using Generative AI.

## Project Overview

The user enters a story concept on a simple web interface. The Flask backend then communicates with two AI APIs:
1.  **Hugging Face Inference API**: To generate a creative 4-panel script with captions and detailed image descriptions.
2.  **Stability AI API**: To generate an image for each of the four panel descriptions.

The final comic strip is displayed on the webpage, with an option to save it as a PDF.

## Technologies Used
- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript
- **AI APIs**:
    - Stability AI API (for Image Generation)
    - Hugging Face Inference API (for Text Generation)
- **Add-ons**: jsPDF and html2canvas for PDF generation.

## Setup and Installation

Follow these steps to get the project running on your local machine.

### Prerequisites
- Python 3.8 or higher
- `pip` (Python package installer)
- Access to a web browser

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd comic-strip-generator
```

### 2. Create a Virtual Environment
It's highly recommended to use a virtual environment to manage project dependencies.
```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
Install all the required Python packages from the `requirements.txt` file.
```bash
pip install -r requirements.txt
```

### 4. Set Up API Keys
This project requires API keys from Stability AI and Hugging Face.

1.  **Create a `.env` file** in the root directory of the project (`comic-strip-generator/`).
2.  **Get your API keys:**
    - **Stability AI**: Go to the [Stability AI Platform](https://platform.stability.ai/account/keys) and get your API key.
    - **Hugging Face**: Go to your [Hugging Face profile settings](https://huggingface.co/settings/tokens) and create an Access Token.
3.  **Add the keys to your `.env` file** like this:

    ```
    STABILITY_API_KEY="your_stability_ai_api_key_here"
    HUGGINGFACE_API_TOKEN="your_huggingface_api_token_here"
    ```

### 5. Run the Flask Application
Once the setup is complete, you can run the application with a single command:
```bash
flask run
```

Open your web browser and navigate to `http://127.0.0.1:5000` to see the application in action!
# comicstrip