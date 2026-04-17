# Plan de Trabajo: Modelado Predictivo Segundo Corte
**Fecha de Creación**: Abril 17, 2026  
**Dataset**: Job Search Platform Efficacy (100,000 estudiantes)  
**Versión del Plan**: 1.0  

---

## 📋 RESUMEN EJECUTIVO

Este documento establece la **hoja de ruta para construir dos modelos predictivos complementarios** sobre un dataset de 100,000 registros de estudiantes en búsqueda de empleo:

1. **Modelo A (Clasificación)**: Predecir la probabilidad de recibir una oferta de trabajo (`Offer_Received`)
2. **Modelo B (Regresión)**: Predecir el salario de la oferta (`Offer_Salary`) para candidatos seleccionados

**Métrica de éxito inicial**: Mejora cuantificable frente a baselines establecidas, equidad por subgrupos, y trazabilidad reproducible en toda la cadena.

---

## 1. OBJETIVO Y CONTEXTO

### 1.1 Definición del Problema

**Contexto de Negocio**:  
Entender qué factores influyen en el éxito de un estudiante para obtener oferta de empleo y, para quienes la reciben, qué variables determinan el salario base. La tasa global de oferta observada es del **34.23%**, con variabilidad significativa por plataforma (Handshake: 36.99%, Indeed: 25.79%).

**Objetivos Analíticos**:
- **Objetivo A**: Construir un modelo de clasificación que prediga `Offer_Received` (binario: 0=sin oferta, 1=con oferta)
- **Objetivo B**: Construir un modelo de regresión que prediga `Offer_Salary` (continuo, en USD, solo para casos con oferta)

### 1.2 Público Objetivo

- **Analistas de Datos**: Necesitan modelos reproducibles y documentados
- **Stakeholders Operativos**: Requieren interpretabilidad y reglas de decisión claras
- **Equipos de Auditoría**: Demandan equidad, trazabilidad y control de sesgos

---

## 2. ESTRUCTURA DEL PLAN (7 FASES)

### FASE 1: Definición y Gobernanza de Datos

**Objetivo**: Congelar el dataset limpio, documentar variables permitidas y crear separaciones reproducibles train/validation/test.

**Actividades**:
1. Crear versión final congelada del dataset limpio (`dataset_limpio_segundo_corte.csv`)
2. Construir diccionario de variables especificando:
   - Tipo de dato (numérico, categórico, ordinal)
   - Rango esperado y valores únicos
   - Uso permitido en entrenamiento (sí/no y razón)
3. Implementar estratificación para separación train/validation/test:
   - **Estrategia**: Estratificar por `Offer_Received` (para clasificación) y quintiles de salario (para regresión)
   - **Proporciones**: 70% train, 15% validation, 15% test
4. Crear un registro de decisiones de gobernanza (quién decide qué variable se incluye/excluye)

**Entregables**:
- `gobernanza_variables.csv` (listado de variables permitidas/bloqueadas con justificación)
- `diccionario_variables.md` (documentación completa)
- `train_validation_test_splits.parquet` (índices de división estratificada)

**Dueño**: Data Steward / Científico de Datos Senior  
**Duración Estimada**: 1-2 días de trabajo

---

### FASE 2: Ingeniería de Variables

**Objetivo**: Construir características que maximicen poder predictivo sin introducir fuga de información.

#### 2.1 Bloqueo Preventivo de Variables

**Excluidas del modelo** (prevención de data leakage):
- `Student_ID`: Solo identificador, sin poder predictivo
- `Company_Size_Offered`: Información post-decisión de oferta
- `Role_Relevance`: Solo existe para quienes recibieron oferta
- `Time_to_Offer_Days`: Información post-resultado
- Cualquier variable derivada del resultado final

#### 2.2 Variables Base Permitidas

| Variable | Tipo | Uso en A (Clasif.) | Uso en B (Regresión) | Justificación |
|----------|------|-----------------|-------------------|----------------|
| GPA | Numérico | ✓ | ✓ | Señal de desempeño académico |
| University_Rating | Categórico | ✓ | ✓ | Prestigio institucional |
| Major_Category | Categórico | ✓ | ✓ | Demanda diferencial por disciplina |
| Region | Categórico | ✓ | ✓ | Mercados laborales geográficos |
| Prior_Internships | Numérico | ✓ | ✓ | Experiencia previa |
| Extra_Curricular_Activities | Numérico | ✓ | ✓ | Señal de compromiso |
| Networking_Events_Attended | Numérico | ✓ | ✓ | Esfuerzo de búsqueda activo |
| School_Size | Categórico | ✓ | ✓ | Contexto institucional |
| Primary_Search_Platform | Categórico | ✓ | ✓ | Canal de búsqueda |
| Months_Searching | Numérico | ✓ | ✓ | Duración del proceso |
| Applications_Submitted | Numérico | ✓ | ✓ | Intensidad de búsqueda |
| First_Round_Interviews | Numérico | ✓ | ✓ | Avance en embudo |
| Second_Round_Interviews | Numérico | ✓ | ✓ | **Más predictivo** (r=0.549) |

