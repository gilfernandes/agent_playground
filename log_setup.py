import logging


def setup_log(module_name: str):
    logging.basicConfig(
        level='INFO', 
        format='%(asctime)s %(message)s', 
        datefmt='%m/%d/%Y %I:%M:%S %p',
        handlers=[
            logging.FileHandler("agent.log"),
            # logging.StreamHandler()
        ]
    )
    return logging.getLogger(module_name)