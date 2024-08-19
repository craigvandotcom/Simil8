from openai import OpenAI
from typing import List
from config import OPENAI_API_KEY
from typing import Dict, Any, List

openai_client = OpenAI(api_key=OPENAI_API_KEY)

def generate_tweet_variations(text: str, num_variations: int = 3) -> List[str]:
    prompt = f"""
    Transform the following text into {num_variations} diverse tweet versions:

    Text: "{text}"

    Instructions:
    - Create {num_variations} tweet versions, each expanding on the ideas in the given text, offering additional context, or relating it to broader concepts.
    - Craft each tweet with the intention of capturing attention and going viral, while educating, providing value, or inspiring action.
    - Keep each tweet within the 280-character limit.
    - Include 1-2 relevant hashtags per tweet to increase discoverability.
    - Incorporate engaging elements such as questions, statistics, or thought-provoking statements.
    - Maintain a consistent tone across all tweets that aligns with the target audience (e.g., professional, casual, humorous).
    - The ultimate goal is to add maximum value, educate, and inspire.

    Format:
    1. [Tweet content]
    2. [Tweet content]
    3. [Tweet content]
    """

    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert in marketing, copywriting, and social media. Your specific area of expertise is X (Twitter). Your job is to transform input text into high-performing tweet variations."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=800
    )

    # Parse the response to extract only the tweet content
    variations = response.choices[0].message.content.strip().split("\n")
    return [variation.split(". ", 1)[1].strip() for variation in variations if variation.strip()]

def generate_thread(text: str, num_tweets: int = 7) -> List[str]:
    prompt = f"""
    Transform the following text into a coherent and engaging thread of {num_tweets} tweets:

    Text: "{text}"

    Thread Structure:
    1. Hook (1 tweet): Capture attention with a surprising fact, question, or bold statement.
    2. Context (1-2 tweets): Briefly explain the background or importance of the topic.
    3. Main Points (varies): Present key ideas, insights, or arguments, one per tweet.
    4. Supporting Details (varies): Provide examples, data, or elaboration for main points.
    5. Addressing Counterarguments (optional, 1-2 tweets): Anticipate and address potential objections.
    6. Conclusion (1 tweet): Summarize key takeaways or restate the main message.

    Instructions:
    1. Create a thread of {num_tweets} tweets that expand on the ideas in the given text, offering additional context, insights, or relating it to broader concepts.
    2. Keep each tweet within the 280-character limit.
    3. Use the thread structure outlined above, adapting as needed for the specific content and tweet count.
    4. Include 1-2 relevant hashtags in strategic places throughout the thread (not every tweet).
    5. Incorporate engaging elements such as questions, statistics, analogies, or thought-provoking statements.
    6. Maintain a consistent tone across all tweets that aligns with the target audience (e.g., professional, casual, humorous).
    7. Use numbering (1/X) at the start of each tweet to help readers follow the thread.
    8. Ensure smooth transitions between tweets for a coherent reading experience.
    9. The ultimate goal is to add maximum value, educate, and inspire.

    Format:
    Tweet 1: [Hook tweet content]
    Tweet 2: [Tweet content]
    [Continue for the specified number of tweets]
    Tweet X: [Conclusion tweet content]
    """

    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert in marketing, copywriting, and social media. Your specific area of expertise is X (Twitter). Your job is to transform input text into high-performing thread variations."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500
    )

    # Parse the response to extract only the tweet content
    tweets = response.choices[0].message.content.strip().split("\n")
    return [tweet.split(": ", 1)[1].strip() for tweet in tweets if tweet.strip() and ": " in tweet]

def create_highlight_thread(highlight: Dict[str, Any]) -> List[str]:
    original_tweet = f"\"{highlight['text']}\"\n🖋️ {highlight['book_author']}\n📚 {highlight['book_title']}"
    variations = generate_tweet_variations(highlight['text'])
    return [original_tweet] + variations