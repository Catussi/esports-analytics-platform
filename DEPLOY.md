# Deploy — eSports Analytics Platform

Guía para publicar **backend en Render** y **frontend en Vercel** (plan gratuito).

---

## Arquitectura en producción

```
[Vercel] Angular SPA  ──HTTPS──▶  [Render] FastAPI + ML
                                        │
                                        ▼
                                 [MySQL gestionado]
```

---

## Parte 1 — Base de datos MySQL

Necesitas un MySQL accesible desde internet. Opciones:

| Proveedor | Notas |
|---|---|
| [PlanetScale](https://planetscale.com/) | MySQL serverless (revisar plan gratuito actual) |
| [Railway](https://railway.app/) | MySQL add-on, fácil de conectar |
| [Aiven](https://aiven.io/) | Trial MySQL |
| Render MySQL | De pago en Render |

Anota: `host`, `puerto`, `usuario`, `contraseña`, `database`.

---

## Parte 2 — Backend en Render

### Opción A: Blueprint (`render.yaml`)

1. Sube el repo a GitHub.
2. En [Render Dashboard](https://dashboard.render.com/) → **New** → **Blueprint**.
3. Conecta el repo; Render detectará `render.yaml`.
4. Completa las variables marcadas `sync: false`:
   - `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DATABASE`
   - `CORS_ORIGINS` → URL de Vercel (ej. `https://tu-app.vercel.app`)

### Opción B: Web Service manual

1. **New** → **Web Service** → conecta GitHub.
2. Configuración:
   - **Runtime:** Docker
   - **Dockerfile path:** `backend/Dockerfile`
   - **Docker context:** `.` (raíz del repo)
   - **Health check path:** `/api/health`
3. Variables de entorno:

| Variable | Ejemplo |
|---|---|
| `MYSQL_HOST` | `xxx.mysql.provider.com` |
| `MYSQL_PORT` | `3306` |
| `MYSQL_USER` | `esports_user` |
| `MYSQL_PASSWORD` | `***` |
| `MYSQL_DATABASE` | `esports_analytics` |
| `CORS_ORIGINS` | `https://tu-app.vercel.app` |
| `RUN_TRAIN_MODEL` | `true` |
| `RUN_SEED` | `false` |
| `APP_ENV` | `production` |
| `DEBUG` | `false` |

4. Deploy. La primera vez el contenedor entrena el modelo (~1–2 min).
5. Verifica: `https://TU-SERVICIO.onrender.com/api/health`
6. Swagger: `https://TU-SERVICIO.onrender.com/api/docs`

### Cargar datos en producción (shell de Render)

En el servicio → **Shell**:

```bash
python -m scripts.seed_csgo --csv-path /data/CSGO.csv --clear
```

> El plan free de Render puede dormir el servicio tras inactividad (cold start ~30–60s).

---

## Parte 3 — Frontend en Vercel

### 1. Actualizar URL de la API

Edita `frontend/src/environments/environment.prod.ts`:

```typescript
export const environment = {
  production: true,
  apiBaseUrl: 'https://TU-SERVICIO.onrender.com/api/v1',
  apiHealthUrl: 'https://TU-SERVICIO.onrender.com/api/health',
};
```

Commit y push.

### 2. Importar en Vercel

1. [vercel.com](https://vercel.com) → **Add New Project**.
2. Importa el repo de GitHub.
3. Configuración:
   - **Root Directory:** `frontend`
   - **Framework Preset:** Angular (o Other)
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist/frontend/browser`
4. Deploy.

`frontend/vercel.json` ya incluye rewrites para SPA routing.

### 3. CORS en el backend

Vuelve a Render y actualiza `CORS_ORIGINS` con la URL real de Vercel:

```
https://tu-proyecto.vercel.app
```

Sin barra final. Si usas preview deployments, puedes añadir varias separadas por coma.

---

## Parte 4 — Verificación final

- [ ] `GET /api/health` → `{"status":"ok"}`
- [ ] `GET /api/v1/players` → lista de jugadores (tras seed)
- [ ] Frontend muestra **API ONLINE**
- [ ] Roster carga jugadores
- [ ] Predicción de clúster funciona

---

## Troubleshooting

| Problema | Solución |
|---|---|
| API OFFLINE en frontend | Revisa URLs en `environment.prod.ts` |
| CORS error en navegador | Añade dominio Vercel a `CORS_ORIGINS` en Render |
| 502 / timeout en Render | Cold start; espera o usa plan de pago |
| Sin jugadores | Ejecuta seed en Shell de Render |
| `/predict` falla | Verifica que exista el `.joblib` (logs de `train_model`) |

---

## URLs para el README / CV

Tras el deploy, añade al `README.md`:

```markdown
## Demo en vivo

- **App:** https://tu-proyecto.vercel.app
- **API Docs:** https://tu-servicio.onrender.com/api/docs
```
