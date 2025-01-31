# capture_chrome_window.py

import pygetwindow as gw
import pyautogui
import time
import argparse
import os
import logging


def setup_logging():
    logging.basicConfig(level=logging.INFO, filename='app.log',
                        format='%(asctime)s %(levelname)s:%(message)s')


def capture_chrome_window(save_path="chrome_screenshot.png"):
    try:
        # Get a list of all open windows with 'Chrome' in the title
        chrome_windows = [window for window in gw.getAllWindows() if 'chrome' in window.title.lower()]

        if not chrome_windows:
            logging.warning("No Google Chrome window found.")
            print("No Google Chrome window found.")
            return False

        # Assuming you want to capture the first Chrome window found
        chrome_window = chrome_windows[0]

        # Bring the Chrome window to the foreground
        chrome_window.activate()
        logging.info(f"Activated Chrome window: {chrome_window.title}")

        # Wait a moment to ensure the window is in the foreground
        time.sleep(1)

        # Get window position and size
        left, top, width, height = chrome_window.left, chrome_window.top, chrome_window.width, chrome_window.height
        logging.info(f"Chrome window position and size: left={left}, top={top}, width={width}, height={height}")

        # Capture the region of the Chrome window
        screenshot = pyautogui.screenshot(region=(left, top, width, height))
        screenshot.save(save_path)
        logging.info(f"Chrome window screenshot saved to {save_path}")
        print(f"Chrome window screenshot saved to {save_path}")
        return True
    except Exception as e:
        logging.error(f"Error capturing Chrome window: {e}")
        print(f"Error capturing Chrome window: {e}")
        return False


def main():
    setup_logging()
    parser = argparse.ArgumentParser(description="Capture a screenshot of the active Google Chrome window.")
    parser.add_argument('--output', type=str, default='chrome_screenshot.png', help='Path to save the screenshot.')

    args = parser.parse_args()

    success = capture_chrome_window(args.output)
    if not success:
        exit(1)


if __name__ == "__main__":
    main()
