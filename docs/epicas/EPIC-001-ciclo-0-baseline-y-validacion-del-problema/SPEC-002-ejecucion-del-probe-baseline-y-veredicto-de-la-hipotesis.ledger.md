---
id: SPEC-002
tipo: ledger
epica: EPIC-001
---
# Ledger — SPEC-002 Ejecución del probe baseline y veredicto de la hipótesis

## Resumen
- Fase: <!-- refleja el estado de la spec; la fuente de verdad es el frontmatter de la spec -->
- Rama: `ft/SPEC-002-ejecucion-del-probe-baseline-y-veredicto-de-la-hipotesis`

## Matriz de criterios de aceptación
<!-- Escritores: sdd-implementador rellena Implementado y Test; sdd-verificador rellena Verif. y Estado. Nunca al revés. -->
<!-- Estados por CA: ✅ cerrado · ⚠️ parcial/con salvedad · 🚧 en curso · ❌ sin empezar · n-a -->
<!-- Un CA está ✅ solo cuando Implementado + Test + Verif. aplicables están en verde. Una salvedad se marca ⚠️, nunca ✅. -->
| CA | Implementado (fichero) | Test (fichero/caso) | Verif. | Estado |
|---|---|---|---|---|
| CA-1 | | | | ❌ |
| CA-2 | | | | ❌ |
| CA-3 | | | | ❌ |
| CA-4 | | | | ❌ |
| CA-5 | | | | ❌ |
| CA-6 | | | | ❌ |
| CA-7 | | | | ❌ |
| CA-8 | | | | ❌ |
| CA-9 | | | | ❌ |
| CA-10 | | | | ❌ |

## Veredicto del verificador
<!-- GREEN/RED + fecha + resumen. Lo escribe SOLO sdd-verificador. -->

## Evidencia visual
<!-- Tabla CA → captura en _qa/SPEC-002/. Informe HTML opcional: _qa/SPEC-002/informe.html -->

## Salvedades / follow-ups
<!-- IDs F-SPEC-002-1, F-SPEC-002-2… con destino (spec futura o EPIC-MEJORA). -->
- **F-SPEC-002-1** (2026-09-29, enmienda de CA-1 / ADR-006; → sdd-implementador, tras la
  re-aprobación): (a) actualizar `probe/README.md` ("Keys and output directory"), que hoy
  dice "never in a file inside the repo", para documentar el `.env` en la raíz del árbol de
  trabajo local, ignorado por git, como alternativa a `Read-Host`, con las comprobaciones de
  CA-1 (a)–(d) y el fragmento de carga en PowerShell que se ejecuta desde `probe/`
  (`Get-Content ..\.env | ForEach-Object { if ($_ -match '^\s*([A-Z_]+)\s*=\s*(.+?)\s*$') { Set-Item "env:$($Matches[1])" $Matches[2] } }`);
  (b) actualizar `docs/ciclo-0/guia-claves-api.md`, sección "Custodia de las claves", que
  hoy dice "no se escriben en ningún sitio": `.env` local ignorado + nota segura en el gestor
  de contraseñas para el traslado; nunca email, mensajería ni nube sin cifrar; revocar si se
  filtra (ADR-006 §4–§6); (c) valorar si `run_probe.py` carga `.env` por sí mismo (parser
  mínimo `NOMBRE=valor`, sin dependencias nuevas, sin sobrescribir variables ya definidas en
  el entorno, sin registrar valores en logs ni en `summary.md`, con test offline). Si se
  hace, se documenta en (a) y el fragmento de PowerShell pasa a ser opcional.
- **F-SPEC-002-2** (2026-09-29; → sdd-implementador de SPEC-008): SPEC-008 no duplica la
  restricción (su CA-7 remite a SPEC-002 CA-1, que ahora admite el `.env`), así que la spec
  no se enmienda. Pero las "Instrucciones para el humano (CA-7)" de su ledger solo muestran
  `Read-Host`: añadir la alternativa de cargar el `.env` de la raíz (mismo fragmento que
  F-SPEC-002-1 (a)) y citar ADR-006.
- **F-SPEC-002-3** (2026-09-29; → humano): negar a los agentes la lectura de `.env` en la
  configuración local de permisos (ADR-006, consecuencias). Fuera del alcance de los roles.

## Cómo retomar (handoff)
<!-- Estado real del trabajo para la siguiente sesión: qué está hecho, qué falta, dónde seguir. -->
- **2026-09-29 (sdd-arquitecto)**: spec en `borrador` por la enmienda de CA-1 y P-2 (claves
  en `.env` local ignorado, ADR-006 en `borrador`). Necesita re-aprobación humana de la spec
  y aprobación de ADR-006. Después: F-SPEC-002-1 y F-SPEC-002-2.