**Nota**: `Accepted_Offer` no se usa en clasificación pues es posterior a `Offer_Received`; tampoco en regresión.

#### 2.3 Ingeniería Específica por Objetivo

**Para Modelo A (Clasificación)**:
1. **Codificación Categórica**:
   - `University_Rating`: One-hot encoding (top 10 instituciones) + "Other"
   - `Major_Category`: Target encoding basado en tasa de oferta
   - `Region`: One-hot encoding
   - `Primary_Search_Platform`: Frecuencia codificada
   - `School_Size`: Ordinal encoding

2. **Variables Derivadas (Embudo)**:
   - `conversion_app_to_1st = First_Round_Interviews / (Applications_Submitted + 1)` (evitar división por cero)
   - `conversion_1st_to_2nd = Second_Round_Interviews / (First_Round_Interviews + 1)`
   - `conversion_2nd_to_offer` (aproximación: Segunda ronda es 80% correlacionada con oferta)

3. **Estandarización**:
   - Numéricos continuos (GPA, Months_Searching, etc.): StandardScaler
   - Contar variables: Normalizacion log o sqrt si distribución sesgada

**Para Modelo B (Regresión)**:
1. **Codificación Categórica**:
   - `Major_Category`: Ordinal según salario medio observado
   - `University_Rating`: Numérica (Top Tier=3, Tier2=2, Tier3=1)
   - `Region`: Dummies o target-encoded
   - Resto igual a Clasificación

2. **Variables Derivadas**:
   - `gpa_major_interaction = GPA × [dummy para STEM]`
   - `internships_major_interaction = Prior_Internships × [dummy para STEM]`
   - `networking_intensity = Networking_Events_Attended / max(Networking_Events_Attended)`

3. **Control de Colinealidad**:
   - Calcular matriz de correlación y eliminar si VIF > 5 para variables numéricos
   - Aplicar PCA si colinealidad extrema

#### 2.4 Validación de Ingeniería

- **Test de Leakage**: Calcular correlación con `Offer_Received` solo usando datos train; aplicar a validation sin reajuste
- **Estabilidad**: Validar que distribuciones de train/validation/test son comparables (KS test)
- **Poder Discriminante**: Verificar que variables derivadas mejoran información mutua frente a baseline

**Entregables**:
- `feature_engineering_pipeline.py` (código reproducible)
- `feature_importance_baseline.csv` (importancia univariada antes del modelo)
- `validation_leakage_report.md` (verificación sin data leakage)

**Dueño**: Feature Engineer / Científico de Datos  
**Duración Estimada**: 3-4 días

---

### FASE 3: Baselines y Línea Base

**Objetivo**: Establecer mínimos de comparación para justificar complejidad de modelos más sofisticados.

#### 3.1 Baselines para Clasificación

| Modelo | Configuración | Propósito |
|--------|---------------|----------|
| **Dummy Classifier (Estrategia: "Most Frequent")** | Predice siempre la clase mayoritaria (no oferta, 65.77%) | Piso mínimo: ~66% accuracy |
| **Dummy Classifier (Estrategia: "Stratified")** | Muestrea respetando proporciones | Baseline sin información |
| **Logistic Regression (L2)** | Regularización por defecto | Modelo lineal interpretable |
| **Decision Tree** | max_depth=5, min_samples_leaf=10 | Captura interacciones simples |

**Métricas de Evaluación**:
- ROC-AUC (área bajo curva)
- Accuracy (% total correcto)
- F1-Score (media armónica Precision-Recall)
- Precision (falsos positivos controlados)
- Recall (falsos negativos controlados)
- Matriz de confusión

#### 3.2 Baselines para Regresión

| Modelo | Configuración | Propósito |
|--------|---------------|----------|
| **Dummy Regressor (Media)** | Predice salario promedio ($76,000) | Baseline sin información |
| **Linear Regression (OLS)** | Sin regularización | Efectos aditivos lineales |
| **Random Forest Regressor** | n_estimators=50, max_depth=10 | Captura no-linealidades |

**Métricas de Evaluación**:
- MAE (Error Absoluto Medio)
- RMSE (Raíz del Error Cuadrático Medio)
- R² (Proporción de varianza explicada)
- MAPE (Error Porcentual Absoluto Medio, robusto a escala)
- Gráficos de residuales (heterocedasticidad, normalidad)

#### 3.3 Criterios de Aceptación de Baseline

**Clasificación**:
- ROC-AUC Logistic > 0.60 (mejor que dummy)
- Mejora significativa en F1 respecto a dummy

**Regresión**:
- RMSE < promedio de salarios / 2 (error menor al 50%)
- R² > 0.30 (explica al menos 30% de varianza)

