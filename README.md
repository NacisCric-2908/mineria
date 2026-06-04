# UniCareer ML

Dashboard de predicción de empleabilidad estudiantil con modelos ML entrenados.

## Inicio rápido

Necesitas **dos terminales** abiertas desde la carpeta `page/`.

**Terminal 1 — Backend (FastAPI, puerto 8000)**
```bash
cd page
pip install -r api/requirements.txt
python -m uvicorn api.server:app --reload --port 8000
```

**Terminal 2 — Frontend (Vite, puerto 3000)**
```bash
cd page
npm install
npm run dev
```

Luego abre **http://localhost:3000**

## Modelos disponibles

| Modelo | Tarea |
|---|---|
| Regresión Logística | Clasificación oferta |
| K-Nearest Neighbors + PCA | Clasificación oferta |
| Árbol de Decisión | Clasificación oferta |
| Naive Bayes | Clasificación oferta |
| SVM (kernel RBF) | Clasificación oferta |
| Logística + PCA | Clasificación oferta |
| Árbol + PCA | Clasificación oferta |
| Regresión Lasso | Predicción salario |
| Análisis de Clustering | Análisis no supervisado |

Cada modelo acepta un CSV con las columnas del dataset y devuelve predicciones descargables.
