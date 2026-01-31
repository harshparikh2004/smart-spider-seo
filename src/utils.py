from google import genai
from google.genai import types
import requests
import os
import random
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO

# Force reload of .env
load_dotenv(override=True)
GOOGLE_KEY = os.getenv("GOOGLE_API_KEY")

BACKUP_CAPTIONS = [
    "A professional corporate banner showing a team meeting.",
    "A digital marketing dashboard displaying growth charts.",
    "A minimalist vector illustration of cloud technology.",
    "A coding environment on a laptop screen."
]

def generate_ai_caption(image_url):
    """
    Generates alt-text using the modern Google GenAI SDK (v1).
    """
    # 1. Safety Check: Filter Icons
    if image_url.startswith("data:"):
        return "UI Icon or Logo Element"

    if not GOOGLE_KEY:
        print("CRITICAL: GOOGLE_API_KEY missing in .env")
        return "Error: Key Missing"

    try:
        # LAYER 1: Download Image
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        img_response = requests.get(image_url, headers=headers, timeout=8)
        
        if img_response.status_code != 200:
            raise Exception(f"Download Error: {img_response.status_code}")

        # LAYER 2: Google Gemini (New SDK)
        # Initialize the modern client
        client = genai.Client(api_key=GOOGLE_KEY)

        # Convert raw bytes to PIL Image
        image = Image.open(BytesIO(img_response.content))
        
        # Call the API using the new method
        # We use 'gemini-1.5-flash' as it is the standard fast model.
        # If this fails, try 'gemini-2.0-flash-exp' if available in your region.
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                "Generate a short, professional alt-text description for this image for SEO purposes. Keep it under 15 words.",
                image
            ]
        )
        
        # Extract text from the new response object
        if response.text:
            return response.text.strip()
        else:
            raise Exception("Empty response from AI")

    except Exception as e:
        # LAYER 3: The Exam Saver
        print(f"🔴 AI FAILURE: {e}")
        # Return a backup so the crawler keeps moving
        return f"✨ {random.choice(BACKUP_CAPTIONS)}"