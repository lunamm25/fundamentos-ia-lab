# Problema y prompt del Vibe Coding (C3)

Escogimos un problema pequeño y fácil de verificar: consumir una API pública, validar la respuesta, calcular estadísticas y graficar. Usamos la temperatura por hora de Manizales en Open-Meteo, porque no pide clave y el resultado se puede comprobar abriendo la URL en el navegador.

Pegamos el mismo prompt, sin cambios y en un chat nuevo, en los tres modelos: ChatGPT, llama3.2:3b y qwen2.5-coder:3b.

```text
Escribe un programa en Python llamado clima.py que haga lo siguiente:

1. Consuma esta API pública (no necesita clave):
   https://api.open-meteo.com/v1/forecast?latitude=5.07&longitude=-75.52&hourly=temperature_2m&timezone=America/Bogota&past_days=7
2. Valide la respuesta: que el código HTTP sea 200, que existan "hourly",
   "time" y "temperature_2m", que las dos listas tengan el mismo tamaño,
   y descarte los valores vacíos (None), informando cuántos descartó.
3. Pase los datos a un DataFrame de pandas con las columnas fecha y
   temperatura, con la fecha en formato de fecha y ordenado por fecha.
4. Calcule y muestre: cantidad de datos, temperatura mínima, máxima,
   promedio, mediana y desviación estándar, y la fecha y hora de la
   temperatura más alta.
5. Genere una gráfica de línea de la temperatura en el tiempo, con título
   y nombres en los ejes, y guárdela como temperatura.png.
6. Si no hay internet o la API falla, muestre un mensaje claro en vez de
   cerrarse con un error.
7. Use solo requests, pandas y matplotlib.
8. Comente el código en español y explique cómo instalar y ejecutar.
9. Al final, sugiere 3 pruebas para comprobar que el programa funciona bien.
```

Para saber si un programa funcionaba, revisamos que trajera 336 datos (7 días pasados más 7 de pronóstico, por 24 horas) y que la temperatura máxima coincidiera con la de la API.
