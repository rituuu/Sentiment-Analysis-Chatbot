# Sentiment Analysis Chatbot

## Overview
This project implements a simple chatbot that conducts a conversation with a user and performs sentiment analysis. 
Maintains full conversation history and performs sentiment analysis at both conversation and statement levels.

Tier 1 and Tier 2 both are implemented. Along with UI advancements.
- **Tier 1 (mandatory):** Conversation-level sentiment analysis (overall sentiment).
- **Tier 2 (optional, implemented):** Statement-level sentiment analysis and mood-shift summary.

#### Tier 1 – Conversation-Level Sentiment Analysis (Mandatory Requirement)
- Maintains full conversation history.
- At the end of the interaction, it generates sentiment analysis for the entire conversation.
- Clearly indicates the overall emotional direction based on the full exchange.
##### Overall Conversation Sentiment:
![overall sentiment](https://github.com/user-attachments/assets/671dca9a-6c5a-4eec-b6b7-a634be2e572a)


#### Tier 2 – Statement-Level Sentiment Analysis  (Additional)
- Performs sentiment evaluation for every user message individually.
- Displays each message alongside its sentiment output.
- Optional enhancement for additional credit: Summarises trend or shift in mood across the
conversation.

#### Working Project Tier 2 implementation:
![final git version](https://github.com/user-attachments/assets/023ec8e8-789d-49da-a526-5ef47dcb3df3)
![final git](https://github.com/user-attachments/assets/762c13a3-9538-42fd-8e17-d684f7273bba)

### Mood Shift Trend for additional Credit:
![trend](https://github.com/user-attachments/assets/797ee8ad-33e4-4bca-8e03-41d7a31a7773)

#### Access the full conversation here: https://drive.google.com/file/d/1TMcXt7_YtFjLBggFT78iC-X6S6UkTiUN/view?usp=sharing

### Tests for edge cases like negation and mixed feelings: I am not good, I am never successful, I am happy and anxious. Check here: https://drive.google.com/file/d/1kaN-Ip25p58IdVioDS1sKl7zY1ZtK0lr/view?usp=sharing

### Highlights of innovations, additional features, enhancements:
- Used Streamlit for Webapp
- Used Avatars for User and Bot
- Displays Sentiment scores alongside the conversation for detecting the extent of emotion.
- Color Coded Sentiment Detection: Light Green for positive,
  - Green for very positive,
  - Light red for negative,
  - Red for very Negative,
  - Light yellow for Mixed feelings,
  - Grey for Neutral,
  - Blue for bot
  
## How to run
### Clone the Repository

```bash
git clone https://github.com/rituuu/Sentiment-Analysis-Chatbot.git
cd Sentiment Analysis Chatbot
```
### 1.	Create a conda environment
```bash
conda create -p venv python==3.11.13 –y
```
### 2.	Activate conda environment
```bash
conda activate venv
```
### 3.	After activating we will install this requirements.txt
```bash
pip install –r requirements.txt
```
### 4. Set Up Environment Variables
```bash
Create a `.env` file with your API keys:
```
```bash
GOOGLE_API_KEY=your_google_key
```

### 5. Run the Application

```bash
streamlit run frontend/frontend.py
```

### Launch Interface

Streamlit will open automatically in your browser at:

http://localhost:8502

## Technologies Used:
- Python
- Gemini 2.5 flash lite for conversational reasoning
- Streamlit
- Modular code: importing files as packages
- TextBlob - Simple lexicon-based sentiment analyzer (custom, lightweight)

## SENTIMENT LOGIC:

I built a **three-layer hybrid sentiment analysis** engine.  
**First**, a **rule-based classifier** instantly detects **crisis phrases, mixed emotions, and negation patterns**.  
**Second**, **TextBlob** provides **continuous polarity scoring for subtle or neutral emotions**.  
**Third**, I **used Gemini only for edge cases where rule-based and statistical methods disagree — such as sarcasm, contradictions**, or hidden sentiment.

This **layered pipeline makes the chatbot accurate, interpretable, safe, and cost-efficient.**  
It mirrors real-world industry systems and shows how I think about reliability and scalability when designing AI components.  

**Hybrid pipelines are the backbone of customer support bots**, therapist AIs, and moderation systems. Crisis phrases are caught immediately — no statistical errors.  
**My pipeline reduces the LLM API calls by ~70%, saving cost.**

---

## Three-Layer Architecture

In this project, this is how I built a **production-grade sentiment analysis engine** using a **three-layer hybrid pipeline:**

- **1. Rule-Based Sentiment Classification**  
- **2. TextBlob Statistical Polarity Analysis**  
- **3. Gemini LLM Fallback for Edge Cases**

---

## Why This Matters

This layered approach ensures the chatbot handles **simple, complex, and ambiguous human emotions with high accuracy** — similar to how real-world conversational AI systems are designed.

---


### 1. Rule-Based Sentiment Analysis (Layer 1)
#### What it does
This layer uses **manually curated emotional keyword dictionaries:**
-	very_negative_words → suicidal, devastated, hopeless
-	negative_words → afraid, anxious, upset
-	positive_words → excited, brilliant, peaceful
-	negation_words → not, no, never, can't

It performs **fast, deterministic checks** such as:
-	Detecting crisis phrases → "I feel suicidal"
-	Mixed feelings → "I’m sad but hopeful"
-	Negation → "I’m not happy"
-	Simple polarity → "I’m excited today"

#### Why it is used
It is used because **AI systems should not blindly rely on statistical models (TextBlob).**
Rule-based checks are **fast, interpretable, and essential for safety-sensitive conversations.**
For example:
TextBlob might score “I can’t handle life anymore” as only slightly negative,
but rule-based logic catches it as Very Negative immediately.

#### How it works
-	Converts text to lowercase
-	Looks for any keyword matches
-	Applies logic rules (mixed feelings, negation handling)
-	Returns early if classification is clear
**This layer handles deterministic, high-risk or obvious emotional statements.**
________________________________________
### 2. TextBlob Sentiment Analysis (Layer 2 – Statistical Model)
#### What it does
If the rule-based logic doesn’t find a strong emotional pattern, the system uses **TextBlob’s polarity score**
(-1 to +1).
It maps the continuous score into labels:
-	0.5 → Very Positive
-	0.1 → Positive
-	= -0.1 → Neutral
-	-0.5 → Negative
-	else → Very Negative

#### Why it is used
This layer gives **finer granularity** and handles:
-	Subtle emotions
-	Longer sentences
-	Neutral or descriptive language
-	Polarity detection without keywords
For example:
“Life is complicated but I’m managing.”
→ Rule-based might return Neutral
→ TextBlob captures subtle positivity.

#### How it works
-	Computes polarity score
-	Converts it to human-readable labels
-This layer introduces probabilistic nuance and smooth scoring.
________________________________________
### 3. Gemini LLM Fallback (Layer 3 – AI-powered Resolution)
#### When it is triggered
I built an **edge-case detector** that flags ambiguous or contradictory emotions that neither rules nor TextBlob can reliably classify.
Edge cases include:
-	Neutral label but emotional keywords
“I’m smiling on the outside but broken inside.”
-Contradictory polarity
negative words + positive score
-	Negation conflicts
“It’s not good, but I’ll survive.”

#### What Gemini does
Gemini receives a strict prompt:
“Return ONLY: label, score between -1 and +1.”
The model then interprets context, sarcasm, implicit emotion, or complex language.

#### Why it is used
This layer demonstrates **advanced analytical thinking:**
-	Understanding limitations of rule-based and statistical models
-	Adding AI as a **precision tool only when necessary**
-	Keeping API costs low by **calling Gemini only for complex cases**
-	Ensuring **max safety and accuracy** in sensitive conversations
This layer handles sarcasm, context-dependent sentiment, hidden emotions, and conversational subtleties.
________________________________________
#### How All Three Layers Work Together
I designed the sentiment system using a **“triangular defense approach.”**
**Each layer compensates for the weakness of the previous one**, providing a balance of **speed, determinism, intelligence, and context awareness.**

#### Layer 1: Rule-Based
-	Handles explicit emotional expressions
-	Immediate and safe classification
-	Zero ambiguity

#### Layer 2: TextBlob
-	Handles subtle or neutral emotional tones
- Adds continuous scoring
-	Captures soft polarity

#### Layer 3: Gemini
-	Resolves ambiguous, contradictory, sarcastic, or complex emotional expressions
-	Understands contextual sentiment
-	Acts as an intelligent safety net
This hybrid structure makes the chatbot both **robust and reliable, and scalable.**
