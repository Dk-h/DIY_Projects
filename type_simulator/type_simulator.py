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


# Your indented paragraph/code block
paragraph = '''

long getPages(const vector<int> pages, const vector<int> threshold) {
int n = pages.size();
vector<pair<int, int>> printers;

for (int i = 0; i < n; ++i) {
printers.emplace_back(threshold[i], pages[i]);
}

// Sort printers by increasing threshold
sort(printers.begin(), printers.end());

// Min heap to keep selected printers' pages
priority_queue<int, vector<int>, greater<int>> minHeap;

for (auto& [thresh, page] : printers) {
if ((int)minHeap.size() < thresh) {
minHeap.push(page);
} else if (!minHeap.empty() && minHeap.top() < page) {
minHeap.pop();
minHeap.push(page);
}
}

// Sum up pages using long long
long long total = 0;
while (!minHeap.empty()) {
total += minHeap.top();
minHeap.pop();
}

return total;
}


'''


# Start typing after Esc key
simulate_typing_on_esc(paragraph, delay=0.01)
