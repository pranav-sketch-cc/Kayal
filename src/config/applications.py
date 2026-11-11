# Application keywords and configured actions.
applications = {
    "open_chrome": {
        "keyword": ["chrome", "google chrome", "browser", "web browser"],
        "response": "Opening Chrome...",
        "action": "start chrome",
        "close_response": "Closing Chrome...",
        "close_action": "powershell -NoProfile -Command \"Get-Process -Name 'chrome' -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 } | ForEach-Object { [void]$_.CloseMainWindow() }\""
    },
    "open_explorer": {
        "keyword": ["file manager", "explorer", "windows explorer", "file explorer"],
        "response": "Opening File Explorer...",
        "action": "start explorer",
        "close_response": "Closing File Explorer windows...",
        "close_action": "powershell -NoProfile -Command \"$shell = New-Object -ComObject Shell.Application; $shell.Windows() | Where-Object { $_.FullName -match 'explorer.exe' } | ForEach-Object { $_.Quit() }\""
    },
    "open_chatgpt": {
        "keyword": ["chatgpt", "openai", "gpt"],
        "response": "Opening ChatGPT...",
        "action": "start chatgpt",
        "close_response": "Closing ChatGPT...",
        "close_action": "powershell -NoProfile -Command \"Get-Process -Name 'ChatGPT' -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 } | ForEach-Object { [void]$_.CloseMainWindow() }\""
    },
    "open_spotify": {
        "keyword": ["spotify", "music", "spotify music"],
        "response": "Opening Spotify...",
        "action": "start https://open.spotify.com",
        "close_response": "Closing Spotify...",
        "close_action": "powershell -NoProfile -Command \"Get-Process -Name 'Spotify' -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 } | ForEach-Object { [void]$_.CloseMainWindow() }\""
    },
    "open_cmd": {
        "keyword": ["command prompt", "cmd", "terminal", "shell"],
        "response": "Opening Command Prompt...",
        "action": "start cmd",
        "close_response": "Closing Command Prompt...",
        "close_action": "powershell -NoProfile -Command \"Get-Process -Name 'cmd' -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 } | ForEach-Object { [void]$_.CloseMainWindow() }\""
    }
}
