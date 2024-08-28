import logging
import json
from typing import Any, Dict

class StructuredLogger(logging.Logger):
    def _log(self, level: int, msg: object, args: tuple, exc_info: Any = None, extra: Dict[str, Any] = None, stack_info: bool = False) -> None:
        if extra is None:
            extra = {}
        extra['log_message'] = msg  # Use 'log_message' instead of 'message'
        msg = json.dumps(extra)
        super()._log(level, msg, args, exc_info, extra, stack_info)

def get_logger(name: str) -> StructuredLogger:
    logger = StructuredLogger(name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger