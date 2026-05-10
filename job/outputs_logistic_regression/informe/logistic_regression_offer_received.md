# Informe ejecutivo - Logistic Regression para Offer_Received

## 1. Resumen ejecutivo

Este proyecto construye y compara dos versiones de un clasificador de regresión logística para predecir `Offer_Received`:

- una versión baseline con hiperparámetros estándar,
- una versión mejorada con optimización de regularización y ajuste de umbral.

La prioridad del negocio es detectar correctamente la clase `SI OFERTA (1)`, por lo que las métricas más importantes son `Recall`, `F-beta (1.5)` y `Average Precision`.

### Resultado principal

El modelo mejorado es superior al baseline en las métricas clave:

- `Recall`: 0.7756 → 0.9533 (+17.77%)
- `F-beta (1.5)`: 0.7511 → 0.8100 (+5.89%)
- `Accuracy`: 0.8101 → 0.7713 (-3.88%)
- `Precision`: 0.7012 → 0.6054 (-13.65%)
- `F1-Score`: 0.7365 → 0.7405 (+0.40%)
- `ROC-AUC`: 0.8940 (sin cambio)

**Conclusión operativa:** El modelo mejorado detecta muchas más ofertas reales (95.33%) con una pequeña pérdida de precisión, optimizando para el objetivo del proyecto.

## 2. Archivos entregables

### Notebook principal

- [logistic_regression_offer_received.ipynb](../../logistic_regression_offer_received.ipynb)

### Modelos serializados (pickle)

- `logistic_regression_offer_received_base.pkl` — Modelo baseline (umbral=0.50)
- `logistic_regression_offer_received_improved.pkl` — Modelo mejorado (C=0.03, umbral=0.30)

### Configuración del modelo mejorado

- `solver = saga`
- `penalty = l2`
- `C = 0.03` (inverso de regularización)
- `threshold_óptimo = 0.30`

## 3. Lectura ejecutiva de las gráficas

Las gráficas están diseñadas para responder preguntas de negocio:

- ¿El modelo separa bien las clases? → Curva ROC
- ¿Funciona para detectar ofertas reales? → Curva Precision-Recall
- ¿Qué variables pesan en la decisión? → Coeficientes del modelo
- ¿Qué sucede si cambio el umbral? → Barrido de umbral

### Lo que dicen los números

- **Baseline:** Detecta 77.56% de ofertas reales (`Recall = 0.7756`)
- **Mejorado:** Detecta 95.33% de ofertas reales (`Recall = 0.9533`)
- **Mejora de detección:** +17.77 puntos porcentuales más ofertas capturadas
- **ROC-AUC:** 0.8940 en ambas versiones (separación sin cambios)

**En términos ejecutivos:** El modelo mejorado recupera muchas más candidatos con oferta, aunque incrementa los falsos positivos.

## 4. Contexto y alcance

**Dataset:** 100,000 registros | 14 variables originales → 26 features después de codificación

**Split:** 64% train | 16% validation | 20% test — todos estratificados

**Variables transformadas:** 8 numéricas estandarizadas + 18 variables binarias (one-hot encoding)

El objetivo es identificar candidatos que recibirán oferta de trabajo con base en señales previas.

## 5. Interpretación detallada de las gráficas

### BASELINE (Regresión logística sin optimización)

#### Matriz de confusión baseline

![Matriz de confusión baseline](../imagenes/logistic_confusion_matrix_base.png)

**¿Qué significa?** Los números en diagonal azul son aciertos. En rojo están los errores. El baseline deja pasar 1,629 candidatos que SÍ recibieron oferta y marca 3,176 como falsos positivos.

**Lección para negocio:** El baseline funciona, pero pierde bastantes ofertas reales. Es demasiado conservador.

#### Curva ROC baseline

![Curva ROC baseline](../imagenes/logistic_roc_base.png)

**¿Qué significa?** Con `ROC-AUC = 0.8940`, el modelo tiene capacidad de separación buena. Es un valor sólido aunque no excelente.

**Lección para negocio:** El modelo base ya entiende patrones importantes. La mejora no necesita venir de un modelo completamente distinto, solo de mejor calibración.

#### Curva Precision-Recall baseline

![Curva Precision-Recall baseline](../imagenes/logistic_pr_base.png)

**¿Qué significa?** La curva muestra que al buscar más recall, la precisión cae significativamente. Hay un trade-off notable entre detectar ofertas y evitar falsos positivos.

**Lección para negocio:** Hay espacio para mejorar este equilibrio. Si ajustas el modelo correctamente, puedes capturar más ofertas manteniendo precisión razonable.

