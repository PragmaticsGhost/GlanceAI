import cv2
import pytesseract
import pyautogui
import numpy as np


# Function to take a screenshot
def take_screenshot():
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    return screenshot


# Function to preprocess image for OCR
def preprocess_image(roi):
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return thresh


# Function to extract text using TesseractOCR
def extract_text(roi):
    processed_roi = preprocess_image(roi)
    text = pytesseract.image_to_string(processed_roi, config='--psm 6')
    return text.strip()


# Main function
def main():
    image = take_screenshot()

    roi = cv2.selectROI("Select Region of Interest", image, showCrosshair=True, fromCenter=False)
    cv2.destroyAllWindows()

    if roi == (0, 0, 0, 0):
        print("No ROI selected.")
        return

    x, y, w, h = roi
    selected_roi = image[y:y + h, x:x + w]

    extracted_text = extract_text(selected_roi)
    print("Extracted Text:")
    with open("extracted_text.txt", "w", encoding="utf-8") as file:
        file.write(extracted_text)
    print(extracted_text)


if __name__ == "__main__":
    main()
