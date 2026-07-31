import pandas as pd
import random
import os
import re

# Ruta del archivo
ruta_excel = os.path.join(os.path.dirname(__file__), '..', 'datos_originales_plano.xlsx')

print("Cargando archivo para ajustar las fechas en lotes...")
df = pd.read_excel(ruta_excel)

# Lotes específicos por mes solicitados por el usuario
lotes_por_mes = {
    'marzo': [(31, 'marzo', '03')],
    'abril': [(7, 'abril', '04'), (20, 'abril', '04')],
    'mayo': [(1, 'mayo', '05'), (5, 'mayo', '05'), (15, 'mayo', '05')],
    'junio': [(2, 'junio', '06'), (19, 'junio', '06')],
    'julio': [(14, 'julio', '07'), (16, 'julio', '07'), (17, 'julio', '07')]
}

def asignar_lote(fecha_actual):
    fecha_str = str(fecha_actual).lower()
    
    # Identificar el mes actual
    mes_detectado = None
    if 'mar' in fecha_str or '/03' in fecha_str: mes_detectado = 'marzo'
    elif 'abr' in fecha_str or '/04' in fecha_str: mes_detectado = 'abril'
    elif 'may' in fecha_str or '/05' in fecha_str: mes_detectado = 'mayo'
    elif 'jun' in fecha_str or '/06' in fecha_str: mes_detectado = 'junio'
    elif 'jul' in fecha_str or '/07' in fecha_str: mes_detectado = 'julio'
    else: mes_detectado = 'marzo' # Default por si hay vacíos
    
    # Elegir uno de los lotes (días) disponibles para ese mes
    opcion = random.choice(lotes_por_mes[mes_detectado])
    dia, nombre_mes, num_mes = opcion
    
    # Variar el formato: "31 de marzo" o "31/03"
    formato = random.choice([1, 2, 3])
    if formato == 1:
        return f"{dia} de {nombre_mes}"
    elif formato == 2:
        return f"{dia:02d}/{num_mes}"
    else:
        return f"{dia} de {nombre_mes.capitalize()}"

# Aplicar la transformación a toda la columna
df['FECHA ATENCION'] = df['FECHA ATENCION'].apply(asignar_lote)

# Asegurar tipo object para guardar
for col in df.columns:
    if df[col].dtype == 'object':
        df[col] = df[col].astype(str)

print("Guardando Excel actualizado...")
try:
    df.to_excel(ruta_excel, index=False)
    print("¡Archivo guardado con éxito! Las fechas ahora reflejan el registro por lotes.")
except PermissionError:
    print("ERROR: Por favor, Cierra el archivo Excel datos_originales_plano.xlsx antes de ejecutar.")
