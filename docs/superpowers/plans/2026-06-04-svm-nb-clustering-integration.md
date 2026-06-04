# SVM + Naive Bayes + Clustering Integration Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Integrar Naive Bayes y SVM al servidor FastAPI + dashboard, y agregar Clustering como vista de análisis.

**Architecture:** Naive Bayes ya tiene PKL+JSON completos — solo necesita registrarse. SVM requiere nuevas celdas en el notebook para generar PKL+JSON estándar antes de registrarse. Clustering es no supervisado (sin `predict_proba`), por lo que se integra como vista de análisis estática (igual que EDA), no como modelo de predicción.

**Tech Stack:** Python / FastAPI / scikit-learn / React 19 / TypeScript / Recharts / TailwindCSS

---

## Mapa de archivos

| Archivo | Acción | Razón |
|---|---|---|
| `datalake_gold/SVM_offer_received.ipynb` | Modificar — agregar celdas al final | Generar PKL base + improved + JSON + plots estándar |
| `datalake_gold/Clustering_Jerarquico_DBSCAN_job.ipynb` | Modificar — agregar celdas al final | Guardar imágenes, JSON y PKL en rutas estándar |
| `page/api/server.py` | Modificar | Registrar naive-bayes, svm; endpoint /api/clustering |
| `page/src/App.tsx` | Modificar | Agregar naive-bayes, svm, clustering al sidebar + vistas |
| `page/src/api.ts` | Modificar | Agregar tipo ClusteringResponse |

---

## Task 1: Registrar Naive Bayes en servidor y frontend

> El PKL y JSON ya existen. Solo hay que conectarlos.
>
> **Files:**
> - Modify: `page/api/server.py`
> - Modify: `page/src/App.tsx`
> - Modify: `page/src/api.ts`

- [ ] **Paso 1: Agregar naive-bayes a MODEL_CONFIGS en server.py**

En `page/api/server.py`, dentro del dict `MODEL_CONFIGS` (después del bloque `"decision-tree-pca"`), agregar:

```python
    "naive-bayes": {
        "pkl": ROOT / "datalake_gold/outputs_naive_bayes/informe/naive_bayes_offer_received_improved.pkl",
        "summary": ROOT / "datalake_gold/outputs_naive_bayes/informe/naive_bayes_offer_received_summary.json",
        "type": "classification",
    },
```

- [ ] **Paso 2: Agregar rama `naive-bayes` a `_normalize_metrics` en server.py**

El JSON de Naive Bayes tiene esta estructura:
```json
{ "model_name": "GaussianNaiveBayes", "metrics": { "threshold_optimized": {...} }, "best_threshold": 0.22 }
```

Agregar después del bloque `elif model_id in ("logistica-pca", "decision-tree-pca"):`:

```python
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
```

- [ ] **Paso 3: Agregar `naive-bayes` a `_IMAGE_DIRS` en server.py**

```python
    "naive-bayes": ROOT / "datalake_gold/outputs_naive_bayes/imagenes",
```

- [ ] **Paso 4: Agregar naive-bayes a `ModelID` y `MODEL_DEFINITIONS` en App.tsx**

En `page/src/App.tsx`, línea ~60, actualizar el tipo:

```typescript
type ModelID = 'eda' | 'logistica' | 'knn' | 'decision-tree' | 'salario' | 'logistica-pca' | 'decision-tree-pca' | 'naive-bayes';
```

En `MODEL_DEFINITIONS`, agregar después del bloque `decision-tree-pca`:

```typescript
  {
    id: 'naive-bayes',
    name: 'Naive Bayes',
    description: 'Clasificador probabilístico Gaussian con ajuste de umbral F-beta (1.5).',
    category: 'ml',
    icon: <BrainCircuit className="w-5 h-5" />,
  },
```

- [ ] **Paso 5: Agregar naive-bayes a `SummariesResponse` en api.ts**

```typescript
  'naive-bayes'?: ModelMetrics;
```

- [ ] **Paso 6: Agregar GALLERY_CONFIGS para naive-bayes en App.tsx**

Dentro del objeto `GALLERY_CONFIGS`, agregar:

```typescript
  'naive-bayes': [
    {
      id: 'resultados',
      label: 'Modelo Optimizado',
      images: [
        { filename: 'naive_bayes_confusion_matrix.png', label: 'Matriz de Confusión', section: 'naive-bayes' },
        { filename: 'naive_bayes_roc_curve.png', label: 'Curva ROC', section: 'naive-bayes' },
        { filename: 'naive_bayes_precision_recall_curve.png', label: 'Precisión-Recall', section: 'naive-bayes' },
        { filename: 'naive_bayes_threshold_tradeoff.png', label: 'Análisis de Umbral', section: 'naive-bayes' },
        { filename: 'naive_bayes_model_comparison.png', label: 'Comparativa Base vs Optimizado', section: 'naive-bayes' },
      ],
    },
    {
      id: 'base',
      label: 'Modelo Base',
      images: [
        { filename: 'naive_bayes_confusion_matrix_base.png', label: 'Confusión (Base)', section: 'naive-bayes' },
        { filename: 'naive_bayes_roc_base.png', label: 'Curva ROC (Base)', section: 'naive-bayes' },
        { filename: 'naive_bayes_pr_base.png', label: 'Precisión-Recall (Base)', section: 'naive-bayes' },
        { filename: 'naive_bayes_target_distribution.png', label: 'Distribución del Target', section: 'naive-bayes' },
      ],
    },
  ],
```

- [ ] **Paso 7: Verificar que el servidor levanta y carga naive-bayes**

