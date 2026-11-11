# Application keywords and configured actions.
# close_action values are PowerShell scripts executed directly by main.py.

applications = {
    "open_chrome": {
        "keyword": ["chrome", "google chrome", "browser", "web browser"],
        "response": "Opening Chrome...",
        "action": "start chrome",
        "close_response": "Closing Chrome windows...",
        "close_action": r"""
$type = @'
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Runtime.InteropServices;
public static class KayalWindowCloser {
    private delegate bool EnumWindowsProc(IntPtr hWnd, IntPtr lParam);
    [DllImport("user32.dll")] private static extern bool EnumWindows(EnumWindowsProc callback, IntPtr lParam);
    [DllImport("user32.dll")] private static extern bool IsWindowVisible(IntPtr hWnd);
    [DllImport("user32.dll")] private static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint processId);
    [DllImport("user32.dll")] private static extern bool PostMessage(IntPtr hWnd, uint msg, IntPtr wParam, IntPtr lParam);
    private static HashSet<int> GetIds(string name) {
        var ids = new HashSet<int>();
        foreach (var p in Process.GetProcessesByName(name)) ids.Add(p.Id);
        return ids;
    }
    public static int Count(string name) {
        var ids = GetIds(name); int count = 0;
        EnumWindows((h, l) => {
            uint pid; GetWindowThreadProcessId(h, out pid);
            if (ids.Contains((int)pid) && IsWindowVisible(h)) count++;
            return true;
        }, IntPtr.Zero);
        return count;
    }
    public static int Close(string name) {
        var ids = GetIds(name); int sent = 0;
        EnumWindows((h, l) => {
            uint pid; GetWindowThreadProcessId(h, out pid);
            if (ids.Contains((int)pid) && IsWindowVisible(h) &&
                PostMessage(h, 0x0010, IntPtr.Zero, IntPtr.Zero)) sent++;
            return true;
        }, IntPtr.Zero);
        return sent;
    }
}
'@
Add-Type -TypeDefinition $type
$before = [KayalWindowCloser]::Count('chrome')
if ($before -eq 0) { Write-Output 'NOT_RUNNING'; exit 0 }
[void][KayalWindowCloser]::Close('chrome')
$deadline = (Get-Date).AddSeconds(8)
do {
    Start-Sleep -Milliseconds 300
    $remaining = [KayalWindowCloser]::Count('chrome')
} while ($remaining -gt 0 -and (Get-Date) -lt $deadline)
if ($remaining -eq 0) { Write-Output 'CLOSED' } else { Write-Output "STILL_RUNNING:$remaining" }
"""
    },
    "open_explorer": {
        "keyword": ["file manager", "explorer", "windows explorer", "file explorer"],
        "response": "Opening File Explorer...",
        "action": "start explorer",
        "close_response": "Closing File Explorer windows...",
        "close_action": r"""
$shell = New-Object -ComObject Shell.Application
$windows = @($shell.Windows() | Where-Object { $_.FullName -match 'explorer.exe' })
if ($windows.Count -eq 0) { Write-Output 'NOT_RUNNING'; exit 0 }
foreach ($window in $windows) { try { $window.Quit() } catch {} }
Start-Sleep -Milliseconds 700
$remaining = @($shell.Windows() | Where-Object { $_.FullName -match 'explorer.exe' })
if ($remaining.Count -eq 0) { Write-Output 'CLOSED' } else { Write-Output "STILL_RUNNING:$($remaining.Count)" }
"""
    },
    "open_chatgpt": {
        "keyword": ["chatgpt", "openai", "gpt"],
        "response": "Opening ChatGPT...",
        "action": "start chatgpt",
        "close_response": "Closing ChatGPT...",
        "close_action": r"""
$targets = @(Get-Process -Name 'ChatGPT' -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 })
if ($targets.Count -eq 0) { Write-Output 'NOT_RUNNING'; exit 0 }
foreach ($p in $targets) { [void]$p.CloseMainWindow() }
Start-Sleep -Seconds 2
$remaining = @(Get-Process -Name 'ChatGPT' -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 })
if ($remaining.Count -eq 0) { Write-Output 'CLOSED' } else { Write-Output "STILL_RUNNING:$($remaining.Count)" }
"""
    },
    "open_spotify": {
        "keyword": ["spotify", "music", "spotify music"],
        "response": "Opening Spotify...",
        "action": "start https://open.spotify.com",
        "close_response": "Closing Spotify...",
        "close_action": r"""
$targets = @(Get-Process -Name 'Spotify' -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 })
if ($targets.Count -eq 0) { Write-Output 'NOT_RUNNING'; exit 0 }
foreach ($p in $targets) { [void]$p.CloseMainWindow() }
Start-Sleep -Seconds 2
$remaining = @(Get-Process -Name 'Spotify' -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 })
if ($remaining.Count -eq 0) { Write-Output 'CLOSED' } else { Write-Output "STILL_RUNNING:$($remaining.Count)" }
"""
    },
    "open_cmd": {
        "keyword": ["command prompt", "cmd", "terminal", "shell"],
        "response": "Opening Command Prompt...",
        "action": "start cmd",
        "close_response": "Closing Command Prompt windows...",
        "close_action": r"""
$type = @'
using System;
using System.Diagnostics;
using System.Runtime.InteropServices;
public static class KayalCmdCloser {
    private const uint WM_CLOSE = 0x0010;
    [DllImport("kernel32.dll", SetLastError=true)] private static extern bool FreeConsole();
    [DllImport("kernel32.dll", SetLastError=true)] private static extern bool AttachConsole(uint processId);
    [DllImport("kernel32.dll")] private static extern IntPtr GetConsoleWindow();
    [DllImport("user32.dll")] private static extern bool PostMessage(IntPtr hWnd, uint msg, IntPtr wParam, IntPtr lParam);
    public static int CloseAll() {
        int sent = 0;
        foreach (var p in Process.GetProcessesByName("cmd")) {
            try {
                FreeConsole();
                if (!AttachConsole((uint)p.Id)) continue;
                IntPtr hwnd = GetConsoleWindow();
                if (hwnd != IntPtr.Zero && PostMessage(hwnd, WM_CLOSE, IntPtr.Zero, IntPtr.Zero)) sent++;
            } catch { }
            finally { try { FreeConsole(); } catch { } }
        }
        return sent;
    }
}
'@
Add-Type -TypeDefinition $type
$targets = @(Get-Process -Name 'cmd' -ErrorAction SilentlyContinue)
if ($targets.Count -eq 0) { Write-Output 'NOT_RUNNING'; exit 0 }
$sent = [KayalCmdCloser]::CloseAll()
$deadline = (Get-Date).AddSeconds(8)
do {
    Start-Sleep -Milliseconds 300
    $remaining = @(Get-Process -Name 'cmd' -ErrorAction SilentlyContinue)
} while ($remaining.Count -gt 0 -and (Get-Date) -lt $deadline)
if ($remaining.Count -eq 0) { Write-Output 'CLOSED' } else { Write-Output "STILL_RUNNING:$($remaining.Count):MESSAGES_SENT:$sent" }
"""
    }
}
