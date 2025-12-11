from dotenv import load_dotenv
import os
import streamlit as st 
from textblob import TextBlob
import pandas as pd
import google.generativeai as genai

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash-lite")

def generate_response(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        msg = str(e).lower()
        if "quota" in msg or "limit" in msg:
            return "It seems we have reached the API quota limit. Please try again later."
        return f"An error occurred: {e}"

# SENTIMENT ANALYZE
def analyze_sentiment(text):
    text_lower = text.lower()

    # --- Keyword Dictionaries ---
    very_negative_words = [
        "hopeless", "terrible", "depressed", "suicidal", "can't handle", "worthless",
        "miserable", "devastated"
    ]
    
    negative_words = [
        "sad", "disappointed", "disappoints", "scared", "afraid", "anxious", "not good",
        "bad", "upset", "hurt", "pain", "stressed" "No", "not", "never", "none", "nobody", "nothing", "nowhere", "neither", "nor",
        "Don't", "isn't", "aren't", "can't", "won't", "haven't", "Awful"
    ]
    
    positive_words = [
        "happy", "good", "great", "excited", "feeling better",
        "joy", "glad", "love", "good mood", "love", "hope", "amazing", "brilliant", "confident", "successful", "kind", 
        "strong", "vibrant", "excellent", "happy", "peaceful", "inspiring"
    ]

    
    if any(word in text_lower for word in very_negative_words):
        return "Very Negative", -0.8

    
    has_negative = any(word in text_lower for word in negative_words)
    has_positive = any(word in text_lower for word in positive_words)

    if has_negative and has_positive:
        return "Mixed Feelings", 0.0

    
    if has_negative:
        return "Negative", -0.4

    if has_positive:
        return "Positive", 0.5

    
    analysis = TextBlob(text)
    score = analysis.sentiment.polarity

    
    if score > 0.5:
        label = "Very Positive"
    elif score > 0.1:
        label = "Positive"
    elif score >= -0.1:
        label = "Neutral"
    elif score > -0.5:
        label = "Negative"
    else:
        label = "Very Negative"

    return label, round(score, 3)
