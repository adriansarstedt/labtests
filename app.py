import os
from openai import OpenAI
import base64

def process_image(image_path):
    # Initialize OpenAI client
    client = OpenAI(api_key="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")

    # Function to encode the image
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    # Encode the image
    base64_image = encode_image(image_path)

    # Read prompt from file
    with open('prompt.txt', 'r') as file:
        prompt = file.read().strip()

    # Make the API call
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
                ]
            }
        ],
        max_tokens=2000
    )

    # Return the result
    return response.choices[0].message.content


import streamlit as st
import tempfile
import os

st.title("Lab Result Tracker")

uploaded_file = st.file_uploader("Choose an image of lab results...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Create a temporary file to save the uploaded image
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name

    with st.spinner('Reading results...'):
        # Process the image
        result = process_image(tmp_file_path)
    
    # Display the result above the image
    st.subheader("Lab Results:")
    st.write(result)

    # Display the image
    st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)

    # Clean up the temporary file
    os.unlink(tmp_file_path)