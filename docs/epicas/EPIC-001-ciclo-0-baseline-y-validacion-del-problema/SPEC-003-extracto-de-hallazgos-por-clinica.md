---
id: SPEC-003
tipo: spec
epica: EPIC-001
estado: borrador
aprobada-por:
historial:
  - {estado: borrador, fecha: 2026-09-23, por: sdd-arquitecto}
---
# SPEC-003 — Extracto de hallazgos por clínica

> Trabajo de **agente**: requiere **código nuevo en `probe/`** (un generador de
> extractos que lee el fichero de resultados de SPEC-001/002). No es código de
> producto ni toca `src/`. Las salidas viven en el espacio privado (ADR-001).

## Problema
El enfoque *datos primero* de EPIC-001 abre cada conversación con un hallazgo
medido sobre la clínica del interlocutor ("he medido qué clínicas recomienda
ChatGPT en Vigo; esto es lo que sale de la vuestra"). Un fundador no comercial
no puede improvisar ese hallazgo a partir de un CSV de 396 filas: necesita, por
clínica objetivo, (a) una o dos frases literales para el primer mensaje y (b) media
página para enseñar en la entrevista. Sin generador, cada extracto es trabajo
manual propenso a errores y a afirmaciones no respaldadas por el dato.

## Usuarios / roles afectados
- Humano: pega la frase en el mensaje (SPEC-004) y enseña la media página en la
  entrevista.
- Interlocutor (dirección de clínica o agencia): lee el extracto.
- Agente: implementa y genera. sdd-verificador: contrasta cifras con el CSV.
- Consultadas: `sdd-metricas` (cifras), `sdd-sanidad-regulacion` (texto, vía el
  dictamen de SPEC-004 CA-9).

## Criterios de aceptación
- **CA-1 (generador offline)**: Dado un fichero de resultados y `brands.csv`, cuando
  se invoque el generador con una o varias clínicas (por nombre de `brands.csv`),
  entonces produce un extracto por clínica sin llamar a ningún proveedor, usando las
  mismas funciones de matching y análisis de SPEC-001 (sin duplicar lógica).
  *Evidencia*: test con fixture; adaptadores de proveedor que lanzan si se invocan;
  revisión de que no hay una segunda implementación de matching.
- **CA-2 (clínica desconocida)**: Dada una clínica que no está en `brands.csv`, cuando
  se pida su extracto, entonces el generador falla con un mensaje claro y no produce
  un extracto con "0 menciones". *Evidencia*: test.
- **CA-3 (contenido)**: Dada una clínica de una especialidad sondeada, cuando se
  genere su extracto, entonces contiene, solo con prompts de su especialidad y su
  ciudad (y los de la otra ciudad si no hay de la suya, indicándolo): fecha de la
  medición; por proveedor, en cuántas de N respuestas válidas aparece la clínica
  (RN-01/RN-02) y su position media (RN-06) si aparece; la cifra ponderada (RN-03,
  RN-04); las hasta 3 clínicas que más aparecen en su lugar con su recuento; hasta 5
  dominios más citados en esas respuestas, si hay URLs; una cita literal breve
  (≤ 40 palabras) de una respuesta real, con proveedor y pregunta; y una nota de
  método de ≤ 3 líneas (API con búsqueda web y ubicación Vigo, 3 repeticiones,
  aproxima pero no replica la app). *Evidencia*: test con fixture que comprueba cada
  elemento y cada cifra contra valores calculados a mano.
- **CA-4 (frase gancho)**: Dado el mismo cálculo, cuando se genere el extracto,
  entonces incluye además un texto de 1–2 frases, ≤ 45 palabras, en castellano, listo
  para pegar en el primer mensaje, que cita una pregunta real de paciente y una cifra
  del extracto (p. ej. "De 9 respuestas de ChatGPT a '¿Cuál es la mejor clínica dental
  de Vigo para implantes?', vuestra clínica aparece en 0; aparecen otras 3"), sin
  adjetivos valorativos sobre competidores. *Evidencia*: test de longitud y de que la
  cifra citada coincide con el extracto; revisión contra la lista de CA-6.
- **CA-5 (formato)**: Dado un extracto generado, cuando se abra, entonces existe en
  Markdown y en un HTML autocontenido (sin recursos externos) que al imprimirse ocupa
  **una sola página A4**. *Evidencia*: impresión a PDF con navegador sin cabeza
  (Playwright/Chrome) y conteo de páginas = 1 para las clínicas de la fixture y para
  el caso más largo de la ejecución real.
- **CA-6 (sin promesas ni descalificaciones)**: Dado el No-negociable "no se promete
  posicionamiento garantizado" y el riesgo sanitario-publicitario, cuando se genere
  cualquier extracto, entonces el texto fijo de la plantilla no contiene promesas de
  resultado ni plazos ("garantizamos", "en X días", "primera posición"), ni
  valoraciones de la calidad clínica de nadie, ni referencia a producto o precio.
  *Evidencia*: test con lista de términos prohibidos sobre la plantilla y la salida;
  la plantilla forma parte del material revisado en el dictamen de SPEC-004 CA-9.
- **CA-7 (variante agencia)**: Dada una especialidad, cuando se pida el panorama para
  una agencia, entonces se genera una media página por especialidad con: % de
  respuestas que nombran clínica local por proveedor, las clínicas más nombradas y
  las fuentes más citadas, con las mismas reglas de CA-3 a CA-6. *Evidencia*: test con
  fixture.
- **CA-8 (salida privada)**: Dado ADR-001, cuando se generen extractos, entonces se
  escriben en el directorio de salida privado o en el directorio por defecto
  ignorado, y `git ls-files` no lista ninguno. *Evidencia*: test de ruta +
  `git ls-files` en el ledger.
- **CA-9 (extractos reales revisados)**: Dada la ejecución completa de SPEC-002,
  cuando se generen los extractos de la primera tanda de objetivos (SPEC-004 CA-1), el
  humano revisa al menos 3 (uno dental, uno de estética o fertilidad/oftalmología, uno
  de agencia) y confirma en el ledger que entiende cada cifra sin ayuda y que la cita
  literal no contiene afirmaciones médicas que no quiera enseñar. *Evidencia*:
  registro con fecha en el ledger. **Acción humana.**

## Entidades y reglas afectadas
- Dominio: Clinic, Speciality, Prompt, Provider, Mention, Position, Share of voice,
  Weighted SoV, Source.
- RN-01, RN-02, RN-03, RN-04, RN-06.
- D-3 (se habla de pacientes que preguntan, no de "visibilidad en IA"), D-8
  (material para clientes en castellano/gallego).
- ADR-001. Depende de SPEC-001 (formato y análisis) y de SPEC-002 (datos reales, para CA-9).

## Fuera de alcance
- El informe de visibilidad completo y con marca (Ciclo 1).
- Recomendaciones de acciones o gaps (Gap, Action): el extracto enseña, no aconseja.
- Clasificación de fuentes por tipo, PresenceCheck.
- Versión en gallego (pendiente de decisión humana, ver notas).
- Hospitales (fase 2, D-2).

## Notas para el gate humano
- **Código nuevo en `probe/`**: un generador de extractos. Es la única spec, junto con
  SPEC-001, que toca código.
- Los extractos **nombran competidores** ante el interlocutor. Es el núcleo del gancho,
  pero entra en el dictamen de `sdd-sanidad-regulacion` (SPEC-004 CA-9); si el dictamen
  lo restringe, CA-3/CA-4 se reescriben antes de implementar.
- `brands.csv` no contiene todas las clínicas de la lista de objetivos de
  `03-…md` §4 (falta, al menos, **HL Dental**). CA-2 impide generar un extracto falso
  con 0 menciones; SPEC-004 CA-1 obliga a darlas de alta antes. Una clínica añadida
  tras la ejecución se recuenta offline sin coste (SPEC-001 CA-5).
- ¿Hace falta versión en gallego del extracto? D-8 dice "gallego/castellano" para
  material de cliente; propongo solo castellano en Ciclo 0.
- **F-SPEC-001-2** (destino esta spec, decidido al refinar SPEC-002 el 2026-09-24): las URLs
  citadas por Gemini (`grounding_chunks[].web.uri`) son redirecciones
  `vertexaisearch.cloud.google.com`; si un extracto muestra fuentes citadas, hay que resolverlas
  a la URL final o marcarlas como no resueltas. Incorporarlo como CA al refinar esta spec.
- Depende de: SPEC-001 (duro), SPEC-002 (para CA-9). Bloquea: SPEC-004 CA-10 (envío).
