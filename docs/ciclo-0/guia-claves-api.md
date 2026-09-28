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
- Guárdalas en tu **gestor de contraseñas** (Bitwarden, 1Password, el de
  Chrome…). **Nunca** en un fichero dentro del repo, que es **público**.
- No se escriben en ningún sitio: las pegas en la terminal cuando el probe las
  pide (`Read-Host` en PowerShell; ver `probe/README.md`) y solo existen
  mientras esa terminal está abierta.
- Si una clave acaba donde no debe, **bórrala** desde su consola y crea otra.
