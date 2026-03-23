# Project_JARVIS

# JARVIC - AI Assistant

JARVIC is a modular, voice-activated AI assistant designed with a futuristic HUD interface. It leverages the Groq API for advanced natural language processing and features a plugin-style skill system for handling various tasks ranging from system operations to weather checking.

## Features

- **Futuristic HUD Interface**: A Sci-Fi inspired Graphical User Interface built with PyQt6.
- **Dual Interaction Modes**:
  - **Voice Mode**: Hands-free interaction using speech recognition and text-to-speech.
  - **Text Mode**: Command-line interface for silent operation.
- **Modular Skill System**: Easily extensible architecture where capabilities are separated into distinct modules:
  - **Weather**: Check current weather conditions (requires API setup).
  - **System Ops**: Control system functions.
  - **Email**: Manage emails.
  - **Web Ops**: Perform web searches and interactions.
  - **File & Text Ops**: file manipulation and text processing.
  - **Memory**: Persistent memory capabilities.
  - And more...
- **Wake Word Detection**: Responds to "Jarvis" (and other direct commands).

## detailed Tech Stack

- **Language**: Python 3
- **GUI**: PyQt6
- **LLM Engine**: Groq API
- **Voice**: `SpeechRecognition` (Input) & `pyttsx3` (Output)
- **Audio**: PyAudio

## Installation

1.  **Clone the Repository** (if applicable) or download the source code.

2.  **Set up a Virtual Environment** (Recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Environment Configuration**:
    - Project requires a `.env` file for API keys.
    - Copy the template:
      ```bash
      cp .env.template .env
      ```
    - Open `.env` and add your **Groq API Key**:
      ```env
      GROQ_API_KEY=your_groq_api_key_here
      ```
    - *(Optional)* Add other keys as required by specific skills (e.g., Weather API, Email creds).

## Usage

### Running the Assistant
To start the standard voice-activated GUI interface:
```bash
python main.py
```

### Text Mode
To run in text-only mode (useful for debugging or silent environments):
```bash
python main.py --text
```

### Controls
- **Voice Commands**: Just say "Jarvis" followed by your command (e.g., "Jarvis, what's the weather?").
- **GUI Controls**: 
  - Click on the central HUD element to **Pause/Resume** listening.
  - Close the window to shut down the application.
- **Direct Commands**: You can also use direct command verbs like "Open", "Search", "Create", etc.

## Project Structure

- `main.py`: Entry point of the application. Handles the main loop and thread management.
- `core/`: Contains core logic for the engine, voice processing, and skill registry.
- `gui/`: Contains the PyQt6 application and UI logic.
- `skills/`: Directory containing all modular skills (plugins).
- `assets/`: Images and resources for the GUI.

##BIG UPDATE:
- Currently this only works on Mac. If you subscribe to my yt channel and did 100 subscribers. I will uplode a JARVIS for windoes.

## License

[MIT License](LICENSE) (or appropriate license)
