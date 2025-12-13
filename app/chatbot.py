import os
from textblob import TextBlob
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Gemini Model Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash-lite")

def generate_response(prompt):
    """
    Standard chat response generator using Gemini.
    Includes safe fallback for quota & unexpected errors.
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        msg = str(e).lower()
        if "quota" in msg or "limit" in msg:
            return "It seems we have reached the API quota limit. Please try again later."
        return f"An error occurred: {e}"

# Sentiment Analyzer
class SentimentAnalyzer:
    """
    Rule-based + TextBlob hybrid sentiment analyzer
    with Gemini fallback for edge cases.
    """

    def __init__(self, llm_model=None):
        """
        llm_model: Gemini model instance injected from outside.
                   Must support model.generate_content(prompt).
        """
        self.llm_model = llm_model

        # Predefined keyword dictionaries
        self.very_negative_words = {
            "hopeless", "terrible", "depressed", "suicidal",
            "can't handle", "worthless", "miserable", "devastated"
        }

        self.negative_words = {
            "sad", "disappointed", "scared", "afraid", "anxious",
            "upset", "hurt", "pain", "stressed", "awful", "bad"
        }

        self.positive_words = {
            "happy", "good", "great", "excited", "feeling better",
            "joy", "glad", "love", "hope", "amazing", "brilliant",
            "confident", "successful", "kind", "strong", "vibrant",
            "excellent", "peaceful", "inspiring"
        }

        self.negation_words = {
            "not", "never", "no", "won't", "dont", "don't",
            "can't", "cannot"
        }
    
    # Main function: Analyze sentiment follows Hybrid Approach
    def analyze_sentiment(self, text: str):
        text_lower = text.lower()
         
        # First, Rule Based Classifier
        # For Hard Very-Negative Patterns return 0.8
        if self._contains_any(text_lower, self.very_negative_words):
            return "Very Negative", -0.8

        # For Mixed Feelings return 0
        has_neg = self._contains_any(text_lower, self.negative_words)
        has_pos = self._contains_any(text_lower, self.positive_words)

        if has_neg and has_pos:
            return "Mixed Feelings", 0.0

        # For Negation Handling
        has_negation = self._contains_any(text_lower, self.negation_words)
        if has_negation and has_pos:
            return "Negative", -0.4

        # Direct Polarity 
        if has_neg:
            return "Negative", -0.4
        if has_pos:
            return "Positive", 0.5

        # Second, using TextBlob Score for more advanced analysis 
        blob_score = TextBlob(text).sentiment.polarity
        tb_label = self._textblob_label(blob_score)

        # Detect Edge Case 
        is_edge_case = self._is_edge_case(
            text_lower=text_lower,
            tb_label=tb_label,
            blob_score=blob_score,
            has_pos=has_pos,
            has_neg=has_neg,
            has_negation=has_negation
        )
        # If not an edge case evaluate directly using Text Blob Score
        if not is_edge_case:
            return tb_label, round(blob_score, 3)

        # If an edge case is detected -> Fallback to Gemini
        return self._llm_fallback(text, tb_label, blob_score)

    # Check if text contains any keyword
    @staticmethod
    def _contains_any(text, words_set):
        return any(word in text for word in words_set)

    # Function to Convert TextBlob numeric polarity → label
    @staticmethod
    def _textblob_label(score):
        if score > 0.5:
            return "Very Positive"
        if score > 0.1:
            return "Positive"
        if score >= -0.1:
            return "Neutral"
        if score > -0.5:
            return "Negative"
        return "Very Negative"

    # Function to Detect Edge cases
    def _is_edge_case(self, text_lower, tb_label, blob_score, has_pos, has_neg, has_negation):
        # Neutral but emotional words present
        if tb_label == "Neutral" and (has_pos or has_neg):
            return True

        # Contradictory emotions
        if self._contains_any(text_lower, self.negative_words | self.very_negative_words) and blob_score > 0.1:
            return True

        # Negation but positive word
        if has_negation and "good" in text_lower:
            return True

        return False


    # Function for Gemini fallback

    def _llm_fallback(self, text, tb_label, blob_score):
        """
        If LLM fails (timeout, API errors), return TextBlob output.
        """
        if not self.llm_model:
            return tb_label, round(blob_score, 3)

        try:
            prompt = f"""
            You are a strict sentiment analyzer.
            Return ONLY: label, numeric score (-1 to +1).
            Message: "{text}"
            """

            response = self.llm_model.generate_content(prompt)
            raw_output = response.text.strip()

            label, score = raw_output.split(",")
            return label.strip(), float(score.strip())

        except Exception:
            # Fail-safe fallback
            return tb_label, round(blob_score, 3)

sentiment_analyzer = SentimentAnalyzer(llm_model=model)

# Create global analyzer instance
sentiment_analyzer = SentimentAnalyzer(llm_model=model)


def analyze_sentiment(text: str):
    """
    Wrapper function so older code that imports analyze_sentiment still works.
    Internally calls the class-based SentimentAnalyzer.
    """
    return sentiment_analyzer.analyze_sentiment(text)
