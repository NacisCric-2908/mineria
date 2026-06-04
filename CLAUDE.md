# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture

This is a data science project ("UniCareer ML") that predicts student employability using a **medallion data architecture** and a **React + FastAPI dashboard**.

```
mineria/
├── datalake_bronze/          # Raw source CSV (100k student records)
├── datalake_silver/          # Cleaned data + EDA outputs (CSVs + PNGs)
│   └── outputs_primer_corte/
│       ├── csv/              # Pre-computed stats used by the EDA API endpoint
│       └── imagenes_png/
├── datalake_gold/            # Trained models + visualizations per algorithm
│   ├── outputs_logistic_regression/
│   ├── outputs_knn/
│   ├── outputs_decision_tree/
│   ├── outputs_regresion/
│   ├── outputs_naive_bayes/
│   ├── outputs_svm/
│   └── PCA/                  # PCA variants of logistic + decision tree
└── page/                     # The web dashboard
    ├── src/                  # React frontend (single App.tsx component)
    ├── api/                  # FastAPI backend (server.py)
    └── images/               # Logo assets
```

**Jupyter notebooks** live inside `datalake_silver/` and `datalake_gold/` next to the outputs they generate.

## Dashboard — Running Locally

The dashboard needs **two processes running simultaneously**:

### 1. FastAPI backend (port 8000)
```bash
cd page
pip install -r api/requirements.txt
python -m uvicorn api.server:app --reload --port 8000
```

### 2. Vite dev server (port 3000)
```bash
cd page
npm install
npm run dev
```

The frontend proxies all `/api/*` requests to the FastAPI backend via Vite's dev server (configured in `vite.config.ts`). TypeScript type-checking serves as the lint step:

```bash
cd page && npm run lint   # tsc --noEmit
```

## Model .pkl Format

All `.pkl` files are saved as Python dicts with this structure:
```python
{
    "pipeline": sklearn.Pipeline,     # scikit-learn pipeline (preprocessor + model)
    "feature_columns": list[str],     # columns the pipeline expects
    "best_threshold": float,          # classification threshold (may be None)
}
```

The backend loads all models at startup from `datalake_gold/` paths defined in `MODEL_CONFIGS` in `page/api/server.py`. If a model fails to load, it logs a warning and continues — the frontend shows "API no disponible" for that model.

## API Endpoints

| Endpoint | Description |
|---|---|
| `GET /api/health` | Liveness check + list of loaded models |
| `GET /api/summaries` | Metrics for all loaded models (from `*_summary.json` files) |
| `GET /api/eda` | Aggregated EDA stats computed from bronze + silver CSVs |
| `POST /api/predict/{model_id}` | Batch inference — returns summary counts/rates |
| `POST /api/predict-csv/{model_id}` | Batch inference — returns annotated CSV download |
| `GET /api/images/{section}/{filename}` | Serves PNG plots from datalake directories |

Valid `model_id` values: `logistica`, `knn`, `decision-tree`, `salario`, `logistica-pca`, `decision-tree-pca`.

## Frontend Structure

The entire React app is in `page/src/App.tsx` (single-file component pattern). Key parts:
- **`MODEL_DEFINITIONS`** — static list of models with their IDs, names, categories
- **`GALLERY_CONFIGS`** — maps each model ID to its PNG filenames and section labels
- **`EDAView`** — fetches `/api/eda` and renders charts using Recharts
- **`ModelView`** — handles CSV upload, calls `/api/predict/{id}`, shows results
- **`ImageGallery`** — tabbed gallery with lightbox for model visualizations
- All API calls are typed in `page/src/api.ts`

Navigation flow: `landing → login → dashboard`. The login is UI-only (no real auth).

## Adding a New Model

1. Train and export the `.pkl` dict (pipeline + feature_columns + best_threshold)
2. Place outputs in `datalake_gold/outputs_<name>/informe/` and images in `.../imagenes/`
3. Add the model to `MODEL_CONFIGS` in `page/api/server.py`
4. Add a normalizer branch in `_normalize_metrics()` in `server.py`
5. Add the `ModelID` type and entry to `MODEL_DEFINITIONS` in `App.tsx`
6. Add `GALLERY_CONFIGS` entry with PNG filenames mapped to their `section` key
