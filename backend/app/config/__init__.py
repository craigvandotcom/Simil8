from .main import Config

def load_prompt(prompt_key):
    return Config.PROMPTS.get(prompt_key, "")

# Export both Config and load_prompt
__all__ = ['Config', 'load_prompt']