```bash
cd page && python -m uvicorn api.server:app --reload --port 8000
# Esperar salida: no debe aparecer [WARN] para naive-bayes
curl http://localhost:8000/api/health
# Esperado: {"status":"ok","loaded_models":["logistica","knn","decision-tree","salario","logistica-pca","decision-tree-pca","naive-bayes"]}
curl http://localhost:8000/api/summaries | python3 -m json.tool | grep naive
# Esperado: "naive-bayes": { ... }
```

- [ ] **Paso 8: Commit**

```bash
git add page/api/server.py page/src/App.tsx page/src/api.ts
git commit -m "feat: register Naive Bayes in server and dashboard"
```

---

## Task 2: Agregar celdas de exportación al notebook SVM

> El notebook SVM usa `pd.get_dummies` fuera del pipeline y no guarda PKL ni JSON.
> Se agregan celdas al **final** del notebook que construyen un pipeline estándar y exportan todos los artefactos.
> **Después de agregar las celdas, el usuario debe re-ejecutar el notebook completo.**
>
> **Files:**
> - Modify: `datalake_gold/SVM_offer_received.ipynb` — agregar 4 celdas al final

- [ ] **Paso 1: Agregar celda markdown de sección**

Agregar al final del notebook una celda Markdown:

```markdown
## Sección de exportación para producción

Pipeline estándar con `ColumnTransformer` (compatible con inferencia sobre nuevos CSV).
Genera PKL base (SVM Lineal), PKL mejorado (SVM RBF + umbral óptimo), curvas estándar y JSON summary.
```

- [ ] **Paso 2: Agregar celda de setup + pipeline base**

```python
from pathlib import Path
import pickle, json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, fbeta_score,
    roc_auc_score, average_precision_score, confusion_matrix,
    roc_curve, precision_recall_curve, ConfusionMatrixDisplay,
)
from sklearn.model_selection import train_test_split

SEED = 42

def resolve_root() -> Path:
    cwd = Path.cwd().resolve()
    for candidate in [cwd, *cwd.parents]:
        if (candidate / "datalake_silver").exists() and (candidate / "datalake_gold").exists():
            return candidate
    raise FileNotFoundError("No se encontró la raíz del proyecto con datalake_silver y datalake_gold.")

ROOT = resolve_root()
DATA_PATH = ROOT / "datalake_silver" / "cleanData" / "dataset_offer_Received.csv"
SVM_OUTPUT = ROOT / "datalake_gold" / "outputs_svm"
IMG_DIR = SVM_OUTPUT / "imagenes"
INF_DIR = SVM_OUTPUT / "informe"
IMG_DIR.mkdir(parents=True, exist_ok=True)
INF_DIR.mkdir(parents=True, exist_ok=True)

TARGET = "Offer_Received"
df_prod = pd.read_csv(DATA_PATH)
X_prod = df_prod.drop(columns=[TARGET])
y_prod = df_prod[TARGET].astype(int)

cat_cols = ["University_Rating", "Major_Category", "Region", "School_Size", "Primary_Search_Platform"]
num_cols = [c for c in X_prod.columns if c not in cat_cols]

X_train_p, X_test_p, y_train_p, y_test_p = train_test_split(
    X_prod, y_prod, test_size=0.2, random_state=SEED, stratify=y_prod
)

preprocessor = ColumnTransformer([
    ("num", StandardScaler(), num_cols),
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
])

# --- Pipeline BASE (SVM Lineal, probability=True) ---
base_pl = Pipeline([
    ("preprocessor", preprocessor),
    ("model", SVC(kernel="linear", C=1.0, probability=True, random_state=SEED)),
])
base_pl.fit(X_train_p, y_train_p)
base_proba = base_pl.predict_proba(X_test_p)[:, 1]
base_pred  = (base_proba >= 0.5).astype(int)

base_metrics = {
    "Accuracy":  accuracy_score(y_test_p, base_pred),
    "Precision": precision_score(y_test_p, base_pred, zero_division=0),
    "Recall":    recall_score(y_test_p, base_pred, zero_division=0),
    "F1-Score":  f1_score(y_test_p, base_pred, zero_division=0),
    "F-beta (1.5)": fbeta_score(y_test_p, base_pred, beta=1.5, zero_division=0),
    "ROC-AUC":   roc_auc_score(y_test_p, base_proba),
}

with open(INF_DIR / "svm_offer_received_base.pkl", "wb") as f:
    pickle.dump({
        "pipeline": base_pl,
        "best_threshold": 0.5,
        "best_params": {"kernel": "linear", "C": 1.0},
        "feature_columns": X_prod.columns.tolist(),
        "numeric_columns": num_cols,
        "categorical_columns": cat_cols,
        "metrics_default_threshold": base_metrics,
        "metrics_optimized_threshold": base_metrics,
        "target_name": TARGET,
        "model_stage": "baseline",
    }, f)
print("Base PKL guardado:", INF_DIR / "svm_offer_received_base.pkl")
print("Métricas base:", {k: round(v, 4) for k, v in base_metrics.items()})
```

- [ ] **Paso 3: Agregar celda del pipeline mejorado + threshold sweep + PKL**

> ⚠️ `SVC(kernel='rbf', probability=True)` sobre 80k filas puede tardar 15-30 minutos.

```python
# --- Pipeline MEJORADO (SVM RBF + umbral óptimo) ---
improved_pl = Pipeline([
    ("preprocessor", preprocessor),
    ("model", SVC(kernel="rbf", C=10.0, gamma="scale", probability=True, random_state=SEED)),
])
improved_pl.fit(X_train_p, y_train_p)
imp_proba = improved_pl.predict_proba(X_test_p)[:, 1]

# Threshold sweep
thr_rows = []
for t in np.arange(0.05, 0.96, 0.01):
    pred_t = (imp_proba >= t).astype(int)
    thr_rows.append({
        "threshold": float(round(t, 2)),
        "precision": float(precision_score(y_test_p, pred_t, zero_division=0)),
        "recall":    float(recall_score(y_test_p, pred_t, zero_division=0)),
        "f1":        float(f1_score(y_test_p, pred_t, zero_division=0)),
        "f_beta_1_5": float(fbeta_score(y_test_p, pred_t, beta=1.5, zero_division=0)),
    })
thr_df = pd.DataFrame(thr_rows)
best_t  = float(thr_df.sort_values(["f_beta_1_5", "recall", "precision"], ascending=False).iloc[0]["threshold"])

imp_pred_opt = (imp_proba >= best_t).astype(int)
imp_pred_050 = (imp_proba >= 0.5).astype(int)

def _m(y_true, y_pred, y_score):
    return {
        "Accuracy":     accuracy_score(y_true, y_pred),
        "Precision":    precision_score(y_true, y_pred, zero_division=0),
        "Recall":       recall_score(y_true, y_pred, zero_division=0),
        "F1-Score":     f1_score(y_true, y_pred, zero_division=0),
        "F-beta (1.5)": fbeta_score(y_true, y_pred, beta=1.5, zero_division=0),
        "ROC-AUC":      roc_auc_score(y_true, y_score),
    }

metrics_050 = _m(y_test_p, imp_pred_050, imp_proba)
metrics_opt = _m(y_test_p, imp_pred_opt, imp_proba)
cm_opt = confusion_matrix(y_test_p, imp_pred_opt, labels=[1, 0])
tp, fn, fp, tn = cm_opt.ravel()

with open(INF_DIR / "svm_offer_received_improved.pkl", "wb") as f:
    pickle.dump({
        "pipeline": improved_pl,
        "best_threshold": best_t,
        "best_params": {"kernel": "rbf", "C": 10.0, "gamma": "scale"},
        "feature_columns": X_prod.columns.tolist(),
        "numeric_columns": num_cols,
        "categorical_columns": cat_cols,
        "metrics_default_threshold": metrics_050,
        "metrics_optimized_threshold": metrics_opt,
        "target_name": TARGET,
        "model_stage": "improved",
    }, f)
print(f"Improved PKL guardado — umbral óptimo: {best_t:.3f}")
print("Métricas optimizadas:", {k: round(v, 4) for k, v in metrics_opt.items()})
```

- [ ] **Paso 4: Agregar celda de gráficas estándar + JSON summary**

```python
# --- Gráficas estándar ---
fpr_b, tpr_b, _ = roc_curve(y_test_p, base_proba)
fpr_i, tpr_i, _ = roc_curve(y_test_p, imp_proba)

# ROC comparativa
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(fpr_b, tpr_b, linewidth=2, label=f'SVM Lineal — AUC={base_metrics["ROC-AUC"]:.4f}')
ax.plot(fpr_i, tpr_i, linewidth=2, color="#d62728", label=f'SVM RBF — AUC={metrics_opt["ROC-AUC"]:.4f}')
ax.plot([0, 1], [0, 1], "--", color="gray")
ax.set(xlabel="FPR", ylabel="TPR", title="Curva ROC — SVM")
ax.legend(loc="lower right"); ax.grid(True, alpha=0.25)
fig.savefig(IMG_DIR / "svm_roc_curve.png", dpi=160, bbox_inches="tight"); plt.show()

# ROC base
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(fpr_b, tpr_b, linewidth=2, color="#1f77b4", label=f'AUC={base_metrics["ROC-AUC"]:.4f}')
ax.plot([0, 1], [0, 1], "--", color="gray")
ax.set(xlabel="FPR", ylabel="TPR", title="Curva ROC (Base - SVM Lineal)")
ax.legend(loc="lower right"); ax.grid(True, alpha=0.25)
fig.savefig(IMG_DIR / "svm_roc_curve_base.png", dpi=160, bbox_inches="tight"); plt.show()

# Confusion matrix optimized
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
ConfusionMatrixDisplay(confusion_matrix=cm_opt, display_labels=["SI OFERTA (1)", "NO OFERTA (0)"]).plot(
    cmap="Blues", ax=axes[0], values_format="d", colorbar=False)
axes[0].set_title(f"Matriz de Confusión — Umbral {best_t:.2f}")
cm_norm = cm_opt.astype(float) / cm_opt.sum(axis=1, keepdims=True)
ConfusionMatrixDisplay(confusion_matrix=cm_norm, display_labels=["SI OFERTA (1)", "NO OFERTA (0)"]).plot(
    cmap="Greens", ax=axes[1], values_format=".2f", colorbar=False)
axes[1].set_title("Matriz de Confusión — Proporción")
fig.savefig(IMG_DIR / "svm_confusion_matrix.png", dpi=160, bbox_inches="tight"); plt.show()

# Confusion matrix base
cm_b = confusion_matrix(y_test_p, base_pred, labels=[1, 0])
fig, ax = plt.subplots(figsize=(6, 5))
ConfusionMatrixDisplay(confusion_matrix=cm_b, display_labels=["SI OFERTA (1)", "NO OFERTA (0)"]).plot(
    ax=ax, cmap="Blues", colorbar=False, values_format="d")
ax.set_title("Matriz de Confusión (Base - SVM Lineal)")
fig.savefig(IMG_DIR / "svm_confusion_matrix_base.png", dpi=160, bbox_inches="tight"); plt.show()

# Precision-Recall improved
prec_i, rec_i, _ = precision_recall_curve(y_test_p, imp_proba)
ap_i = average_precision_score(y_test_p, imp_proba)
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(rec_i, prec_i, linewidth=2, color="#d95f02", label=f"AP={ap_i:.4f}")
ax.set(xlabel="Recall", ylabel="Precision", title="Curva Precision-Recall — SVM RBF")
ax.legend(); ax.grid(True, alpha=0.25)
fig.savefig(IMG_DIR / "svm_precision_recall_curve.png", dpi=160, bbox_inches="tight"); plt.show()

# Precision-Recall base
prec_b, rec_b, _ = precision_recall_curve(y_test_p, base_proba)
ap_b = average_precision_score(y_test_p, base_proba)
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(rec_b, prec_b, linewidth=2, color="#1f77b4", label=f"AP={ap_b:.4f}")
ax.set(xlabel="Recall", ylabel="Precision", title="Curva Precision-Recall (Base - SVM Lineal)")
ax.legend(); ax.grid(True, alpha=0.25)
fig.savefig(IMG_DIR / "svm_pr_base.png", dpi=160, bbox_inches="tight"); plt.show()

# Threshold tradeoff
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(thr_df["threshold"], thr_df["precision"], label="Precision", linewidth=2)
ax.plot(thr_df["threshold"], thr_df["recall"],    label="Recall",    linewidth=2)
ax.plot(thr_df["threshold"], thr_df["f_beta_1_5"],label="F-beta (1.5)", linewidth=2)
ax.axvline(best_t, color="black", linestyle="--", label=f"Umbral óptimo = {best_t:.2f}")
ax.set(xlabel="Threshold", ylabel="Valor de métrica", title="Trade-off de umbral — SVM RBF")
ax.legend(); ax.grid(True, alpha=0.25)
fig.savefig(IMG_DIR / "svm_threshold_tradeoff.png", dpi=160, bbox_inches="tight"); plt.show()

# Comparativa modelos
metric_names = ["Accuracy", "Precision", "Recall", "F1-Score"]
x = np.arange(len(metric_names)); w = 0.35
fig, ax = plt.subplots(figsize=(9, 5))
ax.bar(x - w/2, [base_metrics[m] for m in metric_names], w, label="SVM Lineal (Base)", color="#1f77b4")
ax.bar(x + w/2, [metrics_opt[m] for m in metric_names], w,  label="SVM RBF (Optimizado)", color="#d62728")
ax.set_xticks(x); ax.set_xticklabels(metric_names)
ax.set(ylabel="Valor", title="Comparativa: SVM Lineal vs RBF"); ax.set_ylim(0, 1)
ax.legend(); ax.grid(axis="y", alpha=0.25)
fig.savefig(IMG_DIR / "svm_model_comparison.png", dpi=160, bbox_inches="tight"); plt.show()

# --- JSON Summary ---
SUMMARY_PATH = INF_DIR / "svm_offer_received_summary.json"

def make_jsonable(value):
    if isinstance(value, Path): return str(value)
    if isinstance(value, pd.DataFrame): return json.loads(value.to_json(orient="records", force_ascii=False))
    if isinstance(value, pd.Series):    return json.loads(value.to_json(force_ascii=False))
    if isinstance(value, dict):   return {str(k): make_jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)): return [make_jsonable(i) for i in value]
    if isinstance(value, np.generic): return value.item()
    return value

summary = {
    "model_name": "SVM_RBF",
    "target": TARGET,
    "best_threshold": best_t,
    "best_params": {"kernel": "rbf", "C": 10.0, "gamma": "scale"},
    "metrics": {
        "threshold_0_50": metrics_050,
        "threshold_optimized": metrics_opt,
    },
    "confusion_matrix": {"tp": int(tp), "fn": int(fn), "fp": int(fp), "tn": int(tn)},
    "threshold_preview": thr_df.sort_values("threshold").head(20),
}
with open(SUMMARY_PATH, "w", encoding="utf-8") as f:
    json.dump(make_jsonable(summary), f, indent=2, ensure_ascii=False)
print(f"Summary JSON guardado: {SUMMARY_PATH}")
print("Todos los artefactos SVM generados correctamente.")
```

- [ ] **Paso 5: Re-ejecutar el notebook completo**

Abrir `datalake_gold/SVM_offer_received.ipynb` en Jupyter/VS Code y ejecutar **Restart & Run All**.

Verificar que aparezcan al final:
```
Base PKL guardado: .../outputs_svm/informe/svm_offer_received_base.pkl
Improved PKL guardado — umbral óptimo: 0.XXX
Summary JSON guardado: .../outputs_svm/informe/svm_offer_received_summary.json
Todos los artefactos SVM generados correctamente.
```

- [ ] **Paso 6: Verificar archivos generados**

```bash
ls /Users/apple/mineria/datalake_gold/outputs_svm/informe/
# Esperado: svm_offer_received_base.pkl  svm_offer_received_improved.pkl  svm_offer_received_summary.json
ls /Users/apple/mineria/datalake_gold/outputs_svm/imagenes/
# Esperado: svm_confusion_matrix.png  svm_roc_curve.png  svm_precision_recall_curve.png  svm_threshold_tradeoff.png  ...
```

- [ ] **Paso 7: Commit (solo el notebook, no los artefactos binarios)**

```bash
git add datalake_gold/SVM_offer_received.ipynb
git commit -m "feat: add production export section to SVM notebook"
```

---

## Task 3: Registrar SVM en servidor y frontend

> **Requiere que Task 2 haya sido ejecutado** (PKL y JSON deben existir).
>
> **Files:**
> - Modify: `page/api/server.py`
> - Modify: `page/src/App.tsx`
> - Modify: `page/src/api.ts`

- [ ] **Paso 1: Agregar svm a MODEL_CONFIGS en server.py**

```python
    "svm": {
        "pkl": ROOT / "datalake_gold/outputs_svm/informe/svm_offer_received_improved.pkl",
        "summary": ROOT / "datalake_gold/outputs_svm/informe/svm_offer_received_summary.json",
        "type": "classification",
    },
```

- [ ] **Paso 2: Agregar rama `svm` a `_normalize_metrics`**

El JSON de SVM tiene la misma estructura que naive-bayes. Extender el `elif` existente:

```python
    elif model_id in ("naive-bayes", "svm"):
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
```

- [ ] **Paso 3: Agregar `svm` a `_IMAGE_DIRS`**

```python
    "svm": ROOT / "datalake_gold/outputs_svm/imagenes",
```

- [ ] **Paso 4: Agregar svm a `ModelID` y `MODEL_DEFINITIONS` en App.tsx**

Actualizar el tipo (acumular con el de Task 1):

```typescript
type ModelID = 'eda' | 'logistica' | 'knn' | 'decision-tree' | 'salario' | 'logistica-pca' | 'decision-tree-pca' | 'naive-bayes' | 'svm';
```

En `MODEL_DEFINITIONS`, agregar después de `naive-bayes`:

```typescript
  {
    id: 'svm',
    name: 'Support Vector Machine',
    description: 'SVM con kernel RBF y threshold F-beta para clasificación de oferta laboral.',
    category: 'ml',
    icon: <BrainCircuit className="w-5 h-5" />,
  },
```

- [ ] **Paso 5: Agregar `svm` a SummariesResponse en api.ts**

```typescript
  svm?: ModelMetrics;
```

- [ ] **Paso 6: Agregar GALLERY_CONFIGS para svm en App.tsx**

```typescript
  svm: [
    {
      id: 'optimizado',
      label: 'Modelo Optimizado (RBF)',
      images: [
        { filename: 'svm_confusion_matrix.png',         label: 'Matriz de Confusión',    section: 'svm' },
        { filename: 'svm_roc_curve.png',                label: 'Curva ROC',              section: 'svm' },
        { filename: 'svm_precision_recall_curve.png',   label: 'Precisión-Recall',       section: 'svm' },
        { filename: 'svm_threshold_tradeoff.png',       label: 'Análisis de Umbral',     section: 'svm' },
        { filename: 'svm_model_comparison.png',         label: 'Comparativa Base vs RBF',section: 'svm' },
      ],
    },
    {
      id: 'base',
      label: 'Modelo Base (Lineal)',
      images: [
        { filename: 'svm_confusion_matrix_base.png',    label: 'Confusión (Base)',        section: 'svm' },
        { filename: 'svm_roc_curve_base.png',           label: 'Curva ROC (Base)',        section: 'svm' },
        { filename: 'svm_pr_base.png',                  label: 'Precisión-Recall (Base)', section: 'svm' },
        { filename: 'comparativa_modelos_svm.png',      label: 'Comparativa Original',    section: 'svm' },
        { filename: 'efecto_C_svm_rbf.png',             label: 'Efecto de C',             section: 'svm' },
      ],
    },
  ],
```

- [ ] **Paso 7: Verificar servidor + frontend**

```bash
cd page && python -m uvicorn api.server:app --reload --port 8000
curl http://localhost:8000/api/health
# loaded_models debe incluir "svm"
curl http://localhost:8000/api/summaries | python3 -m json.tool | grep '"svm"'
```

En el browser, abrir `http://localhost:3000`, ingresar al dashboard y verificar que "Support Vector Machine" aparece en el sidebar bajo "Modelos Estándar".

- [ ] **Paso 8: Commit**

```bash
git add page/api/server.py page/src/App.tsx page/src/api.ts
git commit -m "feat: register SVM in server and dashboard"
```

---

## Task 4: Agregar artefactos al notebook de Clustering

> Clustering es **no supervisado**: no predice etiquetas para nuevos datos, por lo que NO puede ser un modelo de predicción del servidor.
> Se integra como **vista de análisis estática** (igual que EDA), mostrando perfiles de clusters e imágenes.
> Se agregan celdas al final del notebook para guardar imágenes, JSON de perfiles y PKL en rutas estándar.
>
> **Files:**
> - Modify: `datalake_gold/Clustering_Jerarquico_DBSCAN_job.ipynb` — agregar celdas al final

- [ ] **Paso 1: Agregar celda de setup de rutas y guardado de imágenes clave**

Agregar al final del notebook una celda que define rutas estándar y guarda las visualizaciones principales:

