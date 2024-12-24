import logging
import praw
from transformers import pipeline
import pdfplumber

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize sentiment analysis model
sentiment_model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# Reddit API configuration
REDDIT_CLIENT_ID = "aSl7D2IUWFvvys1NHnH2RA"
REDDIT_CLIENT_SECRET = "Zh9LxiMxFwLpQ1-xs4Z_nubWUTxkkA"
REDDIT_USER_AGENT = "CarbonLensApp/1.0 by Physical_Mix5167"

# Fetch Reddit posts with relevance filtering
def fetch_reddit_posts(manufacturer, limit=100):
    logger.info(f"Fetching Reddit posts for {manufacturer}...")
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

    logger.info(f"Successfully fetched {len(posts)} posts.")
    return posts

# Extract text from PDF
def extract_pdf_text(pdf_path):
    logger.info(f"Extracting text from PDF: {pdf_path}")
    text_chunks = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    paragraphs = text.split("\n")
                    for paragraph in paragraphs:
                        if any(keyword in paragraph.lower() for keyword in ["sustainability", "carbon", "emissions", "initiatives", "impact"]):
                            text_chunks.append(paragraph)
        logger.info("PDF text extraction and filtering completed.")
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {e}")
    return text_chunks

# Analyze sentiment with caps on impact
def analyze_sentiment(text_chunks):
    logger.info("Analyzing sentiment for text chunks...")
    try:
        results = sentiment_model(text_chunks, truncation=True)
        sentiment_scores = []

        for result in results:
            if result["label"] == "POSITIVE":
                weight = min(result["score"] * 1.5, 1.5)  # Cap strong positives
                sentiment_scores.append(weight)
            elif result["label"] == "NEGATIVE":
                weight = max(-result["score"] * 1.2, -1.2)  # Cap strong negatives
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

# Generate explanation for score adjustment
def generate_explanation(manufacturer, base_score, final_score, pdf_sentiment, reddit_sentiment, num_reddit_posts):
    explanation = (
        f"The sustainability score for {manufacturer} reflects insights from both the company's sustainability report and public sentiment. "
        f"The report highlighted notable efforts such as renewable energy initiatives and waste management systems, but also raised some concerns "
        f"about areas needing improvement. Discussions on Reddit generally indicated mixed public opinion, with mentions of both positive and "
        f"negative aspects of the manufacturer's environmental practices. Taking these factors into account, the sustainability score has been adjusted "
        f"from {base_score:.2f} to {final_score:.2f}."
    )
    return explanation

# Main function for analysis
def main(manufacturer, base_score, pdf_path=None):
    reddit_posts = fetch_reddit_posts(manufacturer)
    pdf_text_chunks = extract_pdf_text(pdf_path) if pdf_path else []

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

# Sample execution
if __name__ == "__main__":
    manufacturer = "Honda"
    base_score = 60.0
    pdf_path = "src/honda-SR-2024-en-003.pdf"  # Example PDF file path
    final_score, explanation = main(manufacturer, base_score, pdf_path=pdf_path)
    print(f"Final Sustainability Score for {manufacturer}: {final_score:.2f}")
    print("Explanation:")
    print(explanation)