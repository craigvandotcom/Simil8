# tweet_generator.py

import json
import logging
import re
from typing import List, Dict, Any
from openai import OpenAI
from anthropic import Anthropic
from ..config import Config, load_prompt

openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
anthropic_client = Anthropic(api_key=Config.ANTHROPIC_API_KEY)

def generate_content(text: str, prompt_key: str, model: str = 'gpt-4', num_variations: int = 6) -> List[str]:
    prompt = load_prompt(prompt_key).format(text=text, num_variations=num_variations)

    logging.info(f"Generated prompt for key '{prompt_key}': {prompt[:100]}...")  # Log first 100 characters of the prompt

    if not prompt.strip():
        logging.error(f"Empty prompt generated for key: {prompt_key}")
        return []  # Return an empty list instead of raising an error

    if model.startswith('gpt'):
        return _generate_openai(prompt, model, num_variations)
    elif model.startswith('claude'):
        return _generate_anthropic(prompt, model, num_variations)
    else:
        raise ValueError(f"Unsupported model: {model}")

def _generate_openai(prompt: str, model: str, num_variations: int) -> List[str]:
    response = openai_client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": Config.PROMPTS["system_prompt"]},
            {"role": "user", "content": prompt}
        ],
        max_tokens=800
    )
    return _parse_response(response.choices[0].message.content.strip(), num_variations)

def _generate_anthropic(prompt: str, model: str, num_variations: int) -> List[str]:
    try:
        # Check if prompt is empty
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty")

        response = anthropic_client.messages.create(
            model=model,
            max_tokens=1000,
            temperature=0.7,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        content = response.content[0].text
        # Try to parse as JSON, if it fails, fall back to text processing
        try:
            variations = json.loads(content)
            if not isinstance(variations, list) or len(variations) != num_variations:
                raise ValueError(f"Expected {num_variations} variations, got: {variations}")
        except json.JSONDecodeError:
            # If JSON parsing fails, process as text
            variations = _parse_response(content, num_variations)
        return variations
    except Exception as e:
        logging.error(f"Error generating content with Anthropic: {str(e)}")
        raise

def _parse_response(content: str, num_variations: int) -> List[str]:
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

    # Ensure we have the correct number of variations and character limit
    return [tweet[:280] for tweet in tweet_list[:num_variations]]

def to_tweet_variations(text: str, highlight: Dict[str, Any] = None) -> List[str]:
    if highlight:
        original_tweet = f"\"{highlight['text']}\"\n\n🖋️ {highlight['book_author']}\n📚 {highlight['book_title']}"
        prompt_key = Config.THREAD_PROMPT_TYPE
        num_variations = 3  # Fixed number for tweet thread
    else:
        prompt_key = Config.TWEET_VARIATIONS_PROMPT_TYPE
        num_variations = Config.TWEET_VARIATIONS_COUNT
    
    logging.info(f"Generating tweet variations with prompt_key: {prompt_key}, num_variations: {num_variations}")
    variations = generate_content(text, prompt_key, Config.AI_MODEL, num_variations)
    logging.info(f"Generated variations: {variations}")
    if highlight:
        result = [original_tweet] + variations
    else:
        result = variations
    logging.info(f"Final result: {result}")
    return result

def to_thread(text: str) -> List[str]:
    thread = generate_content(text, Config.THREAD_PROMPT_TYPE, Config.AI_MODEL, Config.MAX_THREAD_TWEETS)
    return [f"{i+1}/{Config.MAX_THREAD_TWEETS} {tweet.lstrip(f'{i+1}/{Config.MAX_THREAD_TWEETS}').strip()}" for i, tweet in enumerate(thread)]