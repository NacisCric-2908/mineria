# Contexto Operativo Completo - job/

Este documento condensa el contexto de trabajo de toda la carpeta `job/` para que una nueva instancia pueda continuar el plan sin releer todo el proyecto en profundidad.

Fuente principal: `primerCorte.ipynb` + artefactos de `outputs_primer_corte/`.

## 1) Objetivo del proyecto (estado actual)

Analizar la eficacia del embudo de busqueda laboral estudiantil y preparar base robusta para dos modelos predictivos:

- Objetivo A (clasificacion): predecir `Offer_Received`.
- Objetivo B (regresion): estimar `Offer_Salary` (solo casos con oferta).

## 2) Inventario minimo de `job/`

- `guia.txt`: marco de trabajo (problema, datos, limpieza, EDA, interpretacion, entregables).
- `job_search_platform_efficacy_100k.csv`: dataset original (100,000 filas, 20 columnas).
- `primerCorte.ipynb`: notebook integral del primer corte (diagnostico, limpieza, EDA, interpretacion, plan siguiente).
- `consolidar_outputs_primer_corte.py`: script reproducible de consolidacion de outputs redundantes en archivos maestros.
- `requirements.txt`: stack analitico Python.
- `outputs_primer_corte/`: artefactos de salida para trazabilidad, insight y continuidad.

## 3) Lo que hizo `primerCorte.ipynb` (resumen de flujo real)

El notebook sigue una logica secuencial explicita:

1. Setup y configuracion reproducible.
2. Carga de datos y definicion de rutas de salida.
3. Analisis estrategico del problema (pensamiento de ingenieria).
4. Catalogo de variables con foco en riesgo de sesgo y leakage.
5. Diagnostico de calidad de datos (tipos, nulos, duplicados, outliers, categorias, targets).
6. Decisiones de limpieza justificadas una por una.
7. Transformaciones y feature engineering sin perder informacion estructural.
8. EDA univariado y bivariado con multiples familias de graficos.
9. Sintesis de hallazgos, recomendaciones, hipotesis y plan de modelado.
10. Export de datasets, reportes y tablas de soporte.

## 4) Principios metodologicos que se deben preservar

Esta es la forma de trabajo que debe mantenerse en los siguientes pasos.

### 4.1 Regla de oro

Cada bloque debe responder siempre:

- Que se va a hacer.
- Por que se va a hacer.
- Resultado esperado.

### 4.2 Criterios de calidad obligatorios

- Todo cambio debe quedar argumentado, fundamentado y trazable.
- No confundir correlacion con causalidad.
- Diferenciar nulos estructurales de faltantes problematicos.
- Evitar data leakage en features y pipelines.
- Priorizar interpretabilidad operativa, no solo metrica.
- Reportar riesgos y mitigaciones antes de concluir.
- Exportar evidencia replicable de cada etapa.

### 4.3 Politicas concretas heredadas del primer corte

- Nulos estructurales de variables de oferta se conservan; no imputar por defecto.
- Duplicados de `Student_ID` se eliminan solo si existen.
- Outliers se detectan y marcan; no se eliminan sin evidencia de error.
- Estandarizacion de categorias para evitar ruido por typos/capitalizacion.
- Features derivadas deben aportar informacion y evitar fuga del target.

## 5) Estado de datos y limpieza (resultado consolidado)

Segun outputs del primer corte:

- Filas: 100,000 -> 100,000 (retencion 100%).
- Columnas: 20 -> 40 (20 features nuevas en dataset final completo).
- Duplicados exactos detectados: 0.
- Nulos estructurales de variables de oferta: se preservan por validez semantica.

Metrica global de resultado:

- Tasa de oferta: 34.23%.

## 6) Hallazgos clave ya establecidos

