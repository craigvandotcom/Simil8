# tweet_generator.py

import json
import re
from typing import List, Dict, Any
from openai import OpenAI
from config import OPENAI_API_KEY

openai_client = OpenAI(api_key=OPENAI_API_KEY)

def generate_tweet_variations(text: str, num_variations: int = 3) -> List[str]:
    prompt = f"""
    Transform the following text into {num_variations} diverse tweet versions:

    Text: "{text}"

    Instructions:
    - Create exactly {num_variations} tweet versions, each expanding on the ideas in the given text, offering additional context, or relating it to broader concepts.
    - Craft each tweet to add value, by educating or inspiring action.
    - Keep each tweet within the 280-character limit.
    - Incorporate engaging elements such as questions, statistics, or thought-provoking statements.
    - Maintain a consistent tone across all tweets that align with the target audience (professional).
    - The ultimate goal is to add maximum value, educate, and inspire.
    - DO NOT include any hashtags.

    Output Format:
    Provide the tweets as a valid JSON array of strings, like this:
    ["Tweet 1 content", "Tweet 2 content", "Tweet 3 content"]

    Ensure that each tweet is a complete, self-contained string within the array.
    """

    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert in marketing, copywriting, and social media. Your specific area of expertise is X (Twitter). Your job is to transform input text into high-performing tweet variations."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=800
    )

    content = response.choices[0].message.content.strip()

    # Try to parse as JSON
    try:
        tweet_list = json.loads(content)
        if isinstance(tweet_list, list) and len(tweet_list) == num_variations:
            return tweet_list
    except json.JSONDecodeError:
        pass

    # If JSON parsing fails, try to extract tweets using regex
    tweet_pattern = re.compile(r'"([^"]+)"')
    tweet_list = tweet_pattern.findall(content)

    # If we still don't have the correct number of tweets, fall back to splitting by newlines
    if len(tweet_list) != num_variations:
        tweet_list = [line.strip().strip('"') for line in content.split('\n') if line.strip()]

    # Ensure we have the correct number of variations
    tweet_list = tweet_list[:num_variations]

    # Ensure each tweet is within the character limit
    tweet_list = [tweet[:280] for tweet in tweet_list]

    return tweet_list

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
    4. Incorporate engaging elements such as questions, statistics, analogies, or thought-provoking statements.
    5. Maintain a consistent tone across all tweets that aligns with the target audience (professional).
    6. Use numbering (1/{num_tweets}, 2/{num_tweets}, etc.) at the start of each tweet to help readers follow the thread.
    7. Ensure smooth transitions between tweets for a coherent reading experience.
    8. The ultimate goal is to add maximum value, by educating and/or inspiring action.
    9. DO NOT include any hashtags.

    Output Format:
    Provide the tweets as a valid JSON array of strings, like this:
    ["1/{num_tweets} Tweet 1 content", "2/{num_tweets} Tweet 2 content", "3/{num_tweets} Tweet 3 content", ..., "{num_tweets}/{num_tweets} Tweet {num_tweets} content"]

    Ensure that each tweet is a complete, self-contained string within the array, including the numbering.
    """

    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert in marketing, copywriting, and social media. Your specific area of expertise is X (Twitter). Your job is to transform input text into high-performing thread variations."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500
    )

    content = response.choices[0].message.content.strip()

    # Try to parse as JSON
    try:
        tweet_list = json.loads(content)
        if isinstance(tweet_list, list) and len(tweet_list) == num_tweets:
            return tweet_list
    except json.JSONDecodeError:
        pass

    # If JSON parsing fails, try to extract tweets using regex
    tweet_pattern = re.compile(r'"([^"]+)"')
    tweet_list = tweet_pattern.findall(content)

    # If we still don't have the correct number of tweets, fall back to splitting by newlines
    if len(tweet_list) != num_tweets:
        tweet_list = [line.strip().strip('"') for line in content.split('\n') if line.strip()]

    # Ensure we have the correct number of tweets
    tweet_list = tweet_list[:num_tweets]

    # Add numbering if it's not already present
    for i, tweet in enumerate(tweet_list):
        if not tweet.startswith(f"{i+1}/{num_tweets}"):
            tweet_list[i] = f"{i+1}/{num_tweets} {tweet}"

    # Ensure each tweet is within the character limit
    tweet_list = [tweet[:280] for tweet in tweet_list]

    return tweet_list


def create_highlight_thread(highlight: Dict[str, Any]) -> List[str]:
    """
    Creates a thread of tweet variations from a book highlight.

    Args:
        highlight (Dict[str, Any]): A dictionary containing book highlight information.
            - 'book_title': str, title of the book
            - 'text': str, the original highlight text
            - 'book_author': str, author of the book

    Returns:
        List[str]: A list of tweets forming a Twitter thread.
            - First tweet: formatted original book highlight
            - Subsequent tweets: variations of the original highlight
    """
    original_tweet = f"\"{highlight['text']}\"\n\n🖋️ {highlight['book_author']}\n📚 {highlight['book_title']}"
    thread = generate_tweet_variations(highlight['text'], num_variations=3)  # Generate additional tweets
    return [original_tweet] + thread
