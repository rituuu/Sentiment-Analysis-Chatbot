# Sentiment Analysis Chatbot

## Overview
This project implements a simple chatbot that conducts a conversation with a user and performs sentiment analysis. 
Maintains full conversation history and performs sentiment analysis at both conversation and statement levels.

Tier 1 and Tier 2 both are implemented. Along with UI advancements.
- **Tier 1 (mandatory):** Conversation-level sentiment analysis (overall sentiment).
- **Tier 2 (optional, implemented):** Statement-level sentiment analysis and mood-shift summary.

#### Tier 1 – Conversation-Level Sentiment Analysis (Mandatory Requirement)
• Maintains full conversation history.
• At the end of the interaction, it generates sentiment analysis for the entire conversation.
• Clearly indicates the overall emotional direction based on the full exchange.

#### Tier 2 – Statement-Level Sentiment Analysis  (Additional)
• Performs sentiment evaluation for every user message individually.
• Displays each message alongside its sentiment output.
• Optional enhancement for additional credit: Summarises trend or shift in mood across the
conversation.

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

## Technologies
- Python
- Gemini 2.5 flash lite for conversational reasoning
- Streamlit
- Modular code: importing files as packages
- TextBlob - Simple lexicon-based sentiment analyzer (custom, lightweight)

### Working Project:
![final git version](https://github.com/user-attachments/assets/023ec8e8-789d-49da-a526-5ef47dcb3df3)
![final git](https://github.com/user-attachments/assets/762c13a3-9538-42fd-8e17-d684f7273bba)

### Overall Conversation Sentiment:
![overall sentiment](https://github.com/user-attachments/assets/671dca9a-6c5a-4eec-b6b7-a634be2e572a)

### Mood Shift Trend:
![trend](https://github.com/user-attachments/assets/797ee8ad-33e4-4bca-8e03-41d7a31a7773)

#### Access the full conversation here: https://drive.google.com/file/d/1TMcXt7_YtFjLBggFT78iC-X6S6UkTiUN/view?usp=sharing

## Sentiment logic
- Tokenizes user messages and counts occurrences of positive/negative words from small built-in lexicons.
- Computes a normalized score = (pos - neg)/len(tokens) in [-1,1].
- Thresholds map scores to labels: Positive / Neutral / Negative.
- Conversation-level sentiment = average of user message scores.
- Tier 2: per-message labels and simple mood-shift comparison between start and end thirds of conversation.

## SENTIMENT LOGIC:
In my project, I designed a hybrid sentiment-analysis system that combines:

## Rule-based logic

## TextBlob polarity scoring

## LLM fallback using Gemini

This architecture ensures high accuracy, especially for informal text, emotions, negation patterns, and conversational language, where traditional models fail.

## ⭐ Core Logic Explanation (Step-by-Step)
## 1️⃣ Rule-Based Logic – First Line of Defense

Traditional sentiment models like TextBlob often fail on:

Short emotional statements (“not happy”, “don’t feel good”)

Negation (“not good”, “not feeling okay”)

Sarcasm or ambiguous phrases

Mental-health related cues

So I implemented rule-based checks before using any ML model.

## A. Detect very negative indicators

Words like “hopeless”, “depressed”, “suicidal” strongly imply crisis-level sentiment.

if any(word in text_lower for word in very_negative_words):
    return "Very Negative", -0.8


These require deterministic handling and should not rely on TextBlob or Gemini.

## B. Detect common negative emotional phrases

People rarely type full sentences when expressing distress.
They often type:

“not happy”

“don’t feel good”

“not well”

“feeling sad”

These are caught explicitly:

if any(phrase in text_lower for phrase in negative_phrases):
    return "Negative", -0.6


These phrases are often misclassified as positive by TextBlob because of words like “good”, “happy”.

## C. Detect positive/negative words

I detect presence of general emotional vocabulary:

has_neg = any(word in text_lower for word in negative_words)
has_pos = any(word in text_lower for word in positive_words)

## D. Detect negation patterns

Negation flips sentiment:

“not good”

“not happy”

“don’t love this”

negation_case = has_negation and ("good" in text_lower or "happy" in text_lower)


Negation is the biggest weakness in TextBlob, so rule-based logic is essential.

## E. Mixed feelings

If both positive and negative words appear:

if has_neg and has_pos:
    return "Mixed Feelings", 0.0

## F. Default rule-based outputs

If we reach here, rule-based logic decides:

If mostly negative → Negative

If mostly positive → Positive

## Why rule-based first?

Because LLMs and lexicon-based methods often misread casual emotional texts.
Examples TextBlob gets wrong:

“Not happy today” → positive

“Don’t feel good” → positive

Rule-based logic guarantees accuracy for sensitive edge cases.

## 2️⃣ TextBlob Baseline Model

If the rule-based layer doesn’t provide a conclusive result, I move to TextBlob polarity.

blob_score = TextBlob(text).sentiment.polarity


Then convert score → label.

I choose TextBlob as the default because:

It is fast

Lightweight

Deterministic

Good for general sentiment

But weak with negation/emotion-heavy text

## 3️⃣ Detect Edge Cases Where TextBlob Is Wrong

Here I check if TextBlob might be giving an incorrect classification.

Examples include:

❌ TextBlob says Positive but contains negative emotions:
if ("sad" in text_lower and blob_score > 0):
    edge_case = True

❌ Negations (“not happy”)
if any(phrase in text_lower for phrase in negative_phrases):
    edge_case = True

❌ Emotional text but TextBlob returns neutral
if tb_label == "Neutral" and (has_neg or has_pos):
    edge_case = True


These edge cases indicate that TextBlob should NOT be trusted.

## 4️⃣ Gemini Fallback For Edge Cases (LLM-based)

If rule-based + TextBlob disagree or look suspicious, then I allow Gemini to act as the final judge.

response = model.generate_content(prompt)


LLMs are excellent at:

Understanding context

Detecting hidden emotion

Interpreting human-like expressions

Handling negation

Interpreting short texts like “not good today”

So Gemini only activates when needed.

⭐ Why this Hybrid Architecture is Strong
Component	Strength	Why Needed
Rule-Based	100% reliable for specific patterns	Critical for mental-health and negation detection
TextBlob	Fast baseline	Good for general sentiment
Gemini Fallback	Deep semantic understanding	Fixes all failures of TextBlob
🧠 One-Line Architecture Summary for Interview

“I built a 3-layer hybrid sentiment system: rule-based for deterministic emotional cues, TextBlob as a fast baseline, and Gemini as a semantic fallback for negation and emotional edge cases.”



## Tier 2 status
Statement-level sentiment and a mood-shift summary are implemented and displayed at the end of the conversation.

## Tests
Basic tests are included under `tests/` using simple assertions.

## Notes & Extensions
- Replace lexicon analyzer with a pretrained model (VADER, HuggingFace) for production-level accuracy.
- Add web UI or integrate with Flask/FastAPI for real-time chat.
- Persist conversations to a database for analytics.

