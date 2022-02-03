import logging


def BuildCustomLogger(name : str):

    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    
    # logging.basicConfig(level=os.environ.get("LOGLEVEL", "DEBUG"))
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger
