import os
from src.config.applications import applications
from src.config.intention import intention
from src.config.termination import termination


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

    # Cancellation takes priority over all action intents.
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


def execute_command(status, command):

    if status == "CANCELLED":
        print("Okay, command cancelled.")
        return

    if status == "CLOSE_REQUESTED":
        print(f"Close request recognized for {command}. App closing is not implemented yet.")
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
