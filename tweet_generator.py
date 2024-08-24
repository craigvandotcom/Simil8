# tweet_generator.py

import json
import re
from typing import List, Dict, Any
from openai import OpenAI
from config import OPENAI_API_KEY

openai_client = OpenAI(api_key=OPENAI_API_KEY)

def generate_tweet_variations(text: str, num_variations: int = 6) -> List[str]:
    prompt = f"""
    
    Transform the following text into {num_variations} diverse tweet versions:

    Text: "{text}"
    
    Instructions:
    - Create exactly {num_variations} tweet versions, each expanding on the ideas in the given text, offering additional context, or relating it to broader concepts.
    - Craft each tweet to add value by educating or inspiring action.
    - Keep each tweet within the 280-character limit.
    - Authenticity resonates with audiences. Avoid overly promotional language; be genuine.
    - Use active voice to make your tweets more dynamic and direct, increasing engagement.
    - Personalize tweets (e.g., using "you" and "your") to make them more relatable and engaging.
    - Incorporate engaging elements such as statistics or thought-provoking statements.
    - Maintain a consistent tone across all tweets that align with the target audience (professional).
    - DO NOT include any hashtags.
    - DO NOT ask rhetorical questions. Only ask questions that are intended to actually invite engagement.
    
    Specific goals for each tweet variation:
    1. Very similar to the original text, but improved for tweeting
    2. Best possible rephrasing for maximum engagement
    3. If we regard the input text as wisdom, focus on the risks of not implementing this wisdom
    4. If we regard the input text as wisdom, focus on the benefits of implementing this wisdom
    5. If we regard the input text as wisdom, focus on the practical steps to implement this wisdom (use a listicle where suitable)
    6. If we regard the input text as wisdom, focus on inspiring the reader to take action
    
    The ultimate goal is to add maximum value, educate, and inspire.
    
    Output Format:
    Provide the tweets as a valid JSON array of strings, like this:
    ["Tweet 1 content", "Tweet 2 content", "Tweet 3 content", ...]
    
    Ensure that each tweet is a complete, self-contained string within the array.
    """

    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": 
             """
            You are an expert in digital marketing, copywriting, and social media strategy, with a specialized focus on Twitter. Your role is to transform input text into high-performing tweet variations that resonate with a professional audience, maximize engagement, add value, and inspire action. You possess:
            
            Deep understanding of Twitter's unique ecosystem, user behavior, and platform dynamics
            Mastery of concise, impactful writing within the 280-character limit
            Ability to craft engaging content that educates, inspires, and drives action
            Skill in adapting content to various professional contexts and industries
            Knowledge of current social media trends and best practices
            Expertise in creating content that encourages genuine engagement and discussion
            
            Your task is to skillfully use this expertise to generate tweet variations that are authentic, valuable, and tailored to the specific goals outlined in the instructions. Each variation should be optimized for Twitter's unique platform, leveraging your understanding to create diverse and impactful tweets.
            """
            },
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