- Predictor mas asociado a oferta: `Second_Round_Interviews` (corr 0.5492).
- `Interview_Conversion_Rate` aparece como segunda senal fuerte (corr 0.3119).
- Plataforma con mejor tasa en el corte: Handshake 36.99%.
- Plataforma mas baja en el corte: Indeed 25.79%.
- Brecha de canal: 11.20 pp (alta relevancia operativa).
- Volumen de aplicaciones por si solo explica poco (corr baja frente a avance del embudo).

## 7) Inventario completo de outputs y para que sirve cada uno

## 7.1 Datasets

- `dataset_limpio_primer_corte.csv` (100,000 filas): version limpia base para analisis del primer corte.
- `dataset_limpio_completo.csv` (100,000 filas): version extendida con encoding y features derivadas para modelado.

## 7.2 Trazabilidad y calidad

- `metadata_limpieza.csv`: metadatos de antes/despues (filas, columnas, fecha, features nuevas, duplicados).
- `bitacora_calidad.csv`: control de etapa de calidad (carga inicial vs post limpieza).
- `resumen_faltantes.csv`: conteo y porcentaje de faltantes por variable.
- `decisiones_limpieza.csv`: decisiones aplicadas con justificacion, impacto y riesgo evitado.
- `reporte_limpieza_detallado.txt`: reporte narrativo completo de limpieza.
- `outliers_iqr_resumen.csv`: umbrales IQR y porcentaje de outliers por variable.

## 7.3 Resultados analiticos

- `tasa_oferta_por_plataforma.csv`: ranking operativo de eficacia por canal.
- `top_correlaciones_offer_received.csv`: variables con mayor asociacion al target de oferta.
- `interpretaciones_graficos_detalladas.csv`: lectura analitica de visualizaciones.
- `conclusiones_ejecutivas_primer_corte.csv`: conclusiones accionables sintetizadas.
- `01_factores_comparativa.csv`: ranking de factores por magnitud y accionabilidad.
- `02_recomendaciones_operativas.csv`: recomendaciones por horizonte temporal.
- `insights_operativos_maestro.csv`: consolidado maestro de hallazgos ejecutivos, factores, recomendaciones, correlaciones y ranking de plataformas.

## 7.4 Guia y continuidad

- `respuestas_guia_26_preguntas.csv`: banco extendido de respuestas de interpretacion.
- `respuestas_guia_maestro.csv`: fuente oficial consolidada de respuestas de guia para consumo operativo.
- `matriz_consolidacion_outputs.csv`: trazabilidad de que archivos fuente alimentan cada artefacto maestro.
- `indice_outputs_finales.csv`: indice navegable de outputs finales con estado (maestro o soporte) y uso recomendado.
- `inventario_outputs_clasificados.csv`: inventario operativo para distinguir tipo de archivo, uso real y accion recomendada.
- `hipotesis_siguiente_iteracion.csv`: hipotesis para validar en siguiente ciclo.
- `plan_modelado_dos_objetivos.csv`: roadmap del modelado A/B por fases.
- `riesgos_modelado_y_mitigaciones.csv`: riesgos principales y mitigaciones.

## 7.5 Visualizaciones exportadas

Graficos estructurales y EDA:

- `04_exploracion_dataset_dimensions.png`
- `04_tipos_variables.png`
- `04_valores_faltantes.png`
- `04_tamaño_escala_dataset.png`
- `04_relevancia_calidad_4preguntas.png`
- `histogramas_base.png`
- `boxplots_base.png`
- `scatterplots_base.png`
- `correlation_matrix.png`
- `visualizacion_limpieza_resumen.png`

Graficos bivariados/multivariados del primer corte:

- `05_bivariado_scatter_plots.png`
- `06_bivariado_heatmap_correlacion.png`
- `07_bivariado_pairplot.png`
- `08_bivariado_boxplot_violin_strip.png`
- `09_bivariado_lineas_areas_barras.png`

## 8) Metodologia de trabajo obligatoria para siguiente fase (modelado)

Esta seccion define como trabajar para minimizar errores futuros.

