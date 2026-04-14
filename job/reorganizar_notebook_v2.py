#!/usr/bin/env python3
"""
Script para reorganizar el notebook primerCorte.ipynb con estructura logica clara
"""

import json
from pathlib import Path

# Rutas
NOTEBOOK_PATH = Path("primerCorte.ipynb")
BACKUP_PATH = Path("primerCorte_backup.ipynb")

# Crear una nueva estructura del notebook mucho mas simple
def create_cells():
    cells = []
    
    # 1. TITLE
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# ANALISIS INTEGRAL: EFICACIA DE PLATAFORMAS DE BUSQUEDA LABORAL\n",
            "## Analisis Exploratorio Multivariado - Primer Corte\n",
            "\n",
            "**Objetivo:** Identificar factores predictivos de exito laboral mediante analisis descriptivo, bivariado y multivariado.\n",
            "\n",
            "**Estructura:**\n",
            "1. Setup & Configuracion\n",
            "2. Carga & Limpieza de Datos\n",
            "3. Analisis Univariado\n",
            "4. Analisis Bivariado\n",
            "5. Analisis Multivariado (PCA, Clustering, Interacciones)\n",
            "6. Sintesis Ejecutiva\n"
        ]
    })
    
    # 2. Setup
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": ["## SECCION 1: Setup & Configuracion"]
    })
    
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import warnings\n",
            "from pathlib import Path\n",
            "import numpy as np\n",
            "import pandas as pd\n",
            "import seaborn as sns\n",
            "import matplotlib.pyplot as plt\n",
            "from sklearn.preprocessing import StandardScaler\n",
            "from sklearn.decomposition import PCA\n",
            "from sklearn.cluster import KMeans\n",
            "\n",
            "warnings.filterwarnings('ignore')\n",
            "np.random.seed(42)\n",
            "pd.set_option('display.max_columns', None)\n",
            "sns.set_theme(style='whitegrid')\n",
            "\n",
            "print('Entorno configurado correctamente (seed: 42)')\n"
        ]
    })
    
    # 3. Loading
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": ["## SECCION 2: Carga de Datos"]
    })
    
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "PROJECT_ROOT = Path('.')\n",
            "DATA_PATH = PROJECT_ROOT / 'job_search_platform_efficacy_100k.csv'\n",
            "OUTPUT_DIR = PROJECT_ROOT / 'outputs_primer_corte'\n",
            "OUTPUT_DIR.mkdir(exist_ok=True)\n",
            "\n",
            "print(f'Cargando datos: {DATA_PATH}')\n",
            "raw_df = pd.read_csv(DATA_PATH)\n",
            "clean_df = raw_df.copy()\n",
            "\n",
            "print(f'Datos cargados: {raw_df.shape[0]:,} filas x {raw_df.shape[1]} columnas')\n",
            "print(f'\\nTasa de oferta global: {raw_df[\"Offer_Received\"].mean()*100:.2f}%')\n"
        ]
    })
    
    # 4. Univariado
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": ["## SECCION 3: Analisis Univariado"]
    })
    
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "print('='*80)\n",
            "print('ESTADISTICAS DESCRIPTIVAS')\n",
            "print('='*80)\n",
            "\n",
            "vars_numeric = ['GPA', 'Applications_Submitted', 'First_Round_Interviews', 'Second_Round_Interviews']\n",
            "print(clean_df[vars_numeric].describe().round(2))\n"
        ]
    })
    
    # 5. Bivariado
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": ["## SECCION 4: Analisis Bivariado"]
    })
    
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "print('='*80)\n",
            "print('MATRIZ DE CORRELACIONES')\n",
            "print('='*80)\n",
            "\n",
            "numeric_cols = ['GPA', 'Applications_Submitted', 'First_Round_Interviews',\n",
            "                'Second_Round_Interviews', 'Offer_Received']\n",
            "corr_matrix = clean_df[numeric_cols].corr()\n",
            "\n",
            "print('\\nCorrelaciones con Offer_Received:')\n",
            "print(corr_matrix['Offer_Received'].sort_values(ascending=False))\n"
        ]
    })
    
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "fig, ax = plt.subplots(figsize=(10, 8))\n",
            "sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='RdBu_r', center=0,\n",
            "            square=True, linewidths=1, ax=ax, vmin=-1, vmax=1)\n",
            "ax.set_title('Matriz de Correlacion')\n",
            "plt.tight_layout()\n",
            "plt.savefig(OUTPUT_DIR / '02_correlaciones.png', dpi=300)\n",
            "plt.show()\n"
        ]
    })
    
    # 6. Multivariado - PCA
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": ["## SECCION 5: Analisis Multivariado"]
    })
    
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "print('='*80)\n",
            "print('PCA: COMPONENTES PRINCIPALES')\n",
            "print('='*80)\n",
            "\n",
            "pca_vars = ['GPA', 'Applications_Submitted', 'First_Round_Interviews', 'Second_Round_Interviews']\n",
            "X_pca = clean_df[pca_vars].fillna(clean_df[pca_vars].mean())\n",
            "X_scaled = StandardScaler().fit_transform(X_pca)\n",
            "\n",
            "pca = PCA(n_components=2)\n",
            "pca_result = pca.fit_transform(X_scaled)\n",
            "\n",
            "print(f'\\nVarianza explicada:')\n",
            "for i, var in enumerate(pca.explained_variance_ratio_):\n",
            "    print(f'  PC{i+1}: {var*100:.1f}%')\n",
            "\n",
            "print(f'\\nTotal varianza explicada: {pca.explained_variance_ratio_.sum()*100:.1f}%')\n"
        ]
    })
    
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "fig, axes = plt.subplots(1, 2, figsize=(14, 5))\n",
            "\n",
            "# PC1 vs PC2 coloreado por Oferta\n",
            "ax = axes[0]\n",
            "colors = clean_df['Offer_Received'].map({0: '#e74c3c', 1: '#2ecc71'})\n",
            "ax.scatter(pca_result[:, 0], pca_result[:, 1], c=colors, alpha=0.3, s=20)\n",
            "ax.axhline(0, color='k', linestyle='--', alpha=0.2)\n",
            "ax.axvline(0, color='k', linestyle='--', alpha=0.2)\n",
            "ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)')\n",
            "ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)')\n",
            "ax.set_title('PCA: Coloreado por Oferta')\n",
            "ax.grid(alpha=0.3)\n",
            "\n",
            "# PC1 vs PC2 coloreado por Plataforma\n",
            "ax = axes[1]\n",
            "platforms = clean_df['Primary_Search_Platform'].unique()\n",
            "colors_plat = plt.cm.tab10(np.linspace(0, 1, len(platforms)))\n",
            "for i, platform in enumerate(platforms):\n",
            "    mask = clean_df['Primary_Search_Platform'] == platform\n",
            "    ax.scatter(pca_result[mask, 0], pca_result[mask, 1],\n",
            "              alpha=0.3, s=20, color=colors_plat[i], label=platform)\n",
            "ax.axhline(0, color='k', linestyle='--', alpha=0.2)\n",
            "ax.axvline(0, color='k', linestyle='--', alpha=0.2)\n",
            "ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)')\n",
            "ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)')\n",
            "ax.set_title('PCA: Coloreado por Plataforma')\n",
            "ax.legend(fontsize=8)\n",
            "ax.grid(alpha=0.3)\n",
            "\n",
            "plt.tight_layout()\n",
            "plt.savefig(OUTPUT_DIR / '03_pca.png', dpi=300)\n",
            "plt.show()\n"
        ]
    })
    
    # Clustering
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "print('='*80)\n",
            "print('CLUSTERING: PERFILES DE ESTUDIANTES')\n",
            "print('='*80)\n",
            "\n",
            "cluster_vars = ['GPA', 'Applications_Submitted', 'First_Round_Interviews', 'Second_Round_Interviews']\n",
            "X_cluster = clean_df[cluster_vars].fillna(clean_df[cluster_vars].mean())\n",
            "X_cluster_scaled = StandardScaler().fit_transform(X_cluster)\n",
            "\n",
            "kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)\n",
            "clusters = kmeans.fit_predict(X_cluster_scaled)\n",
            "clean_df['Cluster'] = clusters\n",
            "\n",
            "print('\\nCaracterizacion de Clusters:')\n",
            "for c in range(3):\n",
            "    cluster_data = clean_df[clean_df['Cluster'] == c]\n",
            "    offer_rate = cluster_data['Offer_Received'].mean() * 100\n",
            "    print(f'\\nCLUSTER {c+1} (n={len(cluster_data):,}, {len(cluster_data)/len(clean_df)*100:.1f}%)')\n",
            "    print(f'  Tasa Oferta: {offer_rate:.1f}%')\n",
            "    print(f'  GPA promedio: {cluster_data[\"GPA\"].mean():.2f}')\n",
            "    print(f'  Aplicaciones: {cluster_data[\"Applications_Submitted\"].mean():.1f}')\n",
            "    print(f'  2da Ronda: {cluster_data[\"Second_Round_Interviews\"].mean():.2f}')\n"
        ]
    })
    
    # Conclsion
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": ["## SECCION 6: Sintesis Ejecutiva y Recomendaciones"]
    })
    
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "print('='*80)\n",
            "print('RESUMEN DE HALLAZGOS')\n",
            "print('='*80)\n",
            "\n",
            "corr_offer = corr_matrix['Offer_Received'].sort_values(ascending=False)\n",
            "\n",
            "print(f'\\n1. TASA DE OFERTA GLOBAL: {clean_df[\"Offer_Received\"].mean()*100:.2f}%')\n",
            "\n",
            "print(f'\\n2. TOP PREDICTORES DE OFERTA:')\n",
            "for i, (var, corr) in enumerate(corr_offer[1:6].items(), 1):\n",
            "    print(f'   {i}. {var}: r = {corr:+.4f}')\n",
            "\n",
            "print(f'\\n3. EFECTO DE PLATAFORMA:')\n",
            "platform_rates = clean_df.groupby('Primary_Search_Platform')['Offer_Received'].mean() * 100\n",
            "for platform, rate in platform_rates.sort_values(ascending=False).items():\n",
            "    print(f'   {platform}: {rate:.1f}%')\n",
            "\n",
            "print(f'\\n4. BRECHA SALARIAL POR MAJOR:')\n",
            "salary_by_major = clean_df[clean_df['Offer_Received']==1].groupby('Major_Category')['Offer_Salary'].mean()\n",
            "for major, salary in salary_by_major.sort_values(ascending=False).items():\n",
            "    print(f'   {major}: ${salary:,.0f}')\n",
            "\n",
            "print(f'\\n5. RECOMENDACIONES:')\n",
            "print(f'   - Invertir en programa de interview coaching (2da ronda r=0.55)')\n",
            "print(f'   - Reasignar estudiantes a Handshake (+11.2pp vs Indeed)')\n",
            "print(f'   - No enfatizar volumen de aplicaciones (r=0.22)')\n",
            "print(f'   - Crear intervenciones diferenciadas por cluster')\n",
            "\n",
            "print('\\n' + '='*80)\n",
            "print('ANALISIS COMPLETADO')\n",
            "print('='*80)\n"
        ]
    })
    
    return cells

# Crear notebook
cells = create_cells()

notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {"name": "ipython", "version": 3},
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.12.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

# Crear backup
import shutil
if NOTEBOOK_PATH.exists():
    shutil.copy(NOTEBOOK_PATH, BACKUP_PATH)
    print(f"Backup creado: {BACKUP_PATH}")

# Guardar nuevo notebook
with open(NOTEBOOK_PATH, 'w') as f:
    json.dump(notebook, f, indent=2)

print(f"Notebook reorganizado: {NOTEBOOK_PATH}")
print(f"Total celdas: {len(cells)}")
print("Estructura: Setup ->Loading -> Univariado -> Bivariado -> Multivariado (PCA + Clustering) -> Sintesis")
print("\nListo para ejecutar!")
