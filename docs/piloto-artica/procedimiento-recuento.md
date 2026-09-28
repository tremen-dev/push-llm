# Procedimiento de recuento — baseline manual del piloto Clínica Ártica

> SPEC-007 CA-7. Aplica las reglas del dictamen de `sdd-metricas` que consta en el ledger de
> SPEC-007 (CA-2). Está escrito para hacerse a mano o con una hoja de cálculo desde los
> CSV de las pasadas; `tools/count_baseline.py` hace lo mismo y sirve para comprobarlo.
> Entradas y resultado viven en `$PUSHLLM_PRIVADO/piloto-artica/baseline/` (ADR-004): el
> recuento **nunca** se guarda en el repo.

## 0. Preparar
1. Junta en una hoja las filas de los CSV de la pasada 1 y de la pasada 2.
2. Comprueba que no hay filas repetidas (misma `pasada`, `id_pregunta`, `app` y
   `plan_cuenta`) y que toda fila con `respuesta_valida` = `si` tiene `artica_nombrada`
   = `si` o `no`.
3. Rellena, leyendo las capturas, `clinicas_nombradas`, `artica_nombrada`,
   `posicion_artica` y `dominios_citados` con las reglas de mención del dictamen:
   - cuenta como mención el nombre de la clínica o un alias de 4 o más caracteres en el
     texto de la respuesta (RN-01), sin mirar tildes ni mayúsculas;
   - una ficha de fuente o un enlace que solo muestra el dominio no es mención: va a
     `dominios_citados`;
   - un uso de "ártica" como adjetivo que no se refiere a la clínica cuenta igualmente
     (RN-01 literal) pero se marca `#artica-adjetivo` en `observaciones`;
   - el nombre de la médica titular sin el de la clínica no es mención: se marca
     `#medica-sin-clinica` en `observaciones` y se informa aparte;
   - la posición es el puesto de la clínica entre las clínicas o médicos nombrados, sin
     contar directorios (RN-06).
4. Si una misma clínica aparece escrita de varias formas, crea `alias-canonicos.csv`
   (columnas `alias,canonico`) y usa siempre el nombre canónico.

## 1. Filtrar
- **Cuenta** para las cifras principales: preguntas `AV`, `app` = `chatgpt`, `gemini` o
  `google`, `plan_cuenta` = `gratuito` o `sin_sesion`.
- **No cuenta** (se informa aparte, como observación): cuentas de pago, Claude y
  cualquier otra app.
- **Preguntas de marca** (`AM`): nunca en el SoV; se leen aparte.
- **Respuestas válidas**: `respuesta_valida` = `si`. Las demás se cuentan como excluidas.

## 2. Por app (ChatGPT y Gemini)
- Válidas = filas válidas de la app (las dos pasadas juntas).
- SoV bruto (RN-02) = filas con `artica_nombrada` = `si` ÷ válidas. También por pasada.
- Posición media (RN-06) = media de `posicion_artica` en las filas donde sale.
- En su lugar = en las filas válidas sin la clínica, cuántas respuestas nombran a cada
  otra clínica (nombre canónico), de más a menos.

## 3. SoV ponderado (RN-03, RN-04)
Pesos 0,55 (ChatGPT) y 0,25 (Gemini), normalizados a las apps con alguna respuesta válida:
ponderado = (SoV ChatGPT × 0,55 + SoV Gemini × 0,25) ÷ 0,80. Si una app no tiene
respuestas válidas, el ponderado es el SoV de la otra.

## 4. Google, resumen de IA (canal aparte, sin ponderar)
- Búsquedas válidas, cuántas tuvieron resumen de IA (`resumen_ia` = `si`) y en cuántas
  sale la clínica dentro del resumen.
- Dos cifras: sobre todas las búsquedas válidas y sobre las que tuvieron resumen.

## 5. Dominios más citados
Cuenta, en las filas válidas que cuentan (las tres apps), en cuántas filas aparece cada
dominio de `dominios_citados` (sin `www.`), de más a menos.

## 6. Estabilidad por pregunta
Para cada app y pregunta `AV`: en cuántas pasadas sale la clínica de cuántas válidas
("0 de 2", "1 de 2", "2 de 2"). Sirve para leer el ruido (dictamen de CA-2, punto f).

## 7. Preguntas de marca
Por cada fila `AM`: qué dice el asistente de la clínica (dirección, servicios, precios) y
si es correcto frente a la web de la clínica y la foto técnica.

## 8. Resultado
`recuento-antes.md` con las secciones 2 a 7, fecha y ficheros usados. Con el script:

```
python docs/piloto-artica/tools/count_baseline.py P1.csv P2.csv \
    --aliases alias-canonicos.csv --out "$PUSHLLM_PRIVADO/piloto-artica/baseline/recuento-antes.md"
```
