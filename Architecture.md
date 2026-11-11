# Kayal Architecture

## Current Command Flow

```text
User Input
    |
Command Processor
    |
Intent Detection + Application Detection
    |
    +---- OPEN ----> Application Execution
    |
    +---- CLOSE ---> Confirmation Mechanism
                         |
                      YES / NO
                         |
                 +-------+-------+
                 |               |
              CONFIRMED        REJECTED
                 |               |
          Application Close   Cancel Action
```

## Modules

### 1. Wake Word Module
Detects the configured wake word (planned: "Hey Jarvis").

### 2. Speech-to-Text
Converts voice input into text. The current development interface uses terminal input.

### 3. Command Processor
Coordinates intent detection and application detection, then determines the requested action.

### 4. Intent Configuration
Defines hardcoded keyword groups:
- `open`: request to launch an application.
- `close`: request to close an application.
- `cancel`: reject or prevent an action before it is initiated.
- `yes`: affirmative confirmation response.
- `no`: negative confirmation response.

### 5. Confirmation Mechanism
A reusable component that receives a pending action description, asks the user to confirm, and returns a confirmation result. It does not execute the action itself. Unknown responses are not treated as consent and cause another prompt.

### 6. Application Configuration and Execution
Stores application keywords, open actions, and close actions. Opening executes directly; closing requires confirmation first.

### 7. Kayal Termination
The separate `termination.py` configuration contains commands that stop Kayal itself. These are distinct from commands that close external applications.

### 8. Voice Response
Provides spoken responses in a future voice-enabled phase. Current responses are printed in the terminal.

## Future Ideas
- Memory system
- LLM integration
- Code assistant
- Plugin system