**Entregables**:
- `baseline_classification_report.md` (resultados, gráficos ROC, matrices)
- `baseline_regression_report.md` (resultados, residuales, predicciones vs actuals)
- `baseline_comparison_table.csv` (todas las métricas lado a lado)

**Dueño**: Científico de Datos  
**Duración Estimada**: 2-3 días

---

### FASE 4: Optimización de Modelos Principales

**Objetivo**: Entrenar modelos de mejor desempeño con ajuste de hiperparámetros y validación cruzada.

#### 4.1 Modelos Candidatos para Clasificación

**XGBoost Classifier**:
- Hiperparámetros a ajustar:
  - `n_estimators`: 100–300
  - `max_depth`: 3–8
  - `learning_rate`: 0.01–0.1
  - `subsample`: 0.6–0.9
  - `scale_pos_weight`: Ajustado por desbalance de clase
- Estrategia: Validación cruzada estratificada (5 folds)
- Early Stopping: Si validation_loss no mejora en 20 rondas

**LightGBM Classifier**:
- Alternativa más rápida con menos datos
- Hiperparámetros similares a XGBoost
- Validación: Stratified K-Fold (5)

**Decision Threshold Tuning**:
- Evaluar umbrales de 0.30 a 0.70 (por defecto 0.5)
- Objetivo: Maximizar F1 o Recall según necesidad operativa

#### 4.2 Modelos Candidatos para Regresión

**XGBoost Regressor**:
- Hiperparámetros a ajustar:
  - `n_estimators`: 100–500
  - `max_depth`: 4–10
  - `learning_rate`: 0.01–0.1
  - `subsample`: 0.6–1.0
- Validación: K-Fold no estratificada (5)
- Early Stopping: Si validation_rmse no mejora en 30 rondas

**Random Forest Regressor**:
- `n_estimators`: 200–500
- `max_depth`: 15–25
- `min_samples_leaf`: 5–10
- Validación: K-Fold (5)

**Gradient Boosting Regressor (sklearn)**:
- Validación cruzada estándar
- Comparación de velocidad vs XGBoost

#### 4.3 Procedimiento de Búsqueda de Hiperparámetros

**Estrategia 1: Grid Search** (si pocos parámetros)
- Definir grilla exhaustiva
- Duración: < 8 horas en máquina estándar

**Estrategia 2: Random Search** (si muchos parámetros)
- 100–200 iteraciones aleatorias
- Duración: < 4 horas

**Estrategia 3: Bayesian Optimization** (si tiempo/recursos lo permiten)
- Usar `optuna` o `hyperopt`
- ~50 iteraciones inteligentes

**Validación Cruzada Anidada**:
- Loop externo (5 folds): Para estimar error real
- Loop interno: Para ajuste de hiperparámetros en cada fold
- Reportar media ± std de métricas

#### 4.4 Control de Sobreajuste

Para ambos modelos:
1. Monitorear gap entre train_metric y validation_metric
2. Si gap > 0.05 (5 pp), aplicar regularización adicional
3. Usar early stopping y validation sets
4. Reportar métricas test finales (nunca entrenadas)

**Entregables**:
- `tuning_history_classification.csv` (todas las iteraciones, hiperparámetros, métricas)
- `tuning_history_regression.csv` (ídem)
- `best_models_params.json` (configuración ganadora para reproducibilidad)
- `learning_curves.png` (train vs validation por época)

**Dueño**: Científico de Datos  
**Duración Estimada**: 5–7 días

---

### FASE 5: Evaluación Técnica y por Subgrupos

**Objetivo**: Garantizar que los modelos generalizan bien y son equitativos en todos los segmentos de usuario.

#### 5.1 Evaluación de Clasificación

**En el conjunto TEST (datos no vistos)**:

| Métrica | Definición | Umbral Aceptable |
|---------|-----------|-----------------|
| **ROC-AUC** | Área bajo curva ROC (invariante al threshold) | > 0.70 |
| **F1-Score** | Media armónica de Precision y Recall | > 0.50 |
| **Precision** | Verdaderos Positivos / (VP + FP) | > 0.60 |
| **Recall** | Verdaderos Positivos / (VP + FN) | > 0.50 |
| **Specificity** | Verdaderos Negativos / (VN + FP) | > 0.70 |
| **Accuracy** | (VP + VN) / Total | > 0.65 |

**Visualizaciones**:
- Matriz de confusión (en test)
- Curva ROC
- Curva Precision-Recall
- Distribución de scores predichos (histograma)

#### 5.2 Evaluación de Regresión

**En el conjunto TEST (datos no vistos)**:

| Métrica | Definición | Umbral Aceptable |
|---------|-----------|-----------------|
| **MAE** | Media de errores absolutos (en USD) | < $15,000 |
| **RMSE** | Raíz del error cuadrático medio (en USD) | < $20,000 |
| **R²** | Proporción de varianza explicada | > 0.40 |
| **MAPE** | Error porcentual absoluto medio | < 20% |

