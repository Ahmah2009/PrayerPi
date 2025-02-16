import logging
from data.cache import load_time_tuples
import time
import datetime
import subprocess
import sys

# Set up logging
logging.basicConfig(level=logging.DEBUG,  # You can adjust the logging level
                    format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
                    handlers=[logging.StreamHandler()])  # Log to console

def load_schedule():
    """
    Load or define the schedule as a set of tuples.
    Each tuple is in the form (month, day, hour, minute).
    """
    return load_time_tuples()

def run_task():
    """
    Runs your task. Here we call an external script using subprocess.
    Make sure to use the full path and that the script is executable.
    """
    try:
        subprocess.run(
            ["/home/ahmad/PrayerPi/.venv/bin/python", "src/runner.py"],
            check=True,
            stdout=sys.stdout,  # Redirect stdout to sys.stdout (which is captured by systemd)
            stderr=sys.stderr   # Redirect stderr to sys.stderr (which is captured by systemd)
        )
                
        logging.info("Task executed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error("Task execution failed: %s", e)

def main_loop(schedule):
    """
    Main loop that checks every few seconds if the current time (month, day, hour, minute)
    matches any scheduled time. Once a match is found, run the task and sleep for 60 seconds.
    """
    while True:
        now = datetime.datetime.now()
        current_tuple = (now.month, now.day, now.hour, now.minute)
        logging.debug("Current time tuple: %s", current_tuple)
        
        if current_tuple in schedule:
            logging.info(f"Match found for time {current_tuple}! Executing task...")
            run_task()
            # Wait for 60 seconds to avoid triggering the same minute again
            time.sleep(60)
        else:
            # Check again in a few seconds
            time.sleep(5)

if __name__ == "__main__":
    schedule = load_schedule()
    main_loop(schedule)