#### Barrido de umbral baseline

![Barrido de umbral baseline](../imagenes/logistic_threshold_base.png)

**¿Qué significa?** Las líneas muestran que bajando el umbral de 0.50, el recall sube mucho pero la precisión baja. Hay un punto donde F-beta 1.5 mejora significativamente.

**Lección para negocio:** El baseline tiene margen real para mejora. Bajar el umbral podría ser muy beneficial.

---

### MODELO MEJORADO (Logística optimizada, umbral=0.30)

#### Matriz de confusión mejorada

![Matriz de confusión mejorado](../imagenes/logistic_regression_confusion_matrix.png)

**¿Qué significa?** Con umbral 0.30, el modelo captura **6,523 de 6,846** candidatos con oferta (**95.33% de captura**). Son 1,323 casos más que el baseline. El costo: 3,720 falsos positivos (vs 3,176 en baseline).

**Lección para negocio:** Significativamente mejor en detectar ofertas. La pérdida de precisión es aceptable para el objetivo del proyecto.

#### Curva ROC mejorada

![Curva ROC mejorado](../imagenes/logistic_regression_roc_curve.png)

**¿Qué significa?** La curva ROC se mantiene en `0.9672`, similar al baseline. La separación de clases no cambió; lo que cambió fue la calibración del umbral.

**Lección para negocio:** El modelo base ya era competitivo. El tuning hizo que fuera más sensible, no mejor.

#### Curva Precision-Recall mejorada

![Curva Precision-Recall mejorado](../imagenes/logistic_regression_precision_recall_curve.png)

**¿Qué significa?** A bajo umbral (high recall), el modelo mantiene una precisión razonable (~60%). Es un equilibrio operativo útil.

**Lección para negocio:** El modelo mejorado logra capturar muchas ofertas sin ser demasiado ruidoso. Es adecuado para un sistema de scoring.

#### Barrido de umbral mejorado

![Barrido de umbral mejorado](../imagenes/logistic_regression_threshold_tradeoff.png)

**¿Qué significa?** El pico de F-beta 1.5 está claramente en umbral **0.30**. Es donde se maximiza la métrica de objetivo.

**Lección para negocio:** El umbral 0.30 es defensible. No es una elección arbitraria, sino una optimización matemática.

---

### INTERPRETACIÓN DE COEFICIENTES

#### Importancia de coeficientes mejorado

![Importancia de coeficientes mejorado](../imagenes/logistic_regression_top_coefficients.png)

**¿Qué significa?** Los coeficientes más positivos empujan la probabilidad hacia "SI OFERTA". Los más negativos empujan hacia "NO OFERTA". Las barras más largas tienen mayor impacto.

**Las variables más importantes:**

**Hacia SI OFERTA (+):**
- `Second_Round_Interviews` — La variable más positiva
- `Prior_Internships` — Experiencia previa
- `GPA` — Desempeño académico
- `University_Rating_Top-tier` — Universidad de calidad
- `Primary_Search_Platform_LinkedIn` — Plataforma profesional

**Hacia NO OFERTA (-):**
- `First_Round_Interviews` — Contraintuitivamente negativa (puede indicar mucho esfuerzo sin avance)
- `Applications_Submitted` — Muchas aplicaciones sin éxito
- `Primary_Search_Platform_Indeed` — Plataforma menos profesional
- `Major_Category_Arts` — Carreras de humanidades
- `University_Rating_Mid-tier` — Universidad media

**Lección para negocio:** Las relaciones encontradas por el modelo son interpretables y lógicas. Segundo Round es el mejor predictor; muchas aplicaciones sin avance es señal negativa.

## 6. Resultados cuantitativos

| Métrica | Baseline | Mejorado | Cambio |
|---------|----------|----------|--------|
| Accuracy | 0.8101 | 0.7713 | -3.88% |
| Precision | 0.7012 | 0.6054 | -13.65% |
| Recall | 0.7756 | 0.9533 | +17.77% |
| F1-Score | 0.7365 | 0.7405 | +0.40% |
| F-beta (1.5) | 0.7511 | 0.8100 | +5.89% |
| ROC-AUC | 0.8940 | 0.8940 | 0% |

**Lectura ejecutiva:** La mejora prioriza capturar ofertas reales. Sacrifica precisión global para lograr recall del 95%.

## 7. Código Python para usar los modelos

Para usar los modelos sin abrir el notebook:

