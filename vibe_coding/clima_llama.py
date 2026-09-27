import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

def obtener_forecast(api_url, latitude, longitude, timezone, horas):
    try:
        respuesta = requests.get(api_url, params={
            'latitude': latitude,
            'longitude': longitude,
            'timezone': timezone,
            'hourly': horas
        })
        respuesta.raise_for_status()
        return respuesta.json()
    except requests.RequestException as e:
        print(f"Error: {e}")
        return None

def procesar_forecast(forecast):
    if forecast is None:
        print("No se pudo obtener la información de la API.")
        return None
    if 'hourly' not in forecast:
        print("La API no devuelve los datos solicitados.")
        return None
    if 'time' not in forecast['hourly'] or 'temperature_2m' not in forecast['hourly']:
        print("La API no devuelve los datos solicitados.")
        return None
    if len(forecast['hourly']['time']) != len(forecast['hourly']['temperature_2m']):
        print("Los datos no tienen el mismo tamaño.")
        return None
    if np.any(forecast['hourly']['temperature_2m'] == None):
        print("Descartado", np.sum(forecast['hourly']['temperature_2m'] == None))
    else:
        return forecast['hourly']['temperature_2m']
    return None

def crear_dataframe(forecast):
    if forecast is None:
        print("No se pudo obtener la información de la API.")
        return None
    fecha = [datetime.fromtimestamp(forecast[i]['time']) for i in range(len(forecast['hourly']['time']))]
    temperatura = forecast['hourly']['temperature_2m']
    df = pd.DataFrame({
        'fecha': fecha,
        'temperatura': temperatura
    })
    df.sort_values('fecha', inplace=True)
    return df

def calcular_medidas(df):
    if df is None:
        print("No se pudo obtener la información de la API.")
        return None
    min_temp = df['temperatura'].min()
    max_temp = df['temperatura'].max()
    promedio = df['temperatura'].mean()
    mediana = df['temperatura'].median()
    desviacion = df['temperatura'].std()
    return min_temp, max_temp, promedio, mediana, desviacion

def encontrar_max(df):
    if df is None:
        print("No se pudo obtener la información de la API.")
        return None
    max_temp = df['temperatura'].idxmax()
    return df.loc[max_temp, 'fecha'], df.loc[max_temp, 'temperatura']

def graficar_temperature(df):
    if df is None:
        print("No se pudo obtener la información de la API.")
        return None
    plt.plot(df['fecha'], df['temperatura'])
    plt.title('Temperatura en el tiempo')
    plt.xlabel('Fecha')
    plt.ylabel('Temperatura')
    plt.savefig('temperature.png')
    plt.close()

def main():
    api_url = 'https://api.open-meteo.com/v1/forecast'
    latitude = 5.07
    longitude = -75.52
    timezone = 'America/Bogota'
    horas = 'hourly'
    df = None
    forecast = obtener_forecast(api_url, latitude, longitude, timezone, horas)
    if forecast is not None:
        forecast = procesar_forecast(forecast)
        if forecast is not None:
            df = crear_dataframe(forecast)
            if df is not None:
                min_temp, max_temp, promedio, mediana, desviacion = calcular_medidas(df)
                fecha_max, temperatura_max = encontrar_max(df)
                print(f'Cantidad de datos: {len(df)}')
                print(f'Temperatura mínima: {min_temp}')
                print(f'Temperatura máxima: {max_temp}')
                print(f'Promedio de temperatura: {promedio}')
                print(f'Mediana de temperatura: {mediana}')
                print(f'Desviación estándar de temperatura: {desviacion}')
                print(f'Date y hora de la temperatura más alta: {fecha_max} a las {temperatura_max}')
                graficar_temperature(df)
                print('Gráfica de temperatura guardada en temperatura.png')
        else:
            print('No se pudo obtener la información de la API.')
    else:
        print('No se pudo obtener la información de la API.')

if __name__ == "__main__":
    main()
