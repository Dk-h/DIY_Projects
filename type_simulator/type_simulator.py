import json
import time

def load_text_from_json(filename="typewriter_text.json"):
    """
    Load the text content for the typewriter effect from a JSON file.

    Args:
        filename (str): The name of the JSON file containing the text.

    Returns:
        str: The text to display with the typewriter effect.
    """
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("text", "")

def typewriter_effect(text, delay=0.05):
    """
    Prints the given text to the terminal with a typewriter animation.

    Args:
        text (str): The text to display.
        delay (float): Time (in seconds) to wait between each character.
    """
    for char in text:
        print(char, end='', flush=True)  # Print character without newline and flush output
        time.sleep(delay)                # Pause to create typewriter effect
    print()  # Move to the next line after the text is printed

def main():
    """
    Main function to run the typewriter effect.
    Loads the text from a JSON file and displays it with animation.
    """
    text = load_text_from_json()  # Get the text from JSON file
    typewriter_effect(text)       # Display with typewriter effect

if __name__ == "__main__":
    # Entry point for the script
    main()