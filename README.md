# eSports Analytics Platform

Plataforma fullstack para analizar rendimiento de jugadores de CS:GO mediante clustering (K-Means + PCA) sobre métricas de partida. Proyecto orientado a demostrar arquitectura por capas, integración ML y buenas prácticas de testing.

## Stack

| Capa | Tecnología |
|---|---|
| Backend | Python, FastAPI, SQLAlchemy, Pydantic, Uvicorn |
| Base de datos | MySQL 8 (Docker) |
| ML | Scikit-Learn, Joblib, Pandas |
| Frontend | Angular 19, TypeScript, Tailwind CSS, Chart.js |
| Testing | Pytest, Jasmine/Karma |

## Arquitectura

```
proyecto portafolio/
├── backend/                 # API REST + ML
│   ├── app/
│   │   ├── routers/v1/      # Endpoints HTTP
│   │   ├── services/        # Lógica de negocio
│   │   ├── models/          # ORM SQLAlchemy
│   │   ├── schemas/         # DTOs Pydantic
│   │   └── ml/              # Entrenamiento e inferencia
│   └── scripts/             # init_db, seed, train_model
├── frontend/                # SPA Angular
│   └── src/app/
│       ├── core/            # Servicios + modelos TS
│       ├── features/        # Dashboard
│       └── shared/          # Componentes reutilizables
├── docker-compose.yml       # MySQL local
└── CSGO.csv                 # Dataset de entrenamiento/seed
```

## Requisitos previos

- Python 3.11+
- Node.js 20+
- Docker Desktop

## Puesta en marcha (Windows)

### 1. Base de datos

Desde la raíz del proyecto:

```powershell
docker compose up -d
```

### 2. Backend

```powershell
cd backend
Copy-Item .env.example .env
pip install -r requirements.txt
python -m scripts.init_db
python -m scripts.seed_csgo --clear
python -m scripts.train_model
python -m uvicorn app.main:app --reload --port 8000
```

### 3. Frontend

```powershell
cd frontend
npm install
npm start
```

- API: http://localhost:8000/api/docs
- App: http://localhost:4200

## API principal

| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/api/health` | Health check |
| `GET` | `/api/v1/players` | Listado paginado de jugadores |
| `GET` | `/api/v1/players/{id}/stats` | Estadísticas por partida |
| `POST` | `/api/v1/analytics/predict` | Inferencia de clúster ML |

## Pipeline ML

1. **Agregación** — `CSGO.csv` (round-level) → métricas por jugador/partida
2. **Entrenamiento** — `StandardScaler → PCA (3) → K-Means (4)`
3. **Inferencia** — endpoint `/predict` retorna clúster, etiqueta y feedback analítico

## Testing

```powershell
# Backend
cd backend
python -m pytest

# Frontend
cd frontend
npm test -- --watch=false --browsers=ChromeHeadless
npm run build
```

## CI (GitHub Actions)

En cada push/PR a `main`:

- **Backend CI** — `pytest` en Python 3.12
- **Frontend CI** — `npm test` + `npm run build` en Node 20

Workflows en `.github/workflows/`.

## Credenciales MySQL (Docker)

| Campo | Valor |
|---|---|
| Host | `localhost` |
| Puerto | `3306` |
| Usuario | `esports_user` |
| Contraseña | `changeme` |
| Base de datos | `esports_analytics` |

## Dataset

`CSGO.csv` contiene ~79k filas a nivel de round. El script de seed agrega a **3330 partidas** de **362 jugadores** únicos con métricas derivadas (ADR, KAST, rating estimado).

---

Desarrollado como proyecto de portafolio — eSports Analytics Platform.
