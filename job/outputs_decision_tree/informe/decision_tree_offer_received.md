# Informe ejecutivo - Decision Tree para Offer_Received

## 1. Resumen ejecutivo

Este proyecto construye y compara dos versiones de un árbol de decisión para predecir `Offer_Received`:

- una versión baseline para entender el comportamiento base del árbol,
- una versión mejorada con optimización de hiperparámetros y ajuste de umbral.

La prioridad del negocio es detectar correctamente la clase `SI OFERTA (1)`, por lo que las métricas más importantes son `Recall`, `F-beta (1.5)` y `Average Precision`.

### Resultado principal

El modelo mejorado es superior al baseline en las métricas clave:

- `Recall`: 0.9644 → 0.9911 (+2.67%)
- `F-beta (1.5)`: 0.9042 → 0.9060 (+0.18%)
- `Accuracy`: 0.9015 → 0.8894 (-1.21%)
- `Precision`: 0.7928 → 0.7593 (-3.35%)
- `F1-Score`: 0.8702 → 0.8598 (-1.04%)
- `ROC-AUC`: 0.9672 (sin cambio)

**Conclusión operativa:** El modelo mejorado captura virtualmente todas las ofertas reales (99.11%) con una pequeña pérdida de precisión global, optimizando para el objetivo del proyecto.

## 2. Archivos entregables

### Notebook principal

- [decision_tree_offer_received.ipynb](../../decision_tree_offer_received.ipynb)

### Modelos serializados (pickle)

- `decision_tree_offer_received_base.pkl` — Modelo baseline (sin optimización)
- `decision_tree_offer_received_improved.pkl` — Modelo mejorado (optimizado, umbral=0.32)

### Configuración del modelo mejorado

- `criterion = gini`
- `max_depth = None`
- `min_samples_split = 2`
- `min_samples_leaf = 5`
- `ccp_alpha = 0.0001`
- `threshold_óptimo = 0.32`

## 3. Lectura ejecutiva de las gráficas

Las gráficas están diseñadas para responder preguntas de negocio:

- ¿El árbol separa bien las clases? → Curva ROC
- ¿Funciona para detectar ofertas reales? → Curva Precision-Recall
- ¿Qué variables domina el árbol? → Importancia de variables
- ¿Cómo se ve la estructura del árbol? → Vista parcial
- ¿Qué reglas simples explican las decisiones? → Comparación con reglas manuales

### Lo que dicen los números

- **Baseline:** Detecta 96.44% de ofertas reales (`Recall = 0.9644`)
- **Mejorado:** Detecta 99.11% de ofertas reales (`Recall = 0.9911`)
- **Captura de ofertas:** El árbol mejorado apenas deja pasar casos positivos (solo 61 de 6,846)
- **ROC-AUC:** 0.9672 en ambas versiones (árbol ya separaba bien)

**En términos ejecutivos:** El árbol mejorado es casi perfecto en capturar candidatos con oferta, aunque tiene más falsos positivos.

## 4. Contexto y alcance

**Dataset:** 100,000 registros | 14 variables | 65.77% sin oferta, 34.23% con oferta

**Split:** 64% train | 16% validation | 20% test — todos estratificados

El objetivo es identificar candidatos que recibirán oferta de trabajo con base en señales previas de su proceso de búsqueda.

## 5. Interpretación detallada de las gráficas

### BASELINE (Árbol sin optimización)

#### Matriz de confusión baseline

![Matriz de confusión baseline](../imagenes/decision_tree_confusion_base.png)

**¿Qué significa?** Los números en diagonal azul son aciertos. En rojo están los errores. El baseline deja pasar 242 candidatos que SÍ recibieron oferta y marca 1,150 como falsos positivos.

**Lección para negocio:** El baseline ya funciona bien, pero todavía hay margen para mejorar la captura de ofertas reales si ese es el objetivo.

#### Curva ROC baseline

![Curva ROC baseline](../imagenes/decision_tree_roc_base.png)

**¿Qué significa?** Con `ROC-AUC = 0.9672`, el árbol tiene una capacidad de separación excelente desde el inicio. Es uno de los valores más altos posibles.

**Lección para negocio:** El árbol no tiene un problema fundamental de separación. El problema es la decisión de umbral, no la capacidad discriminativa.

#### Curva Precision-Recall baseline

![Curva Precision-Recall baseline](../imagenes/decision_tree_pr_base.png)

**¿Qué significa?** La curva muestra que el árbol mantiene buena precisión incluso a niveles altos de recall. El `Average Precision = 0.9140` indica excelente rendimiento en la clase positiva.

**Lección para negocio:** El árbol ya es competitivo cuando importa la clase positiva. Hay espacio para tuning fino.

#### Barrido de umbral baseline

![Barrido de umbral baseline](../imagenes/decision_tree_threshold_base.png)

**¿Qué significa?** Las líneas muestran que bajando el umbral de 0.50, el recall sube pero la precisión baja. Hay un punto donde F-beta 1.5 puede mejorarse.

**Lección para negocio:** Ajustar el umbral es prometedor, pero el baseline no tiene un punto claro de mejora radical.

---

### MODELO MEJORADO (Árbol optimizado, umbral=0.32)

#### Matriz de confusión mejorada

![Matriz de confusión mejorado](../imagenes/decision_tree_confusion_matrix.png)

**¿Qué significa?** Con umbral 0.32, el árbol captura **6,785 de 6,846** candidatos con oferta (**99.11% de captura**). Solo 61 casos se pierden. El costo: 1,589 falsos positivos.

**Lección para negocio:** Prácticamente perfecto para detectar ofertas. Solo ~1% de las ofertas reales se quedan sin identificar.

#### Curva ROC mejorada

![Curva ROC mejorado](../imagenes/decision_tree_roc_curve.png)

**¿Qué significa?** La curva ROC se mantiene en `0.9672`, idéntica al baseline. La mejora no vino de cambiar el árbol, sino de optimizar el umbral.

**Lección para negocio:** El árbol base ya era excelente. La mejora es puramente de calibración, no de estructura.

#### Curva Precision-Recall mejorada

![Curva Precision-Recall mejorado](../imagenes/decision_tree_precision_recall_curve.png)

**¿Qué significa?** La curva sigue siendo excelente. Con `Average Precision = 0.9140` (igual que baseline), mantiene balance fuerte entre precision y recall.

**Lección para negocio:** El árbol mejorado sigue siendo confiable incluso capturando el 99% de las ofertas.

#### Barrido de umbral mejorado

![Barrido de umbral mejorado](../imagenes/decision_tree_threshold_tradeoff.png)

**¿Qué significa?** El pico de F-beta 1.5 está claramente en umbral **0.32**. Es el punto donde F-beta alcanza su máximo valor de ~0.906.

**Lección para negocio:** El umbral 0.32 es defensible y reproducible. Está optimizado matemáticamente.

---

### INTERPRETACIÓN DE VARIABLES

#### Importancia de variables

![Importancia de variables mejorado](../imagenes/decision_tree_feature_importance.png)

**¿Qué significa?** Las variables más importantes son `Second_Round_Interviews`, `First_Round_Interviews` y `Applications_Submitted`. El árbol usa estas para tomar las primeras divisiones.

**Lección para negocio:** Las entrevistas (especialmente las de segunda ronda) son el factor más predictivo. Es como el árbol "entiende" que más entrevistas = más probable oferta.

#### Vista parcial del árbol

![Vista parcial del árbol mejorado](../imagenes/decision_tree_tree_preview.png)

**¿Qué significa?** Se ve la estructura inicial del árbol. Las primeras divisiones son sobre entrevistas. Si no hay segunda ronda, el árbol empuja fuertemente hacia "NO OFERTA".

**Lección para negocio:** El árbol es interpretable. Las primeras decisiones siguen lógica clara: si no avanzas en entrevistas, baja la probabilidad de oferta.

#### Comparación con reglas manuales

![Comparación con reglas manuales](../imagenes/decision_tree_rule_comparison.png)