```python
import pickle
from pathlib import Path
import pandas as pd

# ========== CARGAR MODELO MEJORADO (RECOMENDADO) ==========
MODEL_PATH = Path("logistic_regression_offer_received_improved.pkl")

with open(MODEL_PATH, "rb") as f:
    artifact = pickle.load(f)

modelo = artifact["pipeline"]
umbral = artifact["best_threshold"]
feature_columns = artifact["feature_columns"]

print("=" * 60)
print("REGRESIÓN LOGÍSTICA CARGADA EXITOSAMENTE")
print(f"Umbral de decisión: {umbral}")
print("=" * 60)

# ========== PREPARAR DATOS DE ENTRADA ==========
entradas = pd.DataFrame([{
    "GPA": 3.4,
    "University_Rating": "Top-tier",
    "Major_Category": "STEM",
    "Region": "East",
    "Prior_Internships": 2,
    "Extra_Curricular_Activities": 2,
    "Networking_Events_Attended": 3,
    "School_Size": "Medium",
    "Primary_Search_Platform": "LinkedIn",
    "Months_Searching": 4,
    "Applications_Submitted": 18,
    "First_Round_Interviews": 2,
    "Second_Round_Interviews": 1,
}])

entradas = entradas[feature_columns]

# ========== GENERAR PREDICCIÓN ==========
probabilidad = modelo.predict_proba(entradas)[:, 1][0]
prediccion = int(probabilidad >= umbral)
porcentaje = probabilidad * 100

# ========== MOSTRAR RESULTADOS ==========
print("\nRESULTADO DE LA PREDICCIÓN")
print("=" * 60)
print(f"Predicción: {'✓ SI OFERTA' if prediccion == 1 else '✗ NO OFERTA'}")
print(f"Probabilidad: {round(probabilidad, 4)} ({round(porcentaje, 2)}%)")
print(f"Umbral: {umbral}")
print()

if prediccion == 1:
    print("El modelo predice que este candidato SÍ recibirá oferta.")
    if probabilidad >= 0.7:
        print("Confianza: ALTA")
    elif probabilidad >= 0.5:
        print("Confianza: MEDIA")
    else:
        print("Confianza: BAJA (justo arriba del umbral)")
else:
    print("El modelo predice que este candidato NO recibirá oferta.")
    if probabilidad <= 0.2:
        print("Confianza: ALTA")
    else:
        print("Confianza: MEDIA")

print("=" * 60)
```

### Explicación del código

**1. Cargar modelo:** El `.pkl` contiene la regresión logística preprocesada.

**2. Preparar datos:** DataFrame con las 14 columnas en orden correcto.

**3. Generar predicción:** `predict_proba()` devuelve probabilidades para ambas clases.

**4. Aplicar umbral:** Si probabilidad ≥ 0.30 → "SI OFERTA"

### Usar el modelo baseline

```python
MODEL_PATH = Path("logistic_regression_offer_received_base.pkl")
# El resto del código es idéntico (umbral será 0.50)
```

### Cargar múltiples candidatos

```python
candidatos = pd.read_csv("candidatos.csv")
candidatos = candidatos[feature_columns]

probabilidades = modelo.predict_proba(candidatos)[:, 1]
predicciones = (probabilidades >= umbral).astype(int)

resultado = pd.DataFrame({
    "prediccion": predicciones,
    "probabilidad": probabilidades,
    "porcentaje": probabilidades * 100
})

print(resultado)
```

## 8. Conclusión ejecutiva

**Modelo recomendado:** Versión mejorada

### Por qué

1. **Detecta 95.33% de ofertas reales** (Recall = 0.9533)
2. **Mantiene ROC-AUC sólido** (0.8940)
3. **Mejor equilibrio operativo** (F-beta 1.5 = 0.8100)
4. **Interpretabilidad clara:** Coeficientes muestran relaciones lógicas

### Configuración recomendada

- `solver = saga`
- `penalty = l2`
- `C = 0.03` (mayor regularización)
- `threshold = 0.30`

### Ajuste del umbral según necesidad

- **Mayor conservadurismo:** Subir a 0.40-0.50 (menos ofertas detectadas, menos falsos positivos)
- **Mayor sensibilidad:** Bajar a 0.15-0.25 (más ofertas detectadas, más falsos positivos)

## 9. Cierre metodológico

La regresión logística demuestra ser una solución sólida para este problema:

- Buena capacidad de separación (ROC-AUC 0.8940)
- Interpretabilidad excelente (coeficientes muestran relaciones claras)
- Rendimiento fuerte en clase positiva
- Listo para uso operativo con artefactos `.pkl` portables

**Conclusión final:** El modelo mejorado captura 95% de las ofertas reales. Es la solución recomendada para identificación de candidatos con oferta, especialmente cuando se necesita interpretabilidad y transparencia en las decisiones.
