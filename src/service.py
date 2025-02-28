import logging
from data.cache import load_time_tuples
import time
import datetime
import subprocess
import sys
import requests
# Set up logging
logging.basicConfig(level=logging.DEBUG,  # You can adjust the logging level
                    format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
                    handlers=[logging.StreamHandler()])  # Log to console


BOT_TOKEN = "7560837008:AAGplQY4p0wbJKW_BI2tZBnIPmGJXWNzpPI"
CHAT_ID = "163458583"

def send_telegram_message(message):
    """Send a message to Telegram chat."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}

    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        logging.info("Message sent to Telegram successfully.")
    except requests.exceptions.RequestException as e:
        logging.error("Failed to send Telegram message: %s", e)


def load_schedule():
    """
    Load or define the schedule as a set of tuples.
    Each tuple is in the form (month, day, hour, minute).
    """
    return load_time_tuples()


def run_task():
    """
    Runs your task and sends the execution result to Telegram.
    """
    try:
        result = subprocess.run(
            ["/home/ahmad/PrayerPi/.venv/bin/python", "src/runner.py"],
            check=True,
            stdout=subprocess.PIPE,  # Capture stdout
            stderr=subprocess.PIPE   # Capture stderr
        )

        # Check if stdout is not None
        output = result.stdout.decode().strip() if result.stdout else "No output"
        logging.info("Task executed successfully.")
        send_telegram_message(f"✅ Task executed successfully:\n{output}")

    except subprocess.CalledProcessError as e:
        error_message = e.stderr.decode().strip() if e.stderr else "No error message"
        logging.error("Task execution failed: %s", error_message)
        send_telegram_message(f"❌ Task execution failed:\n{error_message}")


def main_loop(schedule):
    """
    Main loop that checks every few seconds if the current time (month, day, hour, minute)
    matches any scheduled time. Once a match is found, run the task and sleep for 60 seconds.
    """
    now = datetime.datetime.now()
    current_tuple = (now.month, now.day, now.hour, now.minute)
    logging.debug("Current time tuple: %s", current_tuple)   
    if current_tuple in schedule:
        logging.info(f"Match found for time {current_tuple}! Executing task...")
        run_task()
        # Wait for 60 seconds to avoid triggering the same minute again

if __name__ == "__main__":
    schedule = load_schedule()
    main_loop(schedule)