```python
# === Exportación de artefactos de clustering ===
from pathlib import Path
import pickle, json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def resolve_root() -> Path:
    cwd = Path.cwd().resolve()
    for candidate in [cwd, *cwd.parents]:
        if (candidate / "datalake_silver").exists() and (candidate / "datalake_gold").exists():
            return candidate
    raise FileNotFoundError("No se encontró la raíz del proyecto.")

ROOT = resolve_root()
CLUST_OUTPUT = ROOT / "datalake_gold" / "outputs_clustering"
IMG_DIR = CLUST_OUTPUT / "imagenes"
INF_DIR = CLUST_OUTPUT / "informe"
IMG_DIR.mkdir(parents=True, exist_ok=True)
INF_DIR.mkdir(parents=True, exist_ok=True)

# -- Scatter KMeans (usando variables ya calculadas del notebook: X_pca, km_labels) --
fig, ax = plt.subplots(figsize=(9, 6))
colors_plot = ["#991b1b", "#1d4ed8"]
labels_plot = [f"Cluster {i} ({int((km_labels==i).sum()):,} estudiantes)" for i in range(K_OPTIMO)]
for i in range(K_OPTIMO):
    mask = km_labels == i
    ax.scatter(X_pca[mask, 0], X_pca[mask, 1], c=colors_plot[i], alpha=0.3, s=4, label=labels_plot[i])
ax.set_title("KMeans k=2 — Proyección PCA 2D")
ax.set_xlabel("PC1"); ax.set_ylabel("PC2")
ax.legend(markerscale=4)
plt.tight_layout()
fig.savefig(IMG_DIR / "clustering_kmeans_scatter.png", dpi=160, bbox_inches="tight")
plt.show()

# -- Silhouette comparison chart --
sil_labels   = ["KMeans k=2", "Jerárquico k=2", f"DBSCAN eps={EPS_INICIAL}"]
sil_values   = [
    float(sil_km)   if not np.isnan(float(sil_km))   else 0.0,
    float(sil_hier) if not np.isnan(float(sil_hier)) else 0.0,
    float(sil_db)   if (sil_db == sil_db) else 0.0,
]
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(sil_labels, sil_values, color=["#991b1b", "#1d4ed8", "#059669"])
ax.set_ylabel("Silhouette Score"); ax.set_title("Comparación de Silhouette Score por Algoritmo")
ax.set_ylim(0, 0.3)
for bar, val in zip(bars, sil_values):
    ax.text(bar.get_x() + bar.get_width()/2, val + 0.005, f"{val:.4f}", ha="center", fontsize=10)
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
fig.savefig(IMG_DIR / "clustering_silhouette_comparison.png", dpi=160, bbox_inches="tight")
plt.show()

# -- Tabla cruzada KMeans (offer rate por cluster) --
ct_km_full = pd.crosstab(km_labels, y_real,
                          rownames=["Cluster KMeans"], colnames=["Offer_Received"])
ct_km_full.columns = ["No oferta (0)", "Recibe oferta (1)"]
pct_km_full = ct_km_full.div(ct_km_full.sum(axis=1), axis=0) * 100

fig, ax = plt.subplots(figsize=(7, 4))
pct_plot = pct_km_full.reset_index().melt(id_vars="Cluster KMeans")
colors_ct = {"No oferta (0)": "#64748b", "Recibe oferta (1)": "#991b1b"}
for i, (_, row) in enumerate(pct_km_full.iterrows()):
    ax.bar([i - 0.2, i + 0.2],
           [row["No oferta (0)"], row["Recibe oferta (1)"]],
           width=0.35,
           color=["#64748b", "#991b1b"])
ax.set_xticks([0, 1])
ax.set_xticklabels([f"Cluster 0\n({cluster_profiles[0]['plataforma_dominante']})",
                    f"Cluster 1\n({cluster_profiles[1]['plataforma_dominante']})"])
ax.set_ylabel("% de estudiantes"); ax.set_title("Distribución de Offer_Received por Cluster")
ax.axhline(y_real.mean()*100, color="black", linestyle="--", label=f"Baseline {y_real.mean()*100:.1f}%")
ax.legend(); ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
fig.savefig(IMG_DIR / "clustering_offer_rate_by_cluster.png", dpi=160, bbox_inches="tight")
plt.show()

print("Imágenes guardadas en:", IMG_DIR)
```

- [ ] **Paso 2: Agregar celda de PKL estándar y JSON summary**

```python
# -- PKL estándar de KMeans --
kmeans_pkl_path = INF_DIR / "clustering_kmeans.pkl"
artefacto_std = {
    "modelo": km_model,
    "scaler": scaler,
    "feature_columns_originales": FEATURE_COLS,
    "feature_names_encoded": X_encoded.columns.tolist(),
    "numeric_cols": NUM_COLS,
    "categorical_cols": CAT_COLS,
    "k_optimo": K_OPTIMO,
    "silhouette_score": float(sil_km),
    "cluster_profiles": cluster_profiles,
}
with open(kmeans_pkl_path, "wb") as f:
    pickle.dump(artefacto_std, f)
print(f"PKL guardado: {kmeans_pkl_path}")

# -- JSON Summary --
SUMMARY_PATH = INF_DIR / "clustering_summary.json"

def make_jsonable(value):
    if isinstance(value, Path): return str(value)
    if isinstance(value, pd.DataFrame): return json.loads(value.to_json(orient="records", force_ascii=False))
    if isinstance(value, pd.Series):    return json.loads(value.to_json(force_ascii=False))
    if isinstance(value, dict):   return {str(k): make_jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)): return [make_jsonable(i) for i in value]
    if isinstance(value, np.generic): return value.item()
    return value

# Tabla cruzada serializable
crosstab_data = []
for cluster_id in range(K_OPTIMO):
    mask = km_labels == cluster_id
    crosstab_data.append({
        "cluster": int(cluster_id),
        "n_estudiantes": int(mask.sum()),
        "no_oferta": int((y_real[mask] == 0).sum()),
        "si_oferta": int((y_real[mask] == 1).sum()),
        "offer_rate_pct": round(float(y_real[mask].mean() * 100), 2),
        "plataforma_dominante": str(cluster_profiles[cluster_id]["plataforma_dominante"]),
        "aplicaciones_promedio": round(float(cluster_profiles[cluster_id]["aplicaciones_promedio"]), 1),
        "meses_busqueda_promedio": round(float(cluster_profiles[cluster_id]["meses_busqueda_promedio"]), 1),
        "entrevistas_primera_ronda": round(float(cluster_profiles[cluster_id]["entrevistas_primera_ronda"]), 2),
    })

summary = {
    "dataset_size": int(len(y_real)),
    "baseline_offer_rate_pct": round(float(y_real.mean() * 100), 2),
    "algorithms": {
        "kmeans": {
            "k": K_OPTIMO,
            "silhouette": round(float(sil_km), 4),
            "dunn": round(float(dunn_km), 4),
            "cluster_profiles": crosstab_data,
        },
        "jerarquico": {
            "k": 2,
            "silhouette": round(float(sil_hier), 4) if not np.isnan(sil_hier) else None,
            "dunn": round(float(dunn_hier), 4) if not np.isnan(dunn_hier) else None,
            "sample_size": HIER_SAMPLE,
        },
        "dbscan": {
            "eps": EPS_INICIAL,
            "min_samples": MIN_SAMPLES,
            "n_clusters": n_clusters_db,
            "n_ruido": n_ruido_db,
            "silhouette": round(float(sil_db), 4) if (sil_db == sil_db) else None,
        },
    },
    "conclusion": "No se encontraron clusters naturales alineados con empleabilidad. KMeans separó por plataforma de búsqueda (Handshake vs LinkedIn/Indeed), no por resultado laboral.",
    "images": {
        "kmeans_scatter": str(IMG_DIR / "clustering_kmeans_scatter.png"),
        "silhouette_comparison": str(IMG_DIR / "clustering_silhouette_comparison.png"),
        "offer_rate_by_cluster": str(IMG_DIR / "clustering_offer_rate_by_cluster.png"),
    },
}

with open(SUMMARY_PATH, "w", encoding="utf-8") as f:
    json.dump(make_jsonable(summary), f, indent=2, ensure_ascii=False)
print(f"Summary JSON guardado: {SUMMARY_PATH}")
print("✓ Exportación de clustering completa.")
```

