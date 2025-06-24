import logging

def setup_logging():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("agent_debugger")
    return logger

logger = setup_logging()