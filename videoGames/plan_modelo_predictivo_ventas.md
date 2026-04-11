# Plan Maestro para Modelo Predictivo de Ventas (Seccion 20)

## 1) Objetivo del proyecto
Construir un modelo de regresion para predecir ventas de videojuegos usando el dataset curado.

Objetivo principal:
- Predecir `total_sales_final`.

Objetivo recomendado para modelado:
- Entrenar sobre `log1p(total_sales_final)` para reducir sesgo por cola larga y outliers.

## 2) Principios metodologicos (obligatorios)
- No mezclar periodos futuros en entrenamiento (evitar leakage temporal).
- No ocultar imputaciones: toda imputacion debe dejar trazabilidad.
- Separar reglas deterministicas (contables) de imputaciones estadisticas.
- Reportar resultados globales y por segmento (anio, plataforma, genero).

## 3) Politica oficial para nulos en ventas regionales
Variables regionales:
- `north_america_sales`
- `japan_sales`
- `europe_sales`
- `other_regions_sales`

Variable total:
- `total_sales_final`

Definicion:
- `missing_regional_count` = cantidad de regiones nulas por fila (0 a 4).

### Caso A: faltan 0 regiones
Accion:
- No imputar.
- Verificar consistencia contable:
  - `regional_sum = na + jp + eu + other`
  - `sales_diff = total_sales_final - regional_sum`
- Si `abs(sales_diff) <= 0.01`, tratar como redondeo.

### Caso B: falta 1 region
Accion recomendada (deterministica):
- Imputar con balance contable:
  - `region_faltante = total_sales_final - suma_regiones_observadas`

Reglas de aceptacion:
- Si valor imputado >= 0 y razonable, aceptar imputacion.
- Si valor imputado < 0 o genera inconsistencia fuerte, no imputar y marcar fila para revision.

Campos de trazabilidad:
- `regional_imputation_method = "balance_1_missing"`
- `regional_imputed_flag = 1`

### Caso C: faltan 2 regiones
Accion:
- No existe solucion unica por algebra.
- Para EDA regional: mantener nulos.
- Para modelo (solo si necesitas mas cobertura): imputacion estadistica por grupo.

Orden recomendado de grupos para mediana:
1. (`platform`, `genre`, `release_year`)
2. (`platform`, `genre`)
3. (`platform`)
4. mediana global de la region

Campos:
- `regional_imputation_method = "group_median_2_missing"` (o nivel aplicado)
- `regional_imputed_flag = 1`

### Caso D: faltan 3 regiones
Accion:
- Igual que caso C, pero mas incierto.
- Solo imputar si aporta valor al modelo y no distorsiona distribucion.
- Priorizar excluir del analisis regional fino.

Campos:
- `regional_imputation_method = "group_median_3_missing"` (o nivel aplicado)
- `regional_imputed_flag = 1`

### Caso E: faltan 4 regiones
Subcaso E1: tambien falta `total_sales_final`
- Excluir de cualquier modelo de ventas.

Subcaso E2: existe `total_sales_final` pero no hay regiones
- Mantener para modelo de ventas totales (target global).
- Excluir de modelo por region.
- No inventar reparto regional completo.

## 4) Regla de eliminacion vs conservacion
No eliminar en bloque por tener nulos regionales.

Eliminar solo cuando:
- falta `total_sales_final` (si es target del modelo), o
- faltan features criticas despues de intentar imputacion controlada.

Conservar cuando:
- hay target y al menos bloque minimo de features utiles.

## 5) Variables para modelado
### Target
- Version A: `total_sales_final`
- Version B (preferida): `log1p(total_sales_final)`

### Features base
- Temporales: `release_year`, `release_month`, `release_decade`
- Cualitativas: `platform`, `genre`, `publisher`, `developer`
- Opcionales: `critic_score`, indicadores de calidad/imputacion

### Features de control de calidad (muy recomendadas)
- `missing_regional_count`
- `regional_imputed_flag`
- `regional_imputation_method`
- `sales_consistency_flag`
- `critic_score_missing_flag`

## 6) Estrategia para `critic_score`
Dado su alto missingness, usar dos pipelines y comparar:

Pipeline 1 (conservador):
- No usar `critic_score`.

Pipeline 2 (sensibilidad):
- Imputar por grupo (`platform`, `genre`) con fallback global.
- Agregar `critic_score_missing_flag`.

Criterio:
- Mantener en modelo final solo si mejora metrica de forma estable y consistente por tiempo.

## 7) Particion y validacion (clave)
Usar separacion temporal, por ejemplo:
- Train: hasta 2016
- Validation: 2017-2019
- Test: 2020-2024

Notas:
- Ajustar cortes segun cobertura real por anio.
- Usar validacion cruzada temporal (TimeSeriesSplit o ventana expandida) cuando sea posible.

## 8) Baselines y modelos candidatos
## Baselines (obligatorios)
- Baseline 1: mediana global
- Baseline 2: mediana por (`platform`, `genre`)

## Modelos
- Ridge / Lasso (lineales con regularizacion)
- Random Forest Regressor
- Gradient Boosting (XGBoost o LightGBM si esta disponible)

## 9) Metricas y criterios de exito
Evaluar en escala log y original.

Metricas:
- MAE
- RMSE
- MAPE (solo si no explota con valores cercanos a cero)

Reporte minimo:
- Metricas globales en validation y test
- Error por anio
- Error por plataforma
- Error por genero
- Comparacion contra baselines

Criterio de seleccion:
- Mejor balance entre error, estabilidad temporal e interpretabilidad.

## 10) Riesgos y mitigaciones
Riesgo 1: sesgo de cobertura temporal
- Mitigar con split temporal y reporte por anio.

Riesgo 2: sesgo por missingness no aleatorio
- Mitigar con flags de nulos/imputacion y analisis de sensibilidad.

Riesgo 3: fuga de informacion
- No usar variables derivadas del target de forma directa para predecir target futuro.

Riesgo 4: alta cardinalidad en categoricas
- Agrupar categorias raras o usar encoding robusto.

## 11) Checklist ejecutable (paso a paso)
1. Cargar CSV curado y validar esquema.
2. Construir `missing_regional_count`.
3. Aplicar politica por casos 0/1/2/3/4.
4. Crear columnas de trazabilidad de imputacion.
5. Definir target en escala original y log.
6. Construir features + preprocessing.
7. Hacer split temporal (train/val/test).
8. Entrenar baselines.
9. Entrenar modelos candidatos.
10. Evaluar metricas globales y por subgrupos.
11. Comparar pipelines con/sin `critic_score`.
12. Elegir modelo final y documentar limites.

## 12) Entregables esperados para cumplir Seccion 20
- Notebook de modelado con pipeline reproducible.
- Tabla comparativa de modelos y baselines.
- Graficos de error por tiempo y segmentos.
- Conclusiones de negocio y limitaciones metodologicas.
- Recomendacion final de modelo para uso operativo.

## 13) Decision recomendada final
- No eliminar automaticamente filas por nulos regionales.
- Imputar de forma deterministica cuando falta 1 region.
- Usar imputacion estadistica controlada (con flags) para 2-3 faltantes solo si mejora cobertura util.
- Excluir casos sin target para regresion de ventas.
- Validar siempre con corte temporal para asegurar que el modelo sea defendible.
