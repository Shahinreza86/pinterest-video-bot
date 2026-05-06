import os
import requests
import random
import time
from groq import Groq

# Secrets from GitHub
PINTEREST_TOKEN = os.environ.get('PINTEREST_TOKEN')
GOOGLE_SHEET_ID = os.environ.get('GOOGLE_SHEET_ID')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

client = Groq(api_key=GROQ_API_KEY)

def get_unique_description(product_name):
    """Groq AI ব্যবহার করে ইউনিক এবং প্রফেশনাল ডেসক্রিপশন তৈরি"""
    prompt = f"Write a catchy, high-converting Pinterest description for a product named '{product_name}'. Use a professional yet exciting tone for USA/Europe audience. Include a hook and 3 relevant hashtags."
    
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return completion.choices[0].message.content

def post_to_pinterest():
    # এখানে আপনার ভিডিও তৈরির লজিক এবং পিন্টারেস্ট এপিআই কল থাকবে
    # বর্তমানে আমরা একটি টেস্ট পিন রান করার জন্য বেসিক স্ট্রাকচার রাখছি
    print("AI Video Generation Started...")
    # আপনার গুগল শিট থেকে ডাটা রিড করার কোড এখানে যুক্ত হবে
    
    # উদাহরণস্বরূপ একটি ইউনিক ডেসক্রিপশন জেনারেট করা
    desc = get_unique_description("Smart Kitchen Organizer")
    print(f"Generated Description: {desc}")
    print("Post successfully sent to Pinterest!")

if __name__ == "__main__":
    post_to_pinterest()
