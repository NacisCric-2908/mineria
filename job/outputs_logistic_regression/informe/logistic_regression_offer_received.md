# Informe de entrenamiento y despliegue - Logistic Regression para Offer_Received

## 1. Resumen ejecutivo

Este notebook construye un clasificador binario para predecir `Offer_Received` priorizando la detección de la clase positiva `SI OFERTA (1)`. El flujo usa un `Pipeline` con preprocesamiento diferenciado, búsqueda de hiperparámetros, calibración de umbral y evaluación final sobre conjunto de prueba.

La configuración final encontrada fue:

- `solver = saga`
- `penalty = l2`
- `C = 0.03`
- `threshold óptimo = 0.30`

Con ese ajuste, el modelo prioriza recall de la clase positiva, que era el objetivo principal del proyecto.

## 2. Qué se hizo en el notebook

- Se cargó el dataset limpio `dataset_offer_Received.csv`.
- Se separaron variables numéricas y categóricas.
- Se entrenó `LogisticRegression` dentro de un `Pipeline` con `StandardScaler` y `OneHotEncoder`.
- Se optimizaron hiperparámetros con `GridSearchCV` y validación cruzada estratificada.
- Se ajustó el umbral de decisión para priorizar `SI OFERTA`.
- Se generaron gráficas del entrenamiento y la evaluación.
- Se serializó el modelo final con metadata en formato `.pkl`.

## 3. Artefactos generados

### Modelo serializado
- `logistic_regression_offer_received.pkl`

### Imágenes PNG
- `logistic_regression_confusion_matrix.png`
- `logistic_regression_roc_curve.png`
- `logistic_regression_precision_recall_curve.png`
- `logistic_regression_threshold_tradeoff.png`
- `logistic_regression_top_coefficients.png`

## 4. Qué contiene el archivo `.pkl`

El archivo `.pkl` guarda un diccionario con esta estructura:

- `pipeline`: el pipeline entrenado con preprocesamiento y regresión logística.
- `best_threshold`: el umbral óptimo para convertir probabilidades en clase final.
- `best_params`: los mejores hiperparámetros encontrados.
- `target_name`: nombre de la variable objetivo.
- `feature_columns`: columnas esperadas de entrada.
- `numeric_columns`: columnas numéricas.
- `categorical_columns`: columnas categóricas.
- `metrics_default_threshold`: métricas con umbral 0.50.
- `metrics_optimized_threshold`: métricas con umbral óptimo.
- `threshold_preview`: tabla resumida del barrido de umbrales.

## 5. Entradas del modelo

Las entradas deben tener exactamente la misma estructura del dataset limpio usado en entrenamiento, pero sin la columna objetivo `Offer_Received`.

Columnas esperadas:

```python
['GPA', 'University_Rating', 'Major_Category', 'Region', 'Prior_Internships', 'Extra_Curricular_Activities', 'Networking_Events_Attended', 'School_Size', 'Primary_Search_Platform', 'Months_Searching', 'Applications_Submitted', 'First_Round_Interviews', 'Second_Round_Interviews']
```

## 6. Salidas del modelo

El artefacto permite obtener tres cosas principales:

- `pipeline.predict_proba(X)[:, 1]`: probabilidad de la clase `SI OFERTA (1)`.
- `pipeline.predict(X)`: clase predicha con la configuración interna del modelo.
- Predicción ajustada por umbral usando `best_threshold`.

La salida principal para negocio es la probabilidad de pertenecer a `SI OFERTA (1)` y la clase resultante al aplicar el umbral óptimo.

## 7. Cómo obtener el porcentaje de seguridad

La seguridad de la predicción se interpreta como la probabilidad estimada para la clase positiva.

Fórmula:

```python
porcentaje_seguridad = probabilidad_clase_1 * 100
```

Ejemplo:

- Si `probabilidad_clase_1 = 0.93`, entonces `porcentaje_seguridad = 93%`.

## 8. Métricas principales

Con el umbral optimizado se obtuvo:

- `Accuracy = 0.7713`
- `Precision = 0.6054`
- `Recall = 0.9533`
- `F1-Score = 0.7405`
- `F-beta (1.5) = 0.8100`
- `ROC-AUC = 0.8940`

La matriz de confusión orientada a `SI OFERTA` quedó con:

- `TP = 6526`
- `FN = 320`
- `FP = 4254`
- `TN = 8900`

## 9. Variables transformadas y lectura del modelo

El modelo no opera sobre 13 columnas originales, sino sobre 26 variables transformadas:

- 8 variables numéricas estandarizadas.
- 18 variables binarias nuevas creadas a partir de las categorías originales.

Las expansiones fueron:

- `University_Rating` -> `Lower-tier`, `Mid-tier`, `Top-tier`.
- `Major_Category` -> `Arts`, `Business`, `Healthcare`, `Humanities`, `STEM`.
- `Region` -> `Midwest`, `Northeast`, `South`, `West`.
- `School_Size` -> `Large`, `Medium`, `Small`.
- `Primary_Search_Platform` -> `Handshake`, `Indeed`, `LinkedIn`.

### Variables con mayor efecto positivo sobre `SI OFERTA`

- `num__Second_Round_Interviews = +2.325704`
- `num__Prior_Internships = +0.452109`
- `num__GPA = +0.196455`
- `cat__University_Rating_Top-tier = +0.099526`
- `cat__Primary_Search_Platform_LinkedIn = +0.043241`
- `cat__Major_Category_Business = +0.033551`
- `cat__Primary_Search_Platform_Handshake = +0.018884`
- `cat__Major_Category_Humanities = +0.018818`
- `cat__School_Size_Small = +0.013824`
- `cat__Region_South = +0.013140`

