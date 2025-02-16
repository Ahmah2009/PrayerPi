from data.cache import load_time_tuples
import time
import datetime
import subprocess

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
        subprocess.run(["/opt/PrayerPi/.venv/bin/python", "src/runner.py"],check=True)
        print("Task executed successfully.")
    except subprocess.CalledProcessError as e:
        print("Task execution failed:", e)

def main_loop(schedule):
    """
    Main loop that checks every few seconds if the current time (month, day, hour, minute)
    matches any scheduled time. Once a match is found, run the task and sleep for 60 seconds.
    """
    while True:
        now = datetime.datetime.now()
        current_tuple = (now.month, now.day, now.hour, now.minute)

        if current_tuple in schedule:
            print(f"Match found for time {current_tuple}! Executing task...")
            run_task()
            # Wait for 60 seconds to avoid triggering the same minute again
            time.sleep(60)
        else:
            # Check again in a few seconds
            time.sleep(5)

if __name__ == "__main__":
    schedule = load_schedule()
    main_loop(schedule)