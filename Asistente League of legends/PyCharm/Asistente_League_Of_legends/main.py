import threading
import time
import webbrowser
import pyttsx3
import speech_recognition as sr

engine = pyttsx3.init()
engine_semaphore = threading.Semaphore()

def audio_to_text():
    r = sr.Recognizer()

    with sr.Microphone() as origen:
        # r.pause_threshold = 0.8
        r.energy_threshold = 4000

        print('Puedes comenzar a hablar')

        # Guardar audio
        try:
            audio = r.listen(origen, timeout=3, phrase_time_limit=3)

            # Buscar en google lo escuchado
            text = r.recognize_google(audio, language='es-es')  # Corregir aquí
            print(text)
            return text
        except sr.UnknownValueError:
            return 'Esperando'
        except sr.RequestError:
            print('Ups, sin servicio')
            return 'Esperando'
        except Exception as e:
            print(f'Ups, algo ha salido mal: {e}')
            return 'Esperando'


def saludo():
    talk('Comienza la partida')



def combinaciones_letras_palabras(jugadores, hechizos):
    for jugador in jugadores:
        for hechizo in hechizos:
            yield f'{jugador} {hechizo}'



def requests():
    saludo()
    iniciar_temporizador('criatura', 'dragonmuerto')
    iniciar_temporizador('criatrua', 'primerbaron')

    while True:
        try:
            request = audio_to_text()
            print(request)
            combinaciones = combinaciones_letras_palabras(
                ['top', 'jungla', 'mid', 'adece', 'support', 'criatura', 'buscar'],
                ['curar', 'fantasmal', 'barrera', 'extenuar', 'destello', 'dragonmuerto', 'baronmuerto', 'jugador']
            )
            for combinacion in combinaciones:
                if combinacion in request:
                    jugador, hechizo = combinacion.split()
                    iniciar_temporizador(jugador, hechizo)
                    break

            if 'buscar' in request:
                buscar_en_google()


        except Exception as e:
            print(f'Error en el bucle principal: {e}')



def temporizador(usuario, hechizo, segundos):
    print(f"Iniciando temporizador de {segundos} segundos para {usuario} - {hechizo}")
    time.sleep(segundos)
    mensaje = f'{usuario} ha finalizado {hechizo}'
    if hechizo == 'dragonmuerto':
        mensaje = '30 segundos para que aparezca el dragón'
    if hechizo == 'baronmuerto':
        mensaje = '30 segundos para que aparezca el barón'

    talk(mensaje)
    print(mensaje)



def iniciar_temporizador(jugador, hechizo):
    duracion_temporizador = {
        'curar': 240,
        'fantasmal': 210,
        'barrera': 180,
        'extenuar': 210,
        'destello': 300,
        'dragonmuerto': 270,
        'baronmuerto': 360,
        'primerbaron': 1170,
    }

    duracion = duracion_temporizador.get(hechizo, 0)
    if duracion > 0:
        nombre_temporizador = f"{jugador}_{hechizo}"
        nombre_hilo = threading.Thread(target=temporizador, args=(jugador, hechizo, duracion), name=nombre_temporizador)
        nombre_hilo.start()
        if hechizo == 'dragonmuerto':
            mensaje = "Dragón activado"
        elif hechizo == 'baronmuerto':
            mensaje = "Barón activado"
        else:
            mensaje = f'{hechizo.capitalize()} de {jugador} activada'
        talk(mensaje)


def talk(msg):
    with engine_semaphore:
        newVoiceRate = 200
        engine.setProperty('rate', newVoiceRate)
        engine.setProperty('voice', 'com.apple.eloquence.es-ES.Eddy')
        engine.say(msg)
        engine.runAndWait()


def buscar_en_google():
    talk('Di el nombre del usuario que deseas buscar')
    request = audio_to_text().lower()
    try:
        # Componer la URL de búsqueda en Google
        url = f"https://www.op.gg/summoners/euw/{request}"

        # Abrir el navegador predeterminado con la URL de búsqueda
        webbrowser.open(url)

        print(f"Búsqueda en Google para: {request}")

    except Exception as e:
        print(f"Error al realizar la búsqueda en Google: {e}")



if __name__ == '__main__':
    requests()

