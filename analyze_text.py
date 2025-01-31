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
        "Determine whether the following text contains a multiple-choice question. If the text does contain a "
        "multiple choice question, parse out the question and the possible answers. Reply only with information "
        "pertinent to the question, the question itself, the possible answers, and finally, the correct answer. If "
        "the text does not provide the correct answer, research it and provide the closest answer from the answers "
        "provided."
        f"\nText: {text}\n\n"
    )

    try:
        # Create a chat completion request to OpenAI
        response = client.chat.completions.create(
            model="gpt-4",  # Replace with gpt-4 if preferred
            messages=[
                {"role": "system", "content": "You are purpose-built Multiple Choice Question solver. You solve "
                                              "multiple choice questions with the correct answer."},
                {"role": "user", "content": prompt},
            ],
            temperature=0  # Use 0 for deterministic responses
        )

        logging.info(f"OpenAI API response: {response}")

        # Access the content from the ChatCompletionMessage object
        raw_message = response.choices[0].message.content

        # Replace literal "\n" with actual newlines
        formatted_message = raw_message.replace("\\n", "\n")

        # Print the formatted text for readability, and return it
        print(formatted_message)
        return formatted_message

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