**Análisis de Residuales**:
- Gráfico: Predicción vs Residual (buscar homocedasticidad)
- Gráfico Q-Q (normalidad de residuales)
- Test de Shapiro-Wilk (p > 0.05 para normalidad)
- Análisis por cuantiles (MAE en Q1 vs Q4 de salario)

#### 5.3 Evaluación Segmentada (Equidad)

Para ambos modelos, evaluar desempeño por:

**Segmentación A: Por Región**
- Dividir test en 4 regiones
- Calcular ROC-AUC (clasif.) o RMSE (regresión) por región
- Buscar brecha > 0.05 (ROC) o > $5,000 (RMSE)
- Si existe: Documentar y considerar recalibraciones locales

**Segmentación B: Por Major**
- Dividir test en 5 majors principales
- Calcular métricas por major
- Buscar diferencias significativas

**Segmentación C: Por University_Rating**
- Dividir en 3 tiers (Top/Mid/Low)
- Evaluar si existe sesgo contra instituciones de menor prestigio

**Segmentación D: Por Primary_Search_Platform**
- Dividir en 4 plataformas principales
- Verificar que modelo no favorece plataformas sobrerepresentadas

**Test de Equidad Formal** (si disparidades detectadas):
- Fairness metric: Disparate Impact Ratio (tasa positivos en Grupo A / tasa positivos en Grupo B)
- Objetivo: Ratio > 0.8 (no más del 20% de disparidad)

#### 5.4 Interpretabilidad

**Para Clasificación (Feature Importance)**:
1. Importancia basada en árbol (gain, split)
2. Importancia por permutación (impacto en validation AUC)
3. SHAP Summary Plot (contribución promedio por feature)
4. SHAP Dependence Plots (relación feature-predicción)

**Para Regresión**:
1. Importancia de variables (ídem clasificación)
2. Partial Dependence Plots (relación marginal feature-salario)
3. SHAP Waterfall (explicación instance-specific)

**Entregables**:
- `evaluation_classification_test.md` (métricas, gráficos, interpretación)
- `evaluation_regression_test.md` (ídem)
- `fairness_report_by_segment.csv` (métricas por región, major, etc.)
- `shap_importance_plot.png` (visualización de contribuciones)
- `equity_assessment.md` (recomendaciones si hay disparidades)

**Dueño**: Científico de Datos + Auditor Analítico  
**Duración Estimada**: 4–5 días

---

### FASE 6: Interpretabilidad y Decisión Analítica

**Objetivo**: Traducir resultados técnicos a recomendaciones operativas y reglas de decisión.

#### 6.1 Síntesis de Hallazgos (Clasificación)

**Productos Entregables**:

1. **Feature Importance Report**:
   - Top 10 variables más predictivas de "obtener oferta"
   - Magnitud del efecto (en términos de cambio de probabilidad)
   - Segmentación: ¿El ranking cambia por región o major?

2. **Decision Rules** (reglas operativas):
   - Si `Second_Round_Interviews >= 1` → Probabilidad estimada de oferta = X%
   - Si `Major_Category = STEM + GPA >= 3.5` → Probabilidad = Y%
   - Si `Primary_Search_Platform = Handshake` → Ventaja = +Z pp
   - Etc.

3. **Student Segmentation**:
   - Agrupar estudiantes por probabilidad predicha (Muy Bajo, Bajo, Medio, Alto)
   - Contar y caracterizar cada segmento
   - Recomendaciones: Qué acciones para cada grupo

4. **Drivers Clave de Oferta**:
   - Variable más importante: `Second_Round_Interviews` (r=0.549)
   - Segunda: `Prior_Internships`
   - Tercera: `GPA`
   - Implicación: Llegar a 2ª entrevista es crítico; estrategia debe priorizarla

#### 6.2 Síntesis de Hallazgos (Regresión)

**Productos Entregables**:

1. **Salary Drivers Report**:
   - Efecto marginal de cada variable en salario
   - Ejemplo: "Aumentar GPA de 3.0 a 3.5 = +$2,500 en salario esperado"
   - Quantificar en USD, no en coeficientes crudos

2. **Segmentation de Salarios**:
   - Perfiles de alto/bajo salario (qué combinaciones de variables generan qué salario)
   - Ejemplo: "STEM + Internships + Top 10 University → Salario medio $95k"

3. **Recomendaciones para Negociación**:
   - Benchmarks de salario por major/región/plataforma
   - Diferencias injustificadas que puedan explotarse
   - Identificar si hay discriminación de género/geografía (si datos disponibles)

4. **Elasticidad**:
   - Calcular cuánto cambia salario si X variable varía 1 unidad
   - Ordenar variables por "movimiento de salario" (sensibilidad)

#### 6.3 Reportes Ejecutivos

