# Protocolo de captura desde el móvil — piloto Clínica Ártica

> SPEC-007 CA-3. Para imprimir y seguir al pie de la letra. Preguntas: `prompts-baseline.md`.
> Registro: copia de `plantilla-captura.csv`. Todo lo que generes (capturas, CSV, notas)
> va a `$PUSHLLM_PRIVADO/piloto-artica/baseline/AAAA-MM-DD-pN/`, **nunca al repo**.

## Antes de empezar (una vez por pasada)
1. Crea la carpeta de la pasada (fecha del primer día y `p1` o `p2`) con una copia de la
   plantilla y un fichero `desviaciones.txt` vacío (**registro de desviaciones**).
2. Apunta la **cabecera de sesión**: municipio desde el que preguntas, si la ubicación del
   móvil está activada, y la cuenta que usas en cada app (un alias corto, nunca el email).
   Mide desde Viveiro o A Mariña, y las dos pasadas desde el mismo sitio; si un día no
   puede ser, anótalo en `desviaciones.txt`. Estas condiciones (cuenta, plan, modo, móvil, municipio) son **las mismas
   en todas las pasadas, incluidas las de SPEC-012**; lo que no puedas repetir, a
   desviaciones.
3. Usa siempre la **cuenta gratuita** de cada app (lo que ve la mayoría de pacientes). Una
   cuenta de pago solo como observación aparte, con `plan_cuenta` = `pago`: no cuenta.
4. Reserva 60–90 min seguidos. Si no te da, termina al día siguiente (máximo 2 días).

## Cómo abrir una sesión limpia
- **ChatGPT** (app): sesión iniciada con la cuenta gratuita. Ajustes → Personalización:
  memoria desactivada. Cada pregunta en un **chat temporal** nuevo (icono de chat temporal
  arriba). No cambies el modelo ni actives nada: lo que venga por defecto. `modo` =
  `temporal`.
- **Gemini** (app): cuenta gratuita. Actividad en las apps de Gemini desactivada y sin
  contexto personal. Si hay chat temporal, úsalo (`temporal`); si no, chat nuevo
  (`normal`) y anótalo. No toques el selector de modelo.
- **Google** (Chrome): **pestaña de incógnito**, sin sesión, google.com. Escribe la
  pregunta como búsqueda. Solo cuenta el bloque de resumen creado con IA de arriba; no
  entres en "Modo IA". `modo` = `incognito`, `sesion_iniciada` = `no`, `plan_cuenta` =
  `sin_sesion`.
- **Modelo**: apunta en `modelo_mostrado` lo que la app enseña arriba o en el selector
  (p. ej. el nombre del modelo o "Rápido"); si no enseña nada, `no se muestra`.

## Cómo preguntar
1. Orden: primero todas las `AV` y luego las `AM` en ChatGPT; lo mismo en Gemini; por
   último las `AV` en Google. Dentro de cada app, en el **orden del set**.
2. Copia y pega el **texto literal** de la pregunta. **Una pregunta por conversación
   nueva**. No repreguntes ni pidas aclaraciones.
3. Espera a que la respuesta termine del todo.

## Qué capturar
- Una **captura** de la respuesta completa: si no cabe, captura desplazada (o varias,
  desplazándote). Que la pregunta se vea en la primera.
- Si la respuesta tiene botón de fuentes, ábrelo y captúralo también.
- Google: el resumen de IA desplegado ("Mostrar más"). Si no aparece resumen, captura la
  parte de arriba de los resultados igualmente.
- **Enlace compartido** si la app lo permite (en chat temporal no suele permitirlo:
  escribe `no permite`).

## Reglas anti-contaminación de la atribución
1. **No pulses ningún enlace a la web de la clínica** desde las respuestas.
2. **No busques el nombre de la clínica en Google**: las preguntas AM solo en ChatGPT y
   Gemini.
3. Todo lo que hagas distinto (app caída, sin chat temporal, otra ubicación, otra hora,
   pregunta mal pegada) va al **registro de desviaciones**: qué, por qué y en qué filas.

## Campos por fila (CSV, una fila por pregunta × app)
Obligatorios (los rellenas tú; se pueden copiar de la cabecera de sesión):
- `fecha_hora_local`: AAAA-MM-DD HH:MM (sirve la hora de la captura).
- `pasada`: `p1` o `p2` (en el cierre, lo que diga SPEC-012).
- `id_pregunta`: `AV01`…, `AM01`….
- `app`: `chatgpt`, `gemini`, `google` (o `claude` si se usa como observación).
- `modo`: `temporal`, `normal` o `incognito`.
- `sesion_iniciada`: `si` / `no`.
- `cuenta`: alias corto de la cuenta, nunca el email.
- `plan_cuenta`: `gratuito`, `sin_sesion` o `pago`.
- `modelo_mostrado`: lo que enseña la app.
- `municipio`: desde dónde preguntas.
- `ubicacion_dispositivo`: `si` / `no`.
- `idioma`: `es` o `gl` (el de la pregunta).

También tuyos, al terminar cada pregunta:
- `respuesta_valida`: `si` si la app contestó a la pregunta (aunque diga que no puede
  recomendar); `no` si falló, se cortó o la pregunta se pegó mal (explícalo).
- `resumen_ia`: solo Google, `si` / `no`; en ChatGPT y Gemini, `n-a`.
- `enlace_compartido`, `fichero_captura` (nombre del fichero o ficheros, separados por
  `;`) y `observaciones`. Marcas: `#artica-adjetivo` si "ártica" sale como adjetivo
  (cuenta igual; se revisa a mano) y `#medica-sin-clinica` si sale la médica titular sin
  la clínica (no cuenta como mención).

Los rellena el agente al hacer el recuento, leyendo tus capturas (tú revisas una muestra):
- `clinicas_nombradas`: clínicas o médicos nombrados, en orden de aparición, separados por
  `;` (sin directorios como Doctoralia).
- `artica_nombrada`: `si` / `no`.
- `posicion_artica`: su puesto entre las clínicas nombradas (1 = la primera); vacío si no
  sale.
- `dominios_citados`: dominios de las fuentes, separados por `;`.

## Pasada 2 y siguientes
Igual que la 1: mismas apps, cuentas, modos, móvil y municipio, a una hora parecida
(± 2 h). La pasada 2 va entre 3 y 10 días después de la 1 y **antes de la primera acción**
del piloto. Claude (cuenta gratuita) es opcional y solo observación: si lo usas en una
pasada, úsalo en todas.
