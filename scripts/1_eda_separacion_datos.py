import pandas as pd
import os

# ------------------------------------------------------------
# 1. Cargar el Excel plano original
# ------------------------------------------------------------
ruta_excel = os.path.join(os.path.dirname(__file__), '..', 'datos_originales_plano.xlsx')
datos_planos = pd.read_excel(ruta_excel)

print("=" * 70)
print("   PASO 1: SEPARACION Y ESTRUCTURACION DE DATOS")
print(f"   Total de registros cargados: {len(datos_planos)}")
print("=" * 70)

# ------------------------------------------------------------
# 2. Definir las columnas para el dataset de Atenciones Generales
# ------------------------------------------------------------
columnas_atenciones = [
    'N°', 'DNI', 'NOMBRES', 'APELLIDOS', 'EDAD', 'SEXO',
    'COD. ESTUDIANTE', 'AÑO', 'TIPO', 'FACULTAD', 'ESCUELA / CARRERA',
    'MODALIDAD INGRESO', 'CELULAR', 'CORREO', 'DIRECCION',
    'CASO SOCIAL', 'OBSERVACIONES', 'FECHA ATENCION'
]

# Filtramos la tabla de atenciones solo con esas columnas
tabla_atenciones_raw = datos_planos[columnas_atenciones].copy()

# ------------------------------------------------------------
# 3. Separar las Fichas Socioeconómicas
# ------------------------------------------------------------
# Criterio: Tiene datos en 'MOTIVO EVALUACION' O su 'CASO SOCIAL' menciona evaluación.

# Condición 1: 'MOTIVO EVALUACION' no está vacío
motivo_no_vacio = datos_planos['MOTIVO EVALUACION'].notna()

# Condición 2: 'CASO SOCIAL' contiene la palabra 'evalua'
caso_texto = datos_planos['CASO SOCIAL'].astype(str).str.lower()
caso_tiene_evaluacion = caso_texto.str.contains('evalua', na=False)

# Combinamos ambas condiciones (si cumple cualquiera de las dos)
filtro_es_evaluacion = motivo_no_vacio | caso_tiene_evaluacion

# Creamos la tabla de evaluaciones con todas sus columnas
tabla_evaluaciones_raw = datos_planos[filtro_es_evaluacion].copy()


# ------------------------------------------------------------
# 4. Ajustar 'CASO SOCIAL' si decía 'Orientación' pero tenía motivo de evaluación
# ------------------------------------------------------------
# Si en la tabla de evaluaciones su 'CASO SOCIAL' no decía evaluación (ej. decía "Orientación"), lo corregimos a "Evaluación"

def corregir_caso_social(caso_actual):
    texto = str(caso_actual).lower()
    # Si ya contiene "evalua", se deja igual
    if 'evalua' in texto:
        return caso_actual
    else:
        # Si decía "Orientación" o similar, lo corregimos a "Evaluación"
        return 'Evaluación'

tabla_evaluaciones_raw['CASO SOCIAL'] = tabla_evaluaciones_raw['CASO SOCIAL'].apply(corregir_caso_social)


# ------------------------------------------------------------
# 5. Guardar resultados en la carpeta 'scripts/data_eda/data_separada/'
# ------------------------------------------------------------
carp_salida = os.path.join(os.path.dirname(__file__), 'data_eda', 'data_separada')
os.makedirs(carp_salida, exist_ok=True)

ruta_out_atenciones = os.path.join(carp_salida, 'atenciones_raw.xlsx')
ruta_out_evaluaciones = os.path.join(carp_salida, 'evaluaciones_raw.xlsx')

