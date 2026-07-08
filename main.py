import os

while True:
    key=input("enter command : ").strip().lower()

    #intention and no_intention keywords
    intent = ["open", "start", "run", "launch", "open pannu"]
    no_intent = ["close", "exit", "terminate", "stop", "pannadha", "close pannu"]

    #application keywords
    chrome = ["chrome", "google chrome", "browser", "web browser"]
    file_manager = ["file manager", "explorer", "windows explorer", "file explorer"]
    chatgpt = ["chatgpt", "openai", "gpt"]
    Spotify = ["spotify", "music", "spotify music"]
    cmd = ["command prompt", "cmd", "terminal", "shell"]

    #intention detection
    has_intent = any(word in key for word in intent)
    has_no_intent = any(word in key for word in no_intent)

    #application detection
    def detect_application(key, chrome, file_manager, chatgpt, Spotify, cmd):
        chrome_detected = any(word in key for word in chrome)
        file_manager_detected = any(word in key for word in file_manager)
        chatgpt_detected = any(word in key for word in chatgpt)
        spotify_detected = any(word in key for word in Spotify)
        cmd_detected = any(word in key for word in cmd)

        return chrome_detected, file_manager_detected, chatgpt_detected, spotify_detected, cmd_detected

    #processing command
    def process_command(has_intent, chrome_detected, file_manager_detected, chatgpt_detected, spotify_detected, cmd_detected):
        if  has_intent and chrome_detected:
            return "open_chrome"
        elif has_intent and file_manager_detected:
            return "open_explorer"
        elif has_intent and chatgpt_detected:
            return "open_chatgpt"
        elif has_intent and spotify_detected:
            return "open_spotify"
        elif has_intent and cmd_detected:
            return "open_cmd"
        elif has_no_intent:
            return None
        else:
            return "Command not recognized."

        
    command = process_command(has_intent, *detect_application(key, chrome, file_manager, chatgpt, Spotify, cmd))

    #executing command
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

    execute_command(command)

    if key in ["exit", "close", "terminate kayal", "stop", "pannadha", "kayal close pannu"]:
        print("Exiting the program.")
        break