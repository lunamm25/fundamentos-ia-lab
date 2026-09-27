import requests
import pandas as pd
import matplotlib.pyplot as plt

def fetch_and_process_weather_data():
    try:
        # URL de la API
        api_url =
"https://api.open-meteo.com/v1/forecast?latitude=5.07&longitude=-75.52&hourly=temperature_2m&timezone=America/Bogot"https://api.open-meteo.com/v1/forecast?latitude=5.07&longitude=-75.52&hourly=temperature_2m&timeone=America/Bogota&past_days=7"

        # Realizamos la solicitud a la API
        response = requests.get(api_url)

        # Comprobamos si la respuesta es válida (código HTTP 200)
        if response.status_code != 200:
            print("Error: La solicitud a la API falló.")
            return

        # Convertimos la respuesta JSON a un diccionario
        data = response.json()

        # Validamos que el contenido es el esperado
        if "hourly" not in data or "time" not in data or "temperature_2m" not in data:
            print("Error: Los datos esperados no se encontraron.")
            return

        hourly_data = data["hourly"]
        time_data = data["time"]
        temperature_data = hourly_data["temperature_2m"]

        # Descartamos los valores vacíos (None)
        hourly_data = [temp for temp in hourly_data if temp is not None]
        time_data = [time for time in time_data if time is not None]
        temperature_data = [temp for temp in temperature_data if temp is not None]

        # Cálculo de los datos relevantes
        cantidad_datos = len(temperature_data)
        temperatura_minima = min(temperature_data)
        temperatura_maxima = max(temperature_data)
        temperatura_promedio = sum(temperature_data) / cantidad_datos
        temperatura_mediana = sorted(temperature_data)[cantidad_datos // 2]
        desviacion_estandar = (sum((x - temperatura_promedio) ** 2 for x in temperature_data) / cantidad_datos) **
0.5
        fecha_maxima = time_data[temperature_data.index(temperatura_maxima)]

        # Mostramos los resultados
        print(f"Cantidad de datos: {cantidad_datos}")
        print(f"Temperatura mínima: {temperatura_minima}")
        print(f"Temperatura máxima: {temperatura_maxima}")
        print(f"Temperatura promedio: {temperatura_promedio}")
        print(f"Temperatura mediana: {temperatura_mediana}")
        print(f"Desviación estándar: {desviacion_estandar}")
        print(f"Fecha y hora de la temperatura más alta: {fecha_maxima}")

        # Creamos un DataFrame de pandas
        df = pd.DataFrame({
            'fecha': pd.to_datetime(time_data),
            'temperatura': temperature_data
        })

        # Graficamos la temperatura en el tiempo
        plt.figure(figsize=(10, 5))
        plt.plot(df['fecha'], df['temperatura'], marker='o')
        plt.title('Temperatura en Bogotá, Colombia')
        plt.xlabel('Fecha')
        plt.ylabel('Temperatura (°C)')
        plt.grid(True)
        plt.savefig('temperatura.png')

        plt.show()

    except requests.exceptions.RequestException as e:
        print(f"Error: No se pudo realizar la solicitud a la API ({e})")