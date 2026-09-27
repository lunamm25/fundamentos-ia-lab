# Registro técnico: modelos locales (Componente 2)

**Fecha de prueba:** 22/09/2026 · **Evidencias:** carpeta `evidence/`, archivos `c2_*`

## 1. Equipo usado

| Procesador | RAM | Tarjeta de video | Sistema |
|---|---|---|---|
| AMD Ryzen 5 4600H (6 núcleos / 12 hilos, 3,0 GHz base) | 16 GB (15,4 GB utilizables) | AMD Radeon Graphics integrada: no tiene VRAM propia, usa la RAM | Windows 11 |

## 2. Modelos

| Entorno | Modelo | Tipo | Parámetros | Cuantización | Tamaño en disco | Evidencia |
|---|---|---|---|---|---|---|
| Ollama | `llama3.2:3b` | Generalista | 3B | Pendiente de confirmar con `ollama show` | 2,0 GB | `c2_ollama_01` |
| Ollama | `qwen2.5-coder:3b` | Código | 3B | Pendiente de confirmar con `ollama show` | 1,9 GB | `c2_ollama_01` |
| LM Studio | Llama 3.2 3B Instruct (GGUF) | Generalista | 3B | Q4_K_M | 2,02 GB | `c2_lmstudio_02`, `c2_lmstudio_06` |

## 3. Consultas equivalentes en los dos entornos (chat)

Se hicieron las mismas preguntas en Ollama y en LM Studio con el modelo generalista (Llama 3.2 3B):

1. ¿Qué es la inteligencia artificial? Explícalo de manera sencilla para un estudiante universitario.
2. Si una tienda tiene 120 productos y vende el 25 %, ¿cuántos productos quedan? Explica el procedimiento.
3. ¿Qué es una función en Python? Explícalo de manera sencilla y proporciona un ejemplo.
4. Escribe un programa en Python que permita registrar productos con nombre y precio y luego mostrar todos los productos registrados.

| Pregunta | Ollama: tiempo | Ollama: tokens | Ollama: tokens/s | LM Studio: tokens | LM Studio: tokens/s | LM Studio: primer token |
|---|---:|---:|---:|---:|---:|---:|
| P1: inteligencia artificial | 28,96 s | 393 | 13,85 | 479 | 12,38 | 1,90 s |
| P2: tienda 25 % | 18,45 s | 242 | 13,67 | 277 | 11,29 | 1,09 s |
| P3: función en Python | 30,41 s | 389 | 13,06 | 412 | 10,13s | 1,82s |
| P4: programa de productos | 58,00 s | 618 | 11,49 | 277 | 11,29s | 1.09s |

**Evidencias Ollama:** `c2_ollama_02` a `c2_ollama_11`.  
**Evidencias LM Studio:** `c2_lmstudio_03`, `c2_lmstudio_04`.

## 4. Recursos observados

| Entorno | Memoria | CPU / GPU | Contexto | Evidencia |
|---|---|---|---|---|
| Ollama (`llama3.2:3b`) | El modelo ocupa 2,6 GB (`ollama ps`); el equipo quedó en 76 % de RAM | 100 % CPU | 4096 tokens | `c2_ollama_12`, `c2_ollama_13` |
| LM Studio (Llama 3.2 3B) | El equipo quedó en 12,2 de 15,4 GB (79 %) | CPU al 38 %, GPU integrada al 19 % | — | `c2_lmstudio_05` |

**VRAM:** no aplica como memoria dedicada, porque la tarjeta de video es integrada y utiliza la RAM del equipo.

## 5. API local desde Python

| Programa | API | Pregunta | Tiempo | Velocidad / tokens | Evidencia |
|---|---|---|---|---|---|
| `lmstudio_test.py` | `http://localhost:1234/v1/chat/completions` | P1 modelo de lenguaje | 13,9 s | 108 tokens | `c2_lmstudio_07` a `10` |
| | | P2 función promedio | 48,5 s | 429 tokens | |
| | | P3 `[x**2 for x in range(5)]` | 38,4 s | 369 tokens | |
| `ollama_test.py` | `http://localhost:11434/api/generate` | P2 función promedio | 20,6 s | 13,6 tokens/s | `c2_ollama_14` |
| | | P3 `[x**2 for x in range(5)]` | 17,1 s | 13,9 tokens/s | |

**Servidor de LM Studio:** encendido en `http://127.0.0.1:1234`, evidencia `c2_lmstudio_06`.

## 6. Vibe Coding: generación y depuración de código

### 6.1 Objetivo y metodología

Se utilizó el mismo prompt de Vibe Coding para los dos modelos ejecutados en Ollama:

- `llama3.2:3b` como modelo generalista.
- `qwen2.5-coder:3b` como modelo especializado en código.

El problema solicitado consistió en generar un programa `clima.py` que consulta la API pública de Open-Meteo, valida la respuesta, procesa los datos con pandas, calcula estadísticas y genera la gráfica `temperatura.png`.

Posteriormente, a cada modelo se le proporcionó su propio código inicial junto con el mismo prompt de depuración.

### 6.2 Primera generación

| Métrica | Llama 3.2 3B | Qwen 2.5 Coder 3B |
|---|---:|---:|
| Entorno | Ollama | Ollama |
| Tiempo total | 116,71 s | 109,32 s |
| Tokens generados | 1.227 | 1.263 |
| Velocidad | 11,38 tokens/s | 12,62 tokens/s |
| Ejecución inicial | ❌ Error | ❌ Error |
| Error principal | HTTP 400 | `SyntaxError: unterminated string literal` |

### 6.3 Errores observados en la primera generación

**Llama 3.2 3B**
- Parámetro `hourly` implementado incorrectamente.
- No incluyó `past_days=7`.
- Detectó valores `None`, pero no los eliminó correctamente.
- Incompatibilidad entre la estructura devuelta por el procesamiento y la esperada al crear el DataFrame.
- Utilizó `numpy`, aunque el requisito original indicaba solamente `requests`, `pandas` y `matplotlib`.
- Guardó la gráfica como `temperature.png` en lugar de `temperatura.png`.

**Qwen 2.5 Coder 3B**
- URL duplicada y dañada, provocando un `SyntaxError`.
- Error tipográfico en `timezone`.
- Validación incorrecta de `time` y `temperature_2m` respecto a la estructura JSON.
- No verificó que las listas de tiempo y temperatura tuvieran el mismo tamaño.
- Filtrado independiente de las listas podía romper la correspondencia entre fecha y temperatura.
- Mediana calculada manualmente, con posible error para cantidades pares.
- No ordenó explícitamente el DataFrame por fecha.

### 6.4 Segunda etapa: depuración

Se utilizó el mismo prompt de corrección para ambos modelos, proporcionando a cada uno el código que había generado inicialmente.

| Métrica | Llama 3.2 3B | Qwen 2.5 Coder 3B |
|---|---:|---:|
| Tiempo total | 223,16 s | No finalizada |
| Tokens generados | 1.828 | No finalizado |
| Velocidad | 8,96 tokens/s | No determinada |
| Generación | Código de corrección generado | Generación excesivamente extensa y repetitiva |
| Ejecución posterior | ❌ Error HTTP 400 | No se llegó a ejecutar |
| Resultado | No produjo un programa funcional | Generación interrumpida |

### 6.5 Resultado de la segunda ejecución de Llama

El código corregido generado por Llama fue ejecutado sin modificarlo y produjo un error HTTP 400. La URL mostró el parámetro:

`hourly=hourly=temperature_2m`

Por tanto, la corrección no solucionó el problema de la consulta a Open-Meteo. También continuó faltando `past_days=7`.

### 6.6 Comportamiento de Qwen durante la depuración

Durante la segunda generación, Qwen comenzó a producir una lista muy extensa y repetitiva de supuestos errores. Entre ellos aparecieron referencias a `exec`, `globals`, `locals`, `compile` y `eval`, que no estaban relacionadas con el programa climático que se estaba depurando.

La generación fue interrumpida porque no estaba convergiendo hacia una solución del código. No se ejecutó el código de esta segunda respuesta y, por tanto, no se registra un resultado funcional o un error de ejecución para esta etapa.

