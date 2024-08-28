from .main import Config

def load_prompt(prompt_key):
    prompt = Config.PROMPTS.get(prompt_key, "")
    if not prompt:
        from ..logger import get_logger
        logger = get_logger(__name__)
        logger.warning(f"No prompt found for key: {prompt_key}", extra={"prompt_key": prompt_key})
    return prompt

# Export both Config and load_prompt
__all__ = ['Config', 'load_prompt']