# Qué decir en la exposición

La app baja la temperatura diaria de Manizales (2024 y 2025) desde Open-Meteo. No usa API key. Son 731 días, sin vacíos.

El primer 80 % entrena: 584 días, hasta el 6 de agosto de 2025. El último 20 % se prueba: 147 días, desde el 7 de agosto de 2025. No se mezclan.

Hay dos predicciones, y las dos miran solo días que ya pasaron:

- **Persistencia:** hoy se predice con la temperatura de ayer. Es una sola línea: `shift(1)`.
- **Regresión lineal:** hoy se predice con los 7 días anteriores. Se entrena con `modelo.fit` solo en el primer 80 %. El peso más grande es el de ayer: 0.53.

| Método | MAE (°C) | RMSE (°C) |
|---|---:|---:|
| Persistencia | 0.4769 | 0.6114 |
| Regresión lineal | 0.4083 | 0.5168 |

MAE es el promedio del error, en grados. RMSE hace lo mismo, pero castiga más los días en que el error fue grande. La regresión gana por poco, porque el clima de un día se parece mucho al del anterior.

## Archivos, en orden

1. `api_client.py` pide el JSON.
2. `preprocessing.py` ordena las fechas, revisa que no haya vacíos y corta 80/20.
3. `model.py` arma la persistencia y entrena la regresión.
4. `evaluation.py` calcula MAE y RMSE.
5. `app.py` llama a todo y guarda las gráficas.

La IA ayudó a escribir el código. Las decisiones (API, ciudad, corte 80/20, persistencia y regresión) salen del reparto del grupo. El programa se ejecutó con datos reales.

Para correrlo: `.\.venv\Scripts\python -m serie_temporal.app`
