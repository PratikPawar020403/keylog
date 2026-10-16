# Basic Python Keylogger with HTML Email Reporting

## Why I Built This

After watching *Mr. Robot*, I became curious about how keylogging and activity-monitoring tools work behind the scenes. I discovered that tools for these purposes already existed, but I wanted to go beyond just using them and gain hands-on experience understanding their backend mechanisms.

So, I built a basic keylogger using Python as a learning project to explore keyboard event monitoring, active window tracking, screenshot capture, and report generation.

## What Is This Project?

This is a basic Python-based keylogger developed for educational purposes. It demonstrates how keyboard events can be recorded alongside contextual information, such as the active window title and timestamp.

The project also includes periodic screenshot capture and HTML report generation, bringing together several Python libraries to demonstrate how these components work together.

## How It Works

- **Keyboard Event Logging:** Uses `pynput` to record keyboard events with timestamps.
- **Active Window Tracking:** Uses `win32gui` to retrieve the active window title on Windows.
- **Timer Functionality:** Supports a configurable runtime and stops keyboard listening when the `Esc` key is released.
- **Screenshot Capture:** Uses `pyautogui` to capture screenshots at configurable intervals and save them locally.
- **HTML Report Generation:** Formats recorded keystrokes, active window titles, and timestamps into an HTML table, with references to available screenshots.
- **Email Integration:** Uses Python's `smtplib` and email libraries to construct an HTML email with inline screenshot attachments.
- **Command-Line Options:** Supports configurable execution duration, screenshot intervals, and optional console-output suppression.

## Technologies Used

- Python
- `pynput`
- `pandas`
- `pyautogui`
- `pywin32`
- `threading`
- `argparse`
- `smtplib` and `email.mime`

## Running the Project

Example command:

```bash
python keylogger.py --stealth --timer 60 --screenshot_interval 30
```

**Available arguments:**

- `--stealth`: Attempts to hide the console and suppress console output.
- `--timer`: Sets the keyboard listener's runtime in seconds. Defaults to `0`, meaning no timer is set.
- `--screenshot_interval`: Sets the interval between screenshots in seconds. Defaults to `0`, disabling screenshot capture.

## Disclaimer

This project was created for educational purposes and authorized security research. Use it only in controlled environments and on systems where you have explicit permission. Unauthorized monitoring or collection of another person's information may violate privacy laws and other applicable regulations.
