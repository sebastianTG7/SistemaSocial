# ============================================================
# Script: 3_eda_estandarizacion_formatos.py
# Sección Informe: 4.3.4.3. Estandarización y Normalización de Formatos
# Descripción: Toma la tabla limpia de nulos ('atenciones_sin_nulos.xlsx')
#              y estandariza los formatos de texto, fechas, escuelas,
#              sexo, DNI y casos sociales según el catálogo oficial de la BD.
# ============================================================

import pandas as pd
import os
import re

# ------------------------------------------------------------
# 1. Cargar el dataset de atenciones del Paso 2
# ------------------------------------------------------------
carp_entrada = os.path.join(os.path.dirname(__file__), 'data_eda', 'data_limpieza_nulos')
ruta_atenciones = os.path.join(carp_entrada, 'atenciones_sin_nulos.xlsx')

df = pd.read_excel(ruta_atenciones)

print("=" * 70)
print("   4.3.4.3. ESTANDARIZACION Y NORMALIZACION DE FORMATOS")
print(f"   Total de registros a estandarizar: {len(df)}")
print("=" * 70)


# ------------------------------------------------------------
# 2. Estandarización de SEXO (Catálogo: M / F)
# ------------------------------------------------------------
def estandarizar_sexo(val):
    texto = str(val).strip().upper()
    if texto in ['M', 'MASCULINO', 'H', 'HOMBRE', 'MASC']:
        return 'M'
    elif texto in ['F', 'FEMENINO', 'M', 'MUJER', 'FEM']:
        return 'F'
    elif 'M' in texto:
        return 'M'
    elif 'F' in texto:
        return 'F'
    return 'M' # Por defecto en caso extremo

df['SEXO'] = df['SEXO'].apply(estandarizar_sexo)
print("\n[1/8] Columna SEXO estandarizada a 'M' / 'F'.")


# ------------------------------------------------------------
# 3. Estandarización de DNI y CELULAR (Solo números limpios)
# ------------------------------------------------------------
def limpiar_dni(val):
    # Quita espacios, guiones y caracteres no numéricos
    solo_numeros = re.sub(r'\D', '', str(val))
    return solo_numeros.zfill(8)[:8] # Asegura 8 dígitos

def limpiar_celular(val):
    txt = str(val).strip()
    if txt.endswith('.0'):
        txt = txt[:-2]
    solo_numeros = re.sub(r'\D', '', txt)
    if len(solo_numeros) >= 9:
        return solo_numeros[-9:] # Conserva los 9 dígitos finales
    return ''

def limpiar_codigo_estudiante(val):
    txt = str(val).strip()
    if txt.endswith('.0'):
        txt = txt[:-2]
    if txt in ['nan', 'None', 'NaN', '']:
        return ''
    return txt

df['DNI'] = df['DNI'].apply(limpiar_dni)
df['CELULAR'] = df['CELULAR'].apply(limpiar_celular)
df['COD. ESTUDIANTE'] = df['COD. ESTUDIANTE'].apply(limpiar_codigo_estudiante)
print("[2/8] DNI (8 dígitos), CELULAR (9 dígitos) y COD. ESTUDIANTE limpiados sin decimales.")


# ------------------------------------------------------------
# 4. Estandarización de NOMBRES y APELLIDOS (MAYÚSCULAS COMPLETAS)
# ------------------------------------------------------------
def corregir_nombres_apellidos(row):
    nombres = str(row['NOMBRES']).strip()
    apellidos = str(row['APELLIDOS']).strip()
    
    # Si los apellidos están dentro de la columna Nombres en formato "APELLIDO, NOMBRE"
    if ',' in nombres:
        partes = nombres.split(',')
        apellidos = partes[0].strip().upper()
        nombres = partes[1].strip().upper()
    else:
        nombres = nombres.upper()
        apellidos = apellidos.upper()
        
    return pd.Series([nombres, apellidos])

