import json #распознавание речи
import requests #для запроса к словарю
import pyttsx3 #озвучка
import pyaudio #микрофон
import vosk #офлайн распозн речи
import webbrowser #открытие через браузер

# функция озвучки
engine = pyttsx3.init()

def speak(text):
    #Озвучивает текст и выводит в консоль
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

class Assistant:
    def __init__(self):
        self.data = None #хранение результатов поиска через API
        self.word = None #текущее слово

    def find(self, word):
        #команда поиска слова
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        try:
            res = requests.get(url).json()
            self.data = res
            self.word = word
            speak(f"Found {word}")
        except:
            speak("Error finding word")

    def meaning(self):
        #выводит значение слова
        try:
            meaning = self.data[0]["meanings"][0]["definitions"][0]["definition"]
            speak(meaning)
        except:
            speak("No meaning found")

    def example(self):
        #Команда вывода примера
        try:
            example = self.data[0]["meanings"][0]["definitions"][0]["example"]
            speak(example)
        except:
            speak("No example")

    def save(self):
        #команда сохранения слова и знач
        try:
            meaning = self.data[0]["meanings"][0]["definitions"][0]["definition"]
            with open("words.txt", "a") as f:
                f.write(f"{self.word}: {meaning}\n")
            speak("Saved")
        except:
            speak("Error saving")

    def link(self):
        #Команда открытия сайта
        webbrowser.open("https://dictionaryapi.dev/")
        speak("Opening site")


model = vosk.Model("model_small") #загрузка модели
rec = vosk.KaldiRecognizer(model, 16000) #микр на 16 кГц настройка

pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16,
                 channels=1,
                 rate=16000,
                 input=True,
                 frames_per_buffer=8000)

stream.start_stream() #создается поток данных для прослушивания
#запуск ассистента
assistant = Assistant()
speak("Assistant started. Say a command like find apple, meaning, example, save, link or exit.")

#чтение микрофона
while True:
    data = stream.read(4000, exception_on_overflow=False)

    if rec.AcceptWaveform(data):
        result = json.loads(rec.Result())
        text = result["text"]
        if text:
            print("You:", text)

            # Ключевые команды
            if "find" in text:
                # ищем слово после find
                words = text.split()
                try:
                    index = words.index("find")
                    word = words[index + 1]  # следующее слово после find
                    assistant.find(word)
                except IndexError:
                    speak("No word provided for find")

            elif "meaning" in text:
                assistant.meaning()

            elif "example" in text:
                assistant.example()

            elif "save" in text:
                assistant.save()

            elif "link" in text:
                assistant.link()

            elif "exit" in text:
                speak("Goodbye")
                break
            else:
                speak("Command not recognized")
