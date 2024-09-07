# tweet_generator.py

import json
import re
from typing import List, Dict, Any
from openai import OpenAI
from anthropic import Anthropic
from ..config import Config, load_prompt
from ..logger import get_logger
from ..services.error_reporting import report_error_to_discord

logger = get_logger(__name__)

openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
anthropic_client = Anthropic(api_key=Config.ANTHROPIC_API_KEY)

async def generate_content(text: str, prompt_key: str, model: str = 'gpt-4') -> List[str]:
    try:
        prompt = load_prompt(prompt_key).format(text=text)

        logger.info("Generated prompt", extra={"prompt_key": prompt_key, "prompt_preview": prompt[:100]})

        if not prompt.strip():
            logger.error(f"Empty prompt generated for key: {prompt_key}")
            return []

        if model.startswith('gpt'):
            return await _generate_openai(prompt, model)
        elif model.startswith('claude'):
            return await _generate_anthropic(prompt, model)
        else:
            raise ValueError(f"Unsupported model: {model}")
    except Exception as e:
        error_message = f"Error generating content: {str(e)}"
        logger.error(error_message, exc_info=True)
        await report_error_to_discord(error_message)
        return []

async def _generate_openai(prompt: str, model: str) -> List[str]:
    response = await openai_client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": Config.PROMPTS["system_prompt"]},
            {"role": "user", "content": prompt}
        ],
        max_tokens=800
    )
    return _parse_response(response.choices[0].message.content.strip())

async def _generate_anthropic(prompt: str, model: str) -> List[str]:
    try:
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
        logger.info(f"Anthropic API response: {response}")
        content = response.content[0].text
        logger.info(f"Extracted content: {content}")
        
        variations = _parse_response(content)
        logger.info(f"Parsed variations: {variations}")
        
        return variations if variations else []
    except Exception as e:
        logger.error(f"Error generating content with Anthropic: {str(e)}")
        return []

def _parse_response(content: str) -> List[str]:
    # Try to parse as JSON
    try:
        tweet_list = json.loads(content)
        if isinstance(tweet_list, list):
            return [tweet[:280] for tweet in tweet_list]
    except json.JSONDecodeError:
        pass

    # If JSON parsing fails, try to extract tweets using regex
    tweet_pattern = re.compile(r'"([^"]+)"')
    tweet_list = tweet_pattern.findall(content)

    # If we still don't have any tweets, fall back to splitting by newlines
    if not tweet_list:
        tweet_list = [line.strip().strip('"') for line in content.split('\n') if line.strip()]

    # Ensure character limit
    return [tweet[:280] for tweet in tweet_list]

async def to_tweet_variations(text: str, highlight: Dict[str, Any] = None, prompt_type: str = None) -> List[str]:
    try:
        if highlight:
            original_tweet = f"\"{highlight['text']}\"\n\n🖋️ {highlight['book_author']}\n📚 {highlight['book_title']}"
            prompt_key = Config.TWEET_VARIATIONS_PROMPT_TYPE
        else:
            prompt_key = prompt_type or Config.TWEET_VARIATIONS_PROMPT_TYPE or 'TWEET_VARIATIONS'
        
        logger.info(f"Generating tweet variations with prompt_key: {prompt_key}")
        variations = await generate_content(text, prompt_key, Config.AI_MODEL)
        logger.info(f"Generated variations: {variations}")
        if highlight:
            result = [original_tweet] + variations
        else:
            result = variations
        logger.info(f"Final result: {result}")
        return result
    except Exception as e:
        error_message = f"Error generating tweet variations: {str(e)}"
        logger.error(error_message, exc_info=True)
        await report_error_to_discord(error_message)
        return []

async def to_thread(text: str, prompt_type: str) -> List[str]:
    try:
        thread = await generate_content(text, prompt_type, Config.AI_MODEL)
        return thread
    except Exception as e:
        error_message = f"Error generating thread: {str(e)}"
        logger.error(error_message, exc_info=True)
        await report_error_to_discord(error_message)
        return []