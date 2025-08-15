import speech_recognition as sr
import tkinter as tk
from tkinter import messagebox, ttk
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
import threading

# Available language options
LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese": "zh-CN",
    "Telugu": "te",
    "Tamil": "ta",
    "Kannada": "kn",
    "Malayalam": "ml"
}

def recognize_speech(source_lang):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print(f"Listening ({source_lang})...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            text = recognizer.recognize_google(audio, language=source_lang)
            print(f"You said ({source_lang}): {text}")
            return text
        except sr.UnknownValueError:
            messagebox.showerror("Error", "Sorry, I couldn't understand what you said.")
        except sr.RequestError:
            messagebox.showerror("Error", "Speech Recognition service is unavailable.")
    return ""

def translate_text(text, target_language):
    translator = GoogleTranslator(source="auto", target=target_language)
    translation = translator.translate(text)
    print(f"Translated Text ({target_language}): {translation}")
    return translation

def speak_text(text, language_code):
    tts = gTTS(text=text, lang=language_code, slow=False)
    tts.save("output.mp3")
    os.system("start output.mp3")  # Windows-specific

def process_speech_translation():
    source_lang_code = LANGUAGES[input_lang.get()]
    target_lang_code = LANGUAGES[output_lang.get()]

    spoken_text = recognize_speech(source_lang_code)
    if spoken_text:
        translated_text = translate_text(spoken_text, target_lang_code)
        speak_text(translated_text, target_lang_code)
        translated_text_box.delete(0, tk.END)
        translated_text_box.insert(0, translated_text)

def process_text_translation():
    input_text = manual_input.get()
    if not input_text.strip():
        messagebox.showwarning("Input Required", "Please enter text to translate.")
        return

    target_lang_code = LANGUAGES[output_lang.get()]
    translated_text = translate_text(input_text, target_lang_code)
    speak_text(translated_text, target_lang_code)
    translated_text_box.delete(0, tk.END)
    translated_text_box.insert(0, translated_text)

def on_speech_translate_click():
    threading.Thread(target=process_speech_translation, daemon=True).start()

def on_text_translate_click():
    threading.Thread(target=process_text_translation, daemon=True).start()

# GUI
def create_gui():
    global input_lang, output_lang, manual_input, translated_text_box

    root = tk.Tk()
    root.title("Multilingual Voice/Text Translator")

    tk.Label(root, text="Select Input Language:").pack()
    input_lang = ttk.Combobox(root, values=list(LANGUAGES.keys()))
    input_lang.set("English")
    input_lang.pack()

    tk.Label(root, text="Select Output Language:").pack()
    output_lang = ttk.Combobox(root, values=list(LANGUAGES.keys()))
    output_lang.set("Hindi")
    output_lang.pack()

    tk.Label(root, text="Type Text (Optional):").pack()
    manual_input = tk.Entry(root, width=50)
    manual_input.pack(pady=5)

    translate_text_button = tk.Button(root, text="Translate Typed Text", command=on_text_translate_click, padx=20, pady=10)
    translate_text_button.pack(pady=5)

    translate_speech_button = tk.Button(root, text="Translate Speech", command=on_speech_translate_click, padx=20, pady=10)
    translate_speech_button.pack(pady=5)

    tk.Label(root, text="Translated Output:").pack()
    translated_text_box = tk.Entry(root, width=50)
    translated_text_box.pack(pady=5)

    quit_button = tk.Button(root, text="Quit", command=root.quit, padx=20, pady=10)
    quit_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()