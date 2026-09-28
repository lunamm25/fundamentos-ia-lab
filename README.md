# Laboratorio Parcial 1: Fundamentos de IA para el Desarrollo de Software Aumentado

Fundamentos de Inteligencia Artificial, Ingeniería de Sistemas, Universidad de Manizales.

## Integrantes y reparto

Trabajamos de forma remota en dos sesiones por Google Meet el 22 de septiembre de 2026 (capturas en `evidence/`). Nos repartimos los componentes así:

|Integrante|Componente|
|-|-|
|Andrés Ospina Silva|C0 Mapa mental, C3 Vibe Coding con modelo cloud y consolidación del repositorio|
|Santiago Arias Aguirre|C1 Cartografía de modelos|
|Luna Murillo Moreno|C2 Ollama y LM Studio, C3 Vibe Coding con modelos locales|
|Jerónimo Aristizábal|C4 Reto de series temporales|

## Cómo está organizado

```text
mapa\\\\\\\\\\\\\\\_mental/          C0  mapa en PNG y PDF
cartografia\\\\\\\\\\\\\\\_modelos/  C1  matriz de modelos (CSV)
modelos\\\\\\\\\\\\\\\_locales/      C2  programas que usan la API local y registro de las pruebas
vibe\\\\\\\\\\\\\\\_coding/          C3  prompt, tabla comparativa y código de cada modelo
serie_temporal/       C4  aplicación de series temporales y resultados (output/)
tests/                pruebas del C4
evidence/             capturas: c2\\\\\\\\\\\\\\\_\\\\\\\\\\\\\\\* modelos locales, c3\\\\\\\\\\\\\\\_\\\\\\\\\\\\\\\* vibe coding
```

## Instalación

```bash
python -m venv .venv
.venv\\\\\\\\\\\\\\\\Scripts\\\\\\\\\\\\\\\\activate
pip install -r requirements.txt
```

Ninguna parte necesita API key. Las APIs que usamos (Open-Meteo) son públicas.

## C0 · Mapa mental

`mapa\\\\\\\\\\\\\\\_mental/mapa\\\\\\\\\\\\\\\_mental.png` y `mapa\\\\\\\\\\\\\\\_mental.pdf`. Tiene las cinco ramas que pide la guía: fundamentos, tipos de modelos, funcionamiento, formas de uso e infraestructura. De cada concepto pusimos qué es, para qué sirve, un ejemplo y en qué parte del laboratorio lo usamos. Las líneas punteadas unen conceptos de ramas distintas, por ejemplo Transformers con LLM o cuantización con VRAM.

## C1 · Cartografía de modelos

`cartografia\\\\\\\\\\\\\\\_modelos/Cartografia\\\\\\\\\\\\\\\_Modelos.csv`: 11 modelos en seis categorías (texto, razonamiento, código, visión/multimodal, voz y embeddings), con proveedor, tipo, si es local o cloud, tamaño, hardware, costo y uso recomendado.



Conclusión:
Al analizar las opciones de nuestra cartografía, como equipo concluimos que en inteligencia artificial no existe una «herramienta perfecta» ni un modelo universal que resuelva todas las necesidades. Como ingenieros, debemos elegir según el tipo de tarea, la privacidad de los datos, el hardware disponible y el presupuesto del proyecto.

Si trabajamos con código propietario o información confidencial, primero debemos revisar las políticas de seguridad de la organización y decidir si los datos pueden enviarse a un servicio externo. Cuando el proyecto exige procesamiento local, podemos considerar Llama 3.3 70B para tareas de texto, Qwen3-Coder 30B-A3B para programación y nomic-embed-text-v1.5 para búsqueda semántica. Sus pesos permiten desplegarlos en infraestructura propia, aunque los dos primeros requieren equipos considerablemente más potentes que una computadora portátil convencional.

Cuando la tarea exige razonamiento profundo, investigación o desarrollo de software complejo, los servicios en la nube amplían las opciones. GPT-6 Astra puede apoyar flujos de trabajo avanzados y agentes; Claude Sonnet 5 resulta pertinente para programación y documentación técnica; y Gemini 3.1 Pro se orienta a problemas de investigación y razonamiento exigente. Para asistencia cotidiana dentro del entorno de desarrollo, GitHub Copilot y Gemini Code Assist son opciones prácticas, siempre que su uso cumpla las políticas de la empresa.

