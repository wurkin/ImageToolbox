import sys
sys.path.append('D:\\ImageToolbox')  # Adjust this path as necessary
import logging
from app.gui import run_app
from app.utils import setup_logging

def main():
    """
    Main entry point for the ImageToolbox application.
    """
    # Configure logging for the application
    setup_logging(log_directory='logs', log_level=logging.INFO)
    
    # Log that the application is starting
    logging.info("Starting ImageToolbox application.")
    
    # Run the application's GUI
    try:
        run_app()
    except Exception as e:
        logging.error(f"An error occurred while running the application: {e}")
        raise

if __name__ == "__main__":
    main()