**Documento 1: Executive Summary (1-2 págs)**:
- ¿Qué se hizo?
- ¿Qué se encontró?
- ¿Cuáles son las 3 acciones recomendadas?
- ¿Cuál es el nivel de confianza en los resultados?

**Documento 2: Technical Report (10-15 págs)**:
- Metodología completa (baselines, feature engineering, tuning)
- Resultados de test (métricas, gráficos)
- Evaluación por subgrupos y análisis de equidad
- Limitaciones y riesgos residuales

**Documento 3: Implementation Playbook (5-10 págs)**:
- Cómo usar el modelo en producción
- Thresholds de decisión recomendados
- Monitoreo requerido
- Refresco / retraining schedule

**Entregables**:
- `executive_summary_models.md` (resumen ejecutivo)
- `technical_report_final.md` (reporte completo con metodología)
- `playbook_implementation.md` (guía operativa)
- `shap_interpretation_examples.md` (ejemplos interpretables para stakeholders)

**Dueño**: Científico de Datos + Product Manager  
**Duración Estimada**: 3–4 días

---

### FASE 7: Implementación, Versionado y Monitoreo

**Objetivo**: Dejar los modelos listos para producción con trazabilidad, reproducibilidad y mecanismos de alerta.

#### 7.1 Versionado y Reproducibilidad

**Estructura de Código**:
```
modelos_segundo_corte/
├── data/
│   ├── dataset_limpio_segundo_corte.csv (congelado)
│   ├── train_idx.pkl
│   ├── val_idx.pkl
│   └── test_idx.pkl
├── src/
│   ├── feature_engineering.py (transformadores reproducibles)
│   ├── model_train.py (script de entrenamiento)
│   ├── model_evaluate.py (evaluación)
│   └── predict.py (predicción en batch o online)
├── models/
│   ├── classifier_v1.pkl (mejor modelo de clasificación)
│   ├── regressor_v1.pkl (mejor modelo de regresión)
│   └── scaler_features.pkl (escalador para reproducibilidad)
├── reports/
│   ├── baseline_report.md
│   ├── tuning_results.csv
│   ├── evaluation_report.md
│   └── fairness_report.md
├── tests/
│   ├── test_no_leakage.py
│   ├── test_reproducibility.py
│   └── test_stability.py
└── requirements.txt (versiones exactas de bibliotecas)
```

**Documentación de Versionado**:
- Crear archivo `MODEL_REGISTRY.md`:
  - Versión, fecha, cambios clave, métricas de test
  - Ejemplo: "v1.0 (2026-04-30): XGBoost con 150 estimadores, ROC-AUC=0.72"

#### 7.2 Reproducibilidad Garantizada

1. **Seed Fijo**: Todos los códigos usan `random.seed(42)`, `np.random.seed(42)`, `tf.random.set_seed(42)`
2. **Requirements.txt Pinned**: 
   ```
   pandas==2.0.2
   numpy==1.24.3
   scikit-learn==1.2.2
   xgboost==1.7.5
   shap==0.42.0
   ```
3. **Data Checksum**: Guardar hash MD5 del dataset limpio para verificar que no cambió
4. **Test de Reproducibilidad**: Entrenar modelo 3 veces, verificar que métricas son idénticas (±1e-5)

#### 7.3 Pipeline de Predicción

**Modo Batch** (para cohort histórica):
```python
from predict import BatchPredictor

bp = BatchPredictor(
    model_path="models/classifier_v1.pkl",
    scaler_path="models/scaler_features.pkl"
)

df_nuevos = pd.read_csv("data/nuevos_estudiantes.csv")
predictions = bp.predict(df_nuevos)  # DataFrame con scores y probabilidades
predictions.to_csv("output/predicciones_batch.csv")
```

**Modo Online** (para casos individuales):
```python
from predict import OnlinePredictor

op = OnlinePredictor(model_path="models/classifier_v1.pkl")

student = {
    "GPA": 3.7,
    "Prior_Internships": 2,
    "Second_Round_Interviews": 1,
    # ... resto de variables
}

score, confidence = op.predict_single(student)
print(f"Probabilidad de oferta: {score:.2%} ± {confidence:.2%}")
```

#### 7.4 Monitoreo en Producción

**Métricas a Monitorear** (semanalmente):

1. **Drift de Datos** (¿los datos han cambiado?):
   - Kolmogorov-Smirnov test: p > 0.05 es OK
   - Alertar si distribución de `GPA`, `Applications_Submitted` difieren de baseline training
   - Causa: Cambio demográfico, cambio en proceso de captura

2. **Drift de Performance** (¿el modelo degradó?):
   - Si hay etiquetas disponibles: Calcular ROC-AUC semanal
   - Alertar si ROC-AUC cae > 0.03 desde baseline (0.72 → 0.69)
   - Calcular RMSE semanal para regresión

3. **Estabilidad por Subgrupo** (¿equidad se mantiene?):
   - ROC-AUC mensual por región
   - ROC-AUC mensual por major
   - Alertar si algún subgrupo degrada > 0.05 puntos

