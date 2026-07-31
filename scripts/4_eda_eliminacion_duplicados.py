# ============================================================
# Script: 4_eda_eliminacion_duplicados.py
# Sección Informe: 4.3.4.4. Tratamiento de Registros Duplicados (Unicidad por Mes)
# Descripción: Lee la tabla estandarizada ('atenciones_estandarizadas.xlsx')
#              e identifica duplicados de DNI DENTRO DEL MISMO MES.
#              Un estudiante puede tener atenciones en meses distintos,
#              pero no registros repetidos en el mismo mes.
# ============================================================

import pandas as pd
import os

# ------------------------------------------------------------
# 1. Cargar el dataset estandarizado del Paso 3
# ------------------------------------------------------------
carp_entrada = os.path.join(os.path.dirname(__file__), 'data_eda', 'data_estandarizada')
ruta_atenciones = os.path.join(carp_entrada, 'atenciones_estandarizadas.xlsx')

df = pd.read_excel(ruta_atenciones)

total_inicial = len(df)

print("=" * 70)
print("   4.3.4.4. UNICIDAD: ELIMINACION DE DUPLICADOS EN EL MISMO MES")
print(f"   Total de registros a evaluar: {total_inicial}")
print("=" * 70)


# ------------------------------------------------------------
# 2. Extraer el Mes de la Fecha de Atención (YYYY-MM)
# ------------------------------------------------------------
# Como las fechas están en YYYY-MM-DD, extraemos los primeros 7 caracteres (ej. '2026-03')
df['MES_ATENCION'] = df['FECHA ATENCION'].astype(str).str.slice(0, 7)


# ------------------------------------------------------------
# 3. Identificar duplicados basados en (DNI + MES_ATENCION)
# ------------------------------------------------------------
# Se busca si un mismo DNI se repite dentro del mismo MES de atención
filtro_duplicados = df.duplicated(subset=['DNI', 'MES_ATENCION'], keep='first')

# Separamos los registros
registros_unicos = df[~filtro_duplicados].drop(columns=['MES_ATENCION']).copy()
registros_duplicados = df[filtro_duplicados].drop(columns=['MES_ATENCION']).copy()

total_unicos = len(registros_unicos)
total_duplicados = len(registros_duplicados)
porcentaje_unicidad = round((total_unicos / total_inicial) * 100, 2)

print("\nResultados del análisis de Unicidad Mensual:")
print(f"  - Total atenciones registradas:     {total_inicial}")
print(f"  - Atenciones válidas (únicas/mes):   {total_unicos} ({porcentaje_unicidad}%)")
print(f"  - Duplicados en el mismo mes:        {total_duplicados} ({round(100 - porcentaje_unicidad, 2)}%)")


# ------------------------------------------------------------
# 4. Guardar archivos en 'scripts/data_eda/data_unicidad/'
# ------------------------------------------------------------
carp_salida = os.path.join(os.path.dirname(__file__), 'data_eda', 'data_unicidad')
os.makedirs(carp_salida, exist_ok=True)

ruta_unicos = os.path.join(carp_salida, 'atenciones_unicas.xlsx')
ruta_duplicados = os.path.join(carp_salida, 'registros_duplicados_eliminados.xlsx')

try:
    registros_unicos.to_excel(ruta_unicos, index=False)
    registros_duplicados.to_excel(ruta_duplicados, index=False)
    
    print("\n" + "=" * 70)
    print("   ARCHIVOS GUARDADOS EN 'scripts/data_eda/data_unicidad/':")
    print(f"   1. Atenciones Válidas (Únicas por mes): {ruta_unicos} ({total_unicos} registros)")
    print(f"   2. Duplicados Eliminados del mismo mes: {ruta_duplicados} ({total_duplicados} registros)")
    print("=" * 70)
    print("¡Paso 4.3.4.4 finalizado exitosamente!")
except PermissionError:
    print("\n[ERROR] Cierra los archivos Excel abiertos en Windows e intenta de nuevo.")