### 6.7 Comparación de Vibe Coding

| Aspecto | Llama 3.2 3B | Qwen 2.5 Coder 3B |
|---|---|---|
| Primera generación | Código generado con varios errores | Código generado con varios errores |
| Primera ejecución | HTTP 400 | `SyntaxError` |
| Segunda generación | Produjo una propuesta de corrección | Se volvió extensa y repetitiva |
| Segunda ejecución | HTTP 400 | No se ejecutó |
| Velocidad inicial | 11,38 tokens/s | 12,62 tokens/s |
| Velocidad de depuración | 8,96 tokens/s | No determinada |
| Observación | Revisó el código, pero mantuvo errores funcionales importantes | Se desvió del problema durante la depuración |

## 7. Observaciones generales

- **Velocidad:** en las consultas básicas registradas, Ollama generó a 13,85 y 13,67 tokens/s en P1 y P2, frente a 12,38 y 11,29 tokens/s en LM Studio.
- **Hardware:** ambos entornos se ejecutaron sin tarjeta de video dedicada. `ollama ps` mostró 100 % de CPU en la prueba registrada de Ollama.
- **Uso de memoria:** Ollama registró 2,6 GB ocupados por el modelo y 76 % de RAM total; LM Studio registró 12,2 de 15,4 GB, aproximadamente 79 %.
- **Longitud de respuesta:** la P4 fue la más larga en tokens y tiempo dentro de las consultas de Ollama registradas.
- **Calidad:** en LM Studio, el resultado numérico de la P3 fue correcto (`[0, 1, 4, 9, 16]`), aunque la explicación llamó “llaves” a los corchetes.
- **Calidad:** en Ollama, el cálculo del 25 % de 120 productos fue correcto: 30 vendidos y 90 restantes.
- **Vibe Coding:** ambos modelos necesitaron una segunda etapa de depuración y ninguno produjo una solución funcional desde la primera generación.
- **Vibe Coding – Llama:** la segunda respuesta intentó corregir varios problemas, pero el código ejecutado volvió a producir HTTP 400.
- **Vibe Coding – Qwen:** la segunda generación no llegó a una solución ejecutable y presentó contenido repetitivo y referencias a errores no relacionados con el programa.
- **Interpretación:** los tiempos, tokens y velocidades registrados corresponden a estas pruebas concretas y no deben interpretarse por sí solos como una medida general de calidad de los modelos.

## 8. Pendientes

- Ejecutar `ollama show llama3.2:3b` y `ollama show qwen2.5-coder:3b` para confirmar la cuantización.
- Incorporar las capturas definitivas de Vibe Coding en la carpeta de evidencias, si todavía no fueron guardadas.
- Conservar como evidencia de Qwen la captura de la segunda generación donde se observa el contenido repetitivo y los errores irrelevantes.

## 9. Relación del sistema

**MODELO → OLLAMA / LM STUDIO → API LOCAL → APLICACIÓN PYTHON**

El modelo es el archivo con los pesos. Ollama y LM Studio lo cargan en memoria y permiten acceder al modelo mediante una API local: Ollama utiliza el puerto 11434 y LM Studio el 1234. Los programas `ollama_test.py` y `lmstudio_test.py` envían preguntas a estas API y reciben las respuestas en formato JSON.

## 10. Evidencias principales

- `c2_ollama_01`: modelos disponibles en Ollama.
- `c2_ollama_02` a `c2_ollama_11`: pruebas de chat en Ollama.
- `c2_ollama_12`, `c2_ollama_13`: uso de recursos y `ollama ps`.
- `c2_ollama_14`: prueba de API local de Ollama.
- `c2_lmstudio_02`, `c2_lmstudio_06`: modelo y servidor de LM Studio.
- `c2_lmstudio_03`, `c2_lmstudio_04`: pruebas de chat en LM Studio.
- `c2_lmstudio_05`: uso de recursos en LM Studio.
- `c2_lmstudio_07` a `c2_lmstudio_10`: pruebas de API local de LM Studio.
- Evidencias adicionales de Vibe Coding: respuestas iniciales, errores de ejecución, segunda respuesta de Llama y generación repetitiva de Qwen.
