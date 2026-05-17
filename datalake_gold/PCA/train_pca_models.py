"""
Entrena Regresión Logística y Árbol de Decisión con PCA (90% varianza).
Produce pkl, JSON de resumen e imágenes para cada modelo.
"""
import warnings
warnings.filterwarnings('ignore')

import pickle
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, fbeta_score,
    roc_auc_score, average_precision_score,
    confusion_matrix, roc_curve, precision_recall_curve,
)

ROOT = Path(__file__).parent.parent.parent   # → Medallion/

FEATURE_COLS = [
    'GPA', 'University_Rating', 'Major_Category', 'Region',
    'Prior_Internships', 'Extra_Curricular_Activities',
    'Networking_Events_Attended', 'School_Size', 'Primary_Search_Platform',
    'Months_Searching', 'Applications_Submitted',
    'First_Round_Interviews', 'Second_Round_Intervals',
]
NUMERIC_COLS = [
    'GPA', 'Prior_Internships', 'Extra_Curricular_Activities',
    'Networking_Events_Attended', 'Months_Searching',
    'Applications_Submitted', 'First_Round_Interviews', 'Second_Round_Interviews',
]
CATEGORICAL_COLS = [
    'University_Rating', 'Major_Category', 'Region',
    'School_Size', 'Primary_Search_Platform',
]
FEATURE_COLS = NUMERIC_COLS + CATEGORICAL_COLS   # re-derive clean list
TARGET = 'Offer_Received'

plt.rcParams.update({
    'figure.facecolor': 'white',
    'axes.facecolor': '#f8fafc',
    'axes.grid': True,
    'grid.alpha': 0.35,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'font.family': 'sans-serif',
})
RED = '#991b1b'
RED2 = '#dc2626'
BLUE = '#3b82f6'
GREEN = '#10b981'


def load_data():
    path = ROOT / 'datalake_silver/cleanData/dataset_offer_Received.csv'
    df = pd.read_csv(path)
    X = df[FEATURE_COLS]
    y = df[TARGET]
    return train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)


def make_preprocessor():
    return ColumnTransformer([
        ('num', StandardScaler(), NUMERIC_COLS),
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), CATEGORICAL_COLS),
    ])


def best_threshold(y_true, proba, beta=1.5):
    thresholds = np.arange(0.05, 0.95, 0.005)
    best_t, best_fb = 0.5, 0.0
    for t in thresholds:
        fb = fbeta_score(y_true, (proba >= t).astype(int), beta=beta, zero_division=0)
        if fb > best_fb:
            best_fb, best_t = fb, t
    return round(float(best_t), 4)


def metrics_at(y_true, proba, threshold):
    preds = (proba >= threshold).astype(int)
    return {
        'Accuracy':          round(accuracy_score(y_true, preds), 6),
        'Precision':         round(precision_score(y_true, preds, zero_division=0), 6),
        'Recall':            round(recall_score(y_true, preds, zero_division=0), 6),
        'F1-Score':          round(f1_score(y_true, preds, zero_division=0), 6),
        'F-beta (1.5)':      round(fbeta_score(y_true, preds, beta=1.5, zero_division=0), 6),
        'ROC-AUC':           round(roc_auc_score(y_true, proba), 6),
        'Average Precision': round(average_precision_score(y_true, proba), 6),
    }


def save_plots(model_name, model_id, pipeline, X_test, y_test, proba, opt_thresh, img_dir):
    img_dir.mkdir(parents=True, exist_ok=True)
    pca: PCA = pipeline.named_steps['pca']

    # --- ROC ---
    fpr, tpr, _ = roc_curve(y_test, proba)
    auc = roc_auc_score(y_test, proba)
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(fpr, tpr, color=RED, lw=2.5, label=f'ROC-AUC = {auc:.3f}')
    ax.plot([0, 1], [0, 1], 'k--', alpha=0.4, lw=1)
    ax.fill_between(fpr, tpr, alpha=0.08, color=RED)
    ax.set_xlabel('Tasa de Falsos Positivos'); ax.set_ylabel('Tasa de Verdaderos Positivos')
    ax.set_title(f'Curva ROC — {model_name} + PCA'); ax.legend(loc='lower right')
    fig.tight_layout(); fig.savefig(img_dir / f'{model_id}_roc_curve.png', dpi=150); plt.close()

    # --- Precision-Recall ---
    prec, rec, _ = precision_recall_curve(y_test, proba)
    ap = average_precision_score(y_test, proba)
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(rec, prec, color=RED, lw=2.5, label=f'AP = {ap:.3f}')
    ax.fill_between(rec, prec, alpha=0.08, color=RED)
    ax.set_xlabel('Recall'); ax.set_ylabel('Precisión')
    ax.set_title(f'Curva Precisión-Recall — {model_name} + PCA'); ax.legend()
    fig.tight_layout(); fig.savefig(img_dir / f'{model_id}_pr_curve.png', dpi=150); plt.close()

    # --- Confusion Matrix ---
    preds = (proba >= opt_thresh).astype(int)
    cm = confusion_matrix(y_test, preds)
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Reds', ax=ax,
                xticklabels=['No Oferta', 'Oferta'],
                yticklabels=['No Oferta', 'Oferta'], linewidths=0.5)
    ax.set_title(f'Matriz de Confusión — {model_name} + PCA\n(umbral = {opt_thresh})')
    ax.set_ylabel('Real'); ax.set_xlabel('Predicho')
    fig.tight_layout(); fig.savefig(img_dir / f'{model_id}_confusion_matrix.png', dpi=150); plt.close()

    # --- PCA Variance ---
    cumvar = np.cumsum(pca.explained_variance_ratio_)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(range(1, len(pca.explained_variance_ratio_) + 1),
           pca.explained_variance_ratio_, color=RED, alpha=0.7, label='Por componente')
    ax2 = ax.twinx()
    ax2.plot(range(1, len(cumvar) + 1), cumvar, color=BLUE, lw=2.5, marker='o', ms=4, label='Acumulada')
    ax2.axhline(y=0.90, color='gray', linestyle='--', lw=1.2, alpha=0.7, label='90%')
    ax2.set_ylim(0, 1.05); ax2.set_ylabel('Varianza acumulada', color=BLUE)
    ax.set_xlabel('Componente PCA'); ax.set_ylabel('Varianza individual', color=RED)
    ax.set_title(f'Varianza Explicada por PCA — {model_name}')
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc='center right')
    fig.tight_layout(); fig.savefig(img_dir / f'{model_id}_pca_variance.png', dpi=150); plt.close()

    # --- Threshold tradeoff ---
    tvals = np.arange(0.05, 0.95, 0.01)
    precs, recs, f1s, fbetas = [], [], [], []
    for t in tvals:
        p_ = (proba >= t).astype(int)
        precs.append(precision_score(y_test, p_, zero_division=0))
        recs.append(recall_score(y_test, p_, zero_division=0))
        f1s.append(f1_score(y_test, p_, zero_division=0))
        fbetas.append(fbeta_score(y_test, p_, beta=1.5, zero_division=0))
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(tvals, precs,  color=BLUE,  lw=2, label='Precisión')
    ax.plot(tvals, recs,   color=GREEN, lw=2, label='Recall')
    ax.plot(tvals, f1s,    color='#f59e0b', lw=2, label='F1')
    ax.plot(tvals, fbetas, color=RED,  lw=2.5, label='F-beta(1.5)')
    ax.axvline(x=opt_thresh, color='black', linestyle='--', lw=1.5, alpha=0.6,
               label=f'Umbral óptimo = {opt_thresh}')
    ax.set_xlabel('Umbral de decisión'); ax.set_ylabel('Score')
    ax.set_title(f'Análisis de Umbral — {model_name} + PCA')
    ax.legend(loc='center left'); ax.set_ylim(0, 1.05)
    fig.tight_layout(); fig.savefig(img_dir / f'{model_id}_threshold.png', dpi=150); plt.close()


