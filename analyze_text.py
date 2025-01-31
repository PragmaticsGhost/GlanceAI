"""analyze_text.py v0.1"""

import os
import argparse
import logging
import sys
from openai import OpenAI

client = OpenAI()

def setup_logging():
    """
    Sets up logging to a file.
    """
    logging.basicConfig(
        level=logging.INFO,
        filename='app.log',
        format='%(asctime)s %(levelname)s:%(message)s'
    )


def is_multiple_choice_question(text):
    """
    Determines whether the given text is a multiple-choice question using OpenAI's ChatCompletion API.
    """
    prompt = (
        "Determine whether the following text is a multiple-choice question. If the the text is a multiple choice "
        "question, parse out just the question and the possible answers."
        f"\nText: {text}\n\n"
        "Is there a multiple-choice question in the text?"
    )

    try:
        # Create a chat completion request to OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Replace with gpt-4 if preferred
            messages=[
                {"role": "system", "content": "You are a bot that determines whether a given chunk of text "
                                              "contains a multiple-choice question, and if so, answers it correctly."},
                {"role": "user", "content": prompt},
            ],
            temperature=0  # Use 0 for deterministic responses
        )

        # Extract the assistant's response
        logging.info(f"OpenAI API response: {response}")
        return print(response.choices[0].message)

    except Exception as e:
        logging.error(f"Error communicating with OpenAI API: {e}")
        print(f"Error communicating with OpenAI API: {e}")
        return False


def analyze_text(input_path, output_path):
    """
    Analyzes the extracted text to determine if it is a multiple-choice question.
    """
    try:
        # Read the input text file
        with open(input_path, 'r', encoding='utf-8') as f:
            text = f.read()

        # Determine if the text is a multiple-choice question
        result = is_multiple_choice_question(text)

        # Save the result to the output file
        with open(output_path, 'w', encoding='utf-8') as f:
            if result:
                f.write("Yes")
                print("The detected text is a multiple-choice question.")
            else:
                f.write("No")
                print("The detected text is NOT a multiple-choice question.")

        logging.info(f"Analysis result saved to {output_path}")
        return True

    except Exception as e:
        logging.error(f"Error analyzing text: {e}")
        print(f"Error analyzing text: {e}")
        return False


def main():
    """
    Main function to parse arguments and initiate the analysis.
    """
    setup_logging()
    parser = argparse.ArgumentParser(
        description="Analyze extracted text to determine if it's a multiple-choice question."
    )
    parser.add_argument('--input', type=str, required=True, help='Path to the extracted text file.')
    parser.add_argument('--output', type=str, default='analysis_result.txt', help='Path to save the analysis result.')

    args = parser.parse_args()

    # Run the text analysis
    success = analyze_text(args.input, args.output)
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