4. **Volumen y Composición**:
   - # de predicciones/semana
   - % de cada major en nuevos datos
   - Cambios abruptos → investigar

**Tablero de Monitoreo** (BI tool: Tableau, Looker, o Power BI):
- Gráficos de series temporales de todas las métricas
- Alertas automáticas si thresholds se cruzan
- Reportes semanales enviados a stakeholders

#### 7.5 Plan de Retraining

**Trigger de Retraining**:
1. Si ROC-AUC cae > 0.05 puntos → Reentrenar inmediatamente
2. Cada 3 meses (calendario) → Reentrenamiento preventivo
3. Si cambio estructural en datos detectado → Reentrenamiento urgente

**Proceso de Retraining**:
1. Usar nuevos datos (últimos 3 meses)
2. Combinar con datos históricos (70% viejo, 30% nuevo) para estabilidad
3. Repetir tuning de hiperparámetros (puede cambiar óptimo)
4. Evaluar en test histórico + nuevo (debe mejorar o mantener)
5. Validación A/B: Comparar modelo viejo vs nuevo en 10% de producción
6. Deploy gradual (10% → 50% → 100%)

#### 7.6 Documentación Final

**Entregables**:
- `pipeline_code_final/` (toda la estructura reproducible)
- `MODEL_REGISTRY.md` (versionado y metadata)
- `monitoring_setup.md` (cómo configurar alertas)
- `retraining_procedure.md` (paso a paso para reentrenamiento)
- `reproducibility_test_report.py` (verificación de reproducibilidad)

**Dueño**: Ingeniero de ML / DevOps  
**Duración Estimada**: 3–4 días

---

## 3. RIESGOS IDENTIFICADOS Y MITIGACIONES

| # | Riesgo | Descripción | Probabilidad | Impacto | Mitigación |
|---|--------|-------------|------------|---------|-----------|
| **R1** | **Fuga de Información** | Incluir accidentalmente en entrenamiento variables que se conocen solo post-resultado | Media | Crítico | Realizar test formal de leakage; bloquear variables en pipelines; code review |
| **R2** | **Sesgo por Subgrupos** | Peor desempeño en ciertos majors, regiones o universidades | Media | Alto | Evaluación segmentada obligatoria; identificar disparidades; recalibraciones diferenciales si need |
| **R3** | **Desbalance de Clases** | Clase minoritaria (oferta) sobreprediccionada como mayoritaria | Alta | Medio | Ajustar `scale_pos_weight` en XGBoost; tuning de threshold; usar F1 en lugar de accuracy |
| **R4** | **Sobreajuste** | Modelo memoriza train; bajo desempeño en test | Alta | Alto | Early stopping; validación cruzada anidada; regularización L1/L2; limitar profundidad |
| **R5** | **Nulos Incorrectos** | Nulos estructurales en `Offer_Salary` (sin oferta) mal interpretados | Baja | Medio | Documentar claramente qué nulos son estructurales; evitar imputación ciega |
| **R6** | **Data Drift** | Distribución de datos nueva (años futuros) difiere de training | Media | Medio | Monitoreo semanal; alertas automáticas; retraining cada 3 meses |
| **R7** | **Interpretabilidad Pobre** | Modelo black-box sin explicabilidad a stakeholders | Baja | Medio | Usar SHAP; crear decision rules; mantener modelos simples (LR + DT baselines) |
| **R8** | **Reproducibilidad Fallida** | No se pueden replicar resultados en otra máquina | Baja | Alto | Versionado exacto de paquetes; seeds fijos; tests de reproducibilidad |
| **R9** | **Datos Insuficientes** | Subgrupos con < 100 muestras tienen estimadores inestables | Baja | Bajo | Reporting de N por subgrupo; no hacer decisiones con N < 50 |
| **R10** | **Cambio Estructura Datos** | New variable recolectada, variable desaparece, cambio en definición | Baja | Alto | Monitoreo de schema; pruebas de validación de datos; comunicación con BI |

**Matriz de Prioridades de Mitigación**:
- **Crítica-Inmediata**: R1 (Fuga), R8 (Reproducibilidad)
- **Alta-Temprana**: R2 (Sesgo), R4 (Sobreajuste), R10 (Schema)
- **Media-Progresiva**: R3 (Desbalance), R6 (Drift), R7 (Interpretabilidad)
- **Baja-Monitoreo**: R5 (Nulos), R9 (N Insuficiente)

---

## 4. HIPÓTESIS PARA LA SIGUIENTE ITERACIÓN

A partir de hallazgos de este primer corte, la siguiente iteración debe probar:

### H1: Segunda Entrevista Media la Relación Aplicaciones → Oferta

**Planteamiento**: `Applications_Submitted` → `Second_Round_Interviews` → `Offer_Received`

