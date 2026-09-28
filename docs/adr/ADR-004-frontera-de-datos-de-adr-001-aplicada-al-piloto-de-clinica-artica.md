---
id: ADR-004
tipo: adr
estado: aprobada
historial:
  - {estado: borrador, fecha: 2026-09-28, por: sdd-arquitecto}
  - {estado: aprobada, fecha: 2026-09-28, por: Alberto Fojo}
aprobada-por: Alberto Fojo
---
# ADR-004: Frontera de datos de ADR-001 aplicada al piloto de Clínica Ártica

- Deciders: propone sdd-arquitecto (2026-09-28, desglose de EPIC-002). Aprueba: humano
  (pendiente). Recoge dos decisiones ya tomadas por el humano el 2026-09-28: la clínica ha
  autorizado aparecer con su nombre real en el repo público, y cifras, capturas, analítica,
  Search Console y cualquier dato de pacientes van a `PUSHLLM_PRIVADO`. Pendiente el
  dictamen de `sdd-sanidad-regulacion` de SPEC-009 CA-6, que puede endurecer, pero no
  relajar, esta frontera.
- Specs relacionadas: SPEC-007 a SPEC-012 (EPIC-002). Amplía ADR-001 (no lo supersede).

## Contexto
ADR-001 define el espacio privado (`PUSHLLM_PRIVADO`, fuera del árbol del repo) y la regla
de paso para el **Ciclo 0**, con dos reglas que aquí chocan con la realidad del piloto:
(a) "sin cifras por clínica nombrada" pensando en clínicas que no saben que se las mide;
(b) ejemplos del kit "con una clínica ficticia". En el piloto la clínica es **cliente** y
ha consentido aparecer con su nombre. Además aparecen clases de datos que ADR-001 no
contemplaba: datos de la analítica y de Search Console de la clínica, conteos de la
pregunta "¿cómo nos conociste?", la propuesta económica y el pago, y credenciales de
acceso a sus herramientas.

## Decisión
ADR-001 se aplica a EPIC-002 con estas precisiones:

1. **Nombre de la clínica en el repo público: sí.** "Clínica Ártica", su web y su
   localidad pueden aparecer en specs, catálogos (`probe/prompts.csv`, `probe/brands.csv`),
   plantillas y documentos del piloto. El consentimiento (fecha, quién lo dio en la
   clínica, canal y alcance) se guarda en el espacio privado y se cita en el ledger de
   SPEC-009 por fecha, sin el nombre de la persona.
2. **Cifras, en privado, aunque haya consentimiento.** Van solo a `PUSHLLM_PRIVADO`:
   respuestas en bruto y capturas (manuales o del probe), SoV, posiciones y cualquier cifra
   por clínica (cliente o competidor); datos de la analítica y de Search Console; conteos
   de la pregunta de recepción; propuesta firmada, factura e importes cobrados; notas de
   reunión; datos de personas de la clínica.
3. **Qué puede publicar el repo sobre el piloto**: método, plantillas vacías, catálogo de
   prompts y de marcas, lista de acciones (qué se hizo y cuándo, sin cifras de efecto) y
   el veredicto H1/H3 como **cumple / no cumple** frente al umbral, sin cifras. Los
   competidores se nombran solo en `brands.csv` y nunca junto a una cifra o valoración.
4. **Pacientes**: no se recibe, copia ni guarda ningún dato personal de pacientes (RN-09).
   La clínica entrega solo conteos agregados por semana y señal. Si un fichero que llega de
   la clínica contiene datos de pacientes, se borra y se pide de nuevo agregado; el
   incidente se anota en el ledger sin el dato.
5. **Accesos**: el acceso a analítica y Search Console es con usuario propio del fundador
   y el **mínimo rol de lectura** que permita la tarea (lectura salvo que la instalación
   de SPEC-010 requiera más, y en ese caso se revoca al terminar). Ninguna credencial,
   token ni ID de propiedad va al repo.
6. **Revocación**: si la clínica retira el consentimiento, su nombre deja de aparecer en
   documentos nuevos y se sustituye por "clínica piloto" en los vigentes. El historial de
   git no se reescribe; esto se le explica a la clínica **antes** de publicar nada con su
   nombre (SPEC-009).
7. **Regla de paso**: se mantiene la comprobación de ADR-001 (sin emails, teléfonos ni
   nombres de persona; sin cifras junto a nombres de `brands.csv`), aplicada también a todo
   documento de `docs/piloto-artica/`.

## Consecuencias
### Positivas
- El método del piloto queda público y auditable con el caso real, que es lo que
  interesa a futuros clientes y agencias.
- Un verificador puede comprobar la frontera con `git ls-files` y búsquedas por patrón.

### Negativas / follow-ups
- Los informes quincenales a la clínica (con cifras) viven fuera del repo: el histórico
  del piloto depende del respaldo del espacio privado (follow-up ya abierto en ADR-001).
- El veredicto público sin cifras es menos persuasivo como caso de éxito; publicarlo con
  cifras exigiría otro consentimiento explícito y otro ADR.
- El historial de git conserva el nombre aunque se revoque el consentimiento.

## Alternativas consideradas
- **Seudonimizar a la clínica en el repo ("clínica piloto")**: rechazada; el humano ya
  decidió con la clínica aparecer con su nombre, y seudonimizar un catálogo de marcas
  rompe el matching del probe.
- **Publicar cifras de la clínica con su consentimiento**: rechazada; el humano decidió que
  las cifras van a privado y además arrastraría cifras de competidores por comparación.
- **Superseder ADR-001 con un ADR nuevo general para todos los ciclos**: rechazada por
  ahora; con un solo piloto no hay patrón que generalizar. Se reevalúa en Ciclo 1/3.

<!-- REGLA: un ADR aceptado es INMUTABLE. Para cambiar la decisión, escribe otro ADR que lo supersede (estado del viejo -> bloqueada + nota "superseded por ADR-NNN"). -->
