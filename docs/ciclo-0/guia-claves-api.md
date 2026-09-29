# Guía: claves de API para el probe (SPEC-002, prerrequisito P-2)

> Preparada el 2026-09-24. Los nombres exactos de los menús pueden variar; los
> pasos no. Límite acordado: **20 € por proveedor** (decisión del humano, EPIC-001).

**Diferencia importante:** OpenAI y Anthropic funcionan con **saldo prepagado**, y
ese saldo es un tope real. En Google los **presupuestos solo avisan**, no cortan
el gasto.

## 1. OpenAI (ChatGPT): https://platform.openai.com
1. Entra con tu cuenta o crea una. ChatGPT Plus **no** incluye la API: se paga aparte.
2. **Settings → Billing** → añade una tarjeta y **compra 20 $ de crédito**.
3. En la misma pantalla, **desactiva la recarga automática** (*auto recharge*).
   Así los 20 $ son un tope real.
4. Opcional: en **Settings → Limits**, pon un presupuesto mensual con aviso por email.
5. **API keys** (https://platform.openai.com/api-keys) → **Create new secret key**
   con el nombre `push-llm-probe`.
6. **Copia la clave en ese momento.** Empieza por `sk-` y no se vuelve a mostrar.

## 2. Anthropic (Claude): https://console.anthropic.com
1. Entra con tu cuenta o crea una. Claude Pro **no** incluye la API.
2. **Settings → Billing** → añade una tarjeta y **compra 20 $ de crédito**, con la
   recarga automática desactivada.
3. Opcional: en **Settings → Limits**, pon un límite de gasto mensual.
4. **Settings → API Keys → Create Key** con el nombre `push-llm-probe`.
5. **Copia la clave.** Empieza por `sk-ant-` y tampoco se vuelve a mostrar.

## 3. Google Gemini: https://aistudio.google.com
1. Entra con tu cuenta de Google.
2. **Get API key → Create API key**. Te pedirá crear o elegir un proyecto de
   Google Cloud; crea uno llamado `push-llm`.
3. **Copia la clave.** Empieza por `AIza`.
4. Límite de gasto:
   - **Sin activar la facturación**, la clave funciona en el nivel gratuito. No
     cuesta nada, pero tiene límites de peticiones por minuto y por día, y de
     búsquedas con Google. Para el humo basta; para la ejecución completa puede
     que no.
   - **Si activas la facturación** (en AI Studio, **Set up billing**), crea un
     presupuesto de 20 € en https://console.cloud.google.com → **Billing →
     Budgets & alerts**, con avisos al 50 %, 90 % y 100 %. **Ese presupuesto
     solo avisa, no corta el gasto.** El control real está en el probe: el
     humo estima el coste de la ejecución completa antes de lanzarla, y el
     total previsto no pasa de ~30 €.
   - **Recomendación:** empieza sin facturación. Si choca con los límites, la
     activas y continúas con `--resume`.

## Custodia de las claves
Regla: ADR-006 (claves en un `.env` local ignorado por git) y ADR-007 (`.env.example`
versionado como plantilla sin valores). Actualizado el 2026-09-29.

- **Dónde viven**: en un fichero `.env` en la **raíz de tu copia local del repo**
  (junto a `.env.example`), una por línea: `ANTHROPIC_API_KEY=…`, `OPENAI_API_KEY=…`,
  `GEMINI_API_KEY=…`. Para crearlo, copia `.env.example` como `.env` y rellena los
  valores. `.env` está ignorado por git: **nunca** lo subas (tampoco con `git add -f`).
  Ningún otro fichero del repo lleva claves (ni `probe/.env`, ni configs, ni scripts), y
  `.env.example` se queda siempre con los valores vacíos. El repo es **público**.
- **Cómo las usa el probe**: `run_probe.py` lee solo el `.env` de la raíz al arrancar
  (no hace falta `Read-Host` ni ningún fragmento de PowerShell). Si una variable ya está
  definida en la sesión o en tu entorno de usuario, manda esa y el `.env` no la toca.
  Nunca escribe los valores en pantalla, en `results.csv` ni en `summary.md`. Sin `.env`,
  sigue valiendo ponerlas solo en la sesión (ver `probe/README.md`).
- **Copia y traslado a otra máquina**: guarda el contenido completo del `.env` como
  **nota segura** en tu gestor de contraseñas (Bitwarden, 1Password, el de Chrome…) y,
  en la otra máquina, pégalo en un `.env` nuevo en la raíz del repo. **Nunca** por email,
  mensajería ni en una carpeta de nube sincronizada sin cifrar (OneDrive, Dropbox…); por
  lo mismo, la copia del repo no debe estar dentro de una carpeta así, o el `.env`
  viajaría con ella.
- **Agentes**: ningún agente lee, abre ni copia el `.env`. Si un agente llega a ver una
  clave, se trata como filtrada.
- **Si una clave se filtra** (aparece en el historial de git, en un log, en un chat o la
  ve un agente): **revócala** en su consola y crea otra; actualiza la nota segura y el
  `.env`. Reescribir el historial no basta en un repo público. Los límites de gasto por
  proveedor acotan el daño mientras tanto.
