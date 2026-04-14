# Mineria de Datos - Proyecto Job Search (enfoque exclusivo en job/)

Este repositorio contiene varios recursos, pero este README documenta **solo** el trabajo de la carpeta [job](job).

## Objetivo del proyecto

Analizar la eficacia de plataformas de busqueda laboral estudiantil con un dataset de 100,000 registros, cubriendo:

- Comprension del problema de negocio y analitico.
- Calidad, limpieza y preparacion de datos.
- Analisis exploratorio (EDA) con visualizaciones.
- Interpretacion de hallazgos y definicion de siguiente iteracion de modelado.

## Alcance de este README

- Incluye unicamente el flujo y artefactos de [job](job).
- No documenta la carpeta homicidios.

## Estructura principal

- [job/guia.txt](job/guia.txt): guia de trabajo y preguntas orientadoras.
- [job/job_search_platform_efficacy_100k.csv](job/job_search_platform_efficacy_100k.csv): dataset base (100,000 filas).
- [job/primerCorte.ipynb](job/primerCorte.ipynb): notebook principal del primer corte.
- [job/requirements.txt](job/requirements.txt): dependencias Python.
- [job/outputs_primer_corte](job/outputs_primer_corte): salidas tabulares, bitacoras y graficos.

## Tecnologias

Dependencias declaradas en [job/requirements.txt](job/requirements.txt):

- ipykernel 7.2.0
- numpy 2.4.4
- pandas 3.0.2
- matplotlib 3.10.8
- seaborn 0.13.2
- scikit-learn 1.8.0
- scipy 1.17.1

## Como ejecutar el analisis

1. Crear y activar un entorno virtual en la raiz del repositorio.
2. Instalar dependencias desde [job/requirements.txt](job/requirements.txt).
3. Abrir [job/primerCorte.ipynb](job/primerCorte.ipynb).
4. Ejecutar todas las celdas en orden para regenerar resultados en [job/outputs_primer_corte](job/outputs_primer_corte).

Comandos de referencia:

python3 -m venv .venv
source .venv/bin/activate
pip install -r job/requirements.txt
jupyter notebook job/primerCorte.ipynb

## Resumen del primer corte

De acuerdo con [job/outputs_primer_corte/reporte_limpieza_detallado.txt](job/outputs_primer_corte/reporte_limpieza_detallado.txt):

- Filas originales: 100,000
- Filas finales: 100,000 (retencion 100%)
- Columnas originales: 20
- Columnas finales: 40 (20 features nuevas)

Hallazgos ejecutivos destacados (fuente: [job/outputs_primer_corte/conclusiones_ejecutivas_primer_corte.csv](job/outputs_primer_corte/conclusiones_ejecutivas_primer_corte.csv)):

- Tasa global de oferta: 34.23%
- Handshake e LinkedIn muestran mayor tasa de oferta que Indeed
- El avance a segunda ronda se asocia fuertemente con recibir oferta

## Artefactos generados en outputs_primer_corte

### Tablas y trazabilidad

- [job/outputs_primer_corte/metadata_limpieza.csv](job/outputs_primer_corte/metadata_limpieza.csv)
- [job/outputs_primer_corte/decisiones_limpieza.csv](job/outputs_primer_corte/decisiones_limpieza.csv)
- [job/outputs_primer_corte/bitacora_calidad.csv](job/outputs_primer_corte/bitacora_calidad.csv)
- [job/outputs_primer_corte/resumen_faltantes.csv](job/outputs_primer_corte/resumen_faltantes.csv)
- [job/outputs_primer_corte/outliers_iqr_resumen.csv](job/outputs_primer_corte/outliers_iqr_resumen.csv)
- [job/outputs_primer_corte/reporte_limpieza_detallado.txt](job/outputs_primer_corte/reporte_limpieza_detallado.txt)

### Datasets procesados

- [job/outputs_primer_corte/dataset_limpio_primer_corte.csv](job/outputs_primer_corte/dataset_limpio_primer_corte.csv)
- [job/outputs_primer_corte/dataset_limpio_completo.csv](job/outputs_primer_corte/dataset_limpio_completo.csv)

### Analisis e interpretacion

- [job/outputs_primer_corte/tasa_oferta_por_plataforma.csv](job/outputs_primer_corte/tasa_oferta_por_plataforma.csv)
- [job/outputs_primer_corte/top_correlaciones_offer_received.csv](job/outputs_primer_corte/top_correlaciones_offer_received.csv)
- [job/outputs_primer_corte/conclusiones_ejecutivas_primer_corte.csv](job/outputs_primer_corte/conclusiones_ejecutivas_primer_corte.csv)
- [job/outputs_primer_corte/interpretaciones_graficos_detalladas.csv](job/outputs_primer_corte/interpretaciones_graficos_detalladas.csv)
- [job/outputs_primer_corte/plan_modelado_dos_objetivos.csv](job/outputs_primer_corte/plan_modelado_dos_objetivos.csv)
- [job/outputs_primer_corte/riesgos_modelado_y_mitigaciones.csv](job/outputs_primer_corte/riesgos_modelado_y_mitigaciones.csv)

### Visualizaciones

En [job/outputs_primer_corte](job/outputs_primer_corte) se incluyen visualizaciones de:

- Distribuciones (histogramas)
- Outliers (boxplots, violin, strip)
- Relaciones bivariadas (scatter, pairplot, lineas/areas/barras)
- Correlaciones (heatmap)
- Calidad y estructura del dataset

## Siguiente iteracion recomendada

Tomar como base [job/outputs_primer_corte/plan_modelado_dos_objetivos.csv](job/outputs_primer_corte/plan_modelado_dos_objetivos.csv) para desarrollar dos frentes:

- Clasificacion: probabilidad de Offer_Received.
- Regresion: estimacion de Offer_Salary (condicionada a tener oferta).