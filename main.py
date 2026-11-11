import os
import subprocess
from src.config.applications import applications
from src.config.intention import intention
from src.config.termination import termination
from src.confirmation import request_confirmation


def detect_application(key):
    for app, details in applications.items():
        if any(keyword in key for keyword in details["keyword"]):
            return app
    return None


def process_command(key, detected_app):

    if not key:
        return "NO_COMMAND", None

    has_open_intent = any(word in key for word in intention["open"])
    has_cancel_intent = any(word in key for word in intention["cancel"])
    has_close_intent = any(word in key for word in intention["close"])

    # Explicit negative commands take priority over action intents.
    if has_cancel_intent:
        return "CANCELLED", None

    if has_close_intent:
        if detected_app:
            return "CLOSE_REQUESTED", detected_app
        return "APP_NOT_FOUND", None

    if has_open_intent and detected_app:
        return "ACCEPTED", detected_app

    if detected_app and not has_open_intent:
        return "NO_INTENT", detected_app

    if has_open_intent and detected_app is None:
        return "APP_NOT_FOUND", None

    return "NO_COMMAND", None


def execute_close_action(action):
    """Run a configured PowerShell close script and return its reported result."""
    try:
        result = subprocess.run(
            [
                "powershell.exe",
                "-NoProfile",
                "-NonInteractive",
                "-ExecutionPolicy",
                "Bypass",
                "-Command",
                action
            ],
            capture_output=True,
            text=True,
            timeout=20,
            check=False
        )
    except FileNotFoundError:
        return "POWERSHELL_NOT_FOUND"
    except subprocess.TimeoutExpired:
        return "TIMEOUT"

    if result.returncode != 0:
        error = result.stderr.strip()
        if error:
            print(f"Close action error: {error}")
        return "EXECUTION_FAILED"

    output = result.stdout.strip().upper()
    if "CLOSED" in output:
        return "CLOSED"
    if "NOT_RUNNING" in output:
        return "NOT_RUNNING"
    if "STILL_RUNNING" in output:
        return "STILL_RUNNING"
    if "CLOSE_FAILED" in output:
        return "CLOSE_FAILED"

    return "UNKNOWN_RESULT"


def execute_command(status, command):

    if status == "CANCELLED":
        print("Okay, command cancelled.")
        return

    if status == "CLOSE_REQUESTED":
        details = applications.get(command)
        if details is None or not details.get("close_action"):
            print("Closing this application is not configured.")
            return

        confirmation = request_confirmation(f"close {command}")

        if confirmation == "REJECTED":
            print("Okay, I'll leave it open.")
            return

        print(details["close_response"])
        close_result = execute_close_action(details["close_action"])

        if close_result == "CLOSED":
            print("Application closed successfully.")
        elif close_result == "NOT_RUNNING":
            print("The application is not currently running.")
        elif close_result == "STILL_RUNNING":
            print("The application did not close. It may have an open dialog or unsaved work.")
        elif close_result == "CLOSE_FAILED":
            print("Windows did not accept the close request.")
        elif close_result == "POWERSHELL_NOT_FOUND":
            print("PowerShell was not found. This close action requires Windows PowerShell.")
        elif close_result == "TIMEOUT":
            print("The close operation timed out.")
        else:
            print("The close operation ran, but Kayal could not verify that the application closed.")
        return

    if status == "NO_INTENT":
        print(f"What should I do with {command}?")
        return

    if status == "APP_NOT_FOUND":
        print("Application not recognized.")
        return

    if status == "NO_COMMAND":
        print("No command detected.")
        return

    if status != "ACCEPTED" or command is None:
        print("Unable to execute command.")
        return

    details = applications.get(command)
    if details is None:
        print("Application not recognized.")
        return

    print(details["response"])
    os.system(details["action"])


while True:
    key = input("enter command : ").strip().lower()

    if key in termination["exit_commands"]:
        print("Exiting the program.")
        break

    detected_app = detect_application(key)
    status, command = process_command(key, detected_app)
    execute_command(status, command)
