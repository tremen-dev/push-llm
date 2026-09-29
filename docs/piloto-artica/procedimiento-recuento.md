# Procedimiento de recuento — calibración manual del piloto Clínica Ártica

> SPEC-007 CA-7. Aplica el dictamen de `sdd-metricas` del ledger de SPEC-007 (CA-2, puntos
> (a), (c), (e) y la segunda ampliación (k)–(n)). Está escrito para hacerse a mano o con
> una hoja de cálculo desde el CSV de **una sola pasada** (`antes` o `despues`) y el
> `results.csv` del probe emparejado; `tools/count_baseline.py` hace lo mismo y sirve para
> comprobarlo. Entradas y resultado viven en `$PUSHLLM_PRIVADO/piloto-artica/baseline/`
> (ADR-004): nunca en el repo. Es calibración: **no entra en el criterio Go**, que se
> calcula probe contra probe (SPEC-008 CA-7 y CA-9).

## 0. Preparar
1. Abre el CSV de la pasada. Comprueba que todas las filas tienen la misma `pasada`, que no
   hay filas repetidas (misma `id_pregunta`, `app`, `plan_cuenta` y `municipio`) y que toda
   fila con `respuesta_valida` = `si` tiene `artica_nombrada` = `si` o `no`.
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
3. Si una misma clínica aparece escrita de varias formas, crea `alias-canonicos.csv`
   (columnas `alias,canonico`) y usa siempre el nombre canónico.

## 1. Filtrar
- **Cuenta**: preguntas `AV`, `app` = `chatgpt`, `gemini` o `google`, `plan_cuenta` =
  `gratuito` o `sin_sesion`, `municipio` = `Vilaboa`.
- **No cuenta** (observación aparte): cuentas de pago, Claude, cualquier otra app y las
  filas desde otro municipio (observación de sensibilidad a la ubicación).
- **Preguntas de marca** (`AM`): nunca en ninguna cifra; se leen aparte (§5).
- Filas `AR` o `AG`: no se preguntan a mano; si aparecen, se ignoran.
- **Respuestas válidas**: `respuesta_valida` = `si`. Las demás se cuentan como excluidas.

## 2. Lo que ve el paciente, por app (ChatGPT y Gemini)
- Válidas y excluidas.
- SoV bruto (RN-02) = filas con la clínica ÷ válidas, dado también como "x de n".
- Posición media (RN-06) = media de `posicion_artica` donde sale.
- En su lugar = en las válidas sin la clínica, cuántas respuestas nombran a cada otra
  clínica (nombre canónico), de más a menos.
- **No se calcula SoV ponderado** con la manual (dictamen (n)).

## 3. Google, resumen de IA (canal aparte, fuera del acuerdo y del Go)
- Recuentos "x de n", **sin porcentajes**: búsquedas válidas; cuántas con resumen de IA
  (`resumen_ia` = `si`); en cuántas sale la clínica dentro del resumen, sobre las válidas y
  sobre las que tuvieron resumen. Sin resumen: búsqueda válida y sin la clínica.
- Antes/después (SPEC-012): "x de n → y de n", con las búsquedas con resumen de cada
  pasada. Solo es **cambio claro** con una diferencia de 5 búsquedas o más con la clínica;
  si no, "dentro de lo que varía de un día a otro".

## 4. Dominios más citados
En las filas válidas que cuentan (las tres apps), en cuántas filas aparece cada dominio de
`dominios_citados` (sin `www.`), de más a menos.

## 5. Preguntas de marca
Por cada fila `AM`: qué dice el asistente de la clínica (dirección, servicios, precios) y
si es correcto frente a su web y la foto técnica.

## 6. Comparación app frente a probe
1. **Emparejar**: el `results.csv` del lote Viveiro de la ejecución `AV` del probe
   emparejada (en el "antes", el baseline oficial de SPEC-008 CA-7). Debe tener la columna
   `searched_urls` (posterior a SPEC-013); si no la tiene, no sirve. Distancia = días entre
   las fechas de sus filas `AV` (`timestamp_utc`) y las de la pasada; 0 si se solapan.
   Ventana máxima: **7 días**.
2. **Casillas**: pregunta `AV` × asistente, con ChatGPT = proveedor `openai` y Gemini =
   `gemini` (15 × 2). En el probe, solo filas con `status` = `ok`. En cada run, la clínica
   sale si su nombre está en `brands_mentioned`, y su puesto es el orden en esa lista. Por
   casilla: "k de n" runs con la clínica; **sale** si está en más de la mitad de los runs,
   **no sale** si en menos, **empate** si en la mitad exacta; posición = **mediana** de sus
   puestos.
3. **Acuerdo** por asistente = casillas con el mismo resultado ÷ casillas comparables
   (válida en la app y con al menos un run válido en el probe). Un empate cuenta como
   acuerdo. SoV bruto del probe = runs con la clínica ÷ runs válidos `AV` del asistente.
4. **Veredicto**: "coinciden de forma razonable: sí" solo si (a) la distancia es de 7 días
   o menos, y en ChatGPT y en Gemini (b) hay al menos 12 casillas comparables, (c) el
   acuerdo es del 70 % o más (11 de 15) y (d) la diferencia de SoV bruto entre app y probe
   es de 20 pts o menos. Si falla una, "no". La posición se informa (parecida si difiere
   ± 2 puestos o menos), pero no decide. Se anotan los modelos de los dos lados y las
   diferencias conocidas: Vilaboa frente a Viveiro, modelo de la app frente al de la API,
   catálogo cerrado del probe.
5. **Si es "no"**: revisar, en este orden, la lectura de las casillas en desacuerdo, el
   protocolo manual, la configuración del probe y la diferencia de ubicación; anotar la
   causa y la decisión del humano en el ledger. Hasta entonces no se enseña a la clínica
   ninguna cifra del probe ni se envía la propuesta (SPEC-009). Si se repite la pasada, el
   informe da las dos.

## 7. Resultado
`calibracion-antes.md` (o `calibracion-despues.md`) con las secciones 2 a 6, fechas y
ficheros usados. Con el script:

```
python docs/piloto-artica/tools/count_baseline.py ANTES.csv --probe results.csv \
    --aliases alias-canonicos.csv --out "$PUSHLLM_PRIVADO/piloto-artica/baseline/calibracion-antes.md"
```