La elección también depende del tipo de información. Para analizar imágenes y documentos podemos evaluar Gemini 3.6 Flash o, si necesitamos una alternativa local de visión, LLaVA-OneVision. Para transcribir audio contamos con Whisper large-v3, mientras que ElevenLabs v3 cubre la generación de voz. Si el objetivo es construir un sistema de búsqueda sobre documentos internos, nomic-embed-text-v1.5 ofrece una opción local y text-embedding-3-large una alternativa mediante API.C2 · Modelos locales

Probamos en un portátil con Ryzen 5 4600H, 16 GB de RAM y gráficos integrados, sin tarjeta de video dedicada.


|Programa|Modelos|API local|
|-|-|-|
|Ollama|llama3.2:3b (general) y qwen2.5-coder:3b (código)|`localhost:11434`|
|LM Studio|Llama 3.2 3B Instruct, Q4\_K\_M|`localhost:1234`|

```bash
python modelos\\\\\\\\\\\\\\\_locales/ollama\\\\\\\\\\\\\\\_test.py
python modelos\\\\\\\\\\\\\\\_locales/lmstudio\\\\\\\\\\\\\\\_test.py
```

Los tiempos, la memoria y lo que encontramos al comparar están en `modelos\\\\\\\\\\\\\\\_locales/registro\\\\\\\\\\\\\\\_tecnico.md`.

## C3 · Vibe Coding

Como el docente no entregó un problema, usamos el ejemplo de la guía: consumir una API pública, validar la respuesta, sacar estadísticas y graficar. Tomamos la temperatura por hora de Manizales en Open-Meteo y usamos el mismo prompt en los tres modelos. El prompt, la tabla y la reflexión están en `vibe\\\\\\\\\\\\\\\_coding/comparativo.md`.

```bash
cd vibe\\\\\\\\\\\\\\\_coding/cloud
python clima.py
```

## C4 · Series temporales

Temperatura media diaria de Manizales en 2024 y 2025 (731 días), tomada de Open-Meteo Archive. El 80 % inicial se usa para entrenar y el 20 % final para probar, sin mezclar el orden. Comparamos una persistencia (hoy igual a ayer) con una regresión lineal que usa los 7 días anteriores.

|Método|MAE (°C)|RMSE (°C)|
|-|-:|-:|
|Persistencia|0,4769|0,6114|
|Regresión lineal|0,4083|0,5168|

```bash
python -m serie_temporal.app
python -m pytest
```

El detalle del proceso está en `serie_temporal/proceso.md` y las gráficas en `serie_temporal/output/`.

## Modelos y herramientas de IA usadas

|Parte|Modelo|Herramienta|Fecha|
|-|-|-|-|
|C0|Claude Opus 5.5|Claude (Cowork)|22/09/2026|
|C2|llama3.2:3b, qwen2.5-coder:3b|Ollama|22/09/2026|
|C2|Llama 3.2 3B Instruct Q4\_K\_M|LM Studio|22/09/2026|
|C3 cloud|ChatGPT (versión que mostraba la app: 5.6 luna)|chatgpt.com|22/09/2026|
|C3 local|llama3.2:3b, qwen2.5-coder:3b|Ollama|gpt 5.6 luna|
|C4|Grok 4.7|Cursor|22/09/2026|
|C1|Gemini 3.1 Pro|Google|22/09/2026|

## Qué hizo la IA y qué decidimos nosotros

|Parte|La IA|El equipo|
|-|-|-|
|C0|Ayudó a redactar las definiciones y a dibujar el mapa|Definimos las ramas según la guía y revisamos cada concepto y sus relaciones|
|C2|Ayudó a escribir los programas de prueba de la API|Instalamos, ejecutamos, medimos tiempos y memoria y revisamos las respuestas. Encontramos, por ejemplo, que el modelo llamó "llaves" a los corchetes|
|C3|Cada modelo generó su versión de `clima.py`|Escogimos el problema, escribimos el prompt, ejecutamos, contamos errores y verificamos los datos contra la API|
|C4|Ayudó a separar los módulos y a escribir el código inicial|Escogimos Open-Meteo, Manizales, el periodo 2024-2025, el corte 80/20, la persistencia y la regresión lineal. Ejecutamos el programa con datos reales y revisamos el MAE y el RMSE|
|C1|Estructuró la matriz, recopiló especificaciones técnicas y ayudo en el mejoramiento de la conclusión.|Auditó la información, corrigió la categoría/precios, descartó modelos no públicos y verificó de manera detallada las fuentes.|


