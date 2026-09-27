# Vibe Coding: modelo cloud

| Dato | Valor |
|---|---|
| Modelo | ChatGPT (modelo que mostraba la app: 5.6 luna) |
| Herramienta | chatgpt.com |
| Fecha | 22/09/2026 |
| Prompt | El de `../problema_y_prompt.md`, sin cambios |

## Iteraciones

| # | Qué pasó | Resultado |
|---|---|---|
| 1 | Se pegó el prompt y el modelo entregó `clima.py`. | Al ejecutarlo salió `SyntaxError: invalid syntax` en la línea 213: al copiar la respuesta quedaron en el archivo las marcas ``` del bloque de código. |
| 2 | Se verifico la linea 213. La causa  eran unas líneas que no cerraban y procedimos a borrar las líneas que solo tenían ```. Se borraron a mano. | Funcionó: 336 datos, 0 vacíos, estadísticas y `temperatura.png`. |

**Tiempo total:** menos de 5 minutos.

## Verificación humana

- 336 datos: coincide con 14 días × 24 horas.
- Máxima de 24,00 °C el 17/09/2026 a las 13:00, dentro de los 7 días medidos.
- La gráfica no separa los datos medidos del pronóstico. Desde el 22/09 los valores son predicción.

Evidencias: `evidence/c3_cloud_01_prompt.png`, `c3_cloud_02_resultado.png`, `c3_cloud_03_grafica.png`, `c3_cloud_04_error_y_correccion.png`.

Código final: `clima.py`.
