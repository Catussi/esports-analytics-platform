# Setup — Backend

## Opción A: Todo con Docker (recomendado)

Desde la raíz del proyecto:

```powershell
docker compose up --build -d
docker compose exec api python -m scripts.seed_csgo --csv-path /data/CSGO.csv --clear
```

- API: http://localhost:8000/api/health
- Swagger: http://localhost:8000/api/docs
- Logs: `docker compose logs -f api`

## Opción B: Desarrollo local

### 1. Variables de entorno

Desde `backend/`:

```powershell
Copy-Item .env.example .env
```

## 2. Levantar MySQL con Docker

Desde la **raíz del proyecto** (`proyecto portafolio/`):

```powershell
docker compose up -d
```

> El proyecto Docker se llama `esports-analytics-platform` (definido en `docker-compose.yml`),
> no usa el nombre de la carpeta local.

Espera unos segundos a que MySQL esté listo. Puedes verificar con:

```powershell
docker compose ps
```

## 3. Crear tablas

Desde `backend/`:

```powershell
python -m scripts.init_db
```

## 4. Cargar datos desde CSGO.csv

Desde `backend/`:

```powershell
python -m scripts.seed_csgo --clear
```

Inserta **362 jugadores** y **3330 registros** de partida agregados desde el CSV.

Opciones útiles:

```powershell
python -m scripts.seed_csgo --limit 10000   # prueba rápida con subset
python -m scripts.seed_csgo --clear         # limpia e inserta de nuevo
```

## 5. Entrenar modelo ML (K-Means + PCA)

Desde `backend/`:

```powershell
python -m scripts.train_model
```

Genera `app/ml/models/kmeans_pca_model.joblib` usando las métricas reales del CSV.

## 6. Arrancar la API

Desde `backend/`:

```powershell
python -m uvicorn app.main:app --reload --port 8000
```

- Health: http://localhost:8000/api/health
- Swagger: http://localhost:8000/api/docs

## Errores frecuentes

| Error | Causa | Solución |
|---|---|---|
| `No module named 'scripts'` | Ejecutaste fuera de `backend/` | `cd backend` primero |
| `cp no se reconoce` | Comando de Linux en Windows | Usa `Copy-Item .env.example .env` |
| `Can't connect to MySQL server` | MySQL no está corriendo | `docker compose up -d` desde la raíz |

## Credenciales por defecto (Docker)

- Host: `localhost`
- Puerto: `3306`
- Usuario: `esports_user`
- Contraseña: `changeme`
- Base de datos: `esports_analytics`