df[['NOMBRES', 'APELLIDOS']] = df.apply(corregir_nombres_apellidos, axis=1)
print("[3/8] NOMBRES y APELLIDOS estandarizados a MAYÚSCULAS COMPLETAS.")


# ------------------------------------------------------------
# 5. Estandarización de EDAD (Formato puramente numérico entero)
# ------------------------------------------------------------
def estandarizar_edad(val):
    # Busca el primer número encontrado en el texto (ej. "21 años" -> 21)
    match = re.search(r'\d+', str(val))
    if match:
        return int(match.group(0))
    return 20 # Valor estándar por defecto

df['EDAD'] = df['EDAD'].apply(estandarizar_edad)
print("[4/8] Columna EDAD estandarizada a números enteros.")


# ------------------------------------------------------------
# 6. Estandarización de ESCUELA y FACULTAD (Catálogo Oficial de BD)
# ------------------------------------------------------------
def estandarizar_escuela_y_facultad(row):
    txt = str(row['ESCUELA / CARRERA']).strip().lower()
    
    if 'enf' in txt:
        return pd.Series(['Enfermería', 'Enfermería'])
    elif 'obst' in txt:
        return pd.Series(['Obstetricia', 'Obstetricia'])
    elif 'ing' in txt and 'civ' in txt:
        return pd.Series(['Ingeniería Civil', 'Ingeniería Civil y Arquitectura'])
    elif 'arq' in txt:
        return pd.Series(['Arquitectura', 'Ingeniería Civil y Arquitectura'])
    elif 'ing' in txt and 'sist' in txt:
        return pd.Series(['Ingeniería de Sistemas', 'Ingeniería Industrial, de Sistemas y Mecatrónica'])
    elif 'ing' in txt and 'ind' in txt:
        return pd.Series(['Ingeniería Industrial', 'Ingeniería Industrial, de Sistemas y Mecatrónica'])
    elif 'med' in txt:
        return pd.Series(['Medicina Humana', 'Medicina'])
    elif 'odont' in txt:
        return pd.Series(['Odontología', 'Medicina'])
    elif 'cont' in txt:
        return pd.Series(['Ciencias Contables y Financieras', 'Ciencias Contables y Financieras'])
    elif 'admin' in txt:
        return pd.Series(['Administración', 'Ciencias Administrativas y Turismo'])
    elif 'turis' in txt:
        return pd.Series(['Turismo y Hotelería', 'Ciencias Administrativas y Turismo'])
    elif 'econ' in txt:
        return pd.Series(['Economía', 'Economía'])
    elif 'derech' in txt:
        return pd.Series(['Derecho y Ciencias Políticas', 'Derecho y Ciencias Políticas'])
    elif 'psico' in txt:
        return pd.Series(['Psicología', 'Psicología'])
    elif 'educ' in txt or 'pedag' in txt:
        return pd.Series(['Educación Primaria', 'Ciencias de la Educación'])
    elif 'agro' in txt:
        return pd.Series(['Ingeniería Agronómica', 'Ciencias Agrarias'])
    elif 'vet' in txt or 'zoot' in txt:
        return pd.Series(['Medicina Veterinaria', 'Medicina Veterinaria y Zootecnia'])
    elif 'comunic' in txt or 'social' in txt:
        return pd.Series(['Ciencias de la Comunicación Social', 'Ciencias Sociales'])
    else:
        return pd.Series([str(row['ESCUELA / CARRERA']).strip().title(), str(row['FACULTAD']).strip().title()])

df[['ESCUELA / CARRERA', 'FACULTAD']] = df.apply(estandarizar_escuela_y_facultad, axis=1)
print("[5/8] ESCUELA / CARRERA y FACULTAD estandarizadas según catálogo de BD.")


# ------------------------------------------------------------
# 7. Estandarización de MODALIDAD DE INGRESO (Catálogo Oficial de BD)
# ------------------------------------------------------------
def estandarizar_modalidad(val):
    txt = str(val).strip().lower()
    if 'discap' in txt:
        return 'Discapacidad'
    elif 'cepre' in txt:
        return 'CEPREVAL'
    elif 'violenc' in txt:
        return 'Violencia Politica'
    elif 'campesino' in txt or 'hijo' in txt:
        return 'Hijos de Campesinos'
    elif 'puesto' in txt:
        return 'Primeros Puestos'
    elif 'deport' in txt:
        return 'Deportista Calificado'
    else:
        return 'General'

df['MODALIDAD INGRESO'] = df['MODALIDAD INGRESO'].apply(estandarizar_modalidad)
print("[6/8] MODALIDAD INGRESO estandarizada a catálogo oficial (ej. 'General', 'Discapacidad').")


# ------------------------------------------------------------
# 7. Estandarización de CASO SOCIAL (Catálogo Oficial)
# ------------------------------------------------------------
def estandarizar_caso_social(val):
    txt = str(val).strip().lower()
    
    if 'evalua' in txt and 'segui' in txt:
        return 'Evaluación y Seguimiento'
    elif 'evalua' in txt:
        return 'Evaluación'
    elif 'segui' in txt:
        return 'Seguimiento'
    elif 'orient' in txt:
        return 'Orientación'
    else:
        return 'Orientación'

df['CASO SOCIAL'] = df['CASO SOCIAL'].apply(estandarizar_caso_social)
print("[6/8] CASO SOCIAL estandarizado a categorías oficiales.")


# ------------------------------------------------------------
# 8. Estandarización de FECHA ATENCION (Formato YYYY-MM-DD)
# ------------------------------------------------------------
meses_num = {
    'enero':'01', 'febrero':'02', 'marzo':'03', 'abril':'04',
    'mayo':'05', 'junio':'06', 'julio':'07', 'agosto':'08',
    'septiembre':'09', 'octubre':'10', 'noviembre':'11', 'diciembre':'12'
}

def estandarizar_fecha(val):
    txt = str(val).strip().lower()
    
    # Formato DD/MM/YYYY o DD/MM
    if '/' in txt:
        partes = txt.split('/')
        if len(partes) >= 2:
            dia = partes[0].zfill(2)
            mes = partes[1].zfill(2)
            anio = partes[2] if len(partes) == 3 else '2026'
            return f"{anio}-{mes}-{dia}"
            
    # Formato "31 de marzo" o "31 de marzo del 2026"
    for nombre_mes, num_mes in meses_num.items():
        if nombre_mes in txt:
            match_dia = re.search(r'\d+', txt)
            dia = match_dia.group(0).zfill(2) if match_dia else '01'
            return f"2026-{num_mes}-{dia}"
            
    return '2026-03-31' # Por defecto

df['FECHA ATENCION'] = df['FECHA ATENCION'].apply(estandarizar_fecha)
print("[7/8] FECHA ATENCION estandarizada a formato uniforme YYYY-MM-DD.")


# ------------------------------------------------------------
# 9. Guardar archivo en 'scripts/data_eda/data_estandarizada/'
# ------------------------------------------------------------
carp_salida = os.path.join(os.path.dirname(__file__), 'data_eda', 'data_estandarizada')
os.makedirs(carp_salida, exist_ok=True)

ruta_guardar = os.path.join(carp_salida, 'atenciones_estandarizadas.xlsx')

try:
    df.to_excel(ruta_guardar, index=False)
    print("\n" + "=" * 70)
    print("   ARCHIVO ESTANDARIZADO GUARDADO EXITOSAMENTE:")
    print(f"   - {ruta_guardar} ({len(df)} registros)")
    print("=" * 70)
    print("¡Paso 4.3.4.3 finalizado exitosamente!")
except PermissionError:
    print("\n[ERROR] Cierra el archivo 'atenciones_estandarizadas.xlsx' si está abierto e intenta de nuevo.")
