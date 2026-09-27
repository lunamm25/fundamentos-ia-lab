# Comparativo de Vibe Coding: 3 modelos, el mismo problema

**Problema:** Consumir la API pública Open-Meteo (temperatura por hora en Manizales), validar la respuesta, calcular estadísticas y graficar.  
**Prompt:** `problema_y_prompt.md`, el mismo texto para los 3 modelos.  
**Cómo se mide:** Cada vez que se le pega un error al modelo cuenta como 1 iteración (máximo 5). El código no se corrige a mano.

---

## Modelos usados

| Enfoque | Modelo | Herramienta | Fecha |
|---|---|---|---|
| Local generalista | `llama3.2:3b` | Ollama | 27/09/2026 |
| Local de código | `qwen2.5-coder:3b` | Ollama | 27/09/2026 |
| Cloud de desarrollo | ChatGPT (5.6 luna) | chatgpt.com | 22/09/2026 |

---

## Tabla comparativa

| Criterio | Local general (`llama3.2:3b`) | Local coding (`qwen2.5-coder:3b`) | Cloud coding (ChatGPT 5.6 luna) |
|---|---|---|---|
| **Código ejecutable** | **No.** Falló por configuración de API y lógica de validación destructiva. | **No.** Inutilizable por errores de sintaxis y bucles de salida en la depuración. | **Sí.** Trajo 336 datos reales, 0 vacíos descartados, y generó `temperatura.png`. |
| **Errores encontrados** | 1. Parámetro erróneo (`hourly='hourly'`).<br>2. Error de parsing de fechas ISO (`TypeError` en `fromtimestamp`).<br>3. Descarte destructivo de la estructura JSON en la validación. | 1. `SyntaxError` (URL truncada y saltos de línea rotos en expresiones matemáticas).<br>2. `KeyError` por acceso erróneo a la raíz (`data['time']`).<br>3. Bucle degenerativo de repetición en el chat. | 1. `SyntaxError` accidental por copiado de marcas ` ``` ` al inicio/final del archivo. Cero errores de lógica. |
| **Iteraciones necesarias** | 2 iteraciones (generación inicial + 1 ronda de depuración). No llegó a solución. | 2 iteraciones (generación inicial + intento de depuración interrumpido). No llegó a solución. | 2 iteraciones (generación inicial y 1 consulta rápida para limpiar los backticks). |
| **Tiempo hasta solución** | Fallido (~5,66 min acumulados: 116,71 s inicial + 223,16 s depuración). | Fallido (~1,82 min inicial: 109,32 s; depuración interrumpida por loop). | Menos de 5 min (funcional en primera instancia). |
| **Calidad/claridad del código** | 2/5. Modularizado en funciones, pero con manejo deficiente de estructuras de datos y lógica que invalidaba su propia ejecución. | 1.5/5. Estructura no modular (código monolítico), concatenación rota de URLs y filtrado independiente que desfasaba series de tiempo. | 4/5. 5 funciones limpias, 6 validaciones, uso de `errors="coerce"`. En contra: bloqueaba consola con `plt.show()`. |
| **Documentación** | Comentarios breves en español; sin instrucciones de entorno. | Comentarios básicos en bloques principales, sin guía de paquetes requeridos. | Comentarios detallados en español paso a paso e instrucciones claras de instalación en el chat. |
| **Pruebas sugeridas/generadas** | No sugirió pruebas formales ni casos de test unitarios. | No generó archivo de pruebas ni sugerencias de validación. | Sugeridas en el chat conforme a lo solicitado en el prompt. |
| **Intervención humana necesaria** | **Alta e infructuosa:** Requirió capturar logs de error, pero el modelo fue incapaz de autocorregirse sin reescribirle la instrucción. | **Alta e infructuosa:** Requirió cancelar manualmente la generación para evitar el congelamiento de la sesión. | **Media-baja:** Pegar el error de sintaxis, retirar las marcas ``` y validar la gráfica contra la API. |
| **Ciclo de trabajo** | PROBLEMA → PROMPT → MODELO → CÓDIGO → ERROR HTTP 400 → DEPURE → ERROR HTTP 400 (ESTANCADO) | PROBLEMA → PROMPT → MODELO → CÓDIGO → SYNTAX ERROR → DEPURE → BUCLE INFINITO (INTERRUMPIDO) | PROBLEMA → PROMPT → MODELO → CÓDIGO → EJECUCIÓN → ERROR COPIADO → CORRECCIÓN → SOLUCIÓN |

---

## Resultados de ejecución real

### 1. Modelo Cloud (ChatGPT 5.6 luna - 22/09/2026)

| Dato | Valor |
|---|---|
| Cantidad de datos | 336 (7 días pasados + 7 de pronóstico × 24 horas) |
| Valores vacíos descartados | 0 |
| Temperatura mínima | 11,90 °C |
| Temperatura máxima | 24,00 °C (17/09/2026 a las 13:00) |
| Promedio | 16,21 °C |
| Mediana | 15,70 °C |
| Desviación estándar | 2,60 °C |
| Gráfica generada | `temperatura.png` generada correctamente |