## Conclusión Vibe-coding

1. Código funcional vs. ejecución
Tanto con Llama 3.2 3B como con Qwen 2.5 Coder 3B, ambos modelos entregaron respuestas superficialmente estructuradas, con explicaciones convincentes, bloques de código ordenados y pasos de instalación. Sin embargo, ninguno de los dos programas corrió en el primer intento:   Llama 3.2 3B construyó una consulta con el parámetro hourly=hourly, lo que ocasionó un Error HTTP 400 (Bad Request) al interactuar con el endpoint real de Open-Meteo. Además, confundió la lectura de marcas temporales asumiendo enteros UNIX con fromtimestamp sobre cadenas ISO-8601.   Qwen 2.5 Coder 3B presentó fallas de sintaxis directa: concatenó mal las cadenas de texto de la URL, dejó el exponente 0.5 en una línea huérfana y produjo un KeyError al buscar data["time"] fuera del objeto hourly.   Esto demuestra que los modelos SLM locales (3B) pueden emular la apariencia y el flujo general de una solución en Python, pero carecen del contexto factual preciso sobre contratos de API externos y cometen errores sintácticos elementales bajo restricciones de contexto.   

2. El bucle de depuración y las limitaciones de los modelos compactos
El ciclo de Vibe Coding se define por la interacción continua: PROBLEMA → PROMPT → MODELO → CÓDIGO → EJECUCIÓN → ERROR → CORRECCIÓN → SOLUCIÓN. 
En esta etapa se observó una brecha crítica de comportamiento:   Llama 3.2 3B intentó corregir el código tras una segunda consulta de más de 220 segundos, pero persistió en el error de parámetros de la API, incapaz de salir de la alucinación sobre la firma del endpoint.   
Qwen 2.5 Coder 3B colapsó en un bucle repetitivo y no finalizó su generación de depuración, requiriendo intervención humana obligatoria para detener el proceso.   En contraposición, el modelo Cloud (ChatGPT) alcanzó una solución funcional en menos de 5 minutos e iteró exitosamente con una sola indicación humana menor vinculada al copiado de bloques Markdown.   

3. Rendimiento, hardware y viabilidad operativa
Al ejecutar la inferencia en un entorno local sobre CPU (Ryzen 5 4600H con gráficos integrados compartiendo RAM), la tasa de generación osciló entre 11,38 y 12,62 tokens/s en la etapa inicial, y decayó hasta 8,96 tokens/s en fases largas.   Esto implica que iterar múltiples veces un error en local consume entre 2 y 4 minutos por intento únicamente en cómputo, frente a los pocos segundos que toma un modelo en la nube.   La ventaja de la privacidad total y la gratuidad de Ollama/LM Studio se equilibra frente al costo temporal cuando el modelo carece de la capacidad de razonamiento suficiente para autocorregir excepciones complejas de bibliotecas como Pandas o peticiones HTTP.   

4. La supervisión humana como filtro no negociable
El ejercicio evidenció que el Vibe Coding no consiste en copiar y pegar a ciegas. 
La intervención humana fue estrictamente necesaria para:   Comprender los contratos de datos: Verificar la estructura del JSON devuelto por Open-Meteo (data['hourly']['time'] y data['hourly']['temperature_2m']).   Garantizar la integridad analítica: Evitar que comprensiones de listas independientes desalinearan los índices de fechas y temperaturas al eliminar valores nulos (df.dropna()), un error metodológico que los modelos cometieron reiteradamente.   
Validación semántica: Interpretar que una gráfica de 14 días une 7 días históricos con 7 de pronóstico numérico, aspecto crítico que ningún modelo advirtió por sí solo.   

En conclusión, los modelos locales de 3 mil millones de parámetros son herramientas de apoyo útiles para generar esqueletos sintácticos iniciales o resolver dudas puntuales de funciones, pero en flujos de desarrollo autónomo guiado por errores (Vibe Coding), demandan un nivel de supervisión técnica exhaustivo y prompts con especificaciones muy estrictas para no derivar en código roto. 



