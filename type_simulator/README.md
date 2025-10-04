# Typewriter Effect in Python

This is a simple Python project that prints text to the terminal with a typewriter animation, importing the text from a JSON file.

## Features

- Loads text content from a JSON file for easy editing.
- Realistic typewriter animation in the terminal.
- Minimal and easy to extend.

## Usage

### 1. Prepare Your Text

Edit the `typewriter_text.json` file:

```json
{
  "text": "Hello, this is the typewriter effect! You can put any text here, even multiline.\nEnjoy coding!"
}
```

### 2. Run the Script

```bash
python typewriter.py
```

You’ll see the text appear letter-by-letter, just like a typewriter.

### 3. Customization

- Change the `"text"` in `typewriter_text.json` to anything you like.
- Adjust the `delay` parameter in `typewriter_effect()` for faster or slower typing.

## Requirements

- Python 3.x (uses only the standard library; no extra packages needed)

## License

MIT License

---

Enjoy your animated typewriter!