- [ ] **Paso 3: Re-ejecutar el notebook completo**

Abrir `datalake_gold/Clustering_Jerarquico_DBSCAN_job.ipynb` y ejecutar **Restart & Run All**.

> ⚠️ El notebook tarda varios minutos por el dendrograma (5k filas) y el barrido de DBSCAN.

Verificar salida final:
```
PKL guardado: .../outputs_clustering/informe/clustering_kmeans.pkl
Summary JSON guardado: .../outputs_clustering/informe/clustering_summary.json
✓ Exportación de clustering completa.
```

- [ ] **Paso 4: Commit del notebook**

```bash
git add datalake_gold/Clustering_Jerarquico_DBSCAN_job.ipynb
git commit -m "feat: add artifact export section to Clustering notebook"
```

---

## Task 5: Integrar Clustering en servidor y frontend como vista de análisis

> **Requiere Task 4 completado** (JSON debe existir).
> Clustering se expone como endpoint de solo lectura `/api/clustering` y se renderiza como vista de análisis (similar a EDA, sin panel de predicción).
>
> **Files:**
> - Modify: `page/api/server.py`
> - Modify: `page/src/App.tsx`
> - Modify: `page/src/api.ts`

- [ ] **Paso 1: Agregar endpoint `/api/clustering` en server.py**

Después del endpoint `/api/eda`:

```python
@app.get("/api/clustering")
def get_clustering():
    summary_path = ROOT / "datalake_gold/outputs_clustering/informe/clustering_summary.json"
    if not summary_path.is_file():
        raise HTTPException(404, "clustering_summary.json no encontrado. Re-ejecuta el notebook de clustering.")
    with open(summary_path, encoding="utf-8") as f:
        return json.load(f)
```

Agregar `clustering` a `_IMAGE_DIRS`:

```python
    "clustering": ROOT / "datalake_gold/outputs_clustering/imagenes",
```

- [ ] **Paso 2: Agregar tipo `ClusteringResponse` en api.ts**

```typescript
export interface ClusterProfile {
  cluster: number;
  n_estudiantes: number;
  no_oferta: number;
  si_oferta: number;
  offer_rate_pct: number;
  plataforma_dominante: string;
  aplicaciones_promedio: number;
  meses_busqueda_promedio: number;
  entrevistas_primera_ronda: number;
}

export interface ClusteringResponse {
  dataset_size: number;
  baseline_offer_rate_pct: number;
  algorithms: {
    kmeans: { k: number; silhouette: number; dunn: number; cluster_profiles: ClusterProfile[] };
    jerarquico: { k: number; silhouette: number | null; dunn: number | null; sample_size: number };
    dbscan: { eps: number; min_samples: number; n_clusters: number; n_ruido: number; silhouette: number | null };
  };
  conclusion: string;
}

export async function fetchClustering(): Promise<ClusteringResponse> {
  return apiFetch<ClusteringResponse>('/api/clustering');
}
```

- [ ] **Paso 3: Agregar `clustering` al tipo ModelID y MODEL_DEFINITIONS en App.tsx**

```typescript
type ModelID = 'eda' | 'logistica' | 'knn' | 'decision-tree' | 'salario' | 'logistica-pca' | 'decision-tree-pca' | 'naive-bayes' | 'svm' | 'clustering';
```

En `MODEL_DEFINITIONS`:

```typescript
  {
    id: 'clustering',
    name: 'Análisis de Clustering',
    description: 'KMeans, Clustering Jerárquico y DBSCAN sobre perfiles de estudiantes.',
    category: 'analysis',
    icon: <Users className="w-5 h-5" />,
  },
```

- [ ] **Paso 4: Agregar componente `ClusteringView` en App.tsx**

Agregar después del componente `EDAView`:

