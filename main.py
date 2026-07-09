import os
from src.config.applications import applications

intent = ["open", "start", "run", "launch", "open pannu"]
no_intent = ["close", "exit", "terminate", "stop", "pannadha", "close pannu"]

exit_commands = ["exit", "close", "terminate kayal", "stop", "kayal close pannu"]


def detect_application(key):
    chrome_detected = any(word in key for word in applications["chrome"])
    file_manager_detected = any(word in key for word in applications["file_manager"])
    chatgpt_detected = any(word in key for word in applications["chatgpt"])
    spotify_detected = any(word in key for word in applications["Spotify"])
    cmd_detected = any(word in key for word in applications["cmd"])

    return chrome_detected, file_manager_detected, chatgpt_detected, spotify_detected, cmd_detected


def process_command(
    has_intent,
    has_no_intent,
    chrome_detected,
    file_manager_detected,
    chatgpt_detected,
    spotify_detected,
    cmd_detected,
):
    if has_no_intent:
        return None
    if has_intent and chrome_detected:
        return "open_chrome"
    if has_intent and file_manager_detected:
        return "open_explorer"
    if has_intent and chatgpt_detected:
        return "open_chatgpt"
    if has_intent and spotify_detected:
        return "open_spotify"
    if has_intent and cmd_detected:
        return "open_cmd"
    return None


def execute_command(command):
    if command == "open_chrome":
        print("Opening Chrome...")
        os.system("start chrome")
    elif command == "open_explorer":
        print("Opening File Explorer...")
        os.system("start explorer")
    elif command == "open_chatgpt":
        print("Opening ChatGPT...")
        os.system("start chatgpt")
    elif command == "open_spotify":
        print("Opening Spotify...")
        os.system("start https://open.spotify.com")
    elif command == "open_cmd":
        print("Opening Command Prompt...")
        os.system("start cmd")
    else:
        print("Command not recognized.")


while True:
    key = input("enter command : ").strip().lower()

    if key in exit_commands:
        print("Exiting the program.")
        break

    has_intent = any(word in key for word in intent)
    has_no_intent = any(word in key for word in no_intent)

    detected_apps = detect_application(key)
    command = process_command(has_intent, has_no_intent, *detected_apps)

    execute_command(command)