# Informe técnico — Naive Bayes para Offer_Received

## 1. Alcance del modelado

El experimento se ejecutó sobre 100000 registros con 13 variables predictoras y objetivo binario Offer_Received.
El split estratificado asignó 80000 registros a entrenamiento y 20000 registros a prueba.
La tasa positiva global se ubicó en 34.229%.

## 2. Versión baseline (umbral 0.50)

- Accuracy: 0.801450
- Precision: 0.727849
- Recall: 0.670757
- F1-Score: 0.698138
- F-beta (1.5): 0.687346
- ROC-AUC: 0.880330
- Average Precision: 0.752220
- TN: 11437
- FP: 1717
- FN: 2254
- TP: 4592

## 3. Versión improved (umbral óptimo)

La búsqueda de hiperparámetros seleccionó var_smoothing=1e-06.
El barrido de umbrales determinó best_threshold=0.22.

- Accuracy: 0.774300
- Precision: 0.612722
- Recall: 0.925796
- F1-Score: 0.737405
- F-beta (1.5): 0.800019
- ROC-AUC: 0.880331
- Average Precision: 0.752220
- TN: 9148
- FP: 4006
- FN: 508
- TP: 6338

## 4. Lectura comparativa

- Delta Recall: 0.255039
- Delta F-beta (1.5): 0.112673
- Delta Precision: -0.115127
- Reducción de falsos negativos: 1746

La versión improved priorizó recuperación de positivos y elevó F-beta (1.5), criterio central del objetivo operativo.