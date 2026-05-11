# Informe ejecutivo - Ridge para Offer_Salary

## 1. Resumen ejecutivo

Este informe documenta la version Ridge del modelo de regresion para predecir `Offer_Salary` a partir de `dataset_offer_Salary.csv`.

Ridge agrega regularizacion L2 para estabilizar coeficientes, reducir sensibilidad al ruido y mantener una lectura interpretativa muy cercana a la regresion lineal base.

### Resultado principal

- `MAE test`: 6341.3403
- `RMSE test`: 7944.5669
- `R2 test`: 0.7083
- `RMSE train`: 8014.2404
- `Brecha RMSE (test - train)`: -69.6736

**Lectura operativa:** Ridge confirma que la relacion entre variables y salario esta bien capturada por un esquema lineal regularizado. El desempeno es practicamente identico al de la regresion lineal y muestra que la regularizacion aporta estabilidad, pero no una ventaja decisiva en este dataset.

## 2. Archivos entregables

- Notebook principal: [regresion_offer_salary_completo.ipynb](../../../regresion_offer_salary_completo.ipynb)
- Modelo serializado: `ridge_offer_salary.pkl`
- Informe actual: `ridge_offer_salary.md`

## 3. Configuracion final del modelo

- `model__alpha`: `1`

## 4. Metricas de entrenamiento vs prueba

- **Train**: `MAE=6388.0345` | `RMSE=8014.2404` | `R2=0.7140`
- **Test**: `MAE=6341.3403` | `RMSE=7944.5669` | `R2=0.7083`

La brecha train-test es muy pequena y negativa en `RMSE`, lo que muestra una generalizacion estable. No hay senales de sobreajuste; el modelo se comporta como una version ligeramente mas conservadora de la regresion lineal.

## 5. Lectura ejecutiva de las graficas

### Real vs predicho

![Real vs predicho](../imagenes/ridge_real_vs_predicho.png)

La nube de puntos sigue la diagonal con un patron parecido al de regresion lineal. Esto indica que Ridge conserva la misma capacidad de ajuste general, con una ligera estabilizacion en el comportamiento de los coeficientes.

### Distribucion de residuos

![Distribucion de residuos](../imagenes/ridge_residuos_hist.png)

El histograma muestra una distribucion de errores consistente con el baseline lineal. No hay una mejora dramatica en la dispersion, lo cual es esperable porque Ridge no cambia la familia funcional del modelo; solo controla la magnitud de los coeficientes.

### Residuos vs prediccion

![Residuos vs prediccion](../imagenes/ridge_residuos_vs_prediccion.png)

No aparece un patron no lineal fuerte que sugiera que Ridge haya resuelto una relacion mas compleja. La principal ventaja aqui es la estabilidad, no una nueva estructura de ajuste.

### Variables mas influyentes

![Top variables](../imagenes/ridge_top_weights.png)

### Variables con mayor peso en el modelo

**Coeficientes positivos (empujan salario hacia arriba):**
- `categorical__Major_Category_STEM`: `14078.1763`
- `categorical__Primary_Search_Platform_LinkedIn`: `6998.4645`
- `categorical__University_Rating_Top-tier`: `6759.3360`
- `numeric__Prior_Internships`: `4811.7946`
- `categorical__Major_Category_Business`: `4080.5187`

**Coeficientes negativos (empujan salario hacia abajo):**
- `categorical__Major_Category_Arts`: `-6284.2062`
- `categorical__Major_Category_Humanities`: `-6092.0637`
- `categorical__Primary_Search_Platform_Indeed`: `-6026.0911`
- `categorical__Major_Category_Healthcare`: `-5782.4251`
- `categorical__University_Rating_Lower-tier`: `-3401.4081`

La interpretacion es practicamente la misma que en la regresion lineal, pero con coeficientes ligeramente mas estabilizados. Eso confirma que Ridge no altera el relato del problema; solo lo hace un poco mas robusto ante colinealidad y ruido.


## 6. Uso del modelo serializado

```python
import pickle
from pathlib import Path
import pandas as pd

artifact_path = Path('ridge_offer_salary.pkl')
with open(artifact_path, 'rb') as f:
    artifact = pickle.load(f)

pipeline = artifact['pipeline']
feature_columns = artifact['feature_columns']

nuevo = pd.DataFrame([{col: 0 for col in feature_columns}])
pred_salary = pipeline.predict(nuevo[feature_columns])[0]
print('Prediccion de salario:', round(float(pred_salary), 2))
```

### Explicacion del uso

1. Se carga el modelo serializado.
2. Se recupera el pipeline completo.
3. Se arma un registro con las columnas esperadas.
4. Se predice directamente el salario.

## 7. Comparacion tecnica dentro del taller

Ridge quedo practicamente empatado con regresion lineal. La diferencia en RMSE frente a la regresion lineal fue de solo `0.0246` puntos, una variacion tan pequena que se interpreta como empate tecnico. Frente a Lasso, Ridge quedo apenas por detras por `2.6321` puntos de RMSE.

## 8. Conclusion

El modelo **Ridge** es una muy buena referencia regularizada, pero no logra superar a Lasso. Su valor principal es confirmar que la solucion para este dataset no requiere pasar a una complejidad mayor: una familia lineal bien preprocesada ya resuelve el problema con bastante solidez.

Si se busca estabilidad y una interpretacion muy cercana al baseline, Ridge es una opcion correcta; si se busca el mejor desempeno final, Lasso sigue siendo la alternativa mas fuerte.
