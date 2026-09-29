---
id: ADR-006
tipo: adr
estado: aprobada
historial:
  - {estado: borrador, fecha: 2026-09-29, por: sdd-arquitecto}
  - {estado: aprobada, fecha: 2026-09-29, por: Alberto Fojo}
aprobada-por: Alberto Fojo
---
# ADR-006: Claves de API en un .env local ignorado por git

- Deciders: propone sdd-arquitecto (2026-09-29), a raíz de la decisión del humano (Alberto
  Fojo, 2026-09-29) de guardar las claves de API en un `.env` en la raíz de su copia local
  del repo, ignorado por git, para poder cambiar de máquina llevando solo ese fichero.
  Aprueba: humano (pendiente). Este ADR no decide *si* se usa el `.env` (eso lo decidió el
  humano); fija **las condiciones** con las que encaja en la frontera de ADR-001 y ADR-004.
- Specs relacionadas: SPEC-002 (CA-1, enmendada el 2026-09-29), SPEC-008 (CA-7, que usa
  las claves de SPEC-002 CA-1); cualquier ejecución futura del probe.
- **Amplía ADR-001 y ADR-004 §5 (no los supersede)**, con el mismo patrón que ADR-004
  respecto a ADR-001. El resto de ambos sigue vigente sin cambios.

## Contexto
Hasta hoy la custodia de las claves de API (Anthropic, OpenAI, Gemini) no estaba en ningún
ADR: vivía en SPEC-002 CA-1 ("solo en variables de entorno de la sesión, sin ficheros"),
en `probe/README.md` y en `docs/ciclo-0/guia-claves-api.md`. ADR-001 fija la frontera de
**datos** y rechaza "confiar solo en `.gitignore` dentro del repo" como única medida, porque
un `git add -f` o un fichero renombrado basta para filtrar. ADR-004 §5 dice que "ninguna
credencial, token ni ID de propiedad va al repo".

Teclear tres claves en cada sesión no escala a varias máquinas, y el humano quiere un único
fichero que llevarse. El repo es **público**: una clave en el historial queda expuesta para
siempre aunque se borre después. Hace falta una regla única, verificable y citable por las
specs, en lugar de repetirla en cada una.

## Decisión
1. **Dónde**: las claves de API pueden vivir en un fichero `.env` en la **raíz del árbol de
   trabajo local** del repo, con formato `NOMBRE=valor` (una por línea; nombres
   `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GEMINI_API_KEY`). Sigue valiendo la alternativa
   de ponerlas solo en la sesión o en el entorno de usuario. Ningún otro fichero del árbol
   de trabajo (ni `probe/.env`, ni configs, ni scripts) contiene claves.
2. **"En el repo" significa en el índice o en el historial de git**, no en el árbol de
   trabajo. ADR-004 §5 se lee así para las claves de API: el `.env` ignorado no "va al
   repo" mientras se cumplan las comprobaciones del punto 3.
3. **Comprobaciones verificables** (las ejecuta el verificador en cada spec que lance el
   probe con claves; hoy SPEC-002 CA-1):
   - `git check-ignore -v .env` responde con una regla de `.gitignore` (hoy `.env` y
     `.env.*`);
   - `git log --all --oneline -- .env` sale vacío (nunca se ha commiteado);
   - `git status --porcelain` no lista `.env`;
   - `git ls-files` no lista ningún `.env` ni `.env.*`;
   - la búsqueda de `sk-`, `sk-ant-` y `AIza` en `git log -p --all` no da coincidencias.
4. **Traslado entre máquinas**: el contenido del `.env` se guarda como nota segura en el
   gestor de contraseñas del humano. Nunca por email, mensajería, ni en una carpeta de
   nube sincronizada sin cifrar. Por lo mismo, el árbol de trabajo no debe estar dentro de
   una carpeta sincronizada sin cifrar (OneDrive, Dropbox…), o el `.env` viajaría con ella.
5. **Agentes**: ningún agente lee, imprime ni copia el `.env` ni el valor de una clave;
   cargarlas en el entorno es un paso del humano (o del propio probe, si una spec lo
   añade). Una clave vista por un agente se trata como filtrada.
6. **Si una clave se filtra** (aparece en el historial, en un log, en un chat o la ve un
   agente): se revoca en su consola y se crea otra. Reescribir el historial no basta en un
   repo público. Los límites de gasto por proveedor de SPEC-002 P-2 acotan el daño.

## Consecuencias
### Positivas
- Una sola regla de custodia de claves, citable por SPEC-002, SPEC-008 y las que vengan.
- Cambiar de máquina es copiar un fichero desde el gestor de contraseñas.
- El verificador comprueba la regla con órdenes de git, sin juicio subjetivo.

### Negativas / follow-ups
- Se acepta para las claves lo que ADR-001 rechazó como **única** medida para los datos:
  la protección descansa en `.gitignore`. Un `git add -f .env` la rompe. Mitigación: las
  comprobaciones del punto 3, la revocación del punto 6 y los límites de gasto. El riesgo
  se juzga aceptable porque, a diferencia de los datos, una clave filtrada se invalida en
  minutos.
- La clave queda en claro en el disco local, no solo en memoria. Depende del cifrado del
  disco del humano.
- Los agentes con acceso al árbol de trabajo *pueden* leer el `.env`. Follow-up para el
  humano: añadir una regla de permisos que niegue la lectura de `.env` a los agentes en la
  configuración local (p. ej. `.claude/settings.local.json`). No lo fija este ADR.
- Follow-up para el implementador de SPEC-002: actualizar `probe/README.md` y
  `docs/ciclo-0/guia-claves-api.md`, y valorar que `run_probe.py` cargue `.env` con un
  parser mínimo, con test y sin dependencias nuevas (ver ledger de SPEC-002).

## Alternativas consideradas
- **Solo en la sesión (`Read-Host`)**, lo vigente: se mantiene como opción, pero rechazada
  como única vía porque obliga a teclear tres claves por sesión y máquina, y el humano ha
  decidido otra cosa.
- **Variables de entorno de usuario de Windows**: válidas, pero no son "un fichero que me
  llevo"; tampoco se prohíben.
- **`.env` fuera del repo (p. ej. en `$PUSHLLM_PRIVADO`)**: más robusto frente a
  `git add -f`, pero el humano pidió explícitamente la raíz del repo local; queda como
  alternativa si una comprobación del punto 3 falla alguna vez.
- **Gestor de secretos (Bitwarden CLI, 1Password CLI, `keyring`)**: rechazada por ahora;
  añade una dependencia y un paso de desbloqueo para un probe de pocas ejecuciones.
  Reabrible en el Ciclo 1 si el probe pasa a correr de forma periódica.
- **Enmendar solo SPEC-002 CA-1, sin ADR**: rechazada; la regla constriñe a toda spec que
  use claves (SPEC-008 ya cita SPEC-002 CA-1) y matiza ADR-001/ADR-004, así que su fuente
  de verdad debe ser un ADR y las specs deben referenciarlo.

<!-- REGLA: un ADR aceptado es INMUTABLE. Para cambiar la decisión, escribe otro ADR que lo supersede (estado del viejo -> bloqueada + nota "superseded por ADR-NNN"). -->
