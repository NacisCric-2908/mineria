# Mineria de Datos - Proyecto Job Search

Este README documenta unicamente el trabajo contenido en la carpeta [job](job).

## Objetivo del proyecto

Analizar la eficacia de la busqueda laboral estudiantil con un dataset de 100,000 registros, cubriendo:

- entendimiento del problema de negocio y analitico,
- limpieza y calidad de datos,
- analisis exploratorio (EDA),
- definicion de la siguiente iteracion de modelado predictivo.

## Alcance

- Solo incluye artefactos de [job](job).
- No incluye otras carpetas del repositorio.

## Estructura principal de job

- [job/job_search_platform_efficacy_100k.csv](job/job_search_platform_efficacy_100k.csv): dataset base.
- [job/primerCorte.ipynb](job/primerCorte.ipynb): notebook principal del primer corte.
- [job/logistic_regression_offer_received.ipynb](job/logistic_regression_offer_received.ipynb): notebook de modelado de clasificacion.
- [job/CONTEXTO.md](job/CONTEXTO.md): contexto operativo integral del proyecto.
- [job/resumen.md](job/resumen.md): resumen narrativo de hallazgos.
- [job/PLAN_MODELADO_SECOND_ITERATION.md](job/PLAN_MODELADO_SECOND_ITERATION.md): plan de segundo corte.
- [job/Trabajo_Primer_Corte-GRUPO4.pdf](job/Trabajo_Primer_Corte-GRUPO4.pdf): documento del primer corte.
- [job/requirements.txt](job/requirements.txt): dependencias Python.
- [job/outputs_primer_corte](job/outputs_primer_corte): carpeta de salidas.

## Requisitos

Dependencias en [job/requirements.txt](job/requirements.txt).

## Ejecucion rapida

Desde la raiz del repositorio:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r job/requirements.txt
jupyter notebook job/primerCorte.ipynb
```

## Resultados del primer corte

Fuente principal: [job/outputs_primer_corte/csv/reporte_limpieza_detallado.txt](job/outputs_primer_corte/csv/reporte_limpieza_detallado.txt)

- filas originales: 100,000
- filas finales: 100,000 (retencion 100%)
- columnas originales: 20
- columnas finales: 40 (20 features derivadas)

Hallazgos ejecutivos (fuente: [job/outputs_primer_corte/csv/conclusiones_ejecutivas_primer_corte.csv](job/outputs_primer_corte/csv/conclusiones_ejecutivas_primer_corte.csv)):

- tasa global de oferta: 34.23%
- Handshake y LinkedIn superan a Indeed en tasa de oferta
- avanzar a segunda ronda tiene asociacion fuerte con recibir oferta

## Outputs disponibles

### CSV (trazabilidad, datasets y analisis)

Todos en [job/outputs_primer_corte/csv](job/outputs_primer_corte/csv):

- `metadata_limpieza.csv`
- `decisiones_limpieza.csv`
- `bitacora_calidad.csv`
- `resumen_faltantes.csv`
- `outliers_iqr_resumen.csv`
- `reporte_limpieza_detallado.txt`
- `dataset_limpio_primer_corte.csv`
- `dataset_limpio_completo.csv`
- `dataset_offer_Received.csv`
- `dataset_offer_Salary.csv`
- `tasa_oferta_por_plataforma.csv`
- `top_correlaciones_offer_received.csv`
- `conclusiones_ejecutivas_primer_corte.csv`
- `interpretaciones_graficos_detalladas.csv`
- `plan_modelado_dos_objetivos.csv`
- `riesgos_modelado_y_mitigaciones.csv`
- `hipotesis_siguiente_iteracion.csv`
- `respuestas_guia_26_preguntas.csv`
- `respuestas_guia_iniciales.csv`
- `01_factores_comparativa.csv`
- `02_recomendaciones_operativas.csv`

### Imagenes del EDA

Todas en [job/outputs_primer_corte/imagenes_png](job/outputs_primer_corte/imagenes_png):

- `04_exploracion_dataset_dimensions.png`
- `04_tipos_variables.png`
- `04_valores_faltantes.png`
- `04_tamaño_escala_dataset.png`
- `04_relevancia_calidad_4preguntas.png`
- `histogramas_base.png`
- `boxplots_base.png`
- `scatterplots_base.png`
- `correlation_matrix.png`
- `visualizacion_limpieza_resumen.png`
- `05_bivariado_scatter_plots.png`
- `06_bivariado_heatmap_correlacion.png`
- `07_bivariado_pairplot.png`
- `08_bivariado_boxplot_violin_strip.png`
- `09_bivariado_lineas_areas_barras.png`

## Segundo corte: modelado predictivo

El plan detallado se encuentra en [job/PLAN_MODELADO_SECOND_ITERATION.md](job/PLAN_MODELADO_SECOND_ITERATION.md).

Define:

- 7 fases secuenciales de modelado,
- 2 objetivos (clasificacion de `Offer_Received` y regresion de `Offer_Salary`),
- criterios de exito tecnico, equidad y reproducibilidad,
- riesgos y mitigaciones,
- timeline estimado.

## Nota de mantenimiento

Si se agregan nuevos artefactos en [job/outputs_primer_corte/csv](job/outputs_primer_corte/csv) o [job/outputs_primer_corte/imagenes_png](job/outputs_primer_corte/imagenes_png), actualizar este README para mantener trazabilidad completa.