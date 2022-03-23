import logging

def log_detailed(e, message):
    
    logging.error(message)
    logging.error(e, exc_info=True)