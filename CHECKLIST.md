# Checklist — eSports Analytics Platform

Lista de seguimiento para llevar el proyecto de **funcional** a **listo para portafolio / selección**.

---

## Leyenda

- [ ] Pendiente
- [x] Completado

---

## Fase 0 — Base funcional (completada)

- [x] Backend FastAPI con arquitectura por capas
- [x] MySQL en Docker (`esports-analytics-platform`)
- [x] Modelos ORM: `Player`, `MatchStats`
- [x] API v1: CRUD jugadores + stats + `/analytics/predict`
- [x] Seed desde `CSGO.csv` (362 jugadores, 3330 partidas)
- [x] Entrenamiento ML real (PCA + K-Means → `.joblib`)
- [x] Tests backend con Pytest (12)
- [x] Frontend Angular 19 + Tailwind
- [x] Dashboard: roster, historial, predicción, gráfico de tendencia
- [x] Paginación en roster
- [x] Tests frontend con Jasmine/Karma (6)
- [x] `README.md` raíz con arquitectura y setup

---

## Fase 1 — Repositorio y calidad (prioridad alta)

### Git
- [x] Crear `.gitignore` raíz (`.env`, `node_modules`, `__pycache__`, `.pytest_cache`, `dist/`, etc.)
- [x] Inicializar repositorio Git
- [x] Primer commit limpio (sin secretos ni artefactos generados)
- [ ] Crear repositorio remoto en GitHub
- [ ] Push inicial a `main`

### CI/CD
- [x] Workflow GitHub Actions: **backend** (`pip install` + `pytest`)
- [x] Workflow GitHub Actions: **frontend** (`npm ci` + `npm test` + `npm run build`)
- [ ] Badge de CI en `README.md` (opcional)

### Calidad de código
- [x] Verificar que `.env` no esté trackeado (solo `.env.example`)
- [x] Revisar que `CSGO.zip` no suba al repo si pesa mucho (usar `.gitignore` o Git LFS)
- [x] Ejecutar suite completa local antes de cada push

---

## Fase 2 — Docker y entorno reproducible (prioridad alta)

- [ ] `Dockerfile` para el backend (FastAPI + Uvicorn)
- [ ] Ampliar `docker-compose.yml` con servicio `api`
- [ ] Script o entrypoint: esperar MySQL → `init_db` → opcional seed
- [ ] Documentar `docker compose up` como forma única de levantar todo
- [ ] Probar stack completo en máquina limpia (sin Python/Node local)

---

## Fase 3 — Deploy demo en vivo (prioridad alta para CV)

### Backend
- [ ] Elegir hosting (Railway, Render, Fly.io, etc.)
- [ ] MySQL gestionado o contenedor en cloud
- [ ] Variables de entorno en el proveedor
- [ ] Ejecutar seed + `train_model` en el entorno remoto
- [ ] Verificar `/api/health` y `/api/docs` públicos

### Frontend
- [ ] Elegir hosting (Vercel, Netlify, etc.)
- [ ] Configurar `environment.prod.ts` con URL real de la API
- [ ] Build de producción y deploy
- [ ] Probar CORS backend ↔ frontend en producción

### Documentación
- [ ] Añadir URLs de demo al `README.md`
- [ ] Captura de pantalla del dashboard en el README (opcional)
- [ ] Añadir link al repo en CV / LinkedIn

---

## Fase 4 — Mejoras de producto (prioridad media)

### Backend
- [ ] Endpoint resumen por jugador (`avg_kills`, `avg_rating`, partidas totales)
- [ ] Búsqueda/filtro en `GET /players` (`?q=` nick o steam_id)
- [ ] Alembic para migraciones versionadas (reemplazar solo `init_db`)
- [ ] Índices DB adicionales si hace falta (benchmark básico)

### Frontend
- [ ] Búsqueda en roster
- [ ] Paginación en Match History
- [ ] Estado de carga/error más explícito (toast o banner)
- [ ] Responsive fino en móvil

### ML
- [ ] Script que re-entrena si el CSV cambia
- [ ] Métricas de evaluación (silhouette score) en `train_model`
- [ ] Documentar arquetipos de clúster en README

---

## Fase 5 — Testing avanzado (prioridad media-baja)

- [ ] Test de integración backend con MySQL (contenedor en CI)
- [ ] E2E con Playwright o Cypress: jugador → predicción → resultado
- [ ] Cobertura mínima documentada en README

---

## Fase 6 — Presentación para selección (prioridad media)

- [ ] README: sección **“Decisiones técnicas”** (por qué FastAPI, por qué K-Means, etc.)
- [ ] README: diagrama de arquitectura (mermaid)
- [ ] Preparar pitch de 2 minutos del proyecto
- [ ] Preparar respuestas: trade-offs, escalabilidad, qué mejorarías con más tiempo
- [ ] Video demo corto (opcional, 1–2 min)

---

## Orden sugerido (rápido → impacto)

```
1. Fase 1 — Git + .gitignore + CI
2. Fase 2 — Docker backend en compose
3. Fase 3 — Deploy demo en vivo
4. Fase 4 — Búsqueda + endpoint resumen (quick wins UX)
5. Fase 5 — E2E mínimo
6. Fase 6 — Pulir README para entrevistas
```

---

## Comandos de referencia rápida

```powershell
# Stack local actual
docker compose up -d
cd backend
python -m scripts.init_db
python -m scripts.seed_csgo --clear
python -m scripts.train_model
python -m uvicorn app.main:app --reload --port 8000

cd ../frontend
npm start

# Tests
cd backend && python -m pytest
cd frontend && npm test -- --watch=false --browsers=ChromeHeadless
```

---

*Última actualización: junio 2026*
