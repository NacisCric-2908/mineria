# Informe ejecutivo - Regresion lineal

## 1. Resumen ejecutivo

Este informe presenta el desempeno del modelo **Regresion lineal** para predecir `Offer_Salary` a partir de `dataset_offer_Salary.csv`.

### Resultado principal

- `MAE test`: 6341.3362
- `RMSE test`: 7944.5915
- `R2 test`: 0.7083
- `RMSE train`: 8014.2402
- `Brecha RMSE (test - train)`: -69.6487

**Lectura operativa:** La lectura por coeficientes facilita explicar la direccion de cada variable sobre el salario predicho, sin interpretar causalidad.

## 2. Archivos entregables

- Notebook principal: [regresion_offer_salary_completo.ipynb](../../../regresion_offer_salary_completo.ipynb)
- Modelo serializado: `linear_regression_offer_salary.pkl`
- Informe actual: `linear_regression_offer_salary.md`

## 3. Configuracion final del modelo

- `fit_intercept`: `True`
- `positive`: `False`
- `n_jobs`: `None`

## 4. Metricas de entrenamiento vs prueba

- **Train**: `MAE=6388.0280` | `RMSE=8014.2402` | `R2=0.7140`
- **Test**: `MAE=6341.3362` | `RMSE=7944.5915` | `R2=0.7083`

Interpretacion: una brecha train-test pequena sugiere mejor capacidad de generalizacion; una brecha amplia sugiere riesgo de sobreajuste.

## 5. Lectura ejecutiva de las graficas

### Real vs predicho

![Real vs predicho](../imagenes/linear_regression_real_vs_predicho.png)

Si los puntos se acercan a la diagonal, el modelo predice salarios con mejor precision.

### Distribucion de residuos

![Distribucion de residuos](../imagenes/linear_regression_residuos_hist.png)

Permite revisar si los errores se concentran cerca de cero o si hay colas con errores grandes.

### Residuos vs prediccion

![Residuos vs prediccion](../imagenes/linear_regression_residuos_vs_prediccion.png)

Permite detectar patrones de sesgo: por ejemplo, si el modelo falla mas en rangos altos de salario.

### Variables mas influyentes

![Top variables](../imagenes/linear_regression_top_weights.png)

### Variables con mayor peso en el modelo

**Coeficientes positivos (empujan salario hacia arriba):**
- `categorical__Major_Category_STEM`: `14080.8433`
- `categorical__Primary_Search_Platform_LinkedIn`: `6999.1262`
- `categorical__University_Rating_Top-tier`: `6760.4091`
- `numeric__Prior_Internships`: `4811.7390`
- `categorical__Major_Category_Business`: `4082.1282`

**Coeficientes negativos (empujan salario hacia abajo):**
- `categorical__Major_Category_Arts`: `-6287.9000`
- `categorical__Major_Category_Humanities`: `-6092.3985`
- `categorical__Primary_Search_Platform_Indeed`: `-6027.2600`
- `categorical__Major_Category_Healthcare`: `-5782.6730`
- `categorical__University_Rating_Lower-tier`: `-3402.0021`


## 6. Uso del modelo serializado

```python
import pickle
from pathlib import Path
import pandas as pd

artifact_path = Path('linear_regression_offer_salary.pkl')
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

El modelo **Regresion lineal** queda disponible para uso operativo y comparacion tecnica frente a los otros algoritmos del notebook. Este informe deja trazabilidad completa de metricas, parametros, variables relevantes y artefactos.