**¿Qué significa?** Se compara cómo se comporta el árbol vs reglas simples extraídas de los splits. El árbol típicamente supera reglas manuales porque combina señales de forma más sofisticada.

**Lección para negocio:** El árbol no es una "caja negra". Sus decisiones pueden ser explicadas por reglas simples que los stakeholders pueden entender.

## 6. Resultados cuantitativos

| Métrica | Baseline | Mejorado | Cambio |
|---------|----------|----------|--------|
| Accuracy | 0.9015 | 0.8894 | -1.21% |
| Precision | 0.7928 | 0.7593 | -3.35% |
| Recall | 0.9644 | 0.9911 | +2.67% |
| F1-Score | 0.8702 | 0.8598 | -1.04% |
| F-beta (1.5) | 0.9042 | 0.9060 | +0.18% |
| ROC-AUC | 0.9672 | 0.9672 | 0% |

**Lectura ejecutiva:** La mejora busca capturar más ofertas reales. Sacrifica precisión global para lograr recall del 99%.

## 7. Código Python para usar los modelos

Para usar los modelos sin abrir el notebook:

```python
import pickle
from pathlib import Path
import pandas as pd

# ========== CARGAR MODELO MEJORADO (RECOMENDADO) ==========
MODEL_PATH = Path("decision_tree_offer_received_improved.pkl")

with open(MODEL_PATH, "rb") as f:
    artifact = pickle.load(f)

modelo = artifact["pipeline"]
umbral = artifact["best_threshold"]
feature_columns = artifact["feature_columns"]

print("=" * 60)
print("ÁRBOL DE DECISIÓN CARGADO EXITOSAMENTE")
print(f"Umbral de decisión: {umbral}")
print("=" * 60)

# ========== PREPARAR DATOS DE ENTRADA ==========
entradas = pd.DataFrame([{
    "GPA": 3.3,
    "University_Rating": "Top-tier",
    "Major_Category": "STEM",
    "Region": "West",
    "Prior_Internships": 1,
    "Extra_Curricular_Activities": 2,
    "Networking_Events_Attended": 4,
    "School_Size": "Large",
    "Primary_Search_Platform": "LinkedIn",
    "Months_Searching": 2,
    "Applications_Submitted": 12,
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
    print("El árbol predice que este candidato SÍ recibirá oferta.")
else:
    print("El árbol predice que este candidato NO recibirá oferta.")

print("=" * 60)
```

### Explicación del código

**1. Cargar modelo:** El `.pkl` contiene el árbol preprocesado.

**2. Preparar datos:** DataFrame con las 14 columnas en orden correcto.

**3. Generar predicción:** `predict_proba()` devuelve probabilidades para ambas clases.

**4. Aplicar umbral:** Si probabilidad ≥ 0.32 → "SI OFERTA"

### Usar el modelo baseline

```python
MODEL_PATH = Path("decision_tree_offer_received_base.pkl")
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

1. **Captura 99.11% de ofertas reales** (Recall = 0.9911)
2. **Mantiene ROC-AUC excelente** (0.9672)
3. **Precisión razonable** (0.7593)
4. **Interpretable:** Las decisiones del árbol pueden explicarse a stakeholders

### Configuración recomendada

- `max_depth = None`
- `min_samples_leaf = 5`
- `ccp_alpha = 0.0001`
- `threshold = 0.32`

### Ajuste del umbral según necesidad

- **Mayor conservadurismo:** Subir a 0.45-0.50 (menos ofertas detectadas, menos falsos positivos)
- **Mayor sensibilidad:** Bajar a 0.20-0.25 (más ofertas detectadas, más falsos positivos)

## 9. Cierre metodológico

El árbol de decisión demuestra ser una solución sólida para este problema:

- Excelente capacidad de separación (ROC-AUC 0.9672)
- Interpretabilidad clara (variables importantes son lógicas)
- Rendimiento en clase positiva muy fuerte
- Listo para uso operativo con artefactos `.pkl` portables

**Conclusión final:** El árbol mejorado captura virtualmente todas las ofertas reales. Es la solución recomendada para identificación de candidatos con oferta.
