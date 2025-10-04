import json
import time
import keyboard
import os

def load_text_from_json(filename="typewriter_text.json"):
    """
    Load the text content for the typewriter effect from a JSON file.

    Args:
        filename (str): The name of the JSON file containing the text.

    Returns:
        str: The text to display with the typewriter effect.
    """
    # Get the absolute path to ensure file is found regardless of working directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, filename)
    if not os.path.exists(filepath):
        print(f"Error: '{filename}' not found in {script_dir}. Please create it with a 'text' field.")
        exit(1)
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("text", "")

def simulate_typing_on_esc(text, delay=0.05):
    """
    Waits for the user to press 'Esc', then simulates typing the given text 
    into whatever window is currently focused (using the keyboard package).

    Args:
        text (str): Text to type.
        delay (float): Delay between each keystroke.
    """
    print("Press ESC to start typing...")
    keyboard.wait('esc')  # Wait for the 'Esc' key

    print("Typing will start in 3 seconds... Switch to the target window.")
    # Countdown for user clarity
    for i in range(3, 0, -1):
        print(f"Typing in {i}...", end='\r', flush=True)
        time.sleep(1)

    # Simulate typing into whatever window is currently active
    keyboard.write(text, delay)
    print("\nTyping complete.")

def main():
    """
    Main function to run the typewriter effect with simulated typing.
    Loads the text from a JSON file and types it into the active window after ESC is pressed.
    """
    text = load_text_from_json()  # Get the text from JSON file
    simulate_typing_on_esc(text, delay=0.01)

if __name__ == "__main__":
    # Entry point for the script
    main()