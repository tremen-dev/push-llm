# Procedimiento de recuento — calibración manual del piloto Clínica Ártica

> SPEC-007 CA-7. Aplica el dictamen de `sdd-metricas` del ledger de SPEC-007 (CA-2, puntos
> (a), (c), (e), la segunda ampliación (k)–(n) y la tercera (o)–(s), **calibración por
> nivel**). Está escrito para hacerse a mano o con una hoja de cálculo desde el CSV de
> **una sola pasada** (`antes` o `despues`, 49 filas) y los dos `results.csv` del probe
> emparejados, uno por nivel; `tools/count_baseline.py` hace lo mismo y sirve para
> comprobarlo. Entradas y resultado viven en `$PUSHLLM_PRIVADO/piloto-artica/` (ADR-004):
> nunca en el repo. Es calibración: **no entra en el criterio Go**, que se calcula probe
> contra probe ((C) en `AR`, (D) en `AV`; SPEC-008 CA-11). Cada nivel se cuenta, se compara
> y se dictamina aparte: **ninguna cifra ni veredicto junta los niveles** (ADR-005 §4,
> ADR-009 §2).

## 0. Preparar
1. Abre el CSV de la pasada. Comprueba que todas las filas tienen la misma `pasada`, que no
   hay filas repetidas (misma `id_pregunta`, `app`, `plan_cuenta` y `municipio`), que toda
   fila con `respuesta_valida` = `si` tiene `artica_nombrada` = `si` o `no`, y que el
   reparto es el del protocolo: `AR01`–`AR05` en ChatGPT, Gemini y Google; `AV01`–`AV15` y
   `AM01`–`AM02` en ChatGPT y Gemini (49 filas). No hay filas `AG` ni filas `AV`/`AM` de
   Google; si las hay, la pasada no sigue el protocolo.
2. Rellena, leyendo las capturas, `clinicas_nombradas`, `artica_nombrada`,
   `posicion_artica` y `dominios_citados` con las reglas de mención del dictamen:
   - cuenta como mención el nombre de la clínica o un alias de 4 o más caracteres en el
     texto de la respuesta (RN-01), sin mirar tildes ni mayúsculas;
   - una ficha de fuente o un enlace que solo muestra el dominio no es mención: va a
     `dominios_citados`;
   - un uso de "ártica" como adjetivo cuenta igualmente (RN-01 literal) pero se marca
     `#artica-adjetivo` en `observaciones`;
   - el nombre de la médica titular sin el de la clínica no es mención: se marca
     `#medica-sin-clinica` y se informa aparte;
   - la posición es el puesto de la clínica entre las clínicas o médicos nombrados, sin
     contar directorios (RN-06).
3. Si una misma clínica aparece escrita de varias formas, o es una cadena con varias sedes,
   crea `alias-canonicos.csv` (columnas `alias,canonico`) y usa siempre el nombre canónico
   (una cadena es una marca; la sede va a `observaciones`).

## 1. Filtrar
- **Cuenta**: `app` = `chatgpt`, `gemini` o `google` (este, solo `AR`), `plan_cuenta` =
  `gratuito` o `sin_sesion`, `municipio` = `Vilaboa`. El nivel sale del prefijo del id.
- **No cuenta** (observación aparte): cuentas de pago, Claude, cualquier otra app y las
  filas desde otro municipio (observación de sensibilidad a la ubicación).
- **Preguntas de marca** (`AM`): nunca en ninguna cifra; se leen aparte (§5).
- **Respuestas válidas**: `respuesta_valida` = `si`. Las demás se cuentan como excluidas.

## 2. Lo que ve el paciente, por app y por nivel (ChatGPT y Gemini)
- **Núcleo AV**: válidas y excluidas; SoV bruto (RN-02) = filas con la clínica ÷ válidas,
  también como "x de n"; posición media (RN-06) donde sale; clínicas que aparecen en su
  lugar (en las válidas sin la clínica, cuántas respuestas nombran a cada otra, con su
  nombre canónico).
