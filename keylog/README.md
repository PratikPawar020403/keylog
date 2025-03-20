# Advanced Keylogger with HTML Email Reporting

**Disclaimer:**  
This project is intended for educational and authorized penetration testing purposes only. Unauthorized use of this software is illegal and unethical. Use it only on systems where you have explicit permission.

## Overview

This Python-based keylogger captures:
- Keystrokes with timestamps.
- Active window titles at the time of each keystroke.
- Periodic screenshots.

The captured data is compiled into a well-formatted HTML email that includes a summary table of keystrokes and inline screenshots for easy review.

## Features

- **Keylogging:** Records every keystroke along with the active window title and timestamp.
- **Active Window Logging:** Captures the title of the active window to provide context.
- **Timer Functionality:** Runs the keylogger for a specified duration or until the `Esc` key is pressed.
- **Screenshot Capture:** Takes screenshots at user-defined intervals and stores them locally.
- **Formatted HTML Email:** Sends a detailed HTML email with a formatted table of keystrokes and embedded screenshots.
- **Stealth Mode:** Supports a stealth mode that hides the console output.

## Setup and Installation

### Prerequisites

- Python 3.x

### Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/advanced-keylogger.git
   cd advanced-keylogger

to run :- python keylogger.py --stealth --timer 60 --screenshot_interval 30
