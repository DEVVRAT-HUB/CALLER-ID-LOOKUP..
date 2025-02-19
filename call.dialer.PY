import subprocess
import sys
import platform

def dial_number(phone_number):
    """
    Dials a given phone number using the system's default dialer.
    Works for Windows, macOS, and Linux.
    """
    if platform.system() == "Windows":
        subprocess.run(["explorer", f"tel:{phone_number}"])
    elif platform.system() == "Darwin":  # macOS
        subprocess.run(["open", f"tel:{phone_number}"])
    elif platform.system() == "Linux":
        subprocess.run(["xdg-open", f"tel:{phone_number}"])
    else:
        print("Unsupported operating system")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python call_dialer.py <phone_number>")
        sys.exit(1)
    
    phone_number = sys.argv[1]
    dial_number(phone_number)

