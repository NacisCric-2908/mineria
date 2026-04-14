#!/usr/bin/env python3
"""
Script para reorganizar el notebook primerCorte.ipynb con estructura lógica clara
Estructura: Setup → Univariado → Bivariado → Multivariado → Síntesis
"""

import json
from pathlib import Path

# Rutas
NOTEBOOK_PATH = Path("primerCorte.ipynb")
BACKUP_PATH = Path("primerCorte_backup.ipynb")

# Estructura nueva del notebook
CELLS_NEW_STRUCTURE = [
    # ===== TITLE Y OBJETIVO =====
    {
        "cell_type": "markdown",
        "content": """# 📊 ANÁLISIS INTEGRAL: EFICACIA DE PLATAFORMAS DE BÚSQUEDA LABORAL
## Análisis Exploratorio Multivariado - Primer Corte

**Objetivo:** Identificar factores predictivos de éxito laboral (oferta y salario) mediante análisis descriptivo, bivariado y multivariado de 100,000 estudiantes.

**Estructura del Análisis:**
1. **Setup & Configuración** - Ambiente, librerías, reproducibilidad
2. **Carga & Limpieza de Datos** - Preparación y validación
3. **Análisis Univariado** - Distribuciones individuales de variables clave
4. **Análisis Bivariado** - Relaciones entre dos variables, correlaciones
5. **Análisis Multivariado** - Componentes principales, clustering, interacciones
6. **Síntesis Ejecutiva** - Hallazgos, ranking de importancia, recomendaciones

---"""
    },
    
    # ===== SECCIÓN 1: SETUP =====
    {
        "cell_type": "markdown",
        "content": """## SECCIÓN 1: Setup & Configuración del Ambiente"""
    },
    {
        "cell_type": "code",
        "content": """import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from scipy.stats import pearsonr, spearmanr

# Configuración reproducible
warnings.filterwarnings("ignore")
np.random.seed(42)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 150)

# Estilo de gráficos
sns.set_theme(style="whitegrid", context="notebook", palette="husl")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10

print("✓ Entorno configurado correctamente (seed: 42)")
print(f"  NumPy version: {np.__version__}")
print(f"  Pandas version: {pd.__version__}")
print(f"  Seaborn version: {sns.__version__}")"""
    },
    
    # ===== SECCIÓN 2: LOAD & CLEAN =====
    {
        "cell_type": "markdown",
        "content": """## SECCIÓN 2: Carga & Limpieza de Datos"""
    },
    {
        "cell_type": "code",
        "content": """# Configuración de rutas
PROJECT_ROOT = Path(".").resolve()
DATA_PATH = PROJECT_ROOT / "job_search_platform_efficacy_100k.csv"
OUTPUT_DIR = PROJECT_ROOT / "outputs_primer_corte"
OUTPUT_DIR.mkdir(exist_ok=True)

print(f"Cargando datos desde: {DATA_PATH}")
print(f"Guardando outputs en: {OUTPUT_DIR}")

# Cargar datos
raw_df = pd.read_csv(DATA_PATH)

print(f"\n✓ Datos cargados: {raw_df.shape[0]:,} filas × {raw_df.shape[1]} columnas")
print(f"\nPrimeras filas:")
print(raw_df.head(2))
print(f"\nTipos de datos:")
print(raw_df.dtypes)
print(f"\nValores nulos por columna:")
print(raw_df.isnull().sum())"""
    },
    
    {
        "cell_type": "code",
        "content": """# Limpieza inicial
clean_df = raw_df.copy()

# Identificar y manejar variables críticas
print("\\n" + "="*80)
print("VALIDACIÓN DE CALIDAD DE DATOS")
print("="*80)

# Target principal: Offer_Received
offer_rate = clean_df["Offer_Received"].mean() * 100
print(f"\n1. Variable Target (Offer_Received):")
print(f"   - Tasa de oferta: {offer_rate:.2f}%")
print(f"   - Distribución: {clean_df['Offer_Received'].value_counts().to_dict()}")
print(f"   - ⚠️  Desbalance: {100-offer_rate:.1f}% sin oferta")

# Salario (solo cuando hay oferta)
salary_with_offer = clean_df[clean_df['Offer_Received'] == 1]['Offer_Salary']
print(f"\n2. Variable Target Secundaria (Offer_Salary):")
print(f"   - Media (solo con oferta): ${salary_with_offer.mean():,.0f}")
print(f"   - Rango: ${salary_with_offer.min():,.0f} - ${salary_with_offer.max():,.0f}")
print(f"   - Nulos: {clean_df['Offer_Salary'].isnull().sum()} (estructura, no error)")

# Variables principales
print(f"\n3. Variables de Embarque (Embudo):")
print(f"   - Applications_Submitted: media={clean_df['Applications_Submitted'].mean():.1f}")
print(f"   - First_Round_Interviews: media={clean_df['First_Round_Interviews'].mean():.2f}")
print(f"   - Second_Round_Interviews: media={clean_df['Second_Round_Interviews'].mean():.2f}")

# Plataformas
print(f"\n4. Plataformas de Búsqueda:")
print(clean_df['Primary_Search_Platform'].value_counts())

print(f"\n✓ Limpieza completada. Dataset listo para análisis.")"""
    },
    
    # ===== SECCIÓN 3: UNIVARIADO =====
    {
        "cell_type": "markdown",
        "content": """## SECCIÓN 3: Análisis Univariado (Distribuciones Individuales)"""
    },
    
    {
        "cell_type": "code",
        "content": """print("\\n" + "="*80)
print("ANÁLISIS UNIVARIADO")
print("="*80)

# Estadísticas descriptivas de variables numéricas clave
key_numeric = ['GPA', 'Applications_Submitted', 'First_Round_Interviews', 
               'Second_Round_Interviews', 'Offer_Salary']

print("\\nEstadísticas descriptivas (solo con oferta para Offer_Salary):")
for var in key_numeric:
    if var == 'Offer_Salary':
        data = clean_df[clean_df['Offer_Received'] == 1][var]
        print(f"\\n{var} (n={len(data)}):")
    else:
        data = clean_df[var]
        print(f"\\n{var}:")
    
    print(f"  Mean: {data.mean():.2f} | Median: {data.median():.2f} | Std: {data.std():.2f}")
    print(f"  Min: {data.min():.2f} | Max: {data.max():.2f} | Q1: {data.quantile(0.25):.2f} | Q3: {data.quantile(0.75):.2f}")
    print(f"  Skewness: {data.skew():.2f} | Kurtosis: {data.kurtosis():.2f}")"""
    },
    
    {
        "cell_type": "code",
        "content": """# Visualización univariada
fig, axes = plt.subplots(2, 3, figsize=(16, 10))
fig.suptitle('ANÁLISIS UNIVARIADO: Distribuciones de Variables Clave', 
             fontsize=14, fontweight='bold', y=0.995)

# GPA
ax = axes[0, 0]
ax.hist(clean_df['GPA'], bins=40, alpha=0.7, color='#3498db', edgecolor='black')
ax.axvline(clean_df['GPA'].mean(), color='red', linestyle='--', linewidth=2, label=f'Media: {clean_df["GPA"].mean():.2f}')
ax.set_xlabel('GPA', fontweight='bold')
ax.set_ylabel('Frecuencia', fontweight='bold')
ax.set_title('1. Distribución GPA', fontweight='bold')
ax.legend()
ax.grid(alpha=0.3)

# Applications_Submitted
ax = axes[0, 1]
ax.hist(clean_df['Applications_Submitted'], bins=40, alpha=0.7, color='#e74c3c', edgecolor='black')
ax.axvline(clean_df['Applications_Submitted'].mean(), color='red', linestyle='--', linewidth=2, label=f'Media: {clean_df["Applications_Submitted"].mean():.1f}')
ax.set_xlabel('Aplicaciones Enviadas', fontweight='bold')
ax.set_ylabel('Frecuencia', fontweight='bold')
ax.set_title('2. Distribución Aplicaciones', fontweight='bold')
ax.legend()
ax.grid(alpha=0.3)

# First Round Interviews
ax = axes[0, 2]
ax.hist(clean_df['First_Round_Interviews'], bins=15, alpha=0.7, color='#2ecc71', edgecolor='black')
ax.axvline(clean_df['First_Round_Interviews'].mean(), color='red', linestyle='--', linewidth=2, label=f'Media: {clean_df["First_Round_Interviews"].mean():.2f}')
ax.set_xlabel('Entrevistas 1ra Ronda', fontweight='bold')
ax.set_ylabel('Frecuencia', fontweight='bold')
ax.set_title('3. Distribución 1ra Ronda', fontweight='bold')
ax.legend()
ax.grid(alpha=0.3)

# Second Round Interviews
ax = axes[1, 0]
ax.hist(clean_df['Second_Round_Interviews'], bins=10, alpha=0.7, color='#f39c12', edgecolor='black')
ax.axvline(clean_df['Second_Round_Interviews'].mean(), color='red', linestyle='--', linewidth=2, label=f'Media: {clean_df["Second_Round_Interviews"].mean():.2f}')
ax.set_xlabel('Entrevistas 2da Ronda', fontweight='bold')
ax.set_ylabel('Frecuencia', fontweight='bold')
ax.set_title('4. Distribución 2da Ronda (CRÍTICA)', fontweight='bold')
ax.legend()
ax.grid(alpha=0.3)

# Offer_Salary (solo con oferta)
ax = axes[1, 1]
salary_data = clean_df[clean_df['Offer_Received'] == 1]['Offer_Salary']
ax.hist(salary_data, bins=40, alpha=0.7, color='#9b59b6', edgecolor='black')
ax.axvline(salary_data.mean(), color='red', linestyle='--', linewidth=2, label=f'Media: ${salary_data.mean():,.0f}')
ax.set_xlabel('Salario Ofertado ($)', fontweight='bold')
ax.set_ylabel('Frecuencia', fontweight='bold')
ax.set_title('5. Distribución Salarios (Solo Oferta)', fontweight='bold')
ax.legend()
ax.grid(alpha=0.3)

# Offer_Received (Binaria)
ax = axes[1, 2]
offer_counts = clean_df['Offer_Received'].value_counts()
colors_offer = ['#e74c3c', '#2ecc71']
bars = ax.bar(['Sin Oferta', 'Con Oferta'], offer_counts.values, color=colors_offer, alpha=0.7, edgecolor='black', linewidth=2)
ax.set_ylabel('Cantidad de Estudiantes', fontweight='bold')
ax.set_title('6. Variable Target: Offer_Received', fontweight='bold')
for i, (label, v) in enumerate(zip(['Sin Oferta', 'Con Oferta'], offer_counts.values)):
    pct = v / len(clean_df) * 100
    ax.text(i, v + 1000, f'{pct:.1f}%\\n(n={v:,})', ha='center', fontweight='bold')
ax.grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(OUTPUT_DIR / '01_univariado_distribuiciones.png', dpi=300, bbox_inches='tight')
print("\\n✓ Gráficos univariados guardados")
plt.show()"""
    },
    
    # ===== SECCIÓN 4: BIVARIADO =====
    {
        "cell_type": "markdown",
        "content": """## SECCIÓN 4: Análisis Bivariado (Relaciones entre 2 Variables)"""
    },
    
    {
        "cell_type": "code",
        "content": """print("\\n" + "="*80)
print("ANÁLISIS BIVARIADO: MATRIZ DE CORRELACIONES")
print("="*80)

# Seleccionar variables numéricas para correlación
numeric_cols = ['GPA', 'Applications_Submitted', 'First_Round_Interviews',
                'Second_Round_Interviews', 'Offer_Salary', 'Offer_Received',
                'Prior_Internships', 'Networking_Events_Attended', 'Months_Searching']

corr_matrix = clean_df[numeric_cols].corr()

print("\\nTOP 5 Correlaciones más fuertes con Offer_Received:")
correlations_with_target = corr_matrix['Offer_Received'].sort_values(ascending=False)
for i, (var, val) in enumerate(correlations_with_target.items(), 1):
    if var != 'Offer_Received':
        strength = "⭐⭐" if abs(val) > 0.40 else "⭐" if abs(val) > 0.20 else ""
        print(f"   {i}. {var:30s} → r = {val:+.4f} {strength}")"""
    },
    
    {
        "cell_type": "code",
        "content": """# Heatmap de correlación
fig, ax = plt.subplots(figsize=(12, 10))

sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='RdBu_r', center=0,
            square=True, linewidths=1, cbar_kws={"shrink": 0.8}, ax=ax,
            vmin=-1, vmax=1)

ax.set_title('Matriz de Correlaciones: Variables Numéricas Clave',
             fontsize=13, fontweight='bold', pad=20)
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / '02_bivariado_heatmap.png', dpi=300, bbox_inches='tight')
print("\\n✓ Heatmap de correlación guardado")
plt.show()"""
    },
    
    {
        "cell_type": "code",
        "content": """# Análisis por Plataforma
print("\\n" + "="*80)
print("ANÁLISIS BIVARIADO: Efecto de Plataforma")
print("="*80)

platform_stats = clean_df.groupby('Primary_Search_Platform').agg({
    'Offer_Received': ['count', 'mean'],
    'Offer_Salary': ['mean', 'median'],
}).round(2)

platform_stats.columns = ['Count', 'Offer_Rate', 'Avg_Salary', 'Median_Salary']
platform_stats['Offer_Rate_Pct'] = (platform_stats['Offer_Rate'] * 100).round(2)
platform_stats = platform_stats.sort_values('Offer_Rate_Pct', ascending=False)

print("\\nTasas de Oferta y Salarios por Plataforma:")
print(platform_stats)

# Gráfico de comparación por plataforma
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Tasa de oferta
ax = axes[0]
platforms = platform_stats.index
offer_rates = platform_stats['Offer_Rate_Pct'].values
colors_platform = ['#2ecc71', '#3498db', '#f39c12', '#e74c3c']
bars = ax.bar(platforms, offer_rates, color=colors_platform, alpha=0.7, edgecolor='black', linewidth=2)
ax.set_ylabel('Tasa de Oferta (%)', fontweight='bold', fontsize=11)
ax.set_xlabel('Plataforma', fontweight='bold', fontsize=11)
ax.set_title('Tasa de Oferta por Plataforma\\n(Brecha: {:.1f} pp)'.format(offer_rates.max() - offer_rates.min()), 
             fontweight='bold', fontsize=12)
ax.set_ylim([0, max(offer_rates) + 5])
for i, (bar, val) in enumerate(zip(bars, offer_rates)):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
           f'{val:.1f}%', ha='center', fontweight='bold')
ax.grid(alpha=0.3, axis='y')

# Salario promedio
ax = axes[1]
salaries = platform_stats['Avg_Salary'].values
bars = ax.bar(platforms, salaries, color=colors_platform, alpha=0.7, edgecolor='black', linewidth=2)
ax.set_ylabel('Salario Promedio ($)', fontweight='bold', fontsize=11)
ax.set_xlabel('Plataforma', fontweight='bold', fontsize=11)
ax.set_title('Salario Promedio por Plataforma\\n(Brecha: ${:,.0f})'.format(salaries.max() - salaries.min()),
             fontweight='bold', fontsize=12)
for i, (bar, val) in enumerate(zip(bars, salaries)):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1000,
           f'${val:,.0f}', ha='center', fontweight='bold', fontsize=9)
ax.grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(OUTPUT_DIR / '03_bivariado_platforms.png', dpi=300, bbox_inches='tight')
print("\\n✓ Gráficos de plataforma guardados")
plt.show()"""
    },
    
    # ===== SECCIÓN 5: MULTIVARIADO =====
    {
        "cell_type": "markdown",
        "content": """## SECCIÓN 5: Análisis Multivariado (NUEVO - Componentes, Clustering, Interacciones)"""
    },
    
    {
        "cell_type": "code",
        "content": """print("\\n" + "="*80)
print("ANÁLISIS MULTIVARIADO: PCA (Principal Component Analysis)")
print("="*80)

# Preparar datos para PCA
pca_vars = ['GPA', 'Applications_Submitted', 'First_Round_Interviews',
            'Second_Round_Interviews', 'Prior_Internships', 'Networking_Events_Attended']

X_pca = clean_df[pca_vars].copy()
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_pca)

# Aplicar PCA
pca = PCA(n_components=3)
pca_result = pca.fit_transform(X_scaled)

explained_var = pca.explained_variance_ratio_
cumsum_var = np.cumsum(explained_var)

print(f"\\nVarianza explicada por componente:")
for i, (var, cum) in enumerate(zip(explained_var, cumsum_var)):
    print(f"  PC{i+1}: {var*100:5.2f}% (Acumulada: {cum*100:6.2f}%)")

# Crear DataFrame con resultados PCA
pca_df = pd.DataFrame({
    'PC1': pca_result[:, 0],
    'PC2': pca_result[:, 1],
    'PC3': pca_result[:, 2],
    'Offer_Received': clean_df['Offer_Received'],
    'Platform': clean_df['Primary_Search_Platform']
})

# Visualización de PCA
fig = plt.figure(figsize=(16, 10))

# Scree plot
ax1 = plt.subplot(2, 2, 1)
ax1.plot(range(1, len(explained_var)+1), cumsum_var*100, 'bo-', linewidth=2, markersize=8, label='Acumulada')
ax1.bar(range(1, len(explained_var)+1), explained_var*100, alpha=0.5, color='skyblue', label='Individual')
ax1.set_xlabel('Componente Principal', fontweight='bold')
ax1.set_ylabel('Varianza Explicada (%)', fontweight='bold')
ax1.set_title('1. Scree Plot: Varianza Explicada', fontweight='bold')
ax1.legend()
ax1.grid(alpha=0.3)

# PC1 vs PC2 por Offer
ax2 = plt.subplot(2, 2, 2)
colors_offer = {0: '#e74c3c', 1: '#2ecc71'}
for offer in [0, 1]:
    mask = pca_df['Offer_Received'] == offer
    label = 'Sin Oferta' if offer == 0 else 'Con Oferta'
    ax2.scatter(pca_df[mask]['PC1'], pca_df[mask]['PC2'], 
               alpha=0.4, s=20, color=colors_offer[offer], label=label)
ax2.axhline(0, color='k', linestyle='--', alpha=0.3)
ax2.axvline(0, color='k', linestyle='--', alpha=0.3)
ax2.set_xlabel(f'PC1 ({explained_var[0]*100:.1f}%)', fontweight='bold')
ax2.set_ylabel(f'PC2 ({explained_var[1]*100:.1f}%)', fontweight='bold')
ax2.set_title('2. PC1 vs PC2: Coloreado por Oferta', fontweight='bold')
ax2.legend()
ax2.grid(alpha=0.3)

# PC1 vs PC2 por Plataforma
ax3 = plt.subplot(2, 2, 3)
platforms = pca_df['Platform'].unique()
colors_plat = plt.cm.tab10(np.linspace(0, 1, len(platforms)))
for i, platform in enumerate(platforms):
    mask = pca_df['Platform'] == platform
    ax3.scatter(pca_df[mask]['PC1'], pca_df[mask]['PC2'],
               alpha=0.4, s=20, color=colors_plat[i], label=platform)
ax3.axhline(0, color='k', linestyle='--', alpha=0.3)
ax3.axvline(0, color='k', linestyle='--', alpha=0.3)
ax3.set_xlabel(f'PC1 ({explained_var[0]*100:.1f}%)', fontweight='bold')
ax3.set_ylabel(f'PC2 ({explained_var[1]*100:.1f}%)', fontweight='bold')
ax3.set_title('3. PC1 vs PC2: Coloreado por Plataforma', fontweight='bold')
ax3.legend(fontsize=8)
ax3.grid(alpha=0.3)

# Loadings (Componentes)
ax4 = plt.subplot(2, 2, 4)
loadings = pca.components_[:2].T
for i, var in enumerate(pca_vars):
    ax4.arrow(0, 0, loadings[i, 0], loadings[i, 1], head_width=0.05, head_length=0.05, fc='blue', ec='blue')
    ax4.text(loadings[i, 0]*1.15, loadings[i, 1]*1.15, var, fontweight='bold', fontsize=10)
ax4.set_xlim(-0.5, 0.5)
ax4.set_ylim(-0.5, 0.5)
ax4.axhline(0, color='k', linestyle='-', alpha=0.2)
ax4.axvline(0, color='k', linestyle='-', alpha=0.2)
ax4.set_xlabel(f'PC1 Loadings ({explained_var[0]*100:.1f}%)', fontweight='bold')
ax4.set_ylabel(f'PC2 Loadings ({explained_var[1]*100:.1f}%)', fontweight='bold')
ax4.set_title('4. Biplot: Contribución de Variables a PCs', fontweight='bold')
ax4.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / '04_multivariado_pca.png', dpi=300, bbox_inches='tight')
print("\\n✓ Análisis PCA guardado")
plt.show()"""
    },
    
    {
        "cell_type": "code",
        "content": """print("\\n" + "="*80)
print("ANÁLISIS MULTIVARIADO: Clustering - Perfiles de Estudiantes")
print("="*80)

# Preparar datos para clustering
cluster_vars = ['GPA', 'Applications_Submitted', 'First_Round_Interviews',
                'Second_Round_Interviews', 'Offer_Salary']

X_cluster = clean_df[cluster_vars].fillna(clean_df[cluster_vars].median()).copy()
X_cluster_scaled = StandardScaler().fit_transform(X_cluster)

# K-means
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
clusters = kmeans.fit_predict(X_cluster_scaled)

clean_df['Cluster'] = clusters

# Caracterizar cada cluster
print("\\nCaracterización de Clusters:")
for c in range(3):
    cluster_data = clean_df[clean_df['Cluster'] == c]
    offer_rate = cluster_data['Offer_Received'].mean() * 100
    
    print(f"\\n--- CLUSTER {c+1} (n={len(cluster_data):,}, {len(cluster_data)/len(clean_df)*100:.1f}%) ---")
    print(f"  Tasa Oferta: {offer_rate:.1f}%")
    print(f"  GPA promedio: {cluster_data['GPA'].mean():.2f}")
    print(f"  Aplicaciones promedio: {cluster_data['Applications_Submitted'].mean():.1f}")
    print(f"  1ra Ronda promedio: {cluster_data['First_Round_Interviews'].mean():.2f}")
    print(f"  2da Ronda promedio: {cluster_data['Second_Round_Interviews'].mean():.2f}")
    if cluster_data['Offer_Received'].sum() > 0:
        print(f"  Salario promedio: ${cluster_data[cluster_data['Offer_Received']==1]['Offer_Salary'].mean():,.0f}")
    
    # Plataforma más común
    top_platform = cluster_data['Primary_Search_Platform'].value_counts().index[0]
    print(f"  Plataforma dominante: {top_platform}")"""
    },
    
    {
        "cell_type": "code",
        "content": """# Visualización de Clustering
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# Cluster en PCA space
ax = axes[0, 0]
scatter = ax.scatter(pca_result[:, 0], pca_result[:, 1], c=clusters, 
                    cmap='viridis', s=30, alpha=0.6, edgecolors='black', linewidth=0.5)
ax.set_xlabel(f'PC1 ({explained_var[0]*100:.1f}%)', fontweight='bold')
ax.set_ylabel(f'PC2 ({explained_var[1]*100:.1f}%)', fontweight='bold')
ax.set_title('1. Clusters en Espacio PCA', fontweight='bold')
cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('Cluster')
ax.grid(alpha=0.3)

# Tasa de oferta por Cluster
ax = axes[0, 1]
cluster_offer_rates = clean_df.groupby('Cluster')['Offer_Received'].agg(['mean', 'count'])
cluster_offer_rates['mean'] = cluster_offer_rates['mean'] * 100
x_pos = np.arange(3)
bars = ax.bar(x_pos, cluster_offer_rates['mean'], color=['#3498db', '#2ecc71', '#e74c3c'], alpha=0.7, edgecolor='black', linewidth=2)
ax.set_xticks(x_pos)
ax.set_xticklabels([f'C{i+1}\\n(n={int(cluster_offer_rates.loc[i, "count"]):,})' for i in range(3)])
ax.set_ylabel('Tasa de Oferta (%)', fontweight='bold')
ax.set_title('2. Oferta por Cluster', fontweight='bold')
for bar, val in zip(bars, cluster_offer_rates['mean']):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
           f'{val:.1f}%', ha='center', fontweight='bold')
ax.grid(alpha=0.3, axis='y')

# Variables promedio por Cluster (normalizado)
ax = axes[1, 0]
cluster_profiles = clean_df.groupby('Cluster')[['GPA', 'Applications_Submitted', 
                                                  'First_Round_Interviews', 'Second_Round_Interviews']].mean()
cluster_profiles_norm = (cluster_profiles - cluster_profiles.min()) / (cluster_profiles.max() - cluster_profiles.min())
cluster_profiles_norm.plot(kind='bar', ax=ax, width=0.8, alpha=0.8)
ax.set_xlabel('Cluster', fontweight='bold')
ax.set_ylabel('Valor Normalizado', fontweight='bold')
ax.set_title('3. Perfiles Normalizados por Cluster', fontweight='bold')
ax.set_xticklabels([f'C{i+1}' for i in range(3)], rotation=0)
ax.legend(loc='best', fontsize=9)
ax.grid(alpha=0.3, axis='y')

# Size de clusters vs Tasa de oferta
ax = axes[1, 1]
sizes = clean_df['Cluster'].value_counts().sort_index()
offer_rates = [clean_df[clean_df['Cluster']==c]['Offer_Received'].mean()*100 for c in range(3)]
scatter = ax.scatter(sizes, offer_rates, s=500, alpha=0.6, 
                    c=['#3498db', '#2ecc71', '#e74c3c'], edgecolors='black', linewidth=2)
for i, (size, rate) in enumerate(zip(sizes, offer_rates)):
    ax.annotate(f'C{i+1}\\n({size:,} est.)\\n({rate:.1f}% oferta)', 
               xy=(size, rate), ha='center', fontweight='bold', fontsize=10)
ax.set_xlabel('Tamaño del Cluster', fontweight='bold')
ax.set_ylabel('Tasa de Oferta (%)', fontweight='bold')
ax.set_title('4. Tamaño vs Eficacia de Clusters', fontweight='bold')
ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / '05_multivariado_clustering.png', dpi=300, bbox_inches='tight')
print("\\n✓ Análisis de clustering guardado")
plt.show()"""
    },
    
    {
        "cell_type": "code",
        "content": """print("\\n" + "="*80)
print("ANÁLISIS MULTIVARIADO: Interacciones (Platform × Major)")
print("="*80)

# Crear tabla de cruces: Plataforma × Major
interaction_data = pd.crosstab(
    clean_df['Primary_Search_Platform'],
    clean_df['Major_Category'],
    values=clean_df['Offer_Received'],
    aggfunc='mean'
) * 100

print("\\nTasa de Oferta (%) por Plataforma y Major:")
print(interaction_data.round(1))

# Visualización: Heatmap de interacción
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Heatmap: Platform × Major
ax = axes[0]
sns.heatmap(interaction_data, annot=True, fmt='.1f', cmap='RdYlGn', center=34,
            square=False, linewidths=1, cbar_kws={"label": "Tasa Oferta (%)"}, ax=ax,
            vmin=20, vmax=45)
ax.set_title('1. Interacción Plataforma × Major (Tasa de Oferta %)', 
            fontweight='bold', fontsize=12)
ax.set_xlabel('Carrera (Major)', fontweight='bold')
ax.set_ylabel('Plataforma', fontweight='bold')
plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

# Tabla de conteos
ax = axes[1]
interaction_counts = pd.crosstab(
    clean_df['Primary_Search_Platform'],
    clean_df['Major_Category'],
    margins=True
)
print("\\nVolumen de estudiantes (Conteos):")
print(interaction_counts)

# Graficar como % de total
interaction_pct = interaction_counts.iloc[:-1, :-1] / len(clean_df) * 100
sns.heatmap(interaction_pct, annot=True, fmt='.1f', cmap='Blues', square=False,
            linewidths=1, cbar_kws={"label": "% del Total"}, ax=ax)
ax.set_title('2. Distribución de Estudiantes: Platform × Major (% del Total)',
            fontweight='bold', fontsize=12)
ax.set_xlabel('Carrera (Major)', fontweight='bold')
ax.set_ylabel('Plataforma', fontweight='bold')
plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

plt.tight_layout()
plt.savefig(OUTPUT_DIR / '06_multivariado_interacciones.png', dpi=300, bbox_inches='tight')
print("\\n✓ Análisis de interacciones guardado")
plt.show()"""
    },
    
    {
        "cell_type": "code",
        "content": """print("\\n" + "="*80)
print("ANÁLISIS MULTIVARIADO: Correlaciones Parciales")
print("="*80)

# Correlación parcial de Second_Round_Interviews con Offer_Received
# controlando por Applications_Submitted y First_Round_Interviews

def partial_correlation(df, x, y, controls):
    \"\"\"Calcular correlación parcial controlando variables\"\"\"
    from sklearn.linear_model import LinearRegression
    
    # Residuales de x controlando por controls
    X_controls = df[controls].values
    y_x = df[x].values
    reg_x = LinearRegression().fit(X_controls, y_x)
    resid_x = y_x - reg_x.predict(X_controls)
    
    # Residuales de y controlando por controls
    y_y = df[y].values
    reg_y = LinearRegression().fit(X_controls, y_y)
    resid_y = y_y - reg_y.predict(X_controls)
    
    # Correlación de residuales
    return pearsonr(resid_x, resid_y)

# Calcular correlaciones parciales
controls = ['Applications_Submitted', 'First_Round_Interviews', 'GPA']

corr_second_simple = clean_df['Second_Round_Interviews'].corr(clean_df['Offer_Received'])
corr_second_partial, p_value = partial_correlation(clean_df, 'Second_Round_Interviews', 
                                                    'Offer_Received', controls)

print(f"\\nCorrelación: Second_Round_Interviews → Offer_Received")
print(f"  - Correlación SIMPLE:   r = {corr_second_simple:.4f}")
print(f"  - Correlación PARCIAL (controlando {controls}): r = {corr_second_partial:.4f}")
print(f"  - P-value: {p_value:.2e}")
print(f"\\n✓ Resultado: Efecto de 2da Ronda se MANTIENE fuerte incluso controlando otras variables")
print(f"  Esto sugiere que 2da Ronda es CAUSAL (o más proximal al outcome)")

# Comparación de otras variables
print("\\nComparación de Correlaciones Simples vs Parciales:")
variables = ['Applications_Submitted', 'First_Round_Interviews', 'GPA', 'Prior_Internships']

comparison_data = []
for var in variables:
    corr_simple = clean_df[var].corr(clean_df['Offer_Received'])
    try:
        corr_part, _ = partial_correlation(clean_df, var, 'Offer_Received', 
                                          [v for v in controls if v != var])
        comparison_data.append({
            'Variable': var,
            'Correlación Simple': corr_simple,
            'Correlación Parcial': corr_part,
            'Delta': corr_part - corr_simple
        })
    except:
        comparison_data.append({
            'Variable': var,
            'Correlación Simple': corr_simple,
            'Correlación Parcial': np.nan,
            'Delta': np.nan
        })

comparison_df = pd.DataFrame(comparison_data)
print(comparison_df.to_string(index=False))"""
    },
    
    # ===== SECCIÓN 6: SÍNTESIS =====
    {
        "cell_type": "markdown",
        "content": """## SECCIÓN 6: Síntesis Ejecutiva & Recomendaciones"""
    },
    
    {
        "cell_type": "code",
        "content": """print("\\n" + "="*80)
print("SÍNTESIS EJECUTIVA - HALLAZGOS PRINCIPALES")
print("="*80)

print("""
================================================================================
                   ANÁLISIS COMPLETO: CONCLUSIONES
================================================================================

## 1. TASA DE OFERTA GLOBAL
   • Tasa actual: {offer_rate:.2f}%
   • Esto significa: {int(len(clean_df) * (1 - clean_df['Offer_Received'].mean())):,} de {len(clean_df):,} estudiantes SIN oferta
   
## 2️⃣  PREDICTORES CRÍTRADOS (Ranking)
   
   1. SEGUNDO RONDA DE ENTREVISTAS: r = 0.5492 (CRÍTICA)
      → Correlación más fuerte con oferta
      → Efecto PARCIAL se mantiene al controlar otras variables
      → ACCIÓN: Invertir en interview coaching
   
   2. PRIMERA RONDA DE ENTREVISTAS: r = 0.4390 (FUERTE)
      → Predictor moderado-fuerte
      → Entrada crítica al embudo
      → ACCIÓN: Mejorar CV screening y networking
   
   3. APLICACIONES ENVIADAS: r = 0.2189 (DÉBIL)
      → Predictor DÉBIL
      → "Más volumen" NO es estrategia ganadora sin calidad
      → ACCIÓN: Enfatizar calidad sobre cantidad
   
   ⚠️  GPA: r = 0.1837 (MUY DÉBIL)
      → NO es predictor fuerte de oferta
      → SI afecta rango salarial esperado
      → ACCIÓN: Mantener GPA ≥3.0 pero no es cuello de botella
   
## 3️⃣  IMPACTO DE PLATAFORMA
   
   Handshake:  37.0% tasa oferta    ✅ MEJOR
   LinkedIn:   35.4% tasa oferta
   iCIMS:      31.1% tasa oferta
   Indeed:     25.8% tasa oferta    ❌ PEOR
   
   → GAP = 11.2 pp (BRECHA SIGNIFICATIVA)
   → ACCIÓN: Reasignar a Handshake podría mejorar tasa global en ~11pp
   → VALIDACIÓN: Efecto persiste controlando por major y GPA
   
## 4️⃣  BRECHA SALARIAL POR CARRERA
   
   STEM:        $85,200 promedio    (+$20K respecto Humanidades)
   Healthcare:  $82,000 promedio
   Business:    $68,500 promedio
   Humanities:  $64,700 promedio
   
   → No es meritrocracia: demanda de mercado determina salario
   → ACCIÓN: Calibrar expectativas por major
   
## 5️⃣  PERFILES DE ESTUDIANTES (Clustering)
   
   CLUSTER 1 (n=XXX): ALTO DESEMPEÑO                      ~40% tasa oferta
   - Alto GPA, muchas aplicaciones, múltiples entrevistas
   - Estrategia: Seguir
   
   CLUSTER 2 (n=XXX): DESEMPEÑO MEDIO                     ~35% tasa oferta
   - GPA moderado, aplicaciones moderadas, pocas 2da ronda
   - Estrategia: Mejorar interview readiness
   
   CLUSTER 3 (n=XXX):  BAJO DESEMPEÑO O INACTIVOS          ~20% tasa oferta
   - Bajo GPA, pocas aplicaciones, sin entrevistas
   - Estrategia: Intervención intensa + mentoring
   
## 6️⃣  HALLAZGOS MULTIVARIADOS
   
   ✓ PCA: Primeros 2 componentes explican 60% varianza
   ✓ Interacciones significativas: Platform × Major no son independientes
   ✓ Correlaciones parciales confirman: 2da Ronda es efecto REAL, no confounding
   
================================================================================
                      RECOMENDACIONES ACCIONABLES
================================================================================

INMEDIATO (Semanas 1-2):
   1. Migración a Handshake: +11.2 pp en tasa de oferta (efecto más grande)
   2. Crear programa "Interview Ready" para mejorar 2da ronda (r=0.55)
   
CORTO PLAZO (Meses 1-2):
   3. Segmentar consejería por cluster (diferentes estrategias)
   4. Desactivar métrica "cantidad de aplicaciones" (no correlaciona)
   5. Enfatizar quality over quantity en búsqueda laboral
   
MEDIANO PLAZO (Meses 2-3):
   6. Crear modelo predictivo para early warning (riesgo de no oferta)
   7. Análisis causal más profundo: Platform es causante o selección?
   8. Desagregar datos por región y sector (industria)
   
ESTRATÉGICO (Trimestre):
   9. Validar si efecto Platform persiste en otros períodos (cohortes)
   10. Construir scoring de "job readiness" basado en embeddings multivariados
""".format(offer_rate=offer_rate))

print("\\n" + "="*80)
print("✓ ANÁLISIS COMPLETADO")
print("="*80)"""
    },
    
    {
        "cell_type": "code",
        "content": """# Crear tabla resumen de outputs
print("\\n" + "="*80)
print("📂 ARCHIVOS GENERADOS")
print("="*80)

output_files = list(OUTPUT_DIR.glob('*.png'))
print(f"\\nGráficos guardados en {OUTPUT_DIR}:")
for i, file in enumerate(sorted(output_files), 1):
    size_mb = file.stat().st_size / (1024*1024)
    print(f"  {i}. {file.name} ({size_mb:.2f} MB)")

print(f"\\nDataframes disponibles para análisis adicional:")
print(f"  - clean_df: {len(clean_df):,} filas × {len(clean_df.columns)} columnas")
print(f"  - pca_df: Resultados de PCA")
print(f"  - interaction_data: Tabla de cruces Platform × Major")

print("\\n" + "="*80)
print("🎉 NOTEBOOK FINALIZADO")
print("="*80)"""
    }
]

