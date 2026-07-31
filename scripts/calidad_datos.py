# ============================================================
# Script: calidad_datos.py
# Descripción: Evalúa la calidad de los datos del archivo
#              "datos_originales_plano.xlsx" en 5 dimensiones:
#              1. Completitud
#              2. Consistencia
#              3. Validez
#              4. Unicidad
#              5. Puntualidad
#
# Cada dimensión se calcula con porcentajes simples.
# ============================================================

import pandas as pd
import re
import os

# ============================================================
# PASO 0: Cargar el archivo Excel
# ============================================================

# Construimos la ruta al archivo Excel que está en la carpeta padre
ruta_excel = os.path.join(os.path.dirname(__file__), '..', 'datos_originales_plano.xlsx')

# Leemos el Excel y lo guardamos en un DataFrame (tabla)
df = pd.read_excel(ruta_excel)

# Contamos cuántas filas y columnas tiene nuestro dataset
total_filas = len(df)          # Número total de registros (filas)
total_columnas = len(df.columns)  # Número total de columnas

print("=" * 65)
print("   EVALUACION DE CALIDAD DE DATOS")
print("   Archivo: datos_originales_plano.xlsx")
print(f"   Registros: {total_filas} | Columnas: {total_columnas}")
print("=" * 65)


# ============================================================
# DIMENSION 1: COMPLETITUD (Completeness)
# ============================================================
# Pregunta: ¿Qué porcentaje de celdas tienen valor (no están vacías)?
# Fórmula: (celdas con valor / total de celdas) * 100

print("\n" + "-" * 65)
print("  1. COMPLETITUD")
print("-" * 65)

# Calculamos el total de celdas en todo el dataset
total_celdas = total_filas * total_columnas

# Contamos cuántas celdas NO están vacías (tienen valor)
#.sum() esta sumando las columnas que tienen valor, y el segundo .sum() esta sumando los resultados de las columnas
celdas_con_valor = df.notna().sum().sum()  # .notna() = True si tiene valor

# Contamos cuántas celdas ESTÁN vacías
celdas_vacias = total_celdas - celdas_con_valor

# Calculamos el porcentaje de completitud general
porcentaje_completitud = round((celdas_con_valor / total_celdas) * 100, 2)

print(f"\n  Total de celdas en el dataset: {total_celdas}")
print(f"  Celdas con valor:             {celdas_con_valor}")
print(f"  Celdas vacias:                {celdas_vacias}")
print(f"  Completitud general:          {porcentaje_completitud}%")

# Ahora calculamos la completitud por cada columna
print(f"\n  Completitud por columna:")
print(f"  {'COLUMNA':<25} {'CON VALOR':>10} {'VACIOS':>10} {'% COMPLETO':>12}")
print(f"  {'-'*25} {'-'*10} {'-'*10} {'-'*12}")

# Recorremos cada columna y calculamos su completitud
resultados_completitud = []

for columna in df.columns:
    # Contamos valores no nulos en esta columna
    con_valor = df[columna].notna().sum()
    
    # Contamos valores nulos (vacíos)
    vacios = total_filas - con_valor
    
    # Calculamos el porcentaje
    porcentaje = round((con_valor / total_filas) * 100, 2)
    
    # Guardamos el resultado
    resultados_completitud.append({
        'columna': columna,
        'con_valor': con_valor,
        'vacios': vacios,
        'porcentaje': porcentaje
    })
    
    print(f"  {str(columna):<25} {con_valor:>10} {vacios:>10} {porcentaje:>11}%")

# Identificamos las 5 columnas con MÁS campos vacíos
print(f"\n  Top 5 columnas con mas campos vacios:")
# Ordenamos por porcentaje de menor a mayor (menos completas primero)
ordenados = sorted(resultados_completitud, key=lambda x: x['porcentaje'])
for i, r in enumerate(ordenados[:5]):
    print(f"    {i+1}. {r['columna']}: {r['vacios']} vacios ({100 - r['porcentaje']}% sin llenar)")


