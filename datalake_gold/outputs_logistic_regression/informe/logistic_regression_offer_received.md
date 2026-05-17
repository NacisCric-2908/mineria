# Informe Final - LogisticRegression para Offer_Received

## Resumen ejecutivo

- Modelo: LogisticRegression
- Archivo del modelo: C:\Users\Salda\Desktop\Medallion\datalake_gold\outputs_logistic_regression\informe\logistic_regression_offer_received_improved.pkl
- Archivo del reporte: C:\Users\Salda\Desktop\Medallion\datalake_gold\outputs_logistic_regression\informe\logistic_regression_offer_received.md
- Umbral óptimo: 0.30

## Métricas principales

### Umbral 0.50
- Accuracy: 0.8101
- Precision: 0.7012
- Recall: 0.7756
- F1-Score: 0.7365
- F-beta (1.5): 0.7511
- ROC-AUC: 0.8940

### Umbral optimizado
- Accuracy: 0.7713
- Precision: 0.6054
- Recall: 0.9533
- F1-Score: 0.7405
- F-beta (1.5): 0.8100
- ROC-AUC: 0.8940

## Matriz de confusión

- TP: 6526
- FN: 320
- FP: 4254
- TN: 8900

## Variables más influyentes

          base_variable  importance
Second_Round_Interviews    2.325704
 First_Round_Interviews    0.579221
      Prior_Internships    0.452109
 Applications_Submitted    0.228509
      University_Rating    0.205463
                    GPA    0.196455
Primary_Search_Platform    0.130663
         Major_Category    0.127696
                 Region    0.049365
            School_Size    0.041539

## Conclusión

El modelo final prioriza la detección de la clase positiva `SI OFERTA` y queda guardado junto con sus gráficos y métricas en la carpeta de salida.
