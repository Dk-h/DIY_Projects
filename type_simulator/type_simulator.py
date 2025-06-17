import keyboard
import time

def simulate_typing_on_esc(text, delay=0.05):
    """
    Waits for the user to press 'Esc', then simulates typing the given text.

    Args:
        text (str): Text to type.
        delay (float): Delay between each keystroke.
    """
    print("Press ESC to start typing...")
    keyboard.wait('esc')  # Wait for the 'Esc' key

    print("Typing will start in 3 seconds... Switch to the target window.")
    time.sleep(3)

    keyboard.write(text, delay)
    print("\nTyping complete.")

def remove_indentation(code_block: str) -> str:
    """
    Removes all leading spaces and tabs from each line of a multi-line string.

    Args:
        code_block (str): The indented code or paragraph.

    Returns:
        str: The unindented version of the code.
    """
    lines = code_block.splitlines()
    cleaned_lines = [line.lstrip() for line in lines]
    return '\n'.join(cleaned_lines)

# Your indented paragraph/code block
paragraph = '''

db.Customers.insertMany([
  {
    name: "Rahul Sharma",
    age: 35,
    purchases: ["Laptop", "Phone"]
  },
  {
    name: "Vikram Seth",
    age: 28,
    purchases: ["Tablet", "Headphones"]
  },
  {
    name: "Anjali Gowda",
    age: 40,
    purchases: ["Camera", "Tripod"]
  }
]);

db.Customers.find({ purchases: "Laptop" });



'''
# Define the custom exception
class CustomError(Exception):
    pass

def process_input(data):
    try:
        if not data:
            raise CustomError("Error: Empty input provided.")
        elif len(data) > 255:
            raise CustomError("Error: Input exceeds maximum length.")
        elif any(char.isdigit() for char in data):
            raise CustomError("Error: Input contains invalid characters.")
        else:
            return "Input processed successfully."
    except CustomError as e:
        return str(e)
    finally:
        print("Program execution completed.")

# Example usage:
print(process_input(""))             # Error: Empty input provided.
print(process_input("a" * 256))      # Error: Input exceeds maximum length.
print(process_input("hello123"))     # Error: Input contains invalid characters.
print(process_input("Hello World"))  # Input processed successfully.
'''

Remove indentation before typing
unindented_paragraph = remove_indentation(paragraph)

Start typing after Esc key
simulate_typing_on_esc(unindented_paragraph, delay=0.01)
   if not data:
            raise CustomError("Error: Empty input provided.")
        elif len(data) > 255:
            raise CustomError("Error: Input exceeds maximum length.")
        elif any(char.isdigit() for char in data):
            raise CustomError("Error: Input contains invalid characters.")
        else:
            return "Input processed successfully."
    except CustomError as e:
        return str(e)
    finally:
        print("Program execution completed.")

# Example usage:
print(process_input(""))             # Error: Empty input provided.
print(process_input("a" * 256))      # Error: Input exceeds maximum length.
print(process_input("hello123"))     # Error: Input contains invalid characters.
print(process_input("Hello World"))  # Input processed successfully.
'''

# Remove indentation before typing
unindented_paragraph = remove_indentation(paragraph)

# Start typing after Esc key
simulate_typing_on_esc(unindented_paragraph, delay=0.01)
