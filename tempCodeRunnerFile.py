import os

from dotenv import load_dotenv
from groq import Groq


# Load environment variables
load_dotenv()

# Retrieve the API key
api_key = os.getenv("GROQ_API_KEY")

# Check whether the API key exists
if not api_key:
    raise ValueError("GROQ_API_KEY not found!")

# Create the Groq client
client = Groq(api_key=api_key)

print("Groq client initialized successfully!")
response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {
            "role": "user",
            "content": "What are five types of businesses that need inventory management software?"
        }
    ]
)

print(response.choices[0].message.content)