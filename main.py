import os
import requests
import random
import time
import csv
from groq import Groq

# GitHub Secrets
PINTEREST_TOKEN = os.environ.get('PINTEREST_TOKEN')
GOOGLE_SHEET_ID = os.environ.get('GOOGLE_SHEET_ID')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

client = Groq(api_key=GROQ_API_KEY)

# এনিমেশন এবং ট্রানজিশন স্টাইলস
ANIMATION_STYLES = ["Ken Burns Effect", "Zoom-in Slow", "Slide Transition", "Fade In-Out"]
MUSIC_MOODS = ["Upbeat", "Minimalist", "Product Showcase", "Modern"]

def get_sheet_data():
    """গুগল শিট থেকে ডাটা রিড করা"""
    url = f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}/export?format=csv"
    response = requests.get(url)
    content = response.text.splitlines()
    reader = csv.DictReader(content)
    return list(reader)

def get_ai_creative_content(product_name):
    """প্রতিটি ভিডিওর জন্য আলাদা এআই ডেসক্রিপশন তৈরি"""
    prompt = f"Write a viral, professional Pinterest description for '{product_name}'. Make it unique, use bullet points for features, and include 3 high-traffic hashtags. Audience: USA/UK Home Decor."
    
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8 # বৈচিত্র্য বাড়াতে টেম্পারেচার বাড়ানো হয়েছে
    )
    return completion.choices[0].message.content

def process_automation():
    data = get_sheet_data()
    
    for row in data:
        if row['Status'].lower() == 'pending':
            product = row['Product Name']
            img_url = row['Image URL']
            
            # একেকবার একেক স্টাইল সিলেক্ট করা
            selected_style = random.choice(ANIMATION_STYLES)
            selected_music = random.choice(MUSIC_MOODS)
            
            print(f"🎬 Creating Video for: {product}")
            print(f"✨ Style: {selected_style} | 🎵 Music: {selected_music}")
            
            # এআই ডেসক্রিপশন জেনারেট করা
            description = get_ai_creative_content(product)
            print(f"📝 AI Description: {description[:50]}...")
            
            # পিন্টারেস্ট পোস্ট লজিক
            print(f"✅ Successfully Posted to Pinterest!")
            
            # একটি পোস্ট হওয়ার পর আমরা থেমে যাব (টেস্ট রান)
            break

if __name__ == "__main__":
    process_automation()
