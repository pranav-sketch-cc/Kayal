import os

key=input("enter command : ").strip().lower()

intend = ["open", "start", "run", "launch", "open pannu"]

def process_command(key):
    if  key == "chrome" and key in intend :
        return "open_chrome"
    elif key in intend and key == "file manager":
        return "open_explorer"
    else:
        return None
    
command = process_command(key)

def execute_command(command):
    if command == "open_chrome":
        print("Opening Chrome...")
        os.system("start chrome")
    elif command == "open_explorer":
        print("Opening File Explorer...")
        os.system("start explorer")
    else:
        print("Command not recognized.")

execute_command(command)
