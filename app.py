import os
from openai import OpenAI
import base64
import streamlit as st
import tempfile
from pdf2image import convert_from_path
import io

def process_file(file_path, file_type):
    # Initialize OpenAI client
    client = OpenAI(api_key="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")

    # Function to encode the file
    def encode_file(file_path):
        with open(file_path, "rb") as file:
            return base64.b64encode(file.read()).decode('utf-8')

    # Encode the file
    base64_file = encode_file(file_path)

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
                    {"type": "image_url", "image_url": {"url": f"data:image/{file_type};base64,{base64_file}"}}
                ]
            }
        ],
        max_tokens=2000
    )

    # Return the result
    return response.choices[0].message.content

st.title("Lab Result Tracker")

uploaded_file = st.file_uploader("Choose an image or PDF of lab results...", type=["png", "jpg", "jpeg", "pdf"])

if uploaded_file is not None:
    file_type = uploaded_file.type.split('/')[-1]
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_type}') as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name

    with st.spinner('Reading results...'):
        if file_type == 'pdf':
            # Convert PDF to image
            images = convert_from_path(tmp_file_path)
            img_byte_arr = io.BytesIO()
            images[0].save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            
            # Save the image to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as img_tmp_file:
                img_tmp_file.write(img_byte_arr)
                img_tmp_file_path = img_tmp_file.name
            
            # Process the image
            result = process_file(img_tmp_file_path, 'png')
            os.unlink(img_tmp_file_path)
        else:
            # Process the image directly
            result = process_file(tmp_file_path, file_type)
    
    # Display the result above the file
    st.subheader("Lab Results:")
    st.write(result)

    # Display the file
    if file_type == 'pdf':
        st.write("PDF uploaded. Showing first page:")
        st.image(img_byte_arr, caption='Uploaded PDF (First Page)', use_column_width=True)
    else:
        st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)

    # Clean up the temporary file
    os.unlink(tmp_file_path)