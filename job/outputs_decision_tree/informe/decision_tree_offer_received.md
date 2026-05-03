# Informe de entrenamiento y despliegue - Decision Tree para Offer_Received

## 1. Resumen ejecutivo

Este notebook construye un clasificador binario para predecir `Offer_Received` priorizando la detección de la clase positiva `SI OFERTA (1)`. El flujo usa un `Pipeline` con preprocesamiento diferenciado, búsqueda de hiperparámetros, ajuste de umbral y evaluación final sobre un conjunto de prueba separado.

La configuración final encontrada fue:

- `criterion = gini`
- `max_depth = None`
- `min_samples_split = 2`
- `min_samples_leaf = 5`
- `ccp_alpha = 0.0001`
- `threshold óptimo = 0.32`

Con ese ajuste, el modelo prioriza recall de la clase positiva, que era el objetivo principal del proyecto.

## 2. Qué se hizo en el notebook

- Se cargó el dataset limpio `dataset_offer_Received.csv`.
- Se separaron variables numéricas y categóricas.
- Se entrenó `DecisionTreeClassifier` dentro de un `Pipeline` con `OneHotEncoder`.
- Se optimizaron hiperparámetros con `GridSearchCV` y validación cruzada estratificada.
- Se ajustó el umbral de decisión para priorizar `SI OFERTA`.
- Se generaron gráficas del entrenamiento y la evaluación.
- Se serializó el modelo final con metadata en formato `.pkl`.

## 3. Artefactos generados

### Modelo serializado
- `decision_tree_offer_received.pkl`

### Imágenes PNG
- `decision_tree_confusion_matrix.png`
- `decision_tree_roc_curve.png`
- `decision_tree_precision_recall_curve.png`
- `decision_tree_threshold_tradeoff.png`
- `decision_tree_feature_importance.png`
- `decision_tree_tree_preview.png`
- `decision_tree_rule_comparison.png`

## 4. Qué contiene el archivo `.pkl`

El archivo `.pkl` guarda un diccionario con esta estructura:

- `pipeline`: el pipeline entrenado con preprocesamiento y árbol de decisión.
- `best_threshold`: el umbral óptimo para convertir probabilidades en clase final.
- `best_params`: los mejores hiperparámetros encontrados.
- `target_name`: nombre de la variable objetivo.
- `feature_columns`: columnas esperadas de entrada.
- `numeric_columns`: columnas numéricas.
- `categorical_columns`: columnas categóricas.
- `metrics_default_threshold`: métricas con umbral 0.50.
- `metrics_optimized_threshold`: métricas con el umbral óptimo.
- `threshold_preview`: tabla resumida del barrido de umbrales sobre validation.

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

Con el umbral base de 0.50 se obtuvo:

- `Accuracy = 0.9015`
- `Precision = 0.7928`
- `Recall = 0.9644`
- `F1-Score = 0.8702`
- `F-beta (1.5) = 0.9042`
- `ROC-AUC = 0.9672`
- `Average Precision = 0.9140`

Con el umbral optimizado se obtuvo:

- `Accuracy = 0.8894`
- `Precision = 0.7593`
- `Recall = 0.9911`
- `F1-Score = 0.8598`
- `F-beta (1.5) = 0.9060`
- `ROC-AUC = 0.9672`
- `Average Precision = 0.9140`

La matriz de confusión orientada a `SI OFERTA` quedó con:

- `TP = 6785`
- `FN = 61`
- `FP = 2151`
- `TN = 11003`

## 9. Variables con mayor peso en la decisión

El árbol no usa coeficientes positivos o negativos como una regresión logística. Su interpretación se basa en la frecuencia y profundidad de las divisiones. Las variables con mayor importancia agregada fueron:

- Second_Round_Interviews: 0.6310
- First_Round_Interviews: 0.2006
- Applications_Submitted: 0.1256
- Primary_Search_Platform_Indeed: 0.0207
- Prior_Internships: 0.0132
- GPA: 0.0033
- Primary_Search_Platform_LinkedIn: 0.0030
- Primary_Search_Platform_Handshake: 0.0026
- Major_Category_Arts: 0.0000
- Extra_Curricular_Activities: 0.0000

Las variables que más empujan hacia `SI OFERTA` son las que aparecen cerca de la raíz y reducen más la impureza: sobre todo `Second_Round_Interviews`, `First_Round_Interviews`, `Applications_Submitted` y `GPA`.

## 10. Decisiones técnicas que cambiaron el resultado

1. Se mantuvo `class_weight='balanced'` para no ignorar la clase positiva.
2. Se hizo `train_test_split` estratificado para conservar la proporción de clases.
3. Se entrenó con `GridSearchCV` sobre `criterion`, `max_depth`, `min_samples_split`, `min_samples_leaf` y `ccp_alpha`.
4. La mejor configuración se eligió con `F-beta (1.5)` para priorizar el recall de `SI OFERTA`.
5. El umbral se optimizó sobre validation para reforzar la captura de la clase positiva.

El impacto frente al umbral base de `0.50` fue:

- `Accuracy`: `0.9015 -> 0.8894`
- `Precision`: `0.7928 -> 0.7593`
- `Recall`: `0.9644 -> 0.9911`
- `F1-Score`: `0.8702 -> 0.8598`
- `F-beta (1.5)`: `0.9042 -> 0.9060`
- `ROC-AUC`: `0.9672 -> 0.9672`

## 11. Lectura operativa de la matriz de confusión

Con el orden `[1, 0]`, la lectura prioriza `SI OFERTA`:

- `TP = 6785`: ofertas reales detectadas.
- `FN = 61`: ofertas reales perdidas.
- `FP = 2151`: no ofertas marcadas como oferta.
- `TN = 11003`: no ofertas correctamente descartadas.

En proporción por clase real, el modelo captura aproximadamente `99.11%` de los casos positivos reales y clasifica correctamente cerca de `83.65%` de los casos negativos.

## 12. Script mínimo de inferencia

```python
import pickle
from pathlib import Path
import pandas as pd

MODEL_PATH = Path("job/outputs_decision_tree/informe/decision_tree_offer_received.pkl")

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

El modelo está orientado a minimizar falsos negativos sobre `SI OFERTA`. Por eso el umbral óptimo puede quedar por debajo de 0.50 si eso mejora la captura de positivos reales.

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
