---
id: ADR-001
tipo: adr
estado: aprobada
historial:
  - {estado: borrador, fecha: 2026-09-23, por: sdd-arquitecto}
  - {estado: aprobada, fecha: 2026-09-23, por: Alberto Fojo}
aprobada-por: Alberto Fojo
---
# ADR-001: Frontera de datos del Ciclo 0 entre el repo público y el espacio privado

- Deciders: propone sdd-arquitecto (2026-09-23, desglose de EPIC-001). Aprueba: humano (pendiente). Pendiente también el dictamen de `sdd-sanidad-regulacion` sobre plazos de conservación y tratamiento de datos de contacto (SPEC-004 CA-9), que puede endurecer, pero no relajar, esta frontera.
- Specs relacionadas: SPEC-001, SPEC-002, SPEC-003, SPEC-004, SPEC-005 (EPIC-001).

## Contexto
El repositorio `github.com/tremen-dev/push-llm` es **público**. El Ciclo 0 genera
cuatro clases de datos con sensibilidad muy distinta:

1. Respuestas en bruto de los proveedores (texto de terceros que nombra y valora
   clínicas reales, a veces con afirmaciones erróneas).
2. Cifras por clínica (menciones, posición, quién aparece en su lugar): inteligencia
   de negocio que además, publicada, podría leerse como una valoración pública de
   clínicas concretas.
3. Datos personales de interlocutores (nombre, cargo, email, LinkedIn, notas de lo
   que dijeron, gasto de su clínica).
4. Material genérico (scripts, plantillas, guion, criterios, agregados).

Hoy solo existe una protección parcial: `.gitignore` excluye `probe/results.csv` y
`probe/summary.md`. No hay regla escrita sobre extractos, notas ni agregados.
FOUNDATION (No-negociables) exige RGPD estricto; RN-09 lo fija para pacientes,
pero no cubre interlocutores B2B.

## Decisión
Se definen dos espacios y una regla de paso entre ellos.

**Espacio privado** = un directorio **fuera del árbol de trabajo del repo**, cuya
ruta fija el humano y se referencia en scripts y documentos solo mediante la
variable de entorno `PUSHLLM_PRIVADO` (nunca una ruta literal con nombre de
persona en el repo). Vive ahí, y solo ahí:
- salidas en bruto y copias de trabajo del probe (`results.csv`, `summary.md`,
  ficheros de humo), extractos por clínica generados (SPEC-003);
- lista de contactos con personas (nombres, emails, perfiles), registro de envíos
  y respuestas;
- notas de entrevista nominales, la tabla que asocia pseudónimo ↔ clínica/persona,
  y la hoja de puntuación con identidad;
- el detalle del contraste manual en app real con nombres de clínicas.

Como segunda red, cualquier directorio de salida por defecto que los scripts
creen dentro del repo (p. ej. `probe/out/`) figura en `.gitignore`.

**Repo público** recibe solo:
- scripts, tests, configuración y catálogos (`probe/*.py`, `prompts.csv`,
  `brands.csv`, configuración de modelos y precios);
- plantillas y material genérico del kit (sin datos de ninguna persona; los
  ejemplos usan una clínica ficticia);
- la lista de objetivos **a nivel de clínica** (nombre comercial, especialidad,
  ciudad, web pública, motivo, prioridad), que ya es información pública de
  empresa presente en `03-local-market-vigo-pontevedra.md`, sin personas;
- agregados del probe **por especialidad × proveedor** y el veredicto de la
  hipótesis, **sin cifras por clínica nombrada** (la clínica líder de una
  especialidad se cita como "clínica A");
- el agregado anonimizado de entrevistas: pseudónimos `E01…E10`, segmento de
  grano grueso, puntuaciones, rangos de gasto en tramos, patrones parafraseados;
  sin citas atribuidas a un segmento de menos de 3 entrevistas.

**Regla de paso**: nada cruza del espacio privado al repo salvo un agregado
producido según las reglas anteriores, y todo documento del Ciclo 0 que entre
al repo pasa antes una comprobación automática (sin emails, teléfonos ni nombres
de persona de la lista de contactos; sin cifras junto a nombres de `brands.csv`).

## Consecuencias
### Positivas
- Se puede publicar el método y el veredicto sin exponer a clínicas ni personas.
- El verificador puede comprobar la frontera con `git ls-files` y búsquedas
  por patrón, sin juicio subjetivo.
- Las respuestas en bruto se conservan (No-negociable de FOUNDATION), solo que
  fuera del repo.

### Negativas / follow-ups
- El espacio privado no tiene historial ni copia de seguridad por defecto: el
  humano debe decidir dónde vive (disco local cifrado, nube privada) y su
  respaldo. Follow-up para SPEC-002.
- Un agente que lea el espacio privado envía su contenido al proveedor del
  agente. Si el dictamen de `sdd-sanidad-regulacion` lo restringe para notas
  con datos personales, la anonimización de notas la hace el humano.
- Las cifras por clínica no quedan versionadas: si se quiere comparar Ciclo 0
  con Ciclo 1/2 hará falta conservar los CSV privados con su fecha.

## Alternativas consideradas
- **Repo privado aparte para los datos**: rechazada por ahora; añade infraestructura
  (otro repo, permisos) para un ciclo de dos semanas y sigue sin resolver
  que las notas nominales no deberían versionarse indefinidamente. Reabrible
  en el Ciclo 1 si el volumen de datos crece.
- **Publicar cifras por clínica en el repo** (como ya hace el desk research de
  `03-…md` con afirmaciones cualitativas): rechazada; es inteligencia comercial
  que regala la lista de objetivos y el hallazgo a cualquiera, y publicar "ChatGPT
  no te recomienda" sobre una clínica con nombre es arriesgado sin el dictamen.
- **Confiar solo en `.gitignore` dentro del repo**: rechazada como única medida;
  un `git add -f` o un fichero renombrado basta para filtrar datos. Se mantiene
  como segunda red.

<!-- REGLA: un ADR aceptado es INMUTABLE. Para cambiar la decisión, escribe otro ADR que lo supersede (estado del viejo -> bloqueada + nota "superseded por ADR-NNN"). -->