- **Área de influencia AR**: válidas, excluidas y "x de 5" con la clínica, **sin
  porcentajes**; la posición como **lista de puestos**, sin media; clínicas en su lugar, con
  una cadena de varias sedes como **una marca**.
- **No se calcula SoV ponderado** con la manual, en ningún nivel (dictamen (n), (s)).

## 3. Google, resumen de IA (solo búsquedas AR; canal aparte, fuera de los veredictos y del Go)
- Solo búsquedas AR (5 por pasada). Recuentos "x de 5", **sin porcentajes**: búsquedas
  válidas; cuántas con resumen de IA (`resumen_ia` = `si`); en cuántas sale la clínica
  dentro del resumen, sobre las válidas y sobre las que tuvieron resumen. Sin resumen: búsqueda válida y sin la clínica. El paquete
  de mapas y los resultados normales no cuentan.
- Limitación: se busca desde Vilaboa lugares de Ferrolterra, Lugo o Asturias, y Google pesa
  mucho la ubicación del dispositivo.
- Antes/después (SPEC-012): con 5 búsquedas **solo se describe** ("x de 5 antes, y de 5
  después", con las búsquedas con resumen de cada pasada), sin objetivo ni promesa.

## 4. Dominios más citados, por nivel
En las filas válidas que cuentan de cada nivel (`AV`: ChatGPT y Gemini; `AR`: ChatGPT,
Gemini y Google), en cuántas filas aparece cada dominio de `dominios_citados` (sin `www.`),
de más a menos.

## 5. Preguntas de marca
Por cada fila `AM`: qué dice el asistente de la clínica (dirección, servicios, precios) y
si es correcto frente a su web y la foto técnica.

## 6. Comparación app frente a probe, un nivel cada vez
Lado probe, en los dos niveles: `results.csv` del lote Viveiro con la columna
`searched_urls` (posterior a SPEC-013; si no la tiene, no sirve); solo filas con `status` =
`ok` y del nivel que se compara; ChatGPT = proveedor `openai`, Gemini = `gemini`. En cada
run, la clínica sale si su nombre está en `brands_mentioned`, y su puesto es el orden en
esa lista. Distancia = días entre las fechas de las filas del nivel en el probe
(`timestamp_utc`) y las de las filas del mismo nivel en la pasada; 0 si se solapan.

### 6-AV. Núcleo: "coinciden de forma razonable en AV"
1. **Emparejar**: el `results.csv` del **baseline oficial** (SPEC-008 CA-7) en el "antes";
   en el "después", la medición "después" del probe más cercana. Ventana máxima: **7 días**.
2. **Casillas**: pregunta `AV` × asistente (15 × 2). Por casilla: "k de n" runs con la
   clínica; **sale** si está en más de la mitad de los runs, **no sale** si en menos,
   **empate** si en la mitad exacta; posición = **mediana** de sus puestos.
3. **Acuerdo** por asistente = casillas con el mismo resultado ÷ casillas comparables
   (válida en la app y con al menos un run válido en el probe). Un empate cuenta como
   acuerdo. SoV bruto del probe = runs con la clínica ÷ runs válidos `AV` del asistente.
4. **Veredicto**: "coinciden de forma razonable en AV: sí" solo si (a) la distancia es de 7
   días o menos, y en ChatGPT y en Gemini (b) hay al menos 12 casillas comparables, (c) el
   acuerdo es del 70 % o más (11 de 15) y (d) la diferencia de SoV bruto entre app y probe
   es de 20 pts o menos. Si falla una, "no". La posición se informa (parecida si difiere
   ± 2 puestos o menos), pero no decide. Se anotan los modelos de los dos lados y las
   diferencias conocidas: Vilaboa frente a Viveiro, modelo de la app frente al de la API,
   catálogo cerrado del probe.
5. **Si es "no"**: revisar, en este orden, la lectura de las casillas en desacuerdo, el
   protocolo manual, la configuración del probe y la diferencia de ubicación; anotar la
   causa y la decisión del humano para `AV` en el ledger. Hasta entonces no se enseña a la
   clínica ninguna cifra AV del probe y se revisa la frase "ya sois la clínica que la IA
   recomienda en A Mariña" de SPEC-009 antes de enviar la propuesta. Ninguna cifra manual
   entra en (D).

### 6-AR. Área de influencia: "sin discrepancia gruesa en AR" (veredicto débil)
1. **Emparejar**: el `results.csv` del "antes" de `AR` (SPEC-008 CA-12, 3 runs), no las
   filas AR del baseline oficial (1 run: no se pueden resumir). En el "después", la
   medición `AR` "después" más cercana, con sus 3 runs. Ventana máxima propia: **7 días**,
   comprobada aparte de la de `AV`.
2. **Casillas**: pregunta `AR` × asistente (5 × 2). Una casilla del probe es comparable solo
   con **2 runs válidos** o más y la app válida. Es **unánime** si la clínica sale en todos
   sus runs válidos o en ninguno, y **repartida** si no (1 de 3, 2 de 3, o empate con 2).
   Una repartida es **compatible** con cualquier respuesta de la app.
3. **Discrepancia gruesa**: casilla comparable y unánime (decisiva) que la app contradice:
   el probe la tiene en todos los runs y la app no, o en ninguno y la app sí.
4. **Veredicto**: "sin discrepancia gruesa en AR: sí" solo si (a) la distancia es de 7 días
   o menos, y en ChatGPT y en Gemini (b) hay al menos 4 casillas comparables (de 5), (c) al
   menos 3 casillas decisivas y (d) como mucho 1 discrepancia gruesa. Si falla una, "no".
   Es un **veredicto débil**: con 5 casillas no se puede afirmar que los instrumentos
   coinciden, solo descartar una contradicción clara. Nunca se rotula "coinciden".
5. **Recuentos, sin porcentajes**: "x de 5" respuestas de la app y "k de n" runs del probe
   por asistente, y los puestos de cada casilla como lista, en los dos lados. **No se usa el
   SoV** en el veredicto (con 5 respuestas es ruido). Diferencias conocidas: las preguntas
   se formulan desde Ferrolterra, Lugo o Asturias, la manual se hace desde Vilaboa y el
   probe envía Viveiro, al lado de la clínica: aquí la ubicación pesa más que en `AV`.
6. **Si es "no"**: el mismo orden de revisión de 6-AV, con la ubicación como primera causa
   candidata tras la lectura; anotar la causa y la decisión del humano para `AR` en el
   ledger. Hasta entonces no se enseña a la clínica ninguna cifra AR del probe y se revisa
   la frase del objetivo de SPEC-009 antes de enviar la propuesta. El cálculo de (C) no
   cambia (probe contra probe); el humano decide si (C) sigue tal cual o con la salvedad
   escrita. Un "sí" débil basta para contar el objetivo como objetivo, no como dato.

## 7. Resultado
`calibracion-antes.md` (o `calibracion-despues.md`) con las secciones 2 a 6 por nivel, las
dos ejecuciones emparejadas (fecha y carpeta), **dos veredictos separados** y lo que cada
uno sostiene en SPEC-009 (`AV` → frase "ya sois la clínica que la IA recomienda en A
Mariña"; `AR` → frase del objetivo). Con el script:

```
python docs/piloto-artica/tools/count_baseline.py ANTES.csv \
    --probe-av "$PUSHLLM_PRIVADO/piloto-artica/probe/results.csv" \
    --probe-ar "$PUSHLLM_PRIVADO/piloto-artica/probe-AR-antes/results.csv" \
    --aliases alias-canonicos.csv --out "$PUSHLLM_PRIVADO/piloto-artica/baseline/calibracion-antes.md"
```
