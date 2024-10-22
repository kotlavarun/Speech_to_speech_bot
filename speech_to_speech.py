import os
import cv2
import threading
from gtts import gTTS
import pygame
import time
import google.generativeai as genai
import speech_recognition as sr
from tkinter import *
from PIL import Image, ImageTk
import traceback

# Initialize pygame for audio playback
pygame.mixer.init()


GOOGLE_API_KEY = 'YOUR API KEY'
model = genai.GenerativeModel('gemini-pro')
if GOOGLE_API_KEY is None:
    raise ValueError("GOOGLE_API_KEY not found. Please ensure the API key is set properly.")

genai.configure(api_key=GOOGLE_API_KEY)


recognizer = sr.Recognizer()


keep_conversation_running = True
mic_active = True 


def speech_to_text():
    global mic_active
    if not mic_active:
        return None  

    try:
        with sr.Microphone() as source:
            status_label.config(text="Listening...")
            audio = recognizer.listen(source)
            try:
                
                text = recognizer.recognize_google(audio)
                status_label.config(text="You said: " + text)
                return text
            except sr.UnknownValueError:
                status_label.config(text="Google Speech Recognition could not understand the audio.")
            except sr.RequestError as e:
                status_label.config(text=f"Could not request results from Google Speech Recognition service; {e}")
    except Exception as e:
        status_label.config(text=f"Speech recognition error: {str(e)}")
        print("Error in speech_to_text():", traceback.format_exc())
    return None


def text_to_speech_offline(text):
    global mic_active

    def run_tts():
        try:
            mic_active = False  
            
            tts = gTTS(text=text, lang='en')
            tts.save("output.mp3") 
            
            
            pygame.mixer.music.load("output.mp3")
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                continue  

            
            os.remove("output.mp3")
        except Exception as e:
            status_label.config(text=f"Error in text_to_speech_offline: {str(e)}")
            print("Error in text_to_speech_offline():", traceback.format_exc())
        finally:
            
            time.sleep(2)  
            mic_active = True

    tts_thread = threading.Thread(target=run_tts)
    tts_thread.start()  


def start_conversation():
    global keep_conversation_running
    input_text = speech_to_text()

    if input_text:
        if input_text.lower() == "exit":
            status_label.config(text="You said: 'exit'. Ending conversation.")
            keep_conversation_running = False 
            close_application() 
            return

        # Generate content using AI model
        response = model.generate_content(input_text)
        generated_text = response.text

        
        result_text.delete("1.0", END)
        result_text.insert(END, generated_text)
        text_to_speech_offline(generated_text)  
    else:
        status_label.config(text="No speech input detected. Try again.")

# Function to show video feed from the webcam in a small window
def update_video_feed():
    try:
        ret, frame = video_capture.read()  
        if ret:
           
            frame_resized = cv2.resize(frame, (1000,700))

            
            cv2image = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)  
            imgtk = ImageTk.PhotoImage(image=img)  
            video_label.imgtk = imgtk
            video_label.configure(image=imgtk)
        
       
        video_label.after(10, update_video_feed)
    except Exception as e:
        status_label.config(text=f"Error in update_video_feed: {str(e)}")
        print("Error in update_video_feed():", traceback.format_exc())

def start_conversation_thread():
    global keep_conversation_running
    keep_conversation_running = True
    conversation_thread = threading.Thread(target=start_conversation)
    conversation_thread.daemon = True  
    conversation_thread.start()

def close_application():
    root.quit()  
    video_capture.release()  
    cv2.destroyAllWindows()  

# Create a GUI using Tkinter
root = Tk()
root.title("Speech Bot")
root.geometry("700x500")

# Add a button to start the speech-to-text process
start_button = Button(root, text="Click to speak", command=start_conversation_thread, font=("Arial", 14))
start_button.pack(pady=20)


# Label to display status or spoken text
status_label = Label(root, text="Press the button and start speaking.", font=("Arial", 12))
status_label.pack(pady=10)

# Textbox to display AI-generated response
result_label = Label(root, text="AI Response:", font=("Arial", 12))
result_label.pack(pady=5)

result_text = Text(root, height=5, width=50, wrap=WORD, font=("Arial", 12))
result_text.pack(pady=10)

# Create a label to display the webcam feed (small window)
video_label = Label(root)
video_label.pack(pady=20)

# Initialize the webcam video capture
video_capture = cv2.VideoCapture(0)

# Start updating the video feed
update_video_feed()

# Main loop to run the Tkinter app
root.mainloop()


video_capture.release()
cv2.destroyAllWindows()