### 8.1 Estructura estandar por cada nueva seccion/celda

Para cada bloque del notebook de modelado:

1. Contexto breve del objetivo del bloque.
2. Hipotesis o pregunta tecnica.
3. Decision metodologica (y por que).
4. Implementacion reproducible.
5. Evidencia cuantitativa (metricas/tablas/graficos).
6. Interpretacion operativa.
7. Riesgos, limites y validaciones pendientes.

### 8.2 Checklist previo a entrenar cualquier modelo

- Definir target exacto y universo de entrenamiento.
- Congelar split train/valid/test (estratificado para clasificacion).
- Excluir variables con fuga temporal o post-resultado.
- Revisar desbalance de clase y definir metrica primaria.
- Documentar baseline ingenuo antes de modelos complejos.
- Versionar artefactos y semillas de aleatoriedad.

### 8.3 Checklist para evaluacion y explicacion

- Clasificacion: ROC-AUC, F1, Recall, Precision y matriz de confusion.
- Regresion: MAE, RMSE, R2 y error por cuantiles.
- Evaluacion por subgrupos (Region, Major_Category, University_Rating).
- Comparar contra baseline y justificar mejora real.
- Traducir resultados a decisiones operativas (no solo tecnicas).

### 8.4 Reglas de justificacion minima

Toda afirmacion debe indicar al menos una de estas bases:

- Evidencia descriptiva (tabla/grafico exportado).
- Evidencia estadistica (metrica o test).
- Evidencia de robustez (validacion cruzada, sensibilidad, subgrupos).

Si no hay evidencia, se debe etiquetar explicitamente como hipotesis, no como conclusion.

## 9) Plan de continuidad recomendado (siguiente notebook o fase)

Orden sugerido para el siguiente paso predictivo:

1. Definir pipeline dual (A clasificacion, B regresion) con datasets versionados.
2. Implementar baselines reproducibles para ambos objetivos.
3. Optimizar hiperparametros y umbral (objetivo A) y error robusto (objetivo B).
4. Ejecutar evaluacion por subgrupos y reporte de riesgo de sesgo.

## 10) Plan de Segundo Corte - Modelado Predictivo

**Documento Principal**: [PLAN_MODELADO_SECOND_ITERATION.md](PLAN_MODELADO_SECOND_ITERATION.md)

El plan del segundo corte está completamente documentado en un archivo markdown ejecutable de ~9,000 palabras que incluye:

### Contenido Estructura del Plan

**7 Fases Secuenciales**:

1. **Fase 1 - Gobernanza de Datos** (1-2 días): Congelación de dataset limpio, diccionario de variables, splits train/val/test estratificados
2. **Fase 2 - Ingeniería de Variables** (3-4 días): Bloqueo de variables con fuga, codificación categórica, features derivadas, validación de leakage
3. **Fase 3 - Baselines** (2-3 días): Modelos dummy, Logistic Regression, Decision Trees para establecer mínimos de comparación
4. **Fase 4 - Optimización** (5-7 días): Búsqueda de hiperparámetros con XGBoost, LightGBM, validación cruzada anidada
5. **Fase 5 - Evaluación Técnica y por Subgrupos** (4-5 días): Test final, análisis de equidad, evaluación segmentada por región/major/universidad
6. **Fase 6 - Interpretabilidad y Decisión** (3-4 días): SHAP, feature importance, decision rules operativas, reportes ejecutivos
7. **Fase 7 - Implementación y Monitoreo** (3-4 días): Versionado reproducible, pipeline de predicción, monitoreo de drift, retraining schedule

### Criterios de Éxito Definidos

**Clasificación** (Offer_Received):
- ROC-AUC ≥ 0.70
- F1-Score ≥ 0.55
- Recall ≥ 0.50
- Gap train-test < 0.05

**Regresión** (Offer_Salary):
- RMSE ≤ $18,000
- R² ≥ 0.42
- MAE ≤ $12,000
- Residuales normales (p > 0.05)

