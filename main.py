import time
import PIL.Image
from google import genai
from google.api_core import exceptions

# 1. Configuration & Client Setup
# Get your API key: https://aistudio.google.com/
API_KEY = "YOUR API_KEY"
client = genai.Client(api_key=API_KEY)
MODEL_ID = "gemini-2.5-flash-lite"


def chat_with_vision(image_path, user_query):
    """
    Sends an image and text to Gemini with error handling for rate limits.
    """
    try:
        img = PIL.Image.open(image_path)
        img.thumbnail((1024, 1024))

        for attempt in range(5):
            try:
                print(f"Analyzing image (Attempt {attempt + 1})...")

                response = client.models.generate_content(
                    model=MODEL_ID,
                    contents=[user_query, img]
                )
                return response.text

            except exceptions.ResourceExhausted:
                wait = (2 ** attempt) + 2
                print(f"Rate limit hit (429). Retrying in {wait}s...")
                time.sleep(wait)

        return "Error: Maximum retries exceeded due to rate limits."

    except Exception as e:
        return f"An unexpected error occurred: {e}"


# 2. Execution
if __name__ == "__main__":
    # Path to the image
    IMAGE_FILE = "sample_image.jpg"

    print("--- Welcome to Project 17: Multimodal Vision Bot ---")
    prompt = "What is happening in this image? List all visible objects and any text you find."

    result = chat_with_vision(IMAGE_FILE, prompt)

    print("\n--- AI Response ---")
    print(result)