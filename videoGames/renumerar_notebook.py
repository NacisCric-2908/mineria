#!/usr/bin/env python3
import json
import re

notebook_path = 'videoGames.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Mapeo de reemplazos
cambios = [
    ("## 0) Comprension del problema", "## 1. COMPRENSIÓN DEL PROBLEMA"),
    ("## 1) Objetivos y alcance", "## 1.1 Objetivos y Alcance del EDA"),
    ("## 2) Carga de datos", "## 2. COMPRENSIÓN DE LOS DATOS\n### 2.1 Carga de Datos y Vista Inicial"),
    ("## 3) Diccionario inicial", "## 2.2 Diccionario de Variables"),
    ("## 4) Tipificacion analitica", "## 2.3 Tipificación Analítica"),
    ("## 5) Calidad de datos", "## 2.4 Auditoría de Calidad"),
    ("## 6) Estandarizacion de formato", "## 3. LIMPIEZA Y PREPARACIÓN\n### 3.1 Estandarización de Formato"),
    ("## Estadistica cantidad de datos nulos", "## 3.2 Estadística de Nulos"),
    ("## 7) Consistencia interna", "## 3.3 Consistencia Interna de Ventas"),
    ("## Limpieza regiones nulas", "## 3.4 Limpieza de Registros Nulos"),
    ("## Análisis de Títulos Multiplatforma", "## 3.5 Análisis Multiplatforma"),
    ("## limpieza regiones nulas", "## 3.4 Eliminación de Nulos"),
    ("## Limpieza de Duplicados", "## 3.6 Eliminación de Duplicados"),
    ("## Limpieza de fechas", "## 3.7 Validación de Fechas"),
    ("## 8) Distribuciones numericas", "## 4. ANÁLISIS EXPLORATORIO (EDA)\n### 4.1 Distribuciones Numéricas"),
    ("## 9) Analisis temporal", "## 4.2 Análisis Temporal"),
    ("## 10) Variables cualitativas", "## 4.3 Variables Cualitativas"),
    ("## 11) Potencial analitico", "## 4.4 Potencial Analítico"),
    ("## 12) Diagnostico variable", "## 5. INTERPRETACIÓN Y SÍNTESIS\n### 5.1 Diagnóstico Variable"),
    ("## 13) Sintesis cuantitativa", "## 5.2 Síntesis Cuantitativa"),
    ("## 15) Normalizacion semantica", "## 5.3 Normalización Semántica"),
    ("## 16) Analisis adicional", "## 5.4 Análisis de Concentración"),
    ("## 17) Limpieza y preparacion", "## 5.5 Resumen de Limpieza"),
    ("## 18) Resumen ejecutivo", "## 5.6 Resumen Ejecutivo"),
    ("## 19) Verificacion final", "## 5.7 Verificación CRISP-DM"),
    ("## 20) Proximo objetivo", "## 5.8 Próximos Pasos"),
    ("## 21) INFORME EJECUTIVO", "## 5.9 INFORME EJECUTIVO FINAL"),
]

contador = 0
for cell in nb['cells']:
    if cell['cell_type'] == 'markdown':
        source = cell['source']
        if isinstance(source, list):
            content = ''.join(source)
        else:
            content = str(source)
        
        original = content
        
        for viejo, nuevo in cambios:
            if viejo in content:
                content = content.replace(viejo, nuevo, 1)  # Reemplazar solo la primera ocurrencia
                contador += 1
        
        # Actualizar si cambió
        if content != original:
            if isinstance(cell['source'], list):
                cell['source'] = content.split('\n') if '\n' in content else [content]
            else:
                cell['source'] = content

# Guardar
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2, ensure_ascii=False)

print(f"✅ Renumeración completada")
print(f"📝 Cambios realizados: {contador}")
print("\nNueva estructura:")
print("""
## 1. COMPRENSIÓN DEL PROBLEMA
  └─ 1.1 Objetivos y Alcance

## 2. COMPRENSIÓN DE LOS DATOS
  ├─ 2.1 Carga de Datos
  ├─ 2.2 Diccionario de Variables
  ├─ 2.3 Tipificación Analítica
  └─ 2.4 Auditoría de Calidad

## 3. LIMPIEZA Y PREPARACIÓN
  ├─ 3.1 Estandarización
  ├─ 3.2 Estadística de Nulos
  ├─ 3.3 Consistencia de Ventas
  ├─ 3.4 Limpieza de Nulos
  ├─ 3.5 Análisis Multiplatforma
  ├─ 3.6 Eliminación de Duplicados
  └─ 3.7 Validación de Fechas

## 4. ANÁLISIS EXPLORATORIO (EDA)
  ├─ 4.1 Distribuciones Numéricas
  ├─ 4.2 Análisis Temporal
  ├─ 4.3 Variables Cualitativas
  └─ 4.4 Potencial Analítico

## 5. INTERPRETACIÓN Y SÍNTESIS
  ├─ 5.1 Diagnóstico Variable
  ├─ 5.2 Síntesis Cuantitativa
  ├─ 5.3 Normalización Semántica
  ├─ 5.4 Análisis de Concentración
  ├─ 5.5 Resumen de Limpieza
  ├─ 5.6 Resumen Ejecutivo
  ├─ 5.7 Verificación CRISP-DM
  ├─ 5.8 Próximos Pasos
  └─ 5.9 INFORME EJECUTIVO FINAL
""")
