# Kayal

**Kayal** is a modular AI desktop assistant designed to provide a fast, reliable, and extensible voice interaction experience. The long-term goal is to build a personal assistant that can understand voice commands, perform system tasks, automate workflows, and support natural conversations through modern AI models.

## Vision

To create an intelligent desktop companion that is:

* Voice-first
* Modular and scalable
* Easy to extend with new features
* Privacy-conscious
* Reliable for daily productivity

## Current Development Stage

The project is currently focused on building the core foundation.

### Phase 1

* Project architecture
* Modular code structure
* Configuration management
* Logging
* Environment setup

### Planned Features

* Wake word detection
* Speech-to-Text (STT)
* Text-to-Speech (TTS)
* AI conversation
* Desktop automation
* File and application control
* Internet search
* Plugin support
* Memory system
* Context-aware conversations

## Project Structure

```text
Kayal/
│
├── src/
├── assets/
├── config/
├── docs/
├── tests/
├── .env
├── .gitignore
├── requirements.txt
├── Architecture.md
├── Decisions.md
├── README.md
└── main.py
```

## Tech Stack

* Python
* Git & GitHub
* Virtual Environment (venv)
* Markdown Documentation

Future integrations may include:

* Whisper / Faster-Whisper
* Gemini / OpenAI APIs
* Supabase
* Local LLM support
* Desktop automation libraries

## Getting Started

### Clone the repository

```bash
git clone https://github.com/pranav-sketch-cc/Kayal.git
cd Kayal
```

### Create a virtual environment

```bash
python -m venv .venv
```

### Activate the environment

**Windows (PowerShell)**

```powershell
.\.venv\Scripts\Activate.ps1
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run

```bash
python main.py
```

## Documentation

* `Architecture.md` – System architecture and module design.
* `Decisions.md` – Important design decisions and reasoning.

## Status

🚧 **Under Active Development**

This project is evolving incrementally, with a focus on building a clean architecture before implementing advanced AI capabilities.

## License

This project is currently intended for personal learning and development.
