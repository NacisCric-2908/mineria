# Informe Final - LogisticRegression para Offer_Received

## Resumen ejecutivo

- Modelo: LogisticRegression
- Archivo del modelo: /Users/apple/Documents/Medallion/datalake_gold/PCA/outputs_logistic_regression/informe/logistic_regression_offer_received_improved.pkl
- Archivo del reporte: /Users/apple/Documents/Medallion/datalake_gold/PCA/outputs_logistic_regression/informe/logistic_regression_offer_received.md
- Umbral óptimo: 0.31

## Métricas principales

### Umbral 0.50
- Accuracy: 0.8090
- Precision: 0.6997
- Recall: 0.7745
- F1-Score: 0.7352
- F-beta (1.5): 0.7498
- ROC-AUC: 0.8938

### Umbral optimizado
- Accuracy: 0.7751
- Precision: 0.6107
- Recall: 0.9457
- F1-Score: 0.7421
- F-beta (1.5): 0.8091
- ROC-AUC: 0.8938

## Matriz de confusión

- TP: 6474
- FN: 372
- FP: 4127
- TN: 9027

## Variables más influyentes

base_variable  importance
         PC11    1.609518
          PC2    1.333510
         PC12    0.767285
          PC1    0.668670
          PC7    0.574627
          PC6    0.445793
         PC10    0.303493
          PC4    0.054462
          PC9    0.042725
         PC13    0.020900

## Conclusión

El modelo final prioriza la detección de la clase positiva `SI OFERTA` y queda guardado junto con sus gráficos y métricas en la carpeta de salida.