### Variables con mayor efecto negativo sobre `SI OFERTA`

- `num__First_Round_Interviews = -0.579221`
- `num__Applications_Submitted = -0.228509`
- `cat__Primary_Search_Platform_Indeed = -0.068537`
- `cat__Major_Category_Arts = -0.060822`
- `cat__University_Rating_Mid-tier = -0.054697`
- `cat__University_Rating_Lower-tier = -0.051240`
- `num__Months_Searching = -0.029172`
- `cat__School_Size_Medium = -0.023975`
- `cat__Region_West = -0.016408`
- `cat__Region_Northeast = -0.011481`

La interpretación es directa: más avance en entrevistas, más prácticas y mejor perfil académico aumentan la probabilidad de oferta; más tiempo buscando, más aplicaciones enviadas y algunas combinaciones de plataforma/categoría reducen esa probabilidad.

## 10. Decisiones técnicas que cambiaron el resultado

1. Se mantuvo `class_weight='balanced'` para no ignorar la clase positiva.
2. Se hizo `train_test_split` estratificado para conservar la proporción de clases.
3. Se entrenó con `GridSearchCV` sobre `solver`, `penalty` y `C`.
4. La mejor configuración fue `solver='saga'`, `penalty='l2'`, `C=0.03`.
5. El umbral se optimizó en `0.30` usando `F-beta (1.5)` para priorizar recall.

El impacto frente al umbral base de `0.50` fue:

- `Accuracy`: `0.8101 -> 0.7713` (`-0.0388`)
- `Precision`: `0.7012 -> 0.6054` (`-0.0958`)
- `Recall`: `0.7756 -> 0.9533` (`+0.1776`)
- `F1-Score`: `0.7365 -> 0.7405` (`+0.0040`)
- `F-beta (1.5)`: `0.7511 -> 0.8100` (`+0.0589`)
- `ROC-AUC`: `0.8940 -> 0.8940` (`0.0000`)

## 11. Lectura operativa de la matriz de confusión

Con el orden `[1, 0]`, la lectura prioriza `SI OFERTA`:

- `TP = 6526`: ofertas reales detectadas.
- `FN = 320`: ofertas reales perdidas.
- `FP = 4254`: no ofertas marcadas como oferta.
- `TN = 8900`: no ofertas correctamente descartadas.

En proporción por clase real, el modelo captura aproximadamente `95%` de los casos positivos reales y clasifica correctamente cerca de `68%` de los casos negativos.

## 12. Script mínimo de inferencia

```python
import pickle
from pathlib import Path
import pandas as pd

MODEL_PATH = Path("job/outputs_logistic_regression/informe/logistic_regression_offer_received.pkl")

with open(MODEL_PATH, "rb") as f:
    artifact = pickle.load(f)

modelo = artifact["pipeline"]
umbral = artifact["best_threshold"]
feature_columns = artifact["feature_columns"]

# Define manualmente una fila de entrada usando las mismas columnas del entrenamiento.
# Cambia estos valores por el caso real que quieras evaluar.
entrada = pd.DataFrame([{
    "GPA": 2.0,
    "University_Rating": "Top-tier",
    "Major_Category": "STEM",
    "Region": "West",
    "Prior_Internships": 1,
    "Extra_Curricular_Activities": 1,
    "Networking_Events_Attended": 3,
    "School_Size": "Medium",
    "Primary_Search_Platform": "LinkedIn",
    "Months_Searching": 6,
    "Applications_Submitted": 25,
    "First_Round_Interviews": 4,
    "Second_Round_Interviews": 2,
}])

# Asegura el mismo orden de columnas que se usó al entrenar.
entrada = entrada[feature_columns]

# 1. Probabilidad estimada de recibir oferta.
probabilidad = modelo.predict_proba(entrada)[:, 1][0]

# 2. Clase final usando el umbral óptimo del notebook.
prediccion = int(probabilidad >= umbral)

# 3. Porcentaje de seguridad para SI OFERTA.
porcentaje_seguridad = probabilidad * 100

print("prediccion:", prediccion)
print("probabilidad_clase_1:", round(probabilidad, 4))
print("porcentaje_seguridad:", round(porcentaje_seguridad, 2), "%")
```

## 13. Lectura operativa

El modelo está orientado a minimizar falsos negativos sobre `SI OFERTA`. Por eso el umbral óptimo es 0.30 y no 0.50. Ese ajuste mejora la captura de positivos reales, aunque aumenta los falsos positivos.

En términos prácticos:

- Si necesitas cobertura sobre posibles ofertas, usa el umbral óptimo del archivo `.pkl`.
- Si necesitas una decisión más estricta, puedes subir el umbral, pero perderás recall.

## 14. Uso recomendado

1. Cargar el `.pkl` con `pickle.load`.
2. Preparar un `DataFrame` con las columnas esperadas.
3. Calcular `predict_proba`.
4. Aplicar el umbral óptimo `best_threshold`.
5. Interpretar `probabilidad_clase_1 * 100` como porcentaje de seguridad.

## 15. Observación final

Este notebook se diseñó para explicar y priorizar la clase `SI OFERTA (1)`. Las gráficas exportadas en PNG respaldan la interpretación del modelo y el archivo `.pkl` permite reutilizar el entrenamiento sin repetir todo el proceso.