**Prueba Sugerida**:
- Modelo de mediación (Baron-Kenny)
- Calcular efecto directo vs. indirecto
- Si efecto indirecto > 70% del total: Segunda ronda es el mecanismo clave
- Implicación: Diseñar intervenciones para mejorar tasa de 2ª ronda (no solo aplicaciones)

**Variable a Monitorear**: Ratio `(2nd_interviews / 1st_interviews)`

### H2: Efecto de Plataforma Depende del Major y Rating Universitario

**Planteamiento**: El retorno de usar Handshake vs. Indeed no es igual para STEM que para Humanities

**Prueba Sugerida**:
- Fit modelo con términos de interacción: `Primary_Search_Platform × Major_Category`
- Tabla de odds ratios: Handshake premium by major
- Si interacción significativa: Recomendaciones estratificadas por disciplina
- Implicación: Estudiantes STEM priorizan Handshake; Humanities usan LinkedIn

**Datos Requeridos**: Asegurar que cada combinación (Plataforma, Major) tenga N > 50

### H3: GPA Tiene Efecto Moderado en Salario, Amplificado por Internships

**Planteamiento**: `GPA` → Salario, pero el efecto es mayor si `Prior_Internships >= 2`

**Prueba Sugerida**:
- Fit modelo de regresión con interacción: `GPA × [Internship Dummy]`
- Comparar coef de GPA en ambos grupos
- Si diferencia > $500/0.1 GPA: Interacción confirmada
- Implicación: Internships hacen que GPA sea "más valioso" en negociación salarial

**Datos Requeridos**: Distribuir internships adecuadamente (actual distribution acceptable)

### H4 (Exploratorio): Efecto de "Red Networking" en Conversión

**Planteamiento**: `Networking_Events_Attended` predice `Offer_Received` mejor que volumen de aplicaciones

**Prueba Sugerida**:
- Comparar importancia relativa (SHAP) de networking vs. applications
- Sesión con stakeholders para validar si "quality > quantity"
- Implicación: Reorientar esfuerzo de estudiantes hacia calidad de networking

**Datos Requeridos**: Verificar distribución de networking events (actual parece concentrada)

---

## 5. CRITERIOS DE ÉXITO

### 5.1 Criterios Técnicos

**Clasificación** (`Offer_Received`):
- ✓ ROC-AUC ≥ 0.70 en test
- ✓ F1-Score ≥ 0.55 en test
- ✓ Recall ≥ 0.50 (detectar al menos 50% de ofertas reales)
- ✓ Gap train-test en ROC-AUC < 0.05 (no sobreajuste)

**Regresión** (`Offer_Salary`):
- ✓ RMSE ≤ $18,000 en test
- ✓ R² ≥ 0.42 en test
- ✓ MAE ≤ $12,000 en test
- ✓ Distribución de residuales normal (p > 0.05 en Shapiro-Wilk)

### 5.2 Criterios de Equidad

- ✓ No hay disparidad > 20% (Disparate Impact Ratio > 0.80) entre grupos principales
- ✓ ROC-AUC consistente ± 0.05 entre regiones
- ✓ Diferencia RMSE < $5,000 entre majors
- ✓ Report documentando disparidades residuales (si existen) e impacto operativo

### 5.3 Criterios de Calidad Analítica

- ✓ Cero data leakage (test formal superado)
- ✓ Reproducibilidad: Entrenar 3x, obtener resultados idénticos ± 1e-5
- ✓ 100% de código versionado en Git con history completo
- ✓ Documentación ejecutable (comentarios, docstrings, README)
- ✓ Todos los hiperparámetros justificados (no arbitrarios)

### 5.4 Criterios de Aplicabilidad

- ✓ Stakeholders pueden interpretar recomendaciones (comprenden feature importance)
- ✓ Decision rules definidas (threshold → acción operativa)
- ✓ Pipeline listo para producción (batch + online modes)
- ✓ Monitoreo configurado y alertas activas

---

## 6. HALLAZGOS CLAVE DEL PRIMER CORTE (Input para este Plan)

**Variables Más Predictivas** (correlación con oferta):
1. `Second_Round_Interviews`: r = 0.549 ⭐ **Muy Fuerte**
2. `First_Round_Interviews`: r = 0.485
3. `Prior_Internships`: r = 0.32
4. `GPA`: r = 0.28
5. `University_Rating`: r = 0.18

**Variación de Tasa de Oferta por Plataforma**:
- Handshake: 36.99% ⭐
- LinkedIn: 35.04%
- ZipRecruiter: 34.63%
- Indeed: 25.79%
- **Gap**: 11.2 pp entre best (Handshake) y worst (Indeed)

**Brecha Salarial por Major** (solo ofertas):
- STEM: $86,432 ⭐
- Business: $78,645
- Engineering: $89,201
- Humanities: $65,370
- **Diferencia STEM-Humanities**: $21,062 (32% premium)

