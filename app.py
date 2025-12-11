import streamlit as st 
from textblob import TextBlob
import pandas as pd
import google.generativeai as genai

# ------------------------------
# CONFIGURE GEMINI
# ------------------------------
genai.configure(api_key="AIzaSyDitGXGWuy-tGmjYdwjHhudRzFcBVpFiHw")
model = genai.GenerativeModel("gemini-2.5-flash")

# ------------------------------
# GEMINI RESPONSE FUNCTION
# ------------------------------
def generate_response(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        msg = str(e).lower()
        if "quota" in msg or "limit" in msg:
            return "It seems we have reached the API quota limit. Please try again later."
        return f"An error occurred: {e}"

# ------------------------------
# SENTIMENT ANALYSIS
# ------------------------------
def analyze_sentiment(text):
    text_lower = text.lower()

    # --- Keyword Dictionaries ---
    very_negative_words = [
        "hopeless", "terrible", "depressed", "suicidal", "can't handle", "worthless",
        "miserable", "devastated"
    ]
    
    negative_words = [
        "sad", "disappointed", "disappoints", "scared", "afraid", "anxious", "not good",
        "bad", "upset", "hurt", "pain", "stressed"
    ]
    
    positive_words = [
        "happy", "good", "great", "excited", "feeling better",
        "joy", "glad", "love", "good mood"
    ]

    # --- Rule 1: Check for strong negative first ---
    if any(word in text_lower for word in very_negative_words):
        return "Very Negative", -0.8

    # --- Rule 2: Check for mixed emotions ---
    has_negative = any(word in text_lower for word in negative_words)
    has_positive = any(word in text_lower for word in positive_words)

    if has_negative and has_positive:
        return "Mixed Feelings", 0.0

    # --- Rule 3: Check clear positive or negative ---
    if has_negative:
        return "Negative", -0.4

    if has_positive:
        return "Positive", 0.5

    # --- Rule 4: Fallback to TextBlob ---
    analysis = TextBlob(text)
    score = analysis.sentiment.polarity

    # TextBlob final mapping (adjusted)
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


# ------------------------------
# STREAMLIT UI
# ------------------------------
st.title("Sentiment Analysis Chatbot")

# Initialize session state
if 'conversation' not in st.session_state:
    st.session_state['conversation'] = []   # full chat history
if 'sentiments' not in st.session_state:
    st.session_state['sentiments'] = []     # list of (msg, score, label)

# ------------------------------
# USER INPUT FORM
# ------------------------------
with st.form("chat_form"):
    user_input = st.text_input("You:")
    send = st.form_submit_button("Send")

if send and user_input:
    # Store user message
    st.session_state['conversation'].append(("User", user_input))

    # Sentiment for this message (Tier 2)
    label, score = analyze_sentiment(user_input)
    st.session_state['sentiments'].append((user_input, score, label))

    # Bot Reply using Gemini
    bot_reply = generate_response(user_input)
    st.session_state['conversation'].append(("Bot", bot_reply))

# ------------------------------
# DISPLAY CHAT HISTORY
# ------------------------------
st.subheader("Conversation")
for speaker, msg in st.session_state['conversation']:
    if speaker == "User":
        st.write(f"**User:** {msg}")
    else:
        st.write(f"**Bot:** {msg}")

# ------------------------------
# STATEMENT-LEVEL SENTIMENT (Tier 2)
# ------------------------------
if st.session_state['sentiments']:
    st.subheader("Statement-Level Sentiments (Tier 2)")
    for msg, score, label in st.session_state['sentiments']:
        st.write(f"User: \"{msg}\" → **Sentiment: {label}** *(score = {round(score,3)})*")

# ------------------------------
# CONVERSATION-LEVEL SENTIMENT (Tier 1)
# ------------------------------
if st.button("Show Overall Conversation Sentiment"):
    st.subheader("Overall Conversation Sentiment (Tier 1)")

    if st.session_state['sentiments']:
        scores = [s for (_, s, _) in st.session_state['sentiments']]
        avg = sum(scores) / len(scores)

        # Label for whole conversation
        if avg > 0.1:
            overall_label = "Overall Positive — user is generally satisfied."
        elif avg < -0.1:
            overall_label = "Overall Negative — general dissatisfaction."
        else:
            overall_label = "Overall Neutral — mixed or unclear emotion."

        st.write(f"**Average Sentiment Score:** {round(avg, 3)}")
        st.write(f"**Overall Conversation Sentiment:** {overall_label}")
    else:
        st.write("No user messages yet.")

# ------------------------------
# MOOD SHIFT TREND (Tier 2 Optional)
# ------------------------------
if st.button("Show Mood Shift Trend"):
    st.subheader("Mood Shift Across Conversation (Tier 2 Bonus)")

    sentiments = st.session_state['sentiments']
    if len(sentiments) < 3:
        st.write("Not enough data to compute mood shift.")
    else:
        scores = [s for (_, s, _) in sentiments]
        n = len(scores)
        start_avg = sum(scores[:n//3]) / (n//3)
        end_avg = sum(scores[-(n//3):]) / (n//3)
        delta = end_avg - start_avg

        if delta > 0.1:
            trend = "Mood is improving"
        elif delta < -0.1:
            trend = "Mood is declining"
        else:
            trend = "Mood is stable"

        st.write(f"Start Avg: {round(start_avg,3)}")
        st.write(f"End Avg: {round(end_avg,3)}")
        st.write(f"Change: {round(delta,3)}")
        st.write(f"**Trend:** {trend}")

