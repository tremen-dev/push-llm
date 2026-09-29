# Protocolo de captura desde el móvil — calibración del piloto Clínica Ártica

> SPEC-007 CA-3. Para imprimir y seguir al pie de la letra. Preguntas: `prompts-baseline.md`
> (para copiar: `preguntas-en-orden.txt`, privado). Registro: copia del CSV prerrellenado
> de la pasada (o de `plantilla-captura.csv`). Todo lo que generes (capturas, CSV, notas) va
> a `$PUSHLLM_PRIVADO/piloto-artica/baseline/AAAA-MM-DD-antes/` (o `-despues/`), **nunca al
> repo**.

La medición del piloto la hace el probe. Esta pasada a mano **calibra**: comprueba, en el
área de influencia (AR) y en el núcleo (AV) por separado, que lo que ve el paciente se
parece a lo que mide el probe, mide el resumen de IA de Google en AR y da capturas reales
para la reunión. Hay **una pasada "antes"** (`pasada` =
`antes`) y **una "después"** (`despues`, al cierre, SPEC-012).

## Antes de empezar
1. **Ventanas**: la pasada se empareja con **las dos ejecuciones** del probe: la de AV (el
   **baseline oficial del probe**, SPEC-008 CA-7) y la de AR (el "antes" de AR, SPEC-008
   CA-12). Hazla como mucho **7 días** después de cada una (en el "después", de las
   mediciones "después" del probe) y antes de la primera acción. Fuera de una ventana, ese
   nivel no calibra.
2. Crea la carpeta de la pasada (fecha del primer día) con la copia del CSV, un fichero
   `desviaciones.txt` vacío (**registro de desviaciones**) y una carpeta `capturas/`.
3. Apunta la **cabecera de sesión**: municipio, si la ubicación del móvil está activada y
   la cuenta de cada app (un alias corto, nunca el email). **Municipio fijo: Vilaboa**, para
   todas las pasadas (antes y después). La ubicación del móvil, activada o no, con un ajuste
   idéntico en todas las pasadas. Nada de VPN ni de simular el GPS. Estas condiciones
   (cuenta, plan, modo, móvil, municipio) son **las mismas en las dos pasadas** (mismas en
   todas las pasadas, incluida la de SPEC-012); lo que no puedas repetir, a desviaciones.
   *Limitación*: el probe envía la ubicación Viveiro. En el núcleo afecta poco en ChatGPT y
   Gemini, porque la pregunta nombra el lugar. En AR **pesa más**: las preguntas hablan
   desde Ferrolterra, Lugo o Asturias y ni Vilaboa ni Viveiro están allí; en Google, sus
   resúmenes de IA y Maps pesan mucho la ubicación del dispositivo.
4. Usa siempre la **cuenta gratuita** de cada app (lo que ve la mayoría de pacientes). Una
   cuenta de pago solo como observación aparte, con `plan_cuenta` = `pago`: no cuenta.
5. Son **49 consultas**: 60–90 min de preguntas más 20–25 min de CSV y capturas. Si no te
   da, termina al día siguiente (máximo 2 días seguidos): el corte cae entre apps (nunca
   dentro de una) y se anota en desviaciones.

## Cómo abrir una sesión limpia
- **ChatGPT** (app): cuenta gratuita. Ajustes → Personalización: memoria desactivada. Cada
  pregunta en un **chat temporal** nuevo. No cambies el modelo ni actives nada. `modo` =
  `temporal`.
- **Gemini** (app): cuenta gratuita. Actividad en las apps de Gemini desactivada y sin
  contexto personal. Si hay chat temporal, úsalo (`temporal`); si no, chat nuevo
  (`normal`) y anótalo. No toques el selector de modelo.
- **Google** (Chrome): **pestaña de incógnito**, sin sesión, google.com. Escribe la
  pregunta como búsqueda. Solo cuenta el bloque de resumen creado con IA de arriba; no
  entres en "Modo IA". `modo` = `incognito`, `sesion_iniciada` = `no`, `plan_cuenta` =
  `sin_sesion`.
- **Modelo**: apunta en `modelo_mostrado` lo que enseña la app; si nada, `no se muestra`.

## Cómo preguntar
1. Orden por app, igual en las dos pasadas: en ChatGPT, primero el bloque AR, después el AV
   y por último las AM (22 consultas); lo mismo en Gemini (22); por último, en Google solo
   el bloque AR (5; nunca AV, AM ni AG). Dentro de cada bloque, en el **orden del set**.
2. Copia y pega el **texto literal** de la pregunta. **Una pregunta por conversación
   nueva**. No repreguntes ni pidas aclaraciones.
3. Espera a que la respuesta termine del todo.

## Qué capturar
- Una **captura** de la respuesta completa (captura desplazada o varias, desplazándote).
  Que la pregunta se vea en la primera.
- Si la respuesta tiene botón de fuentes, ábrelo y captúralo también.
- Google (AR): el resumen de IA desplegado ("Mostrar más"). Si no aparece resumen, captura
  la parte de arriba de los resultados igualmente.
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
- `fecha_hora_local`: AAAA-MM-DD HH:MM.
- `pasada`: `antes` o `despues`.
- `id_pregunta`: `AR01`…`AR05`, `AV01`…`AV15`, `AM01`, `AM02`.
- `app`: `chatgpt`, `gemini`, `google` (o `claude` si se usa como observación).
- `modo`: `temporal`, `normal` o `incognito`.
- `sesion_iniciada`: `si` / `no`.
- `cuenta`: alias corto de la cuenta, nunca el email.
- `plan_cuenta`: `gratuito`, `sin_sesion` o `pago`.
- `modelo_mostrado`: lo que enseña la app.
- `municipio`: `Vilaboa`.
- `ubicacion_dispositivo`: `si` / `no`.
- `idioma`: `es` o `gl` (el de la pregunta).

También tuyos, al terminar cada pregunta:
- `respuesta_valida`: `si` si la app contestó (aunque diga que no puede recomendar); `no`
  si falló, se cortó o la pregunta se pegó mal (explícalo).
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

## Opcional
Claude (cuenta gratuita) solo como observación: si lo usas en una pasada, úsalo en las dos.
Si estás en Viveiro, puedes repetir solo el bloque AR de Google y Maps como **observación
de sensibilidad a la ubicación**, con `municipio` = `Viveiro`, en una carpeta aparte
(`AAAA-MM-DD-antes-sensibilidad/`). Queda fuera del cómputo.
