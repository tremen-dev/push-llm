# Kit de la reunión y propuesta del piloto (SPEC-009)

Plantillas **sin datos de la clínica** (ADR-004): ni cifras, ni hallazgos concretos, ni nombres de persona, ni emails o teléfonos salvo marcadores `{…}`. Lo rellenado (guion personalizado, hoja de hallazgo, propuesta con nombres y fechas, PDF, respuesta de la clínica, consentimientos, factura) vive solo en `$PUSHLLM_PRIVADO/piloto-artica/reunion/`.

| Fichero | Para qué | CA |
|---|---|---|
| `guion.md` | Guion literal de la reunión, 44 min, con 16 preguntas sobre hechos pasados | CA-1, CA-2 |
| `apoyo.md` | Objeciones con respuesta literal y frases para volver a hechos | CA-5 |
| `propuesta.md` | Propuesta de una página, precio de ADR-010 | CA-3 |
| `acuerdos.md` | Anexo 1: acuerdos para poder medir | CA-4 |
| `encargo-tratamiento.md` | Anexo 2: contrato de encargo del tratamiento (artículo 28 del RGPD) | CA-6 |

## Frontera
- **En el repo**: estas plantillas, las herramientas (`../tools/meeting_docs.py`, `../tools/build_pdf.mjs`) y el ledger de SPEC-009, este solo con veredictos y fechas.
- **En privado**: `valores.json` (los valores de los marcadores, con `_pendiente` y `_personas`), `guion-artica.md`, `apoyo-artica.md`, `hoja-hallazgo.md` y la carpeta `propuesta/` con lo generado.
- El texto fijo de la propuesta que cuenta el punto de partida ("ya sois la clínica que la IA recomienda en A Mariña") es un veredicto sin cifra que ya está en EPIC-002 y ADR-009, y lo permite ADR-004 §3. Cualquier matiz sobre la clínica va en el marcador `{matiz_punto_de_partida}`, en privado.

## Cómo generar la propuesta en PDF
Con el diseño de `design/tremen-ds` (`doc.css`, cuerpo `.v-papel`, portada `.v-tremendo`), como la propuesta de Recepción digital. Necesita conexión (fuentes y Paged.js desde CDN) y Playwright o Chrome.

```
python docs/piloto-artica/tools/meeting_docs.py build \
  --valores "$PUSHLLM_PRIVADO/piloto-artica/reunion/valores.json" \
  --salida  "$PUSHLLM_PRIVADO/piloto-artica/reunion/propuesta" [--borrador]
node docs/piloto-artica/tools/build_pdf.mjs \
  "$PUSHLLM_PRIVADO/piloto-artica/reunion/propuesta/propuesta.html" \
  "$PUSHLLM_PRIVADO/piloto-artica/reunion/propuesta/propuesta.pdf"
```

Sin `--borrador`, el generador se niega si queda algún valor en `_pendiente` o algún marcador sin rellenar. Los dos comandos se niegan a escribir dentro del repo.

## Comprobaciones
```
python docs/piloto-artica/tools/meeting_docs.py check                     # plantillas del repo
python docs/piloto-artica/tools/meeting_docs.py check --solo --privado F  # copias privadas
python -m pytest -q docs/piloto-artica/tools/tests/test_meeting_kit.py
```
