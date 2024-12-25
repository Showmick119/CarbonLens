import logging
import praw
from transformers import pipeline
import pdfplumber
import json
import os
from datetime import datetime
from random_forest_model import aggregated_scores

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize sentiment analysis model
sentiment_model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english", device=0)

# Reddit API configuration
REDDIT_CLIENT_ID = "aSl7D2IUWFvvys1NHnH2RA"
REDDIT_CLIENT_SECRET = "Zh9LxiMxFwLpQ1-xs4Z_nubWUTxkkA"
REDDIT_USER_AGENT = "CarbonLensApp/1.0 by Physical_Mix5167"

# Cache versioning
CACHE_VERSION = "1.0"  # Update this whenever the model or logic changes
CACHE_TIMESTAMP = "cache_timestamp.json"

# Check if cache is valid
def is_cache_valid(cache_file):
    if not os.path.exists(cache_file):
        return False

    try:
        with open(CACHE_TIMESTAMP, "r") as f:
            cache_metadata = json.load(f)
            return cache_metadata.get("version") == CACHE_VERSION
    except Exception as e:
        logger.error(f"Error reading cache metadata: {e}")
        return False

# Update cache metadata
def update_cache_metadata():
    metadata = {
        "version": CACHE_VERSION,
        "timestamp": datetime.now().isoformat()
    }
    with open(CACHE_TIMESTAMP, "w") as f:
        json.dump(metadata, f)


# Prefetch Reddit posts and cache results
def prefetch_reddit_posts(manufacturer, limit=50, cache_file="reddit_cache.json"):
    logger.info(f"Prefetching Reddit posts for {manufacturer}...")
    cache = {}

    # Load cache if valid
    if is_cache_valid(cache_file):
        with open(cache_file, "r") as f:
            cache = json.load(f)

    # Return cached data if available
    if manufacturer in cache:
        logger.info(f"Using cached Reddit posts for {manufacturer}.")
        return cache[manufacturer]

    # Fetch posts from Reddit
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )
    posts = []
    try:
        for post in reddit.subreddit("all").search(
            f"{manufacturer} sustainability OR environment OR manufacturing impact",
            limit=limit,
            sort="relevance"
        ):
            if not post.stickied:
                posts.append(post.title + " " + post.selftext)
    except Exception as e:
        logger.error(f"Error fetching Reddit posts: {e}")

    # Update cache
    cache[manufacturer] = posts
    with open(cache_file, "w") as f:
        json.dump(cache, f)
    update_cache_metadata()

    logger.info(f"Successfully fetched {len(posts)} posts for {manufacturer}.")
    return posts


# Prefetch and cache PDF processing
def prefetch_pdf_text(pdf_path, cache_file="pdf_cache.json"):
    logger.info(f"Prefetching PDF text for {pdf_path}...")
    cache = {}

    # Load cache if valid
    if is_cache_valid(cache_file):
        with open(cache_file, "r") as f:
            cache = json.load(f)

    # Return cached data if available
    if pdf_path in cache:
        logger.info(f"Using cached PDF text for {pdf_path}.")
        return cache[pdf_path]

    # Extract text from PDF
    text_chunks = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    paragraphs = text.split("\n")
                    for paragraph in paragraphs:
                        if any(keyword in paragraph.lower() for keyword in ["sustainability", "carbon", "emissions", "initiatives", "impact", "decarbonisation", "ev"]):
                            text_chunks.append(paragraph)
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {e}")

    # Update cache
    cache[pdf_path] = text_chunks
    with open(cache_file, "w") as f:
        json.dump(cache, f)
    update_cache_metadata()

    logger.info("PDF text extraction and caching completed.")
    return text_chunks

# Analyze sentiment
def analyze_sentiment(text_chunks):
    logger.info("Analyzing sentiment for text chunks...")
    try:
        results = sentiment_model(text_chunks, truncation=True, batch_size=16)
        sentiment_scores = []

        for result in results:
            if result["label"] == "POSITIVE":
                weight = min(result["score"] * 3.0, 3.0)  # Cap strong positives
                sentiment_scores.append(weight)
            elif result["label"] == "NEGATIVE":
                weight = max(-result["score"] * 2.4, -2.4)  # Cap strong negatives
                sentiment_scores.append(weight)

        logger.info("Sentiment analysis completed.")
        return sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
    except Exception as e:
        logger.error(f"Error during sentiment analysis: {e}")
        return 0

# Adjust sustainability score with balanced scaling
def adjust_sustainability_score(base_score, pdf_sentiment, reddit_sentiment, num_reddit_posts):
    pdf_weight = 0.6  # Give significant weight to the PDF
    reddit_weight = 0.4  # Reddit posts collectively contribute less
    scaling_factor = 1 + (num_reddit_posts / 200)  # Gradual increase for large datasets

    combined_sentiment = (pdf_weight * pdf_sentiment) + (reddit_weight * reddit_sentiment)
    adjustment = combined_sentiment * 10 * scaling_factor

    adjustment = min(max(adjustment, -20), 20)  # Cap adjustment to -20 to +20
    adjusted_score = base_score + adjustment
    return max(0, min(100, adjusted_score))  # Ensure score stays within bounds

# Generate general explanation for score adjustment of all the manufacturers
def generate_explanation(manufacturer, base_score, final_score, pdf_sentiment, reddit_sentiment, num_reddit_posts):
    explanation = f"""
    The sustainability score for {manufacturer} combines insights from the company's official sustainability report and public sentiment gathered online.
    The sustainability report highlighted commendable initiatives, such as promoting renewable energy and implementing waste management systems. 
    However, the report primarily focused on future plans and aspirations, with limited evidence of concrete efforts in the current product series. 
    As a result, the score could not be adjusted significantly based on the report alone. Meanwhile, discussions on Reddit presented a mixed perspective, with users mentioning both positive steps and ongoing challenges in the manufacturer's 
    environmental practices. This suggests that public perception remains divided. Considering the report's promises and public sentiment, the sustainability 
    score has been adjusted from {base_score:.2f} to {final_score:.2f}.
    """
    return explanation.strip()

# Main function for analysis
def main(manufacturer, base_score, pdf_path=None):
    reddit_posts = prefetch_reddit_posts(manufacturer)
    pdf_text_chunks = prefetch_pdf_text(pdf_path) if pdf_path else []

    if not reddit_posts and not pdf_text_chunks:
        logger.warning("No relevant texts found for analysis.")
        return base_score, "No relevant data to adjust the sustainability score."

    reddit_sentiment = analyze_sentiment(reddit_posts)
    pdf_sentiment = analyze_sentiment(pdf_text_chunks)

    num_reddit_posts = len(reddit_posts)
    final_score = adjust_sustainability_score(base_score, pdf_sentiment, reddit_sentiment, num_reddit_posts)
    explanation = generate_explanation(manufacturer, base_score, final_score, pdf_sentiment, reddit_sentiment, num_reddit_posts)

    logger.info(f"Final adjusted score for {manufacturer}: {final_score:.2f}")

    return final_score, explanation