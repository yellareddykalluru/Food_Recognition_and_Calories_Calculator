import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# Configure Gemini API Key (Replace with your actual key)
API_KEY = "AIzaSyDQnQA2Ah73lidOqvlqob6BKHwriL6G7Ws"
genai.configure(api_key=API_KEY)

def recognize_food_and_calories(image_bytes):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Define the prompt
        prompt = """Analyze the given food image and provide:
        1. The name of the food item.
        2. An estimated calorie count per serving.
        Respond in this format:
        Food: <name> and next like more details and print the calories in new line always
        Calories: <value> kcal"""

        # Corrected way to send the image
        response = model.generate_content([
            prompt,
            {"mime_type": "image/jpeg", "data": image_bytes}
        ])

        # Extract response text
        result_text = response.text.strip()
        return result_text
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit UI
st.title("🍔 AI-Powered Food & Calorie Detector")

uploaded_file = st.file_uploader("Upload a food image", type=["jpg", "png", "jpeg", "webp"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Convert image to bytes
    img_bytes = io.BytesIO()
    image.save(img_bytes, format="JPEG")
    img_bytes = img_bytes.getvalue()

    # Get food & calories from Gemini
    result = recognize_food_and_calories(img_bytes)
    
    # Display result
    st.subheader("🔍 AI Detection Result")
    st.write(result)
