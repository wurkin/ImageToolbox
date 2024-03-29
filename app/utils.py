import logging
import os

def setup_logging(log_directory='logs', log_level=logging.INFO):
    """
    Configures the logging environment. Creates a log file in the specified directory.
    
    Parameters:
    - log_directory: The directory where log files will be stored.
    - log_level: The minimum logging level messages to record.
    """
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    log_filename = os.path.join(log_directory, 'ImageToolbox.log')
    
    # Basic logging configuration
    logging.basicConfig(level=log_level,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename=log_filename,
                        filemode='a')
    
    # Adding logging to console as well
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console_handler.setFormatter(formatter)
    logging.getLogger('').addHandler(console_handler)

def dummy_utility_function():
    """
    Placeholder for a utility function. Implement additional utility functions as needed.
    """
    pass

# Example usage of setup_logging
if __name__ == "__main__":
    setup_logging()
    logging.info("Logging is configured and ready to use.")