```typescript
const ClusteringView = ({ apiOnline }: { apiOnline: boolean }) => {
  const [data, setData] = useState<ClusteringResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!apiOnline) { setLoading(false); return; }
    fetchClustering()
      .then(setData)
      .catch(() => setData(null))
      .finally(() => setLoading(false));
  }, [apiOnline]);

  if (loading) return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      {[...Array(3)].map((_, i) => (
        <div key={i} className="card p-6 animate-pulse"><div className="h-4 bg-slate-100 rounded w-24 mb-3" /><div className="h-8 bg-slate-200 rounded w-32" /></div>
      ))}
    </div>
  );

  if (!data) return (
    <div className="card p-8 flex items-center gap-4 border-amber-200 bg-amber-50">
      <AlertCircle className="w-6 h-6 text-amber-500 shrink-0" />
      <div>
        <p className="font-bold text-amber-800">API no disponible</p>
        <p className="text-sm text-amber-700">Inicia el servidor con: <code className="bg-amber-100 px-1 rounded">python -m uvicorn api.server:app --reload --port 8000</code></p>
      </div>
    </div>
  );

  const km = data.algorithms.kmeans;
  const hier = data.algorithms.jerarquico;
  const db = data.algorithms.dbscan;
  const COLORS_C = ['#991b1b', '#1d4ed8'];

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      {/* KPIs */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <KPICard title="Silhouette KMeans" value={km.silhouette.toFixed(4)} icon={<Database className="w-6 h-6" />} sub={`k=${km.k} · estructura débil < 0.10`} />
        <KPICard title="Silhouette Jerárquico" value={hier.silhouette?.toFixed(4) ?? '—'} icon={<Users className="w-6 h-6" />} sub={`muestra ${hier.sample_size.toLocaleString('es-CO')} filas`} />
        <KPICard title="DBSCAN Clusters" value={String(db.n_clusters)} icon={<Search className="w-6 h-6" />} sub={`eps=${db.eps} · ${db.n_ruido.toLocaleString('es-CO')} puntos ruido`} />
      </div>

      {/* Perfiles de clusters KMeans */}
      <div className="card p-6">
        <h4 className="text-lg font-bold mb-4 flex items-center gap-2">
          <Users className="w-5 h-5 text-red-800" />
          Perfiles de Clusters — KMeans (k=2)
        </h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {km.cluster_profiles.map((p) => (
            <div key={p.cluster} className="bg-slate-50 rounded-xl p-5 border border-slate-100">
              <div className="flex items-center justify-between mb-4">
                <h5 className="font-bold text-slate-800">Cluster {p.cluster}</h5>
                <span className="text-xs font-bold px-2 py-1 rounded-full" style={{ background: COLORS_C[p.cluster] + '22', color: COLORS_C[p.cluster] }}>
                  {p.n_estudiantes.toLocaleString('es-CO')} est.
                </span>
              </div>
              <div className="grid grid-cols-2 gap-3 text-sm">
                <div><p className="text-slate-400 text-xs font-bold uppercase">Plataforma</p><p className="font-bold text-red-800">{p.plataforma_dominante}</p></div>
                <div><p className="text-slate-400 text-xs font-bold uppercase">Tasa de Oferta</p><p className="font-bold text-slate-800">{p.offer_rate_pct.toFixed(1)}%</p></div>
                <div><p className="text-slate-400 text-xs font-bold uppercase">Aplicaciones Avg</p><p className="font-bold text-slate-800">{p.aplicaciones_promedio}</p></div>
                <div><p className="text-slate-400 text-xs font-bold uppercase">Meses Búsqueda</p><p className="font-bold text-slate-800">{p.meses_busqueda_promedio}</p></div>
              </div>
            </div>
          ))}
        </div>
        <div className="mt-4 p-4 bg-slate-900 text-slate-300 rounded-xl text-sm">
          <p className="font-bold text-white mb-1">Hallazgo principal</p>
          <p>{data.conclusion}</p>
        </div>
      </div>

      {/* Galería de imágenes */}
      <div className="card p-6">
        <ImageGallery
          tabs={[{
            id: 'resultados',
            label: 'Visualizaciones',
            images: [
              { filename: 'clustering_kmeans_scatter.png',       label: 'KMeans — Proyección PCA 2D', section: 'clustering' },
              { filename: 'clustering_silhouette_comparison.png',label: 'Comparativa Silhouette',     section: 'clustering' },
              { filename: 'clustering_offer_rate_by_cluster.png',label: 'Tasa de Oferta por Cluster', section: 'clustering' },
            ],
          }]}
          title="Visualizaciones de Clustering"
        />
      </div>
    </div>
  );
};
```

Agregar la importación de `fetchClustering` y `ClusteringResponse` desde `./api` en la línea de imports de App.tsx.

- [ ] **Paso 5: Conectar `ClusteringView` en el render del dashboard en App.tsx**

En la sección del `main` donde se renderiza el contenido, extender el condicional:

```typescript
{activePage === 'eda' ? (
  <EDAView apiOnline={apiOnline} />
) : activePage === 'clustering' ? (
  <ClusteringView apiOnline={apiOnline} />
) : (
  <ModelView model={activeModel} apiOnline={apiOnline} />
)}
```

- [ ] **Paso 6: Verificar servidor + frontend**

```bash
cd page && python -m uvicorn api.server:app --reload --port 8000
curl http://localhost:8000/api/clustering | python3 -m json.tool | head -30
# Esperado: { "dataset_size": 100000, "baseline_offer_rate_pct": 34.229, ... }
```

Abrir `http://localhost:3000`, ingresar al dashboard y verificar que "Análisis de Clustering" aparece en el sidebar bajo "Análisis Principal" y muestra los perfiles de clusters.

- [ ] **Paso 7: Commit final**

```bash
git add page/api/server.py page/src/App.tsx page/src/api.ts
git commit -m "feat: add Clustering analysis view to server and dashboard"
```

---

## Self-Review

**Spec coverage:**
- ✅ Naive Bayes: PKL existente → registrado en server + frontend con galería
- ✅ SVM: nuevas celdas generan PKL+JSON+plots estándar → registrado en server + frontend
- ✅ Clustering: nuevo endpoint `/api/clustering` + vista de análisis con perfiles + galería

**Placeholder scan:** Ninguno detectado. Todos los pasos tienen código completo.

**Type consistency:**
- `ClusteringResponse` definido en api.ts, importado en App.tsx
- `ClusterProfile` usado en `ClusteringView` coincide con la interfaz
- `ModelID` actualizado consistentemente en Tasks 1, 3 y 5
- `_normalize_metrics` para `"naive-bayes"` y `"svm"` combinados en un `elif` en Task 3

**Dependencias entre tasks:**
- Task 3 requiere Task 2 ejecutado (PKL/JSON deben existir en disco)
- Task 5 requiere Task 4 ejecutado (JSON de clustering debe existir)
- Tasks 1, 2 y 4 son independientes entre sí
