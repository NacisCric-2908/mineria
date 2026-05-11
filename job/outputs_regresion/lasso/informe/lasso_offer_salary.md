# Informe ejecutivo - Lasso

## 1. Resumen ejecutivo

Este informe presenta el desempeno del modelo **Lasso** para predecir `Offer_Salary` a partir de `dataset_offer_Salary.csv`.

### Resultado principal

- `MAE test`: 6339.7907
- `RMSE test`: 7941.9348
- `R2 test`: 0.7085
- `RMSE train`: 8014.7539
- `Brecha RMSE (test - train)`: -72.8191

**Lectura operativa:** La lectura por coeficientes facilita explicar la direccion de cada variable sobre el salario predicho, sin interpretar causalidad.

## 2. Archivos entregables

- Notebook principal: [regresion_offer_salary_completo.ipynb](../../../regresion_offer_salary_completo.ipynb)
- Modelo serializado: `lasso_offer_salary.pkl`
- Informe actual: `lasso_offer_salary.md`

## 3. Configuracion final del modelo

- `model__alpha`: `10`

## 4. Metricas de entrenamiento vs prueba

- **Train**: `MAE=6388.4189` | `RMSE=8014.7539` | `R2=0.7140`
- **Test**: `MAE=6339.7907` | `RMSE=7941.9348` | `R2=0.7085`

Interpretacion: una brecha train-test pequena sugiere mejor capacidad de generalizacion; una brecha amplia sugiere riesgo de sobreajuste.

## 5. Lectura ejecutiva de las graficas

### Real vs predicho

![Real vs predicho](../imagenes/lasso_real_vs_predicho.png)

Si los puntos se acercan a la diagonal, el modelo predice salarios con mejor precision.

### Distribucion de residuos

![Distribucion de residuos](../imagenes/lasso_residuos_hist.png)

Permite revisar si los errores se concentran cerca de cero o si hay colas con errores grandes.

### Residuos vs prediccion

![Residuos vs prediccion](../imagenes/lasso_residuos_vs_prediccion.png)

Permite detectar patrones de sesgo: por ejemplo, si el modelo falla mas en rangos altos de salario.

### Variables mas influyentes

![Top variables](../imagenes/lasso_top_weights.png)

### Variables con mayor peso en el modelo

**Coeficientes positivos (empujan salario hacia arriba):**
- `categorical__Major_Category_STEM`: `19833.9501`
- `categorical__University_Rating_Top-tier`: `10066.6696`
- `categorical__Major_Category_Business`: `9833.9417`
- `categorical__Primary_Search_Platform_LinkedIn`: `7962.5759`
- `numeric__Prior_Internships`: `4809.1823`

**Coeficientes negativos (empujan salario hacia abajo):**
- `categorical__Primary_Search_Platform_Indeed`: `-5019.2704`
- `categorical__Major_Category_Arts`: `-292.5596`
- `categorical__Major_Category_Humanities`: `-240.9746`
- `numeric__Networking_Events_Attended`: `-114.1643`
- `categorical__School_Size_Small`: `-38.9119`


## 6. Uso del modelo serializado

```python
import pickle
from pathlib import Path
import pandas as pd

artifact_path = Path('lasso_offer_salary.pkl')
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

El modelo **Lasso** queda disponible para uso operativo y comparacion tecnica frente a los otros algoritmos del notebook. Este informe deja trazabilidad completa de metricas, parametros, variables relevantes y artefactos.