# ============================================================
# DIMENSION 2: CONSISTENCIA (Consistency)
# ============================================================
# Pregunta: ¿Cuántas variantes diferentes existen para un mismo
#           concepto en las columnas categóricas clave?
# Fórmula: Si una columna debería tener N categorías pero tiene M,
#           entonces la variabilidad = ((M - N) / M) * 100

print("\n" + "-" * 65)
print("  2. CONSISTENCIA")
print("-" * 65)

# Definimos las columnas importantes y cuántas categorías
# DEBERÍAN tener si los datos fueran consistentes
columnas_categoricas = {
    'SEXO': 2,                  # Solo debería ser: M, F
    'CASO SOCIAL': 4,           # Orientación, Evaluación y Seguimiento, Seguimiento, Orient. Derivación
    'SISFOH': 3,                # No Pobre, Pobre, Pobre Extremo
    'SEGURO': 5,                # SIS, EsSalud, SIS Independiente, Privado, Ninguno
    'TIPO VIVIENDA': 5,         # Propia, Alquilada, Hipotecada, Alojado, Cuidador
    'MODALIDAD INGRESO': 7,     # General, CEPREVAL, Discapacidad, etc.
    'ESCUELA / CARRERA': 29,    # 29 escuelas en el catálogo
}

print(f"\n  {'COLUMNA':<25} {'ESPERADAS':>10} {'ENCONTRADAS':>12} {'% VARIABIL.':>12}")
print(f"  {'-'*25} {'-'*10} {'-'*12} {'-'*12}")

resultados_consistencia = []
#.items() devuelve tuplas (clave, valor), en este caso (COLUMNA, CATEGORIAS_ESPERADAS)
for columna, categorias_esperadas in columnas_categoricas.items():
    if columna in df.columns:
        # Contamos cuántos valores ÚNICOS distintos hay en la columna
        # (ignorando los vacíos)
        valores_unicos = df[columna].dropna().nunique()
        
        # Calculamos el porcentaje de variabilidad
        # Si hay más valores únicos que los esperados, hay inconsistencia
        if valores_unicos > categorias_esperadas:
            # Hay variantes de más
            variantes_extra = valores_unicos - categorias_esperadas
            porcentaje_variabilidad = round((variantes_extra / valores_unicos) * 100, 2)
        else:
            # No hay variantes extra (los datos son consistentes)
            porcentaje_variabilidad = 0.0
        
        # Porcentaje de consistencia (lo contrario de variabilidad)
        porcentaje_consistencia = round(100 - porcentaje_variabilidad, 2)
        
        resultados_consistencia.append({
            'columna': columna,
            'esperadas': categorias_esperadas,
            'encontradas': valores_unicos,
            'variabilidad': porcentaje_variabilidad,
            'consistencia': porcentaje_consistencia
        })
        
        print(f"  {columna:<25} {categorias_esperadas:>10} {valores_unicos:>12} {porcentaje_variabilidad:>11}%")

# Calculamos el promedio general de consistencia
if resultados_consistencia:
    promedio_consistencia = round(
        sum(r['consistencia'] for r in resultados_consistencia) / len(resultados_consistencia), 2
    )
    print(f"\n  Consistencia promedio general: {promedio_consistencia}%")


# ============================================================
# DIMENSION 3: VALIDEZ (Validity)
# ============================================================
# Pregunta: ¿Qué porcentaje de fechas cumple un formato estándar
#           (YYYY-MM-DD o DD/MM/YYYY) vs textos libres ("3 de marzo")?

print("\n" + "-" * 65)
print("  3. VALIDEZ (Formato de fechas)")
print("-" * 65)

# Definimos los patrones de formato estándar usando expresiones simples
# DD/MM/YYYY (ej: 15/03/2026)

# Contadores
fechas_formato_estandar = 0
fechas_texto_libre = 0
fechas_vacias = 0

# Clasificamos cada fecha
clasificacion_fechas = {
    'DD/MM/YYYY': 0,
    'Texto libre': 0,
}