**Equidad**:
- Disparate Impact Ratio > 0.80 (sin discriminación > 20%)
- Consistencia ROC-AUC ± 0.05 entre regiones
- Diferencia RMSE < $5,000 entre majors

### Riesgos Identificados (10 total)

Matriz de mitigación con probabilidad/impacto:
- R1: Data Leakage (CRÍTICA)
- R2: Sesgo por Subgrupos
- R3: Desbalance de Clases
- R4: Sobreajuste
- R5-R10: Calidad, Drift, Interpretabilidad, Reproducibilidad, etc.

### Hipótesis para Siguiente Iteración

- H1: Segunda entrevista media relación entre aplicaciones y oferta
- H2: Efecto de plataforma depende del major
- H3: GPA amplificado por internships
- H4: Networking > volumen de aplicaciones

### Timeline Estimado

**21-30 días calendario** (1 mes) con equipo multidisciplinaria:
- 1x Data Scientist (full-time)
- 1x Feature Engineer (0.5 FTE)
- 1x Auditor Analítico (0.3 FTE)
- 1x ML Engineer (0.5 FTE)
- 1x PM (0.2 FTE)

### Datos y Contexto de Entrada

Utiliza como base:
- `dataset_limpio_primer_corte.csv` (100,000 filas)
- Hallazgos consolidados en outputs_primer_corte/
- Correlaciones y predictores identificados en primer corte
5. Exportar artefactos de la fase en una nueva carpeta de outputs (por ejemplo `outputs_modelado_segundo_corte/`).

## 10) Convencion de trabajo para futuras instancias

Si una instancia nueva entra al proyecto, debe:

1. Leer este documento completo primero.
2. Validar que los outputs listados existan y no esten corruptos.
3. Usar `dataset_limpio_completo.csv` como base de modelado (excepto justificacion contraria).
4. Mantener el estilo de razonamiento: argumento -> evidencia -> interpretacion -> decision.
5. No borrar ni sobreescribir artefactos historicos sin versionado.

Con esto se preserva continuidad tecnica, trazabilidad analitica y calidad metodologica.

## 11) Estado del refactor profesional (abril 2026)

Se implemento una primera fase de refactor para reducir sobrecarga sin perder informacion:

1. `primerCorte.ipynb` ahora tiene una portada metodologica mas profesional y elimina interpretacion anticipada hardcodeada en introduccion.
2. Se elimino duplicacion tecnica de setup en una seccion intermedia, reemplazandola por validacion de consistencia del entorno.
3. Se agrego un bloque de utilidades para export y estandarizacion de secciones, con foco en mantenibilidad.
4. Se consolidaron outputs redundantes en artefactos maestros de consulta principal.
5. Se elimino el duplicado estricto `respuestas_guia_iniciales.csv` y se estandarizo `respuestas_guia_maestro.csv` como fuente oficial.

Regla de continuidad desde este punto:

- Consultar primero los archivos con estado `maestro` en `indice_outputs_finales.csv`.
- Usar archivos `soporte` solo para trazabilidad fina o auditoria de detalle.

Clasificacion practica de outputs (para uso diario):

- `tipo = imagen_grafica_png`: imagenes de graficas listas para informe.
- `tipo = tabla_reporte`: tablas para imprimir informacion y evidencia cuantitativa.
- `estado_uso = maestro_activo`: salida prioritaria para lectura directa.
- `estado_uso = soporte_generado_notebook`: salida de soporte que el notebook usa o exporta de forma directa.
- `estado_uso = soporte_no_referenciado_directo`: soporte historico/tecnico que se conserva por trazabilidad.

Politica de imagenes:

- Todas las graficas exportadas en `outputs_primer_corte/` deben terminar en `.png`.
- La verificacion de formatos se ejecuta automaticamente en `consolidar_outputs_primer_corte.py`.