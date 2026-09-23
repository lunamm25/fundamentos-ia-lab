import time
import requests

URL = "http://localhost:11434/api/generate"

MODELOS = ["llama3.2:3b", "qwen2.5-coder:3b"]

PREGUNTAS = [
    "Explica en 3 líneas qué es un modelo de lenguaje.",
    "Escribe una función en Python que calcule el promedio de una lista de números sin usar librerías.",
    "Explica qué hace este código de Python: [x**2 for x in range(5)]",
]


def preguntar(modelo, pregunta):
    datos = {"model": modelo, "prompt": pregunta, "stream": False}
    inicio = time.time()
    r = requests.post(URL, json=datos, timeout=300)
    r.raise_for_status()
    segundos = time.time() - inicio
    respuesta = r.json()
    tokens_s = respuesta["eval_count"] / (respuesta["eval_duration"] / 1e9)
    return respuesta["response"], segundos, tokens_s


if __name__ == "__main__":
    try:
        for modelo in MODELOS:
            print(f"\n=========== {modelo} ===========")
            for i, pregunta in enumerate(PREGUNTAS, start=1):
                texto, segundos, tokens_s = preguntar(modelo, pregunta)
                print(f"\n--- Pregunta {i}: {pregunta}")
                print(texto.strip())
                print(f"[Tiempo: {segundos:.1f} s | Velocidad: {tokens_s:.1f} tokens/s]")
    except requests.exceptions.ConnectionError:
        print("No se pudo conectar con Ollama. ¿Está abierto? Revise http://localhost:11434")
    except requests.exceptions.HTTPError as e:
        print(f"Ollama respondió con error: {e}. ¿Ya descargó el modelo con 'ollama pull'?")