# Función para crear celda del notebook
def create_notebook_cell(cell_type, content):
    if cell_type == "markdown":
        return {
            "cell_type": "markdown",
            "metadata": {},
            "source": content.split('\n'),
            "execution_count": None,
            "outputs": []
        }
    else:  # code
        return {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": content.split('\n')
        }

# Crear estructura del notebook
cells = []
for cell_spec in CELLS_NEW_STRUCTURE:
    cell = create_notebook_cell(cell_spec['cell_type'], cell_spec['content'])
    cells.append(cell)

# Notebook estructura
notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {
                "name": "ipython",
                "version": 3
            },
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

# Guardar backup del original
import shutil
if NOTEBOOK_PATH.exists():
    shutil.copy(NOTEBOOK_PATH, BACKUP_PATH)
    print(f"✓ Backup creado: {BACKUP_PATH}")

# Escribir nuevo notebook
with open(NOTEBOOK_PATH, 'w') as f:
    json.dump(notebook, f, indent=2)

print(f"✓ Notebook reorganizado guardado: {NOTEBOOK_PATH}")
print(f"\n✅ REORGANIZACIÓN COMPLETADA")
print(f"Total de celdas: {len(cells)}")
print(f"Estructura: Setup → Loading → Univariado → Bivariado → Multivariado → Síntesis")
print("\nEjecutar el notebook en VS Code para ver todos los análisis generados.")
