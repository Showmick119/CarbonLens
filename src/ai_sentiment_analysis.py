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
        return cache[pdf_path], cache.get("num_pages", 0)

    # Extract text from PDF and get number of pages
    text_chunks = []
    num_pages = 0
    try:
        with pdfplumber.open(pdf_path) as pdf:
            num_pages = len(pdf.pages)  # Get the number of pages
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    paragraphs = text.split("\n")
                    for paragraph in paragraphs:
                        if any(keyword in paragraph.lower() for keyword in [
                            "sustainability", "carbon", "emissions", "initiatives", 
                            "resource", "responsible", "electric", "recycle", 
                            "renewable", "impact", "decarbonisation", "ev"
                        ]):
                            text_chunks.append(paragraph)
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {e}")

    # Update cache
    cache[pdf_path] = text_chunks
    cache["num_pages"] = num_pages
    with open(cache_file, "w") as f:
        json.dump(cache, f)
    update_cache_metadata()

    logger.info(f"PDF text extraction and caching completed. Pages: {num_pages}")
    return text_chunks, num_pages

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

# Generate logic-based explanation specific to each manufacturer and their PDF and Reddit sentiment, as well as our personal research on the companies
def generate_dynamic_explanation(manufacturer, base_score, final_score, pdf_sentiment, reddit_sentiment, num_reddit_posts, pdf_pages):
    explanation = f"""
    The sustainability evaluation for {manufacturer} incorporates a thorough analysis of both their internal strategies and public perception. 

    **Internal Analysis:**  
    The sustainability report, spanning {pdf_pages} pages, highlights {
        'a pioneering approach in decarbonisation and resource efficiency' if pdf_sentiment > 0.7 else 
        'a balanced focus on sustainable practices and moderate improvements' if pdf_sentiment > 0.3 else 
        'limited and underwhelming commitments to significant environmental changes'
    }. 
    Their initiatives {
        'showcase developments in hybrid vehicles, electric vehicles (EVs), resource recycling, and carbon emissions reduction' if pdf_sentiment > 0.7 else 
        'include respectable attempts to align with industry standards in emissions control and resource management, however much works needs to be done, thus the sustainability score cannot be changed significantly' if pdf_sentiment > 0.3 else 
        'lack the innovation and accountability needed to reduce their carbon emissions and address global environmental challenges'
    }.  

    **Public Perception:**  
    Based on {num_reddit_posts} Reddit posts, sentiment among stakeholders and the public is {
        'overwhelmingly positive, reflecting strong support for their sustainability processes' if reddit_sentiment > 0.7 else 
        'somewhat mixed, with pockets of appreciation for certain initiatives and criticism for others' if reddit_sentiment > 0.3 else 
        'largely negative, signaling dissatisfaction with the company’s approach to sustainability'
    }. Comments often {
        'praise innovative EV and Hybrid strategies, as well as improved manufacturing processes which pave the way for the decarbonisation efforts' if reddit_sentiment > 0.7 else 
        'highlight progress in specific areas but question their long-term vision and how realistic its implementation is' if reddit_sentiment > 0.3 else 
        'criticize inefficiencies and the perceived lack of genuine commitment to sustainability'
    }.  

    **Score Adjustments:**  
    Starting from a base score of {base_score:.2f}, adjustments have been made to reflect both the depth of their reported initiatives and the sentiment of public discourse. The final score of {final_score:.2f} {
        'represents a commendable improvement due to bold and effective strategies' if final_score > base_score else 
        'indicates a need for significant enhancements in transparency and impact-driven initiatives'
    }.

    **Manufacturer-Specific Insights:**  
    {
        'While, BMW continues to make strides in EV efficiency and sustainable manufacturing processes, underscoring their long-term dedication to resource optimization. Their current processes do not show the strongest adherence to sustainabilty.' if manufacturer == 'BMW' else
        'Ford has taken notable strides in renewable energy integration within their production facilities, though challenges in scaling their EV range remain.' if manufacturer == 'Ford' else
        'General Motors showcases impressive decarbonisation through advanced EV adoption, but questions linger about their supply chain sustainability.' if manufacturer == 'General Motors' else
        'Honda’s focus on hybrid technologies and resource-efficient production places them as a balanced contributor, though deeper carbon neutrality goals are awaited.' if manufacturer == 'Honda' else
        'Hyundai stands out for its aggressive push in EV markets, with a strong emphasis on hydrogen fuel cell innovation, though resource optimization and manufacturing processes still need improvements.' if manufacturer == 'Hyundai' else
        'Kia has aligned itself closely with Hyundai’s strategies but still faces differentiation challenges in its EV and decarbonisation approaches.' if manufacturer == 'Kia' else
        'Mazda remains heavily reliant on gasoline technologies but has shown incremental progress in exploring alternative powertrains.' if manufacturer == 'Mazda' else
        'Mercedes has recently excelled in premium hybrid and EV production, as well as advanced decarbonisation initiatives, showing strong improvement and setting a high benchmark for luxury automotive sustainability.' if manufacturer == 'Mercedes' else
        'Nissan’s strides in EV affordability and market penetration are commendable, though criticisms around their supply chain’s environmental impact still persist.' if manufacturer == 'Nissan' else
        'Stellantis benefits from its diverse portfolio, but its fragmented approach to sustainability across brands creates mixed perceptions.' if manufacturer == 'Stellantis' else
        'Subaru’s focus on lightweight vehicles and fuel efficiency is noteworthy, but their pace in embracing Hybrid and EV technology lags competitors.' if manufacturer == 'Subaru' else
        'Toyota continues to innovate with hybrid technologies, though their slower transition to fully electric platforms raises questions about their long-term strategy.' if manufacturer == 'Toyota' else
        'Volkswagen’s transformation post-diesel scandal is remarkable, driven by aggressive EV rollout and enhanced resource efficiency measures.'
    }

    **Final Remarks:**  
    This assessment underscores the mutual influence between {manufacturer}’s internal sustainability efforts and external perception, providing a nuanced understanding of their environmental impact.
    """
    return explanation.strip()

# Main function for analysis
def main(manufacturer, base_score, pdf_path=None):
    reddit_posts = prefetch_reddit_posts(manufacturer)
    pdf_text_chunks, pdf_pages = prefetch_pdf_text(pdf_path) if pdf_path else ([], 0)

    if not reddit_posts and not pdf_text_chunks:
        logger.warning("No relevant texts found for analysis.")
        return base_score, "No relevant data to adjust the sustainability score."

    reddit_sentiment = analyze_sentiment(reddit_posts)
    pdf_sentiment = analyze_sentiment(pdf_text_chunks)

    num_reddit_posts = len(reddit_posts)
    final_score = adjust_sustainability_score(base_score, pdf_sentiment, reddit_sentiment, num_reddit_posts)
    explanation = generate_dynamic_explanation(
        manufacturer, base_score, final_score, pdf_sentiment, reddit_sentiment, num_reddit_posts, pdf_pages
    )

    logger.info(f"Final adjusted score for {manufacturer}: {final_score:.2f}")
    return final_score, explanation