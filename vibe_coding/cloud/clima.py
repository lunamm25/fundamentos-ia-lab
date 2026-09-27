# clima.py
# Programa para consultar datos de temperatura mediante la API de Open-Meteo,
# procesarlos con pandas y generar una gráfica con matplotlib.

import requests
import pandas as pd
import matplotlib.pyplot as plt


# URL de la API de Open-Meteo
URL_API = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=5.07"
    "&longitude=-75.52"
    "&hourly=temperature_2m"
    "&timezone=America/Bogota"
    "&past_days=7"
)


def obtener_datos():
    """Consulta la API y valida la respuesta."""

    try:
        # Realizar la solicitud con un tiempo máximo de espera
        respuesta = requests.get(URL_API, timeout=10)

    except requests.exceptions.RequestException as error:
        print("No fue posible conectarse a Internet o a la API.")
        print(f"Detalle: {error}")
        return None

    # Validar código HTTP
    if respuesta.status_code != 200:
        print(
            f"La API respondió con un código HTTP inesperado: "
            f"{respuesta.status_code}"
        )
        return None

    # Intentar convertir la respuesta a JSON
    try:
        datos = respuesta.json()
    except ValueError:
        print("La respuesta de la API no contiene un JSON válido.")
        return None

    # Validar que exista la sección "hourly"
    if "hourly" not in datos:
        print("La respuesta no contiene la sección 'hourly'.")
        return None

    hourly = datos["hourly"]

    # Validar que existan las listas requeridas
    if "time" not in hourly:
        print("La respuesta no contiene la lista 'time'.")
        return None

    if "temperature_2m" not in hourly:
        print("La respuesta no contiene la lista 'temperature_2m'.")
        return None

    fechas = hourly["time"]
    temperaturas = hourly["temperature_2m"]

    # Validar que ambas listas tengan el mismo tamaño
    if len(fechas) != len(temperaturas):
        print(
            "Error de validación: las listas 'time' y "
            "'temperature_2m' tienen tamaños diferentes."
        )
        return None

    # Eliminar registros cuya temperatura sea None
    datos_validos = [
        (fecha, temperatura)
        for fecha, temperatura in zip(fechas, temperaturas)
        if temperatura is not None
    ]

    descartados = len(temperaturas) - len(datos_validos)

    print(f"Valores vacíos (None) descartados: {descartados}")

    # Verificar que todavía existan datos después de la limpieza
    if not datos_validos:
        print("No existen datos válidos para procesar.")
        return None

    return datos_validos


def procesar_datos(datos):
    """Convierte los datos en un DataFrame y los ordena por fecha."""

    # Crear DataFrame con las columnas solicitadas
    df = pd.DataFrame(datos, columns=["fecha", "temperatura"])

    # Convertir la columna fecha a formato de fecha/hora
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")

    # Convertir la temperatura a valores numéricos
    df["temperatura"] = pd.to_numeric(
        df["temperatura"], errors="coerce"
    )

    # Eliminar registros que no pudieron convertirse correctamente
    df = df.dropna(subset=["fecha", "temperatura"])

    # Ordenar cronológicamente
    df = df.sort_values("fecha").reset_index(drop=True)

    return df


def mostrar_estadisticas(df):
    """Calcula y muestra las estadísticas solicitadas."""

    if df.empty:
        print("No hay datos disponibles para calcular estadísticas.")
        return

    cantidad = len(df)
    minima = df["temperatura"].min()
    maxima = df["temperatura"].max()
    promedio = df["temperatura"].mean()
    mediana = df["temperatura"].median()

    # Desviación estándar muestral
    desviacion = df["temperatura"].std()

    # Obtener el registro correspondiente a la temperatura máxima
    indice_maximo = df["temperatura"].idxmax()
    registro_maximo = df.loc[indice_maximo]

    print("\n" + "=" * 45)
    print("ESTADÍSTICAS DE TEMPERATURA")
    print("=" * 45)

    print(f"Cantidad de datos:              {cantidad}")
    print(f"Temperatura mínima:             {minima:.2f} °C")
    print(f"Temperatura máxima:             {maxima:.2f} °C")
    print(f"Temperatura promedio:            {promedio:.2f} °C")
    print(f"Temperatura mediana:             {mediana:.2f} °C")
    print(f"Desviación estándar:             {desviacion:.2f} °C")
    print(
        f"Temperatura más alta registrada: "
        f"{registro_maximo['fecha'].strftime('%Y-%m-%d %H:%M')} "
        f"({registro_maximo['temperatura']:.2f} °C)"
    )

    print("=" * 45)


def generar_grafica(df):
    """Genera y guarda la gráfica de temperatura."""

    plt.figure(figsize=(12, 6))

    plt.plot(
        df["fecha"],
        df["temperatura"],
        linewidth=1.5
    )

    plt.title("Temperatura en el tiempo")
    plt.xlabel("Fecha y hora")
    plt.ylabel("Temperatura (°C)")

    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    # Guardar la gráfica como archivo PNG
    plt.savefig("temperatura.png", dpi=150)

    # Mostrar la gráfica
    plt.show()

    print("\nGráfica guardada correctamente como: temperatura.png")


def main():
    """Función principal del programa."""

    print("Consultando datos meteorológicos...")
    
    datos = obtener_datos()

    # Si la API falló, terminar de forma controlada
    if datos is None:
        return

    # Procesar los datos
    df = procesar_datos(datos)

    # Verificar que haya datos después del procesamiento
    if df.empty:
        print("No quedaron datos válidos después del procesamiento.")
        return

    # Mostrar estadísticas
    mostrar_estadisticas(df)

    # Generar gráfica
    generar_grafica(df)


# Punto de entrada del programa
if __name__ == "__main__":
    main()