for fecha in df['FECHA ATENCION']:
    # Si la fecha está vacía
    if pd.isna(fecha):
        fechas_vacias += 1
        continue
    
    # Convertimos a texto para analizar
    fecha_texto = str(fecha).strip()
    
    # Verificamos si cumple el formato DD/MM/YYYY (ej: 15/03/2026)
    # Usamos una comprobación simple: tiene 2 barras y termina en 4 dígitos
    partes_barra = fecha_texto.split('/')
    es_dd_mm_yyyy = (
        len(partes_barra) == 3 and          # Tiene 3 partes separadas por /
        len(partes_barra[2]) == 4 and        # El año tiene 4 dígitos
        partes_barra[0].isdigit() and        # El día es número
        partes_barra[1].isdigit() and        # El mes es número
        partes_barra[2].isdigit()            # El año es número
    )
    
    if es_dd_mm_yyyy:
        clasificacion_fechas['DD/MM/YYYY'] += 1
        fechas_formato_estandar += 1
    else:
        # Es texto libre (cualquier otro formato)
        clasificacion_fechas['Texto libre'] += 1
        fechas_texto_libre += 1

# Calculamos los porcentajes
total_fechas_evaluadas = total_filas - fechas_vacias
porcentaje_estandar = round((fechas_formato_estandar / total_fechas_evaluadas) * 100, 2)
porcentaje_texto_libre = round((fechas_texto_libre / total_fechas_evaluadas) * 100, 2)

print(f"\n  Total de fechas evaluadas: {total_fechas_evaluadas}")
print(f"  Fechas vacias:            {fechas_vacias}")
print(f"\n  Formato estandar (DD/MM/YYYY): {fechas_formato_estandar} ({porcentaje_estandar}%)")
print(f"  Texto libre (otros formatos):  {fechas_texto_libre} ({porcentaje_texto_libre}%)")
print(f"\n  Validez de formato de fechas: {porcentaje_estandar}%")


# ============================================================
# DIMENSION 4: UNICIDAD (Uniqueness)
# ============================================================
# Pregunta: ¿Hay DNI repetidos? ¿Cuántos registros son duplicados?
# Fórmula: (registros únicos / total registros) * 100

print("\n" + "-" * 65)
print("  4. UNICIDAD")
print("-" * 65)

# --- Análisis por DNI ---
# Contamos cuántos DNI únicos hay
dni_unicos = df['DNI'].nunique()

# Contamos cuántos DNI están repetidos (aparecen más de 1 vez)
conteo_dni = df['DNI'].value_counts()          # Cuenta cuántas veces aparece cada DNI
dni_repetidos = conteo_dni[conteo_dni > 1]     # Filtramos solo los que aparecen más de 1 vez
cantidad_dni_repetidos = len(dni_repetidos)     # Cuántos DNI distintos están repetidos

# Total de filas que son "duplicadas" (las extras)
filas_duplicadas_dni = conteo_dni[conteo_dni > 1].sum() - cantidad_dni_repetidos

# Porcentaje de unicidad por DNI
porcentaje_unicidad_dni = round((dni_unicos / total_filas) * 100, 2)

print(f"\n  --- Por DNI ---")
print(f"  Total de registros:     {total_filas}")
print(f"  DNI unicos:             {dni_unicos}")
print(f"  DNI repetidos:          {cantidad_dni_repetidos}")
print(f"  Filas duplicadas:       {filas_duplicadas_dni}")
print(f"  Unicidad por DNI:       {porcentaje_unicidad_dni}%")

# Mostramos cuáles DNI están repetidos
if cantidad_dni_repetidos > 0:
    print(f"\n  DNI repetidos encontrados:")
    for dni, veces in dni_repetidos.items():
        print(f"    DNI {dni}: aparece {veces} veces")

# --- Análisis por Nombre Completo ---
# Creamos una columna temporal uniendo nombres + apellidos
df['nombre_completo_temp'] = (
    df['NOMBRES'].astype(str).str.strip().str.upper() + ' ' +
    df['APELLIDOS'].astype(str).str.strip().str.upper()
)

nombres_unicos = df['nombre_completo_temp'].nunique()
porcentaje_unicidad_nombres = round((nombres_unicos / total_filas) * 100, 2)

print(f"\n  --- Por Nombre Completo ---")
print(f"  Nombres unicos:         {nombres_unicos}")
print(f"  Unicidad por nombre:    {porcentaje_unicidad_nombres}%")

