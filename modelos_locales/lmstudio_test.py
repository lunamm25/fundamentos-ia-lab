import time
import requests

URL = "http://localhost:1234/v1"

PREGUNTAS = [
    "Explica en 3 líneas qué es un modelo de lenguaje.",
    "Escribe una función en Python que calcule el promedio de una lista de números sin usar librerías.",
    "Explica qué hace este código de Python: [x**2 for x in range(5)]",
]


def modelo_disponible():
    # Pide la lista de modelos y toma el primero que no sea de embeddings
    r = requests.get(f"{URL}/models", timeout=10)
    r.raise_for_status()
    for m in r.json()["data"]:
        if "embed" not in m["id"]:
            return m["id"]
    raise RuntimeError("No hay ningún modelo de chat en LM Studio")


def preguntar(modelo, pregunta):
    datos = {
        "model": modelo,
        "messages": [{"role": "user", "content": pregunta}],
        "temperature": 0.2,
    }
    inicio = time.time()
    r = requests.post(f"{URL}/chat/completions", json=datos, timeout=300)
    r.raise_for_status()
    segundos = time.time() - inicio
    respuesta = r.json()
    texto = respuesta["choices"][0]["message"]["content"]
    tokens = respuesta.get("usage", {}).get("completion_tokens")
    return texto, segundos, tokens


if __name__ == "__main__":
    try:
        modelo = modelo_disponible()
        print(f"=========== {modelo} ===========")
        for i, pregunta in enumerate(PREGUNTAS, start=1):
            texto, segundos, tokens = preguntar(modelo, pregunta)
            print(f"\n--- Pregunta {i}: {pregunta}")
            print(texto.strip())
            print(f"[Tiempo: {segundos:.1f} s | Tokens generados: {tokens}]")
    except requests.exceptions.ConnectionError:
        print("No se pudo conectar con LM Studio. ¿Encendió el servidor (pestaña Developer)?")
    except (requests.exceptions.HTTPError, RuntimeError) as e:
        print(f"Error: {e}")