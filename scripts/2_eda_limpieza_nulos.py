# ============================================================
# Script: 2_eda_limpieza_nulos.py
# Sección Informe: 4.3.4.2. Tratamiento y Limpieza de Valores Nulos
# Descripción: Imputación inteligente de valores nulos basada en reglas
#              de negocio (Código de estudiante, Año, Edad, Facultad).
# ============================================================

import pandas as pd
import os
import re

# ------------------------------------------------------------
# 1. Cargar la tabla de atenciones separada del Paso 1
# ------------------------------------------------------------
carp_entrada = os.path.join(os.path.dirname(__file__), 'data_eda', 'data_separada')
ruta_atenciones = os.path.join(carp_entrada, 'atenciones_raw.xlsx')

atenciones = pd.read_excel(ruta_atenciones)

print("=" * 70)
print("   4.3.4.2. TRATAMIENTO Y LIMPIEZA INTELIGENTE DE NULOS")
print(f"   Total de registros iniciales: {len(atenciones)}")
print("=" * 70)


# ------------------------------------------------------------
# 2. Descartar registros SIN ESCUELA / CARRERA (Dato vital)
# ------------------------------------------------------------
# Separamos los registros sin escuela a un archivo aparte para no ensuciar los reportes
filtro_sin_escuela = atenciones['ESCUELA / CARRERA'].isna() | (atenciones['ESCUELA / CARRERA'].astype(str).str.strip() == '')

descartados_sin_escuela = atenciones[filtro_sin_escuela].copy()
atenciones_limpias = atenciones[~filtro_sin_escuela].copy()

print(f"\n[1/7] Filtrado de registros sin Escuela:")
print(f"  - Registros conservados (con Escuela): {len(atenciones_limpias)}")
print(f"  - Registros descartados (sin Escuela): {len(descartados_sin_escuela)}")


# ------------------------------------------------------------
# 3. Imputación inteligente de COD. ESTUDIANTE, AÑO y TIPO
# ------------------------------------------------------------
# Regla: Extraer el año de ingreso a partir del código de estudiante (ej. 20261001 -> 2026)

def deducir_año_y_tipo(row):
    codigo = str(row['COD. ESTUDIANTE']).strip()
    
    # Si el código tiene al menos 4 dígitos iniciales (ej. 2025...)
    match = re.search(r'^(20\d{2})', codigo)
    
    if match:
        anio_ingreso = int(match.group(1))
        
        # Lógica de años académicos
        if anio_ingreso == 2026: return 1, 'Estudiante', 18
        elif anio_ingreso == 2025: return 2, 'Estudiante', 19
        elif anio_ingreso == 2024: return 3, 'Estudiante', 20
        elif anio_ingreso == 2023: return 4, 'Estudiante', 21
        elif anio_ingreso == 2022: return 5, 'Estudiante', 22
        elif anio_ingreso == 2021: return 6, 'Estudiante', 23
        else: return 'Egresado', 'Egresado', 24
    else:
        # Si no se puede deducir del código
        return 'No especificado', 'Estudiante', 20

# Aplicamos la función para calcular valores faltantes
años_calculados = []
tipos_calculados = []
edades_calculadas = []

for idx, fila in atenciones_limpias.iterrows():
    anio_deducido, tipo_deducido, edad_deducida = deducir_año_y_tipo(fila)
    
    # Si 'AÑO' está vacío, usamos el deducido
    if pd.isna(fila['AÑO']) or str(fila['AÑO']).strip() == '':
        años_calculados.append(anio_deducido)
    else:
        años_calculados.append(fila['AÑO'])
        
    # Si 'TIPO' está vacío, usamos el deducido
    if pd.isna(fila['TIPO']) or str(fila['TIPO']).strip() == '':
        tipos_calculados.append(tipo_deducido)
    else:
        tipos_calculados.append(fila['TIPO'])
        
    # Si 'EDAD' está vacía, usamos la edad deducida por código
    if pd.isna(fila['EDAD']) or str(fila['EDAD']).strip() == '':
        edades_calculadas.append(edad_deducida)
    else:
        edades_calculadas.append(fila['EDAD'])

atenciones_limpias['AÑO'] = años_calculados
atenciones_limpias['TIPO'] = tipos_calculados
atenciones_limpias['EDAD'] = edades_calculadas

# Rellenar COD. ESTUDIANTE si está vacío con DNI y limpiar decimales (.0)
codigos_limpios = []
for idx, fila in atenciones_limpias.iterrows():
    val = fila['COD. ESTUDIANTE']
    if pd.isna(val) or str(val).strip() == '':
        val = fila['DNI']
    txt = str(val).strip()
    if txt.endswith('.0'):
        txt = txt[:-2]
    codigos_limpios.append(txt)

atenciones_limpias['COD. ESTUDIANTE'] = codigos_limpios

print("[2/7] Imputacion de AÑO, TIPO, EDAD y COD. ESTUDIANTE completada.")


# ------------------------------------------------------------
# 4. Imputación inteligente de SEXO basada en Nombres
# ------------------------------------------------------------
def inferir_sexo(row):
    sexo_actual = str(row['SEXO']).strip().upper()
    if sexo_actual in ['M', 'MASCULINO', 'H', 'HOMBRE', 'F', 'FEMENINO', 'MUJER']:
        return row['SEXO'] # Conservar si ya existe
    
    # Si está vacío, inferimos por el primer nombre
    nombres = str(row['NOMBRES']).strip().upper().split()
    primer_nombre = nombres[0] if nombres else ''
    
    # Nombres femeninos comunes o terminados en A
    if primer_nombre.endswith('A') or primer_nombre in ['MARIA', 'LUZ', 'CARMEN', 'RUTH', 'FLOR']:
        return 'F'
    else:
        return 'M'

atenciones_limpias['SEXO'] = atenciones_limpias.apply(inferir_sexo, axis=1)
print("[3/7] Imputacion de SEXO basada en nombres completada.")


# ------------------------------------------------------------
# 5. Detección automática de FACULTAD según la Escuela
# ------------------------------------------------------------
def deducir_facultad(row):
    facultad_actual = row['FACULTAD']
    if pd.notna(facultad_actual) and str(facultad_actual).strip() != '':
        return facultad_actual
    
    escuela = str(row['ESCUELA / CARRERA']).lower()
    
    if 'enf' in escuela: return 'Enfermería'
    elif 'obst' in escuela: return 'Obstetricia'
    elif 'med' in escuela or 'odont' in escuela: return 'Medicina'
    elif 'ing' in escuela or 'arq' in escuela or 'sist' in escuela or 'civ' in escuela: return 'Ingeniería Civil y Arquitectura'
    elif 'cont' in escuela: return 'Ciencias Contables y Financieras'
    elif 'admin' in escuela: return 'Ciencias Administrativas y Turismo'
    elif 'derech' in escuela: return 'Derecho y Ciencias Políticas'
    elif 'educ' in escuela or 'pedag' in escuela: return 'Ciencias de la Educación'
    elif 'agro' in escuela or 'zoot' in escuela: return 'Ciencias Agrarias'
    else: return 'Ciencias Sociales'

atenciones_limpias['FACULTAD'] = atenciones_limpias.apply(deducir_facultad, axis=1)
print("[4/7] Asignacion automatica de FACULTAD segun Escuela completada.")


# ------------------------------------------------------------
# 6. Rellenar Modalidad de Ingreso, Caso Social y Opcionales
# ------------------------------------------------------------
# Modalidad de Ingreso: si está vacío -> "General" (Title Case acorde a BD)
atenciones_limpias['MODALIDAD INGRESO'] = atenciones_limpias['MODALIDAD INGRESO'].fillna('General')

# Caso Social: si está vacío -> "Orientación"
atenciones_limpias['CASO SOCIAL'] = atenciones_limpias['CASO SOCIAL'].fillna('Orientación')

# Campos opcionales de contacto (dejar vacíos para almacenamiento limpio en BD)
atenciones_limpias['CORREO'] = atenciones_limpias['CORREO'].fillna('')
atenciones_limpias['CELULAR'] = atenciones_limpias['CELULAR'].fillna('')
atenciones_limpias['DIRECCION'] = atenciones_limpias['DIRECCION'].fillna('')
atenciones_limpias['OBSERVACIONES'] = atenciones_limpias['OBSERVACIONES'].fillna('')
atenciones_limpias['APELLIDOS'] = atenciones_limpias['APELLIDOS'].fillna('')

print("[5/7] Relleno de Modalidad de Ingreso, Caso Social y datos opcionales completado.")


# ------------------------------------------------------------
# 7. Guardar archivos en 'scripts/data_eda/data_limpieza_nulos/'
# ------------------------------------------------------------
carp_salida = os.path.join(os.path.dirname(__file__), 'data_eda', 'data_limpieza_nulos')
os.makedirs(carp_salida, exist_ok=True)

ruta_guardar = os.path.join(carp_salida, 'atenciones_sin_nulos.xlsx')
ruta_descartados = os.path.join(carp_salida, 'registros_descartados_sin_escuela.xlsx')

try:
    atenciones_limpias.to_excel(ruta_guardar, index=False)
    descartados_sin_escuela.to_excel(ruta_descartados, index=False)
    
    print("\n" + "=" * 70)
    print("   ARCHIVOS GUARDADOS EN 'scripts/data_eda/data_limpieza_nulos/':")
    print(f"   1. Atenciones Limpias: {ruta_guardar} ({len(atenciones_limpias)} filas)")
    print(f"   2. Registros Descartados: {ruta_descartados} ({len(descartados_sin_escuela)} filas)")
    print("=" * 70)
    print("¡Paso 4.3.4.2 finalizado exitosamente!")
except PermissionError:
    print("\n[ERROR] Cierra los archivos Excel abietos en Windows e intenta de nuevo.")
