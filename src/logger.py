import logging

def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Sets a logger with a specified name and logging level."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    fh=logging.FileHandler(f"{name}.log")
    formatter=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger