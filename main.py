import os
import subprocess
import datetime
import random
import webbrowser
import platform
import pyttsx3
import speech_recognition as sr
from transformers import pipeline
import requests
from bs4 import BeautifulSoup

engine = pyttsx3.init()

def speak(text):
    engine.say(f"{text}")
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
            audio = recognizer.listen(source, timeout=30, phrase_time_limit=30)
            command = recognizer.recognize_google(audio, language="pt-BR")
            print(f"Você disse: {command}")
            return command.lower()
        except sr.UnknownValueError:
            return ""
        except sr.WaitTimeoutError:
            return ""
        except sr.RequestError:
            speak("Desculpe patrão, o serviço de reconhecimento de fala está indisponível.")
            return ""

OS_TYPE = platform.system()

APP_CACHE = {}

def find_application(app_name):
    """
    Busca o caminho do aplicativo pelo nome.
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
    Abre um aplicativo pelo nome.
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
    
def open_azure(area):
    if area == "portal":
        url = f"https://portal.azure.com/#home"
        webbrowser.open(url)
        speak(f"Abrindo o portal azure!")
    elif area == "demandas" or area == "demanda" or area == "cards" or area == "boards" or area == "devops":
        url = f"https://dev.azure.com/forlogic/Adven.tech/_boards/board/t/Dev/Backlog%20items"
        webbrowser.open(url)
        speak(f"Abrindo os boards azure!")
    else:
        speak(f"Desculpe patrão, mas ainda não conheço essa área!")

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

def alfred_quotes():
    quotes = [
        "Por que caímos, patrão? Para aprendermos a nos levantar.",
        "Alguns homens só querem ver o mundo pegar fogo.",
        "Até mesmo o Batman precisa de ajuda, patrão. Estou aqui para isso."
    ]
    speak(random.choice(quotes))

def search_web(query):
    """
    Realiza uma busca no Google e retorna títulos, URLs e snippets dos resultados.
    """
    try:
        url = f"https://www.google.com/search?q={query}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            speak("Desculpe patrão, não consegui acessar o Google no momento.")
            return

        soup = BeautifulSoup(response.text, "html.parser")
        
        results = []
        for g in soup.select(".tF2Cxc"):
            title = g.select_one("h3").text if g.select_one("h3") else "Sem título"
            link = g.select_one(".yuRUbf a")["href"] if g.select_one(".yuRUbf a") else "Sem link"
            snippet = g.select_one(".IsZvec").text if g.select_one(".IsZvec") else "Sem descrição"
            results.append({"title": title, "link": link, "snippet": snippet})
        
        if not results:
            speak("Não encontrei nada relevante para sua pesquisa.")
        else:
            speak("Aqui estão os resultados:")
            for i, result in enumerate(results[:5], 1):
                print(f"{i}. {result['title']}\n   Link: {result['link']}\n   Descrição: {result['snippet']}\n")
                speak(f"Resultado {i}: {result['title']}")
        
    except Exception as e:
        speak(f"Desculpe patrão, ocorreu um erro: {str(e)}")
                
def process_command(command):
    if "sair" in command:
        speak("Tudo bem, se precisar é só chamar patrão!")
        return "exit"
    elif "google" in command:
        query = command.replace("abrir google", "").strip()
        search_google(query)
    elif "youtube" in command:
        query = command.replace("abrir youtube", "").strip()
        open_youtube(query)
    elif "piada" in command:
        tell_joke()
    elif "hora" in command:
        get_time()
    elif "abrir" in command:
        app_name = command.replace("abrir", "").strip()
        open_application(app_name)
    elif "desenvolvimento" in command:
        area = command.replace("do desenvolvimento", "").strip()
        open_azure(area)
    elif "frase" in command or "motivação" in command:
        alfred_quotes()
    elif "pesquisar" in command or "procurar" in command:
        query = command.replace("pesquisar", "").replace("procurar", "").strip()
        search_web(query)
    else:
        speak("Desculpe, não entendi o comando patrão.")

def run_assistant():
    activated = False
    speak("Olá patrão! Estou pronto para ajudar. Basta me chamar dizendo Alfred.")
    while True:
        command = listen()
        if not activated:
            if "alfred" in command:
                speak("Estou ouvindo patrão!")
                activated = True
        else:
            if process_command(command) == "exit":
                activated = False

if __name__ == "__main__":
    run_assistant()
