# Informe ejecutivo - Gradient Boosting para Offer_Salary

## 1. Resumen ejecutivo

Este informe documenta el modelo **Gradient Boosting** para predecir `Offer_Salary` a partir de `dataset_offer_Salary.csv`.

Gradient Boosting construye árboles secuenciales que corrigen los errores del paso anterior. En este taller quedó muy cerca de la familia lineal, pero sin superarla.

### Resultado principal

- `MAE test`: 6349.8631
- `RMSE test`: 7951.8339
- `R2 test`: 0.7077
- `RMSE train`: 7981.4820
- `Brecha RMSE (test - train)`: -29.6482

**Lectura operativa:** Gradient Boosting ofrece una generalización razonable y un comportamiento muy cercano al de regresión lineal y Ridge, pero no logra arrebatarles el liderazgo a los modelos lineales regularizados. Su principal valor aquí es que confirma la estabilidad de la señal del problema: el salto de complejidad no produce una mejora significativa.

## 2. Archivos entregables

- Notebook principal: [regresion_offer_salary_completo.ipynb](../../../regresion_offer_salary_completo.ipynb)
- Modelo serializado: `gradient_boosting_offer_salary.pkl`
- Informe actual: `gradient_boosting_offer_salary.md`

## 3. Configuracion final del modelo

- `model__learning_rate`: `0.1`
- `model__max_depth`: `2`
- `model__n_estimators`: `200`
- `model__subsample`: `0.8`

## 4. Metricas de entrenamiento vs prueba

- **Train**: `MAE=6362.6054` | `RMSE=7981.4820` | `R2=0.7163`
- **Test**: `MAE=6349.8631` | `RMSE=7951.8339` | `R2=0.7077`

La brecha train-test es pequeña y, de hecho, el `RMSE` de prueba resulta un poco menor que el de entrenamiento (`-29.6482`). Esto sugiere un comportamiento estable, aunque no suficiente para superar al mejor modelo. La generalización es buena, pero la mejora frente a la familia lineal es marginal.

## 5. Lectura ejecutiva de las graficas

### Real vs predicho

![Real vs predicho](../imagenes/gradient_boosting_real_vs_predicho.png)

La dispersión sigue un patrón consistente, pero no tan ajustado como el de Lasso. El gráfico muestra que el modelo aproxima bien la tendencia general, aunque con más variabilidad que la mejor solución final.

### Distribucion de residuos

![Distribucion de residuos](../imagenes/gradient_boosting_residuos_hist.png)

Los residuos aparecen repartidos de forma razonable alrededor de cero. El modelo no presenta un sesgo extremo, pero tampoco mejora claramente la precisión del mejor enfoque lineal.

### Residuos vs prediccion

![Residuos vs prediccion](../imagenes/gradient_boosting_residuos_vs_prediccion.png)

Este gráfico ayuda a revisar si el boosting captura patrones no lineales relevantes. La lectura práctica es que sí aprende relaciones útiles, pero no lo suficiente como para justificar su mayor complejidad frente a Lasso.

### Variables mas influyentes

![Top variables](../imagenes/gradient_boosting_top_weights.png)

### Variables con mayor importancia

- `categorical__Major_Category_STEM`: `0.3060`
- `categorical__Primary_Search_Platform_LinkedIn`: `0.1960`
- `numeric__Prior_Internships`: `0.1862`
- `categorical__University_Rating_Top-tier`: `0.1127`
- `categorical__Major_Category_Business`: `0.0540`
- `categorical__Major_Category_Healthcare`: `0.0367`
- `categorical__Major_Category_Humanities`: `0.0334`
- `categorical__Primary_Search_Platform_Indeed`: `0.0315`
- `numeric__GPA`: `0.0274`
- `categorical__Major_Category_Arts`: `0.0131`

Las variables más importantes vuelven a ser las mismas que en el resto del taller. Eso es una buena señal: el modelo está captando la misma estructura subyacente del problema, pero sin una mejora real suficiente para desplazar a la solución regularizada.


## 6. Uso del modelo serializado

```python
import pickle
from pathlib import Path
import pandas as pd

artifact_path = Path('gradient_boosting_offer_salary.pkl')
with open(artifact_path, 'rb') as f:
    artifact = pickle.load(f)

pipeline = artifact['pipeline']
feature_columns = artifact['feature_columns']

nuevo = pd.DataFrame([{col: 0 for col in feature_columns}])
pred_salary = pipeline.predict(nuevo[feature_columns])[0]
print('Prediccion de salario:', round(float(pred_salary), 2))
```

### Explicación del uso

1. Se carga el modelo en pickle.
2. Se reutiliza el pipeline completo con preprocesamiento.
3. Se arma una fila con el mismo esquema de variables.
4. Se calcula la predicción de salario.

## 7. Comparación técnica dentro del taller

Gradient Boosting quedo muy cerca de la familia lineal, pero aún por detrás de Lasso por `9.8991` puntos de RMSE. Eso lo posiciona como un modelo competitivo, aunque no como el ganador. En comparación con Random Forest y el árbol simple, sí ofrece una mejor relación entre sesgo y varianza, pero no alcanza el mejor equilibrio global.

## 8. Conclusion

El modelo **Gradient Boosting** es sólido y competitivo, pero en este dataset no supera a la solución lineal regularizada. Su papel dentro del taller es importante porque confirma que la señal es relativamente estable y que la ganancia de complejidad es limitada.

Si se prioriza el mejor desempeño, Lasso sigue siendo la elección final. Si se valora explorar una alternativa no lineal cercana en calidad, Gradient Boosting es la mejor de las opciones basadas en árboles.