def train_model(label, model_id, classifier, X_train, X_test, y_train, y_test, out_dir):
    print(f'\n=== {label} + PCA ===')

    informe = out_dir / 'informe'
    imagenes = out_dir / 'imagenes'
    informe.mkdir(parents=True, exist_ok=True)

    pipeline = Pipeline([
        ('preprocessor', make_preprocessor()),
        ('pca', PCA(n_components=0.90, random_state=42)),
        ('model', classifier),
    ])
    pipeline.fit(X_train, y_train)

    proba = pipeline.predict_proba(X_test)[:, 1]
    pca: PCA = pipeline.named_steps['pca']
    n_comp = int(pca.n_components_)
    var_exp = float(pca.explained_variance_ratio_.sum())

    m_default = metrics_at(y_test, proba, 0.5)
    opt_t = best_threshold(y_test.values, proba)
    m_opt = metrics_at(y_test, proba, opt_t)

    print(f'  PCA: {n_comp} components → {var_exp:.1%} varianza')
    print(f'  Umbral óptimo: {opt_t}')
    print(f'  Accuracy: {m_opt["Accuracy"]:.4f}  |  F1: {m_opt["F1-Score"]:.4f}  |  ROC-AUC: {m_opt["ROC-AUC"]:.4f}')

    # Save pkl (same structure as existing models)
    pkl_data = {
        'pipeline': pipeline,
        'best_threshold': opt_t,
        'best_params': {k: v for k, v in classifier.get_params().items()},
        'target_name': TARGET,
        'feature_columns': FEATURE_COLS,
        'numeric_columns': NUMERIC_COLS,
        'categorical_columns': CATEGORICAL_COLS,
        'metrics_default_threshold': m_default,
        'metrics_optimized_threshold': m_opt,
        'pca_n_components': n_comp,
        'pca_explained_variance': round(var_exp, 4),
        'model_stage': 'pca',
    }
    pkl_path = informe / f'{model_id}.pkl'
    with open(pkl_path, 'wb') as f:
        pickle.dump(pkl_data, f)
    print(f'  Guardado: {pkl_path.relative_to(ROOT)}')

    # Save JSON summary
    summary = {
        'model_name': label + '_PCA',
        'target': TARGET,
        'pca': {
            'n_components': n_comp,
            'explained_variance': round(var_exp, 4),
            'target_variance': 0.90,
        },
        'best_threshold': opt_t,
        'metrics': {
            'threshold_0_50': m_default,
            'threshold_optimized': m_opt,
        },
    }
    json_path = informe / f'{model_id}_summary.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f'  Guardado: {json_path.relative_to(ROOT)}')

    # Generate plots
    save_plots(label, model_id, pipeline, X_test, y_test, proba, opt_t, imagenes)
    print(f'  Imágenes: {len(list(imagenes.glob("*.png")))} PNGs en {imagenes.relative_to(ROOT)}')


def main():
    print('Cargando datos...')
    X_train, X_test, y_train, y_test = load_data()
    print(f'  Train: {len(X_train):,} | Test: {len(X_test):,}')

    pca_root = ROOT / 'datalake_gold/PCA'

    # Logistic Regression + PCA
    train_model(
        label='LogisticRegression',
        model_id='logistica_pca',
        classifier=LogisticRegression(
            C=0.03, penalty='l2', solver='saga', max_iter=3000, random_state=42
        ),
        X_train=X_train, X_test=X_test, y_train=y_train, y_test=y_test,
        out_dir=pca_root / 'outputs_logistica_pca',
    )

    # Decision Tree + PCA
    train_model(
        label='DecisionTree',
        model_id='decision_tree_pca',
        classifier=DecisionTreeClassifier(
            ccp_alpha=0.0001, criterion='gini', max_depth=None,
            min_samples_leaf=5, min_samples_split=2, random_state=42,
        ),
        X_train=X_train, X_test=X_test, y_train=y_train, y_test=y_test,
        out_dir=pca_root / 'outputs_decision_tree_pca',
    )

    print('\n✓ Entrenamiento completo.')


if __name__ == '__main__':
    main()
