import os
import requests
import random
import csv
from groq import Groq

# GitHub Secrets থেকে ডাটা নেওয়া
PINTEREST_TOKEN = os.environ.get('PINTEREST_TOKEN')
GOOGLE_SHEET_ID = os.environ.get('GOOGLE_SHEET_ID')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

client = Groq(api_key=GROQ_API_KEY)

def get_sheet_data():
    """গুগল শিট থেকে ডেটা রিড করা"""
    url = f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}/export?format=csv"
    response = requests.get(url)
    content = response.text.splitlines()
    reader = csv.DictReader(content)
    return list(reader)

def get_ai_description(product_name):
    """Groq AI দিয়ে ইউনিক ডেসক্রিপশন তৈরি"""
    prompt = f"Create a viral Pinterest description for '{product_name}'. Use a professional tone for USA audience with 3 hashtags."
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content

def post_to_pinterest(image_url, title, description, link):
    """পিন্টারেস্ট এপিআই ব্যবহার করে সরাসরি পোস্ট করা"""
    post_url = "https://api.pinterest.com/v5/pins"
    headers = {
        "Authorization": f"Bearer {PINTEREST_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # পিন্টারেস্টের জন্য পে-লোড (বোর্ড আইডি অটোমেটিক হ্যান্ডেল হবে যদি আপনার টোকেন পারমিশন থাকে)
    data = {
        "title": title,
        "description": description,
        "link": link,
        "media_source": {
            "source_type": "image_url",
            "url": image_url
        }
    }
    
    response = requests.post(post_url, headers=headers, json=data)
    return response.status_code

def run_bot():
    print("🚀 Starting Pinterest Automation...")
    data = get_sheet_data()
    
    for row in data:
        if row['Status'].lower() == 'pending':
            product = row['Product Name']
            img = row['Image URL']
            affiliate_link = row['Target URL']
            
            print(f"📦 Processing: {product}")
            
            # AI ডেসক্রিপশন তৈরি
            desc = get_ai_description(product)
            
            # পিন্টারেস্টে পোস্ট
            status = post_to_pinterest(img, product, desc, affiliate_link)
            
            if status == 201:
                print(f"✅ Successfully posted {product} to Pinterest!")
            else:
                print(f"❌ Failed to post {product}. Status Code: {status}")
            
            # টেস্ট রানের জন্য আপাতত একটি করে পোস্ট হবে
            break

if __name__ == "__main__":
    run_bot()
