import os
from src.config.applications import applications
from src.config.intention import intention
from src.config.termination import termination

exit_commands = ["exit", "close", "terminate kayal", "stop", "kayal close pannu"]


def detect_application(key):
    for app,details in applications.items():
        if any(keyword in key for keyword in details["keyword"]): 
            return app
    return None


def process_command(key,detected_app):

    has_intent = any(word in key for word in intention["has_intention"])
    has_no_intent = any(word in key for word in intention["no_intention"])

    if has_intent and detected_app:
        return "Command Accepted. Initializing....", detected_app
    elif has_no_intent:
        return "Okay, I won't open any application.", None
    elif detected_app is None:
        return "Application not recognized.", None


    return None


def execute_command(status,command):
   
    if status == "CANCELLED":
        print("Okay, command cancelled.")
        return

    if status == "NO_INTENT":
        print("What should I do with that application?")
        return

    if status == "APP_NOT_FOUND":
        print("Application not recognized.")
        return

    details = applications[command]
    print(details["response"])
    os.system(details["action"])

while True:
    key = input("enter command : ").strip().lower()

    if key in termination["exit_commands"]:
        print("Exiting the program.")
        break

    detected_apps = detect_application(key)
    response, command = process_command(key, detected_apps)

    print(response)
    execute_command(response, command)