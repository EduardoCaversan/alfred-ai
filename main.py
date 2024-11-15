import os
import subprocess
import datetime
import random
import webbrowser
import platform
import pyttsx3
import speech_recognition as sr
from transformers import pipeline

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

recognizer = sr.Recognizer()

def listen():
    """
    Escuta o comando do usuário com timeout ajustado para evitar cortes prematuros.
    """
    with sr.Microphone() as source:
        print("Ouvindo...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
            command = recognizer.recognize_google(audio, language="pt-BR")
            print(f"Você disse: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Desculpe, não entendi. Pode repetir?")
            return ""
        except sr.WaitTimeoutError:
            speak("Você ficou em silêncio por muito tempo. Tente novamente.")
            return ""
        except sr.RequestError:
            speak("Serviço de reconhecimento de fala indisponível.")
            return ""

OS_TYPE = platform.system()

APP_CACHE = {}

def find_application(app_name):
    """
    Busca o caminho do aplicativo pelo nome. Funciona no Windows, macOS e Linux.
    """
    global APP_CACHE

    if app_name in APP_CACHE:
        return APP_CACHE[app_name]

    try:
        if OS_TYPE == "Windows":
            command = f'where {app_name}'
        elif OS_TYPE in ["Linux", "Darwin"]:
            command = f'which {app_name}'
        else:
            speak("Sistema operacional não suportado para busca automática de aplicativos.")
            return None

        path = subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL).decode("utf-8").strip()
        if path:
            APP_CACHE[app_name] = path
            return path
        else:
            speak(f"Não consegui encontrar o aplicativo {app_name}.")
            return None
    except subprocess.CalledProcessError:
        speak(f"Não encontrei {app_name}. Verifique se está instalado e tente novamente.")
        return None

def open_application(app_name):
    """
    Abre um aplicativo pelo nome, usando o caminho encontrado dinamicamente.
    """
    path = find_application(app_name)
    if path:
        try:
            subprocess.Popen([path])
            speak(f"Abrindo {app_name}.")
        except Exception as e:
            speak(f"Não consegui abrir o {app_name}. Erro: {str(e)}")
    else:
        speak(f"Não consegui localizar o aplicativo {app_name}.")

def search_google(query):
    if query == "":
        url = f"https://www.google.com"
        webbrowser.open(url)
        speak(f"Abrindo o Google.")
    else:
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        speak(f"Abrindo o Google para pesquisar {query}.")

def open_youtube(query):
    if query == "":
        url = f"https://www.youtube.com"
        webbrowser.open(url)
        speak(f"Abrindo o YouTube.")
    else:
        url = f"https://www.youtube.com/results?search_query={query}"
        webbrowser.open(url)
        speak(f"Abrindo o YouTube para pesquisar {query}.")

def tell_joke():
    jokes = [
        "Por que o livro de matemática se suicidou? Porque tinha muitos problemas.",
        "Por que o computador foi ao médico? Porque estava com um vírus.",
        "O que o pato disse para a pata? Vem Quá!"
    ]
    speak(random.choice(jokes))

def get_time():
    now = datetime.datetime.now()
    time_str = now.strftime("%H:%M")
    speak(f"A hora atual é {time_str}.")

def predict_intention(command):
    """
    Preve a intenção do comando usando um modelo de classificação de linguagem
    e fallback para verificações manuais.
    """
    nlp = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    possible_intentions = ["saudação", "abrir navegador", "hora", "piada", "abrir aplicativo"]
    result = nlp(command, candidate_labels=possible_intentions)

    if "google" in command or "youtube" in command:
        return "abrir navegador"
    elif "hora" in command:
        return "hora"
    elif "piada" in command:
        return "piada"
    elif "abrir" in command:
        return "abrir aplicativo"
    return result['labels'][0]

def process_command(command):
    if command:
        intention = predict_intention(command)

        if intention == "saudação":
            speak("Olá! Como posso ajudar?")
        elif intention == "abrir navegador":
            if "google" in command:
                query = command.replace("abrir google", "").strip()
                search_google(query)
            elif "youtube" in command:
                query = command.replace("abrir youtube", "").strip()
                open_youtube(query)
        elif intention == "hora":
            get_time()
        elif intention == "piada":
            tell_joke()
        elif intention == "abrir aplicativo":
            app_name = command.replace("abrir", "").strip()
            open_application(app_name)
        else:
            speak("Desculpe, não entendi o comando.")

def run_assistant():
    speak("Olá! Estou pronto para ajudar. Você pode falar agora.")
    while True:
        command = listen()
        if "sair" in command:
            speak("Até logo!")
            break
        elif command:
            process_command(command)

if __name__ == "__main__":
    run_assistant()