from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
import pandas as pd
import pickle
import json
import io
import numpy as np
from pathlib import Path

app = FastAPI(title="UniCareer ML API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ROOT = Path(__file__).parent.parent.parent  # Medallion root

MODEL_CONFIGS = {
    "logistica": {
        "pkl": ROOT / "datalake_gold/outputs_logistic_regression/informe/logistic_regression_offer_received_improved.pkl",
        "summary": ROOT / "datalake_gold/outputs_logistic_regression/informe/logistic_regression_offer_received_summary.json",
        "type": "classification",
        "threshold": 0.3,
    },
    "knn": {
        "pkl": ROOT / "datalake_gold/outputs_knn/informe/knn_offer_received_pca.pkl",
        "summary": ROOT / "datalake_gold/outputs_knn/informe/knn_offer_received_summary.json",
        "type": "classification",
        "threshold": 0.325,
    },
    "decision-tree": {
        "pkl": ROOT / "datalake_gold/outputs_decision_tree/informe/decision_tree_offer_received_improved.pkl",
        "summary": ROOT / "datalake_gold/outputs_decision_tree/informe/decision_tree_offer_received_summary.json",
        "type": "classification",
        "threshold": 0.325,
    },
    "salario": {
        "pkl": ROOT / "datalake_gold/outputs_regresion/lasso/informe/lasso_offer_salary.pkl",
        "summary": ROOT / "datalake_gold/outputs_regresion/regresion_offer_salary_completo_summary.json",
        "type": "regression",
    },
    "logistica-pca": {
        "pkl": ROOT / "datalake_gold/PCA/outputs_logistica_pca/informe/logistica_pca.pkl",
        "summary": ROOT / "datalake_gold/PCA/outputs_logistica_pca/informe/logistica_pca_summary.json",
        "type": "classification",
    },
    "decision-tree-pca": {
        "pkl": ROOT / "datalake_gold/PCA/outputs_decision_tree_pca/informe/decision_tree_pca.pkl",
        "summary": ROOT / "datalake_gold/PCA/outputs_decision_tree_pca/informe/decision_tree_pca_summary.json",
        "type": "classification",
    },
    "naive-bayes": {
        "pkl": ROOT / "datalake_gold/outputs_naive_bayes/informe/naive_bayes_offer_received_improved.pkl",
        "summary": ROOT / "datalake_gold/outputs_naive_bayes/informe/naive_bayes_offer_received_summary.json",
        "type": "classification",
    },
}

_models: dict = {}
_summaries: dict = {}


def _normalize_metrics(model_id: str, raw: dict) -> dict:
    """Extract a consistent metrics object from the raw JSON summary."""
    if model_id == "logistica":
        m = raw["metrics"]["threshold_optimized"]
        return {
            "type": "classification",
            "accuracy": m["Accuracy"],
            "precision": m["Precision"],
            "recall": m["Recall"],
            "f1": m["F1-Score"],
            "roc_auc": m["ROC-AUC"],
            "threshold": raw["best_threshold"],
            "model_name": raw["model_name"],
        }
    elif model_id == "knn":
        m = raw["pca_model"]["metrics"]
        return {
            "type": "classification",
            "accuracy": m["Accuracy"],
            "precision": m["Precision"],
            "recall": m["Recall"],
            "f1": m["F1-Score"],
            "roc_auc": m["ROC-AUC"],
            "threshold": raw["pca_model"]["best_threshold"],
            "model_name": raw["model_name"],
        }
    elif model_id == "decision-tree":
        m = raw["metrics"]["threshold_0_50"]
        return {
            "type": "classification",
            "accuracy": m["Accuracy"],
            "precision": m["Precision"],
            "recall": m["Recall"],
            "f1": m["F1-Score"],
            "roc_auc": m["ROC-AUC"],
            "threshold": 0.5,
            "model_name": raw["model_name"],
        }
    elif model_id == "salario":
        b = raw["best_model"]
        return {
            "type": "regression",
            "r2": b["R2_test"],
            "mae": b["MAE_test"],
            "rmse": b["RMSE_test"],
            "model_name": b["modelo"],
            "all_models": raw.get("comparison", []),
        }
    elif model_id in ("logistica-pca", "decision-tree-pca"):
        m = raw["metrics"]["threshold_optimized"]
        pca = raw.get("pca", {})
        return {
            "type": "classification",
            "accuracy": m["Accuracy"],
            "precision": m["Precision"],
            "recall": m["Recall"],
            "f1": m["F1-Score"],
            "roc_auc": m["ROC-AUC"],
            "threshold": raw["best_threshold"],
            "model_name": raw["model_name"],
            "pca_components": pca.get("n_components"),
            "pca_variance": pca.get("explained_variance"),
        }
    elif model_id == "naive-bayes":
        m = raw["metrics"]["threshold_optimized"]
        return {
            "type": "classification",
            "accuracy": m["Accuracy"],
            "precision": m["Precision"],
            "recall": m["Recall"],
            "f1": m["F1-Score"],
            "roc_auc": m["ROC-AUC"],
            "threshold": raw["best_threshold"],
            "model_name": raw["model_name"],
        }
    return {}


@app.on_event("startup")
async def load_models():
    for model_id, cfg in MODEL_CONFIGS.items():
        try:
            with open(cfg["pkl"], "rb") as f:
                pkl_data = pickle.load(f)
            # pkl files are saved as dicts with 'pipeline', 'feature_columns', 'best_threshold'
            pipeline = pkl_data["pipeline"]
            feature_cols = pkl_data.get("feature_columns", [])
            threshold = pkl_data.get("best_threshold", cfg.get("threshold", 0.5)) or 0.5
            _models[model_id] = {
                "pipeline": pipeline,
                "type": cfg["type"],
                "threshold": threshold,
                "feature_columns": feature_cols,
            }
            with open(cfg["summary"], encoding="utf-8") as f:
                raw = json.load(f)
                _summaries[model_id] = _normalize_metrics(model_id, raw)
        except Exception as e:
            print(f"[WARN] Could not load model '{model_id}': {e}")


@app.get("/api/summaries")
def get_summaries():
    return _summaries


@app.get("/api/eda")
def get_eda():
    bronze = ROOT / "datalake_bronze/job_search_platform_efficacy_100k.csv"
    platform_file = ROOT / "datalake_silver/outputs_primer_corte/csv/tasa_oferta_por_plataforma.csv"
    correlations_file = ROOT / "datalake_silver/outputs_primer_corte/csv/top_correlaciones_offer_received.csv"
    missing_file = ROOT / "datalake_silver/outputs_primer_corte/csv/resumen_faltantes.csv"
    metadata_file = ROOT / "datalake_silver/outputs_primer_corte/csv/metadata_limpieza.csv"

    df = pd.read_csv(bronze)
    total = len(df)
    offered = df[df["Offer_Received"] == 1]
    offer_rate = round(float(offered.shape[0] / total) * 100, 1)
    avg_salary = round(float(offered["Offer_Salary"].mean()))

    # Completeness from silver metadata
    completeness = 100.0
    try:
        meta = pd.read_csv(metadata_file)
        rows = int(meta["cleaned_rows"].iloc[0])
        orig = int(meta["original_rows"].iloc[0])
        completeness = round(rows / orig * 100, 1)
    except Exception:
        pass

    # Platform breakdown from silver pre-computed CSV
    platform_data = []
    try:
        pf = pd.read_csv(platform_file)
        for _, row in pf.iterrows():
            platform_data.append({
                "name": str(row["Primary_Search_Platform"]),
                "value": round(float(row["offer_rate_pct"]), 1),
            })
    except Exception:
        counts = df["Primary_Search_Platform"].value_counts(normalize=True) * 100
        platform_data = [{"name": k, "value": round(float(v), 1)} for k, v in counts.items()]

    # Salary by major category
    salary_by_major = (
        offered.groupby("Major_Category")["Offer_Salary"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )
    salary_by_major_data = [
        {"major": str(row["Major_Category"]), "salary": round(float(row["Offer_Salary"]))}
        for _, row in salary_by_major.iterrows()
    ]

    # Top correlations from silver
    correlations = []
    try:
        corr = pd.read_csv(correlations_file, index_col=0)
        for feat, row in corr.iterrows():
            correlations.append({
                "feature": str(feat),
                "correlation": round(float(row.iloc[0]), 4),
            })
    except Exception:
        pass

    # Pipeline tracking counts
    tracking = [
        {"name": "Total Estudiantes", "value": total},
        {"name": "Recibieron Oferta", "value": int(offered.shape[0])},
        {"name": "Sin Oferta", "value": int(total - offered.shape[0])},
    ]

    # Platform source counts for pie
    plat_counts = df["Primary_Search_Platform"].value_counts()
    pie_data = [
        {"name": str(k), "value": int(v)}
        for k, v in plat_counts.items()
    ]

    return {
        "total_records": total,
        "offer_rate": offer_rate,
        "avg_salary": avg_salary,
        "completeness": completeness,
        "platform_offer_rates": platform_data,
        "salary_by_major": salary_by_major_data,
        "correlations": correlations,
        "tracking": tracking,
        "pie_data": pie_data,
    }


@app.post("/api/predict/{model_id}")
async def predict(model_id: str, file: UploadFile = File(...)):
    if model_id not in _models:
        available = list(_models.keys())
        raise HTTPException(404, f"Modelo '{model_id}' no encontrado. Disponibles: {available}")

    content = await file.read()
    try:
        df = pd.read_csv(io.BytesIO(content))
    except Exception as e:
        raise HTTPException(400, f"Error leyendo CSV: {e}")

    model_info = _models[model_id]
    pipeline = model_info["pipeline"]

    # Select only the feature columns the model was trained on
    feature_cols = model_info.get("feature_columns", [])
    if feature_cols:
        missing = [c for c in feature_cols if c not in df.columns]
        if missing:
            raise HTTPException(
                422,
                f"Columnas requeridas no encontradas: {missing}. "
                f"El CSV debe incluir: {feature_cols}"
            )
        df = df[feature_cols]
    else:
        for col in ["Offer_Received", "Offer_Salary", "Student_ID"]:
            if col in df.columns:
                df = df.drop(columns=[col])

    try:
        if model_info["type"] == "classification":
            proba = pipeline.predict_proba(df)[:, 1]
            threshold = model_info["threshold"]
            preds = (proba >= threshold).astype(int)
            positive = int(preds.sum())
            negative = int(len(preds) - positive)
            return {
                "type": "classification",
                "total": int(len(df)),
                "positive": positive,
                "negative": negative,
                "positive_rate": round(float(preds.mean()) * 100, 1),
                "avg_probability": round(float(proba.mean()) * 100, 1),
                "threshold_used": threshold,
            }
        else:
            preds = pipeline.predict(df)
            return {
                "type": "regression",
                "total": int(len(df)),
                "mean_salary": int(round(float(preds.mean()))),
                "median_salary": int(round(float(np.median(preds)))),
                "min_salary": int(round(float(preds.min()))),
                "max_salary": int(round(float(preds.max()))),
            }
    except Exception as e:
        raise HTTPException(422, f"Error en inferencia: {str(e)}")


@app.post("/api/predict-csv/{model_id}")
async def predict_csv_download(model_id: str, file: UploadFile = File(...)):
    if model_id not in _models:
        raise HTTPException(404, f"Modelo '{model_id}' no encontrado.")

    content = await file.read()
    try:
        df = pd.read_csv(io.BytesIO(content))
    except Exception as e:
        raise HTTPException(400, f"Error leyendo CSV: {e}")

    model_info = _models[model_id]
    pipeline = model_info["pipeline"]
    out_df = df.copy()

    feature_cols = model_info.get("feature_columns", [])
    if feature_cols:
        missing = [c for c in feature_cols if c not in df.columns]
        if missing:
            raise HTTPException(422, f"Columnas requeridas no encontradas: {missing}.")
        input_df = df[feature_cols]
    else:
        input_df = df.copy()
        for col in ["Offer_Received", "Offer_Salary", "Student_ID"]:
            if col in input_df.columns:
                input_df = input_df.drop(columns=[col])

    try:
        if model_info["type"] == "classification":
            threshold = model_info["threshold"]
            proba = pipeline.predict_proba(input_df)[:, 1]
            preds = (proba >= threshold).astype(int)
            out_df["Probabilidad_Oferta"] = proba.round(4)
            out_df["Prediccion_Oferta"] = preds
        else:
            preds = pipeline.predict(input_df)
            out_df["Salario_Predicho"] = preds.round(2)
    except Exception as e:
        raise HTTPException(422, f"Error en inferencia: {str(e)}")

    buf = io.StringIO()
    out_df.to_csv(buf, index=False)
    buf.seek(0)
    filename = f"predicciones_{model_id}.csv"
    return StreamingResponse(
        io.BytesIO(buf.getvalue().encode("utf-8")),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@app.get("/api/health")
def health():
    return {"status": "ok", "loaded_models": list(_models.keys())}


# --- Image serving ---

_IMAGE_DIRS: dict[str, Path] = {
    "silver": ROOT / "datalake_silver/outputs_primer_corte/imagenes_png",
    "logistica": ROOT / "datalake_gold/outputs_logistic_regression/imagenes",
    "knn": ROOT / "datalake_gold/outputs_knn/imagenes",
    "decision-tree": ROOT / "datalake_gold/outputs_decision_tree/imagenes",
    "salario": ROOT / "datalake_gold/outputs_regresion/lasso/imagenes",
    "regresion": ROOT / "datalake_gold/outputs_regresion",
    "logistica-pca": ROOT / "datalake_gold/PCA/outputs_logistica_pca/imagenes",
    "decision-tree-pca": ROOT / "datalake_gold/PCA/outputs_decision_tree_pca/imagenes",
    "naive-bayes": ROOT / "datalake_gold/outputs_naive_bayes/imagenes",
}

_ALLOWED_EXT = {".png", ".jpg", ".jpeg", ".svg"}


@app.get("/api/images/{section}/{filename}")
def serve_image(section: str, filename: str):
    if section not in _IMAGE_DIRS:
        raise HTTPException(404, f"Sección '{section}' no existe")
    if Path(filename).suffix.lower() not in _ALLOWED_EXT:
        raise HTTPException(400, "Tipo de archivo no permitido")
    # Guard against path traversal
    base = _IMAGE_DIRS[section].resolve()
    target = (base / filename).resolve()
    if not str(target).startswith(str(base)):
        raise HTTPException(403, "Acceso denegado")
    if not target.is_file():
        raise HTTPException(404, f"Imagen '{filename}' no encontrada")
    return FileResponse(str(target), media_type="image/png")
