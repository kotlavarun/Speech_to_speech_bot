# Speech_to_speech_bot
This project enables real-time speech recognition and speech generation, allowing users to interact through voice. It uses Google Speech Recognition for speech-to-text conversion and Google Text-to-Speech (gTTS) for generating responses.

## Features
- **Real-time Speech Recognition**: Captures speech input from the microphone and converts it into text.
- **Text-to-Speech Generation**: Converts text to audio using Google TTS, with playback via `pygame`.
- **GUI Interface**: A simple `tkinter` interface for displaying speech recognition results and statuses.
- **Error Handling**: Displays errors and updates in the interface to guide users.

## Requirements
To run this project, you'll need the following libraries installed:

```bash
pip install opencv-python
pip install gtts
pip install pygame
pip install google-generativeai
pip install SpeechRecognition
pip install pillow