**Calidad de Datos**:
- 0 duplicados exactos
- Nulos estructurales en `Offer_Salary`, etc.: 65,771 casos (66%) = sin oferta → esperado
- Sin duplicados de ID_COLUMN
- Distribución de GPA, Applications bien formada (sin outliers extremos)

---

## 7. TIMELINE Y ASIGNACIÓN

| Fase | Duración | Dueño Primario | Dependencias |
|------|----------|----------------|----|
| 1. Gobernanza | 1-2 días | Data Steward | Ninguna |
| 2. Ingeniería Vars | 3-4 días | Feature Engineer | Fase 1 |
| 3. Baselines | 2-3 días | Científico Datos | Fase 2 |
| 4. Optimización | 5-7 días | Científico Datos | Fase 3 |
| 5. Evaluación | 4-5 días | Científico Datos + Auditor | Fase 4 |
| 6. Interpretabilidad | 3-4 días | Científico Datos + PM | Fase 5 |
| 7. Implementación | 3-4 días | ML Engineer / DevOps | Fase 6 |
| **Total** | **21-30 días** | Equipo Multidisciplinaria | Secuencial |

**Cronograma Sugerido**: 1 mes calendario (2026 May 1 – May 31)

---

## 8. RECURSOS REQUERIDOS

### 8.1 Datos
- Dataset limpio congelado: `dataset_limpio_primer_corte.csv` ✓ (disponible)
- Cualquier variable adicional (a confirmar con BI)

### 8.2 Herramientas

**Software**:
- Python 3.9+
- Librerías: pandas, scikit-learn, xgboost, lightgbm, shap, optuna
- Jupyter Notebook o VSCode con Python extension
- Git (versionado)
- Optional: Docker (reproducibilidad)

**Computación**:
- Máquina estándar: 8 GB RAM, 4 cores suficiente para este volumen
- GPU (optional): 1x T4 acelera tuning ~3x (no crítica)

**Infraestructura BI**:
- Tableau / Looker / Power BI para monitoreo (asumir disponible)

### 8.3 Personas
- 1x Científico de Datos (full-time, 4 semanas)
- 1x Feature Engineer (0.5 FTE, 2 semanas)
- 1x Auditor Analítico / Fairness Specialist (0.3 FTE, 1 semana)
- 1x ML Engineer / DevOps (0.5 FTE, 1 semana post-hoc)
- 1x Product Manager (0.2 FTE, 1 semana, guía operativa)

**Costo Total Estimado**: ~$15k-20k USD (asumiendo salarios internos)

---

## 9. ACEPTACIÓN Y SIGN-OFF

Versión: **1.0**  
Fecha: **Abril 17, 2026**  
Estado: **Pendiente de Aprobación**  

**Firma de Aprobación** (completar):
- [ ] Científico de Datos Lead: _________________ Fecha: _____
- [ ] Data Steward / Governance: _________________ Fecha: _____
- [ ] Stakeholder de Negocio: _________________ Fecha: _____

**Cambios Posteriores** (documentar versión y cambios):
- Versión 1.1: [Cambio] por [Razón] - [Fecha]

---

## APÉNDICE A: Glosario de Términos

| Término | Definición |
|---------|-----------|
| **Data Leakage** | Incluir información que no estaría disponible en predicción real (ej: variable post-decisión) |
| **Overfit / Sobreajuste** | Modelo memoriza training data; bajo desempeño en nuevos datos |
| **Feature Engineering** | Construcción de nuevas variables a partir de datos crudos |
| **Cross Validation** | Técnica para estimar error real dividiendo datos múltiples veces |
| **Hyperparameter Tuning** | Búsqueda de mejores valores de parámetros del modelo |
| **ROC-AUC** | Métrica de clasificación: área bajo curva ROC (rango 0-1) |
| **F1-Score** | Media armónica de Precision y Recall; balanceado para datos desbalanceados |
| **RMSE** | Raíz del error cuadrático medio; penaliza errores grandes |
| **SHAP** | Explainable AI technique para interpretar contribución de cada variable |
| **Fairness / Equidad** | Asegurar que modelo no discrimina sistemáticamente a subgrupos |
| **Drift** | Cambio en distribución de datos (Data Drift) o performance (Model Drift) en el tiempo |

---

## APÉNDICE B: Referencias y Documentación Relacionada

1. **Dataset Limpio**: `job/outputs_primer_corte/csv/dataset_limpio_primer_corte.csv`
2. **Reporte Primer Corte**: `job/outputs_primer_corte/csv/respuestas_guia_26_preguntas.csv`
3. **Diccionario de Variables**: `job/CONTEXTO.md` (anterior analysis)
4. **Decisiones de Limpieza**: `job/outputs_primer_corte/csv/decisiones_limpieza.csv`

---

**Fin del Plan de Modelado Predictivo - Segundo Corte**

*Este documento debe ser leído, validado y ejecutado de forma secuencial. Cada fase entrega productos requeridos para la siguiente.*

