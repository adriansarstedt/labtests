import os
from openai import OpenAI
import base64

# Initialize OpenAI client
client = OpenAI(api_key="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")

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
image_path = "labcorpresults.png"

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
                {"type": "image_url", "image_url": {"url": "data:image/png;base64," + base64_image}}
            ]
        }
    ],
    max_tokens=1000
)

# Print the result
print(response.choices[0].message.content)
