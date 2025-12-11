# Chatbot with Sentiment Analysis

## Overview
This project implements a simple chatbot that maintains full conversation history and performs sentiment analysis at both conversation and statement levels.

- **Tier 1 (mandatory):** Conversation-level sentiment analysis (overall sentiment).
- **Tier 2 (optional, implemented):** Statement-level sentiment analysis and mood-shift summary.

## Technologies
- Python 3 (no external dependencies)
- Modular code: `sentiment.py`, `chatbot.py`, `app.py`
- Simple lexicon-based sentiment analyzer (custom, lightweight)

## How to run
```bash
# from project root
python3 app.py
# Interact in CLI. Type 'exit' or 'quit' to finish and view summary.
```

## Sentiment logic
- Tokenizes user messages and counts occurrences of positive/negative words from small built-in lexicons.
- Computes a normalized score = (pos - neg)/len(tokens) in [-1,1].
- Thresholds map scores to labels: Positive / Neutral / Negative.
- Conversation-level sentiment = average of user message scores.
- Tier 2: per-message labels and simple mood-shift comparison between start and end thirds of conversation.

## Tier 2 status
Statement-level sentiment and a mood-shift summary are implemented and displayed at the end of the conversation.

## Tests
Basic tests are included under `tests/` using simple assertions.

## Notes & Extensions
- Replace lexicon analyzer with a pretrained model (VADER, HuggingFace) for production-level accuracy.
- Add web UI or integrate with Flask/FastAPI for real-time chat.
- Persist conversations to a database for analytics.

