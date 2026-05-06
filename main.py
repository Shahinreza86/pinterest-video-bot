import os
from groq import Groq

# গিটহাব সিক্রেট থেকে এপিআই কী নেওয়া হবে
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

def generate_description(product):
    client = Groq(api_key=GROQ_API_KEY)
    prompt = f"Create a viral Pinterest title and 1-line description for: {product}. Use hashtags."
    
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content

print("Pinterest Bot System Initialized!")
# আপনার শিট থেকে ডাটা পড়ার অংশটি আমরা এরপরে যোগ করব
