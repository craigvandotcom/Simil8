from .main import Config
import logging

def load_prompt(prompt_key):
    prompt = Config.PROMPTS.get(prompt_key, "")
    if not prompt:
        logging.warning(f"No prompt found for key: {prompt_key}")
    return prompt

# Export both Config and load_prompt
__all__ = ['Config', 'load_prompt']