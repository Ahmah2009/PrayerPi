import pygame
import threading
import logging
import evdev
import time
import sys

# Global variable to keep track of the sound playing status
sound_playing = False
exit_flag = False  # Flag to exit the program

def play_prayer_alert(prayer_name):
    """Plays a sound alert using Pygame."""
    global sound_playing, exit_flag
    logging.info(f"Time for {prayer_name}!")

    pygame.mixer.music.load("/opt/PrayerPi/prayer_alert.mp3")  # Replace with your sound file
    pygame.mixer.music.play()
    sound_playing = True

    while pygame.mixer.music.get_busy():  # Wait for the sound to finish playing
        time.sleep(0.1)  # Reduce CPU usage while waiting for the sound to finish
    sound_playing = False

    print("Sound finished playing.")
    exit_flag = True  # Set the flag to True once sound is done, which will exit the main loop

def start_sound():
    """Initialize Pygame and start playing the prayer alert sound."""
    pygame.mixer.init()
    play_prayer_alert("Prayer")

def stop_sound():
    """Stops the sound if it is playing."""
    global sound_playing
    if sound_playing:
        pygame.mixer.music.stop()
        sound_playing = False
        logging.info("Sound stopped due to input event.")
        exit_flag = True  # Exit flag set if input is received

def monitor_device(device_path):
    """Monitor a specific input device for key events."""
    try:
        device = evdev.InputDevice(device_path)
        print(f"Listening for input on {device.path} ({device.name})")

        for event in device.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                key_event = evdev.categorize(event)

                if key_event.keystate == key_event.key_down:
                    print(f"Input detected from {device.name} ({device.path}): {key_event.keycode}")
                    stop_sound()  # Stop sound if any key is pressed
                    break  # Exit the loop after detecting a key press

    except Exception as e:
        print(f"Error reading device {device_path}: {e}")

def find_input_devices():
    """Find all available input devices and monitor them in parallel threads."""
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

    if not devices:
        print("No input devices found!")
        return

    print("Detected input devices:")
    for device in devices:
        print(f"- {device.path}: {device.name}")

    # Start a thread for each device
    for device in devices:
        threading.Thread(target=monitor_device, args=(device.path,), daemon=True).start()

if __name__ == "__main__":
    # Start input device monitoring in the background
    find_input_devices()

    # Start the prayer alert sound in a separate thread
    sound_thread = threading.Thread(target=start_sound, daemon=True)
    sound_thread.start()

    # Keep the main program running until either the sound ends or input is detected
    while not exit_flag:
        time.sleep(0.1)  # Keep checking if we need to exit

    print("Exiting the script.")
    sys.exit()  # Exit the program when either sound ends or button is pressed