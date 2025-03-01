# main.py v0.2

import subprocess
import os
import sys
import logging
import time


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        filename='app.log',
        format='%(asctime)s %(levelname)s: %(message)s'
    )


def run_command(command):
    try:
        logging.info(f"Running command: {' '.join(command)}")
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        logging.info(f"Command output: {result.stdout}")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Command '{' '.join(command)}' failed with error: {e.stderr}")
        print(f"Error executing {' '.join(command)}: {e.stderr}")
        return False


def main():
    setup_logging()
    print("Starting the computer vision project workflow continuously...")

    # Define file paths
    screenshot_path = "chrome_screenshot.png"
    extracted_text_path = "extracted_text.txt"
    analysis_result_path = "analysis_result.txt"

    try:
        while True:
            print("\n--- Running workflow iteration ---")

            # Step 1: Capture Chrome Window
            print("Step 1: Capturing Chrome window...")
            cmd_capture = [sys.executable, "ROIExtractor.py", "--output", extracted_text_path]
            if not run_command(cmd_capture):
                print("Failed to capture Chrome window. Skipping this iteration.")
                time.sleep(5)
                continue  # Skip to the next iteration

            # Step 2: Extract Text
            #print("Step 2: Extracting text from image...")
            #cmd_extract = [sys.executable, "extract_text.py", "--input", screenshot_path, "--output",
            #               extracted_text_path]
            #if not run_command(cmd_extract):
            #    print("Failed to extract text. Skipping this iteration.")
            #    time.sleep(5)
            #    continue

            # Step 3: Analyze Text
            print("Step 3: Analyzing extracted text...")
            cmd_analyze = [sys.executable, "analyze_text.py", "--input", extracted_text_path, "--output",
                           analysis_result_path]
            if not run_command(cmd_analyze):
                print("Failed to analyze text. Skipping this iteration.")
                time.sleep(5)
                continue

            # Final Result
            if os.path.exists(analysis_result_path):
                with open(analysis_result_path, 'r') as f:
                    result = f.read().strip()
                print(f"Analysis Result: {result}")
            else:
                print("No analysis result found.")

            print("Workflow iteration completed successfully.")

            # Wait for a few seconds before the next iteration.
            time.sleep(5)

    except KeyboardInterrupt:
        print("\nWorkflow interrupted by user. Exiting.")


if __name__ == "__main__":
    main()

