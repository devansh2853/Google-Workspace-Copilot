import pyfiglet
import re

def show_banner():
    banner = pyfiglet.figlet_format("Google Workspace Copilot CLI")
    print(banner)

def isValidMail(email: str) -> bool:
    """Basic regex validation for email address."""
    regex = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return re.match(regex, email) is not None