### 2. Modelos Locales (Llama 3.2 3B y Qwen 2.5 Coder 3B - 27/09/2026)

* **Llama 3.2 3B:** No arrojó métricas numéricas. La ejecución arrojó un error HTTP 400 por enviar parámetros inválidos al endpoint (`hourly='hourly'`). En la fase de depuración, modificó aspectos superficiales del código pero persistió en el mismo parámetro HTTP erróneo tras 223,16 s de procesamiento a 8,96 tok/s.
* **Qwen 2.5 Coder 3B:** No arrojó métricas numéricas. Falló en la carga inicial debido a un `SyntaxError` inmediato (un salto de línea huérfano con `0.5` y URLs concatenadas sin operadores). En la etapa de depuración, entró en un patrón de degeneración de salida con repeticiones continuas que obligaron a terminar el proceso.

---

## Reflexión técnica

### 1. Cumplimiento de requisitos y tipos de errores
* **Modelos locales (3B):** Ninguno logró completar los 9 requisitos del flujo de trabajo. Aunque intentaron estructurar la consulta HTTP y el cálculo estadístico, fallaron en aspectos críticos de integración:
  * **Conocimiento de APIs:** Ambos asumieron esquemas erróneos de la API de Open-Meteo (Llama envió parámetros inválidos; Qwen buscó `data['time']` en la raíz en lugar de `data['hourly']['time']`).
  * **Manejo de tipos y series temporales:** Llama intentó convertir texto ISO-8601 con `datetime.fromtimestamp()`, y Qwen filtró valores nulos con listas independientes por comprensión, lo que habría roto la correspondencia temporal entre horas y temperaturas de haber llegado a ejecutarse.
* **Modelo Cloud:** Cumplió la totalidad de los requisitos funcionales a la primera pasada de inferencia, fallando únicamente por un detalle de formateo al exportar el texto Markdown a un script `.py`.

### 2. Capacidad de depuración autónoma (Vibe Coding estricto)
Bajo la regla de no corregir a mano y únicamente retroalimentar con el error de consola:
* Los modelos locales de 3B mostraron una **baja ventana de contexto efectivo** y dificultades de razonamiento causal en código. Llama 3.2 no relacionó el código HTTP 400 con su diccionario de parámetros `params`, mientras que Qwen 2.5 Coder perdió el control del espacio de tokens, cayendo en alucinaciones repetitivas.
* El modelo cloud demostró comprensión inmediata de su propio error sintáctico, guiando al usuario para remover los delimitadores Markdown en un solo paso.

### 3. Comparativa entre enfoques locales (General vs. Código)
A pesar de que `qwen2.5-coder:3b` está entrenado específicamente para desarrollo de software, su rendimiento no superó cualitativamente a `llama3.2:3b`:
* **Velocidad:** Qwen tuvo un rendimiento de salida inicial superior (12,62 tok/s frente a 11,38 tok/s de Llama).
* **Robustez sintáctica:** Paradójicamente, Llama 3.2 (generalista) entregó una sintaxis de Python válida y estructurada modularmente en funciones, mientras que Qwen generó código roto con cadenas abiertas y líneas desalineadas.
* **Estabilidad:** Llama finalizó sus generaciones de forma coherente en ambas etapas; Qwen sufrió colapsos de repetición en respuestas extensas.

### 4. Balance operativo: Modelos Locales vs. Soluciones Cloud
* **Hardware y velocidad:** En un procesador móvil con gráficos integrados (Ryzen 5 4600H), la velocidad de inferencia local osciló entre 9 y 13 tok/s (100 % de carga en CPU y ~2,6 GB de RAM ocupada). Cada iteración requirió entre 2 y 4 minutos de cómputo por respuesta, haciendo el ciclo de depuración lento e ineficiente cuando no hay resolución positiva.
* **Privacidad vs. Autonomía:** Los modelos locales garantizan privacidad absoluta y gratuidad sin depender de conexión a internet. Sin embargo, para tareas que involucran integración de APIs externas, dependencias complejas de manipulación de datos (`pandas`, `numpy`) y depuración interactiva, un modelo local de **3B parámetros resulta insuficiente**.
* **Conclusión:** Para flujos reales de *Vibe Coding* donde el usuario delega la lógica al modelo, el modelo Cloud es el único que ofreció viabilidad práctica (resolución en menos de 5 minutos). Para igualar esta experiencia en local se requeriría saltar a modelos de al menos 7B–14B parámetros cuantizados (como Qwen 2.5 Coder 7B/14B o DeepSeek-R1-Distill), condicionado a disponer de una GPU con VRAM dedicada para sostener velocidades interactivas.