# Limpiamos la columna temporal
df = df.drop(columns=['nombre_completo_temp'])


# ============================================================
# DIMENSION 5: PUNTUALIDAD (Timeliness)
# ============================================================
# Pregunta: ¿Con qué frecuencia se registran los datos?
# Analizamos la distribución por MES, pero evaluamos el
# "Procesamiento por Lotes" (qué porcentaje del mes se registra
# en un solo día).

print("\n" + "-" * 65)
print("  5. PUNTUALIDAD (Evaluacion de procesamiento por lotes)")
print("-" * 65)

# Diccionario de meses
meses_espanol = {
    '03':'marzo', '04':'abril', '05':'mayo', '06':'junio', '07':'julio',
    'marzo':'marzo', 'abril':'abril', 'mayo':'mayo', 'junio':'junio', 'julio':'julio',
    'mar':'marzo', 'abr':'abril', 'may':'mayo', 'jun':'junio', 'jul':'julio'
}

# Función para extraer solo el mes de la fecha
def extraer_mes(f):
    f_str = str(f).strip().lower()
    for clave, mes in meses_espanol.items():
        if clave in f_str:
            return mes
    return 'desconocido'

# Limpiamos las fechas para extraer exactitud diaria
def limpiar_dia_exacto(f):
    f_str = str(f).strip().lower()
    if '/' in f_str:
        partes = f_str.split('/')
        if len(partes) >= 2:
            try:
                mes_str = meses_espanol.get(partes[1].zfill(2), 'desconocido')
                return f"{int(partes[0])} de {mes_str}"
            except: pass
    return f_str

df['mes'] = df['FECHA ATENCION'].apply(extraer_mes)
df['fecha_exacta'] = df['FECHA ATENCION'].apply(limpiar_dia_exacto)

# Filtramos nulos
df_valido = df[df['mes'] != 'desconocido']

if not df_valido.empty:
    print(f"\n  Analisis de registro acumulado (Batching) por mes:")
    print(f"  {'MES':<12} {'REGISTROS':>10} {'DIA PICO (LOTE)':>20} {'% ACUMULADO':>15}")
    print(f"  {'-'*12} {'-'*10} {'-'*20} {'-'*15}")
    
    concentracion_promedio = 0
    meses_evaluados = 0
    
    # Agrupamos por mes
    for mes in ['marzo', 'abril', 'mayo', 'junio', 'julio']:
        datos_mes = df_valido[df_valido['mes'] == mes]
        total_mes = len(datos_mes)
        
        if total_mes > 0:
            # Encontramos el día con más registros en ese mes
            dia_pico = datos_mes['fecha_exacta'].value_counts().index[0]
            cantidad_pico = datos_mes['fecha_exacta'].value_counts().iloc[0]
            pct_pico = round((cantidad_pico / total_mes) * 100, 2)
            
            concentracion_promedio += pct_pico
            meses_evaluados += 1
            
            print(f"  {mes.capitalize():<12} {total_mes:>10} {dia_pico.capitalize():>20} {pct_pico:>14}%")
    
    if meses_evaluados > 0:
        concentracion_promedio = round(concentracion_promedio / meses_evaluados, 2)
        print(f"\n  Concentracion promedio mensual en un solo dia: {concentracion_promedio}%")
        
        # La puntualidad es lo contrario a la concentración
        # Si amontonan el 80% en un día, la puntualidad es 20% (Mala)
        porcentaje_puntualidad = round(100 - concentracion_promedio, 2)
        
        if concentracion_promedio > 50:
            print(f"Mala puntualidad.")
        else:
            print(f"Buena puntualidad.")
else:
    porcentaje_puntualidad = 0
    print(f"  No hay fechas validas para evaluar.")

df = df.drop(columns=['mes', 'fecha_exacta'], errors='ignore')

# Sobrescribimos la variable para que pase a la tabla final
porcentaje_pico = concentracion_promedio


# ============================================================
# TABLA RESUMEN DE METRICAS DE CALIDAD
# ============================================================

print("\n\n" + "=" * 90)
print("   TABLA RESUMEN DE METRICAS DE CALIDAD DE DATOS")
print("=" * 90)


# Función simple para asignar nivel según el porcentaje
# Escala: 1-5 donde 5 es excelente y 1 es muy malo
def asignar_nivel(porcentaje):
    """
    Asigna un nivel de calidad basado en el porcentaje.
    - 90-100%: Alto (5)
    - 75-89%:  Medio-Alto (4)
    - 60-74%:  Medio (3)
    - 40-59%:  Medio-Bajo (2)
    - 0-39%:   Bajo (1)
    """
    if porcentaje >= 90:
        return "Alto", 5
    elif porcentaje >= 75:
        return "Medio-Alto", 4
    elif porcentaje >= 60:
        return "Medio", 3
    elif porcentaje >= 40:
        return "Medio-Bajo", 2
    else:
        return "Bajo", 1


# Construimos la tabla resumen
# Cada fila tiene: Dimensión, Métrica, N, %, Nivel, Escala
tabla_resumen = []

# 1. Completitud
nivel_comp, escala_comp = asignar_nivel(porcentaje_completitud)
tabla_resumen.append({
    'dimension': 'Completitud',
    'metrica': 'Celdas con valor vs total',
    'n': total_celdas,
    'porcentaje': porcentaje_completitud,
    'nivel': nivel_comp,
    'escala': escala_comp
})

# 2. Consistencia
if resultados_consistencia:
    nivel_cons, escala_cons = asignar_nivel(promedio_consistencia)
    tabla_resumen.append({
        'dimension': 'Consistencia',
        'metrica': 'Uniformidad en columnas categoricas',
        'n': sum(r['encontradas'] for r in resultados_consistencia),
        'porcentaje': promedio_consistencia,
        'nivel': nivel_cons,
        'escala': escala_cons
    })

# 3. Validez
nivel_val, escala_val = asignar_nivel(porcentaje_estandar)
tabla_resumen.append({
    'dimension': 'Validez',
    'metrica': 'Fechas en formato estandar',
    'n': total_fechas_evaluadas,
    'porcentaje': porcentaje_estandar,
    'nivel': nivel_val,
    'escala': escala_val
})

# 4. Unicidad
nivel_uni, escala_uni = asignar_nivel(porcentaje_unicidad_dni)
tabla_resumen.append({
    'dimension': 'Unicidad',
    'metrica': 'Registros unicos por DNI',
    'n': total_filas,
    'porcentaje': porcentaje_unicidad_dni,
    'nivel': nivel_uni,
    'escala': escala_uni
})

# 5. Puntualidad
# Convertimos la distribución a un porcentaje de "buena puntualidad"
# (100% - concentración en un solo mes = más distribuido = mejor)
porcentaje_puntualidad = round(100 - porcentaje_pico, 2)
nivel_punt, escala_punt = asignar_nivel(porcentaje_puntualidad)
tabla_resumen.append({
    'dimension': 'Puntualidad',
    'metrica': 'Distribucion temporal de registros',
    'n': total_filas,
    'porcentaje': porcentaje_puntualidad,
    'nivel': nivel_punt,
    'escala': escala_punt
})

# Imprimimos la tabla resumen formateada
print(f"\n  {'DIMENSION':<16} {'METRICA':<38} {'N':>6} {'%':>8} {'NIVEL':<12} {'ESCALA':>6}")
print(f"  {'-'*16} {'-'*38} {'-'*6} {'-'*8} {'-'*12} {'-'*6}")

for fila in tabla_resumen:
    print(f"  {fila['dimension']:<16} {fila['metrica']:<38} {fila['n']:>6} {fila['porcentaje']:>7}% {fila['nivel']:<12} {fila['escala']:>5}/5")

# Calculamos el puntaje promedio general
promedio_general = round(sum(f['escala'] for f in tabla_resumen) / len(tabla_resumen), 2)
porcentaje_general = round(sum(f['porcentaje'] for f in tabla_resumen) / len(tabla_resumen), 2)

print(f"\n  {'PROMEDIO GENERAL':<16} {'Calidad global del dataset':<38} {'':>6} {porcentaje_general:>7}% {'':>12} {promedio_general:>5}/5")

print("="*90)