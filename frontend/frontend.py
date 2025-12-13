import streamlit as st
from textblob import TextBlob
import pandas as pd
import google.generativeai as genai
from app.chatbot import generate_response, analyze_sentiment

# STREAMLIT WEB APP UI
st.title("Sentiment Analysis Chatbot")

if "conversation" not in st.session_state:
    st.session_state["conversation"] = []  # full chat history

if "sentiments" not in st.session_state:
    st.session_state["sentiments"] = []  # list of (msg, score, label)

def get_color(label):
    color_map = {
        "Positive": "#d4fcd4",       # light green
        "Very Positive": "#b2fab4",
        "Negative": "#ffd6d6",       # light red
        "Very Negative": "#ffb3b3",
        "Mixed Feelings": "#fff4cc", # light yellow
        "Neutral": "#e6e6e6"         # grey
    }
    return color_map.get(label, "#e6e6e6")


# AVATARS
USER_AVATAR = "🧑"
BOT_AVATAR  = "🤖"

# USER INPUT FORM
with st.form("chat_form"):
    user_input = st.text_input("You:")    # user input
    send = st.form_submit_button("Send")

if send and user_input:
    # Store user message
    st.session_state["conversation"].append(("User", user_input))

    # Sentiment analysis for this message
    label, score = analyze_sentiment(user_input)
    st.session_state["sentiments"].append((user_input, score, label))

    # Bot Reply using Gemini Reasoning
    bot_reply = generate_response(user_input)
    st.session_state["conversation"].append(("Bot", bot_reply))

st.subheader("Conversation")

for (speaker, msg), (_, score, label) in zip(
    st.session_state["conversation"][::2], 
    st.session_state["sentiments"]
):
    # Only user messages get sentiment color
    bg = get_color(label)

    # USER
    st.markdown(
        f"""
        <div style='padding:10px; border-radius:10px; margin-bottom:5px; background-color:{bg};'>
            <b>{USER_AVATAR} You:</b> {msg} <br>
            <small><i>Sentiment: {label} (score: {round(score,3)})</i></small>
        </div>
        """,
        unsafe_allow_html=True
    )

    # BOT
    bot_msg = st.session_state["conversation"][st.session_state["conversation"].index((speaker, msg)) + 1][1]
    st.markdown(
        f"""
        <div style='padding:10px; border-radius:10px; margin-bottom:12px; background-color:#e8f0fe;'>
            <b>{BOT_AVATAR} Bot:</b> {bot_msg}
        </div>
        """,
        unsafe_allow_html=True
    )

# CONVERSATION-LEVEL SENTIMENT (Tier 1)
if st.button("Show Overall Conversation Sentiment"):
    st.subheader("Overall Conversation Sentiment (Tier 1)")
    
    if st.session_state["sentiments"]:
        scores = [s for (_, s, _) in st.session_state["sentiments"]]
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

# MOOD SHIFT TREND
if st.button("Show Mood Shift Trend"):
    st.subheader("Mood Shift Across Conversation (Tier 2 Bonus)")

    sentiments = st.session_state["sentiments"]
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
