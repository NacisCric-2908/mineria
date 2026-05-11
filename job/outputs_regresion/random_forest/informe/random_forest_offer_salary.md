# Informe ejecutivo - Random Forest

## 1. Resumen ejecutivo

Este informe presenta el desempeno del modelo **Random Forest** para predecir `Offer_Salary` a partir de `dataset_offer_Salary.csv`.

### Resultado principal

- `MAE test`: 6421.5444
- `RMSE test`: 8031.7346
- `R2 test`: 0.7018
- `RMSE train`: 7820.8640
- `Brecha RMSE (test - train)`: 210.8706

**Lectura operativa:** La lectura por importancia permite identificar las variables que mas explican la variacion del salario dentro del modelo.

## 2. Archivos entregables

- Notebook principal: [regresion_offer_salary_completo.ipynb](../../../regresion_offer_salary_completo.ipynb)
- Modelo serializado: `random_forest_offer_salary.pkl`
- Informe actual: `random_forest_offer_salary.md`

## 3. Configuracion final del modelo

- `model__max_depth`: `8`
- `model__min_samples_leaf`: `5`
- `model__n_estimators`: `400`

## 4. Metricas de entrenamiento vs prueba

- **Train**: `MAE=6233.9354` | `RMSE=7820.8640` | `R2=0.7276`
- **Test**: `MAE=6421.5444` | `RMSE=8031.7346` | `R2=0.7018`

Interpretacion: una brecha train-test pequena sugiere mejor capacidad de generalizacion; una brecha amplia sugiere riesgo de sobreajuste.

## 5. Lectura ejecutiva de las graficas

### Real vs predicho

![Real vs predicho](../imagenes/random_forest_real_vs_predicho.png)

Si los puntos se acercan a la diagonal, el modelo predice salarios con mejor precision.

### Distribucion de residuos

![Distribucion de residuos](../imagenes/random_forest_residuos_hist.png)

Permite revisar si los errores se concentran cerca de cero o si hay colas con errores grandes.

### Residuos vs prediccion

![Residuos vs prediccion](../imagenes/random_forest_residuos_vs_prediccion.png)

Permite detectar patrones de sesgo: por ejemplo, si el modelo falla mas en rangos altos de salario.

### Variables mas influyentes

![Top variables](../imagenes/random_forest_top_weights.png)

### Variables con mayor importancia

- `categorical__Major_Category_STEM`: `0.3184`
- `categorical__Primary_Search_Platform_LinkedIn`: `0.2716`
- `numeric__Prior_Internships`: `0.1360`
- `categorical__Major_Category_Business`: `0.1082`
- `categorical__University_Rating_Top-tier`: `0.1018`
- `numeric__GPA`: `0.0326`
- `categorical__Primary_Search_Platform_Handshake`: `0.0092`
- `categorical__Primary_Search_Platform_Indeed`: `0.0089`
- `numeric__Applications_Submitted`: `0.0042`
- `numeric__Months_Searching`: `0.0018`


## 6. Uso del modelo serializado

```python
import pickle
from pathlib import Path
import pandas as pd

artifact_path = Path('random_forest_offer_salary.pkl')
with open(artifact_path, 'rb') as f:
    artifact = pickle.load(f)

pipeline = artifact['pipeline']
feature_columns = artifact['feature_columns']

# Ejemplo: reemplazar por un registro real con las mismas columnas
nuevo = pd.DataFrame([{col: 0 for col in feature_columns}])
pred_salary = pipeline.predict(nuevo[feature_columns])[0]
print('Prediccion de salario:', round(float(pred_salary), 2))
```

## 7. Conclusion

El modelo **Random Forest** queda disponible para uso operativo y comparacion tecnica frente a los otros algoritmos del notebook. Este informe deja trazabilidad completa de metricas, parametros, variables relevantes y artefactos.
