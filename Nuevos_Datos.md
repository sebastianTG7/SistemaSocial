1. Tabla: fichas_socioeconomicas (Datos Consolidados)
Esta tabla almacena una sola fila por evaluación. Contiene respuestas cerradas (listas) y números puros para que tu EDA y tu modelo matemático funcionen a la perfección.

id (Número Entero - Clave Primaria)

persona_id (Número Entero - Clave Foránea que conecta con tu tabla personas)

Contexto de la Evaluación:

motivo_evaluacion (Texto / Lista desplegable): Valores estrictos: Comedor Universitario, Exoneración o Reducción de Pago, Derivación a otra Área, Caso Especial, Modalidad de Ingreso
Clasificación de Vulnerabilidad (SISFOH y Salud):

sisfoh_condicion (Texto / Lista desplegable): No Pobre, Pobre, Pobre Extremo.

tiene_discapacidad (Booleano: Sí/No)

tipo_discapacidad (Texto / Lista desplegable): Ninguna, Visual, Motora, Auditiva, Mental, Otro(especifica).
tipo_seguro (Texto / Lista desplegable): SIS Gratuito, EsSalud, SIS Independiente, Privado, Ninguno.
Estructura y Dinámica Familiar:

estructura_familiar (Texto / Lista desplegable): Nuclear, Monoparental, Extendida, Unipersonal, Ensamblada.

dinamica_familiar (Texto / Lista desplegable): Armonioso, Moderadamente Armonioso, Conflictiva, Altamente Conflictiva.
Datos Económicos (Variables Numéricas Críticas):

ingreso_familiar_total (Decimal): Suma total de los ingresos de todos los miembros del hogar (ej. 350.00).

ingreso_becas_bonos (Decimal): Monto en soles si recibe Beca Permanencia u otros bonos del Estado.

egreso_alquiler (Decimal): Pago mensual de vivienda (colocar 0.00 si es casa propia).

egreso_alimentacion (Decimal): Gasto estimado mensual en comida.

egreso_servicios (Decimal): Gasto sumado de Luz, Agua y Teléfono/Internet.

egreso_educacion_otros (Decimal): Gastos en pasajes, copias, salud, etc.
Características de la Vivienda (Filtros de Pobreza):

tipo_vivienda (Texto / Lista desplegable): Propia, Alquilada, Hipotecada, Alojado por familiares, Cuidador.

material_paredes (Texto / Lista desplegable): Ladrillo/Cemento, Adobe/Tapia, Madera, Otros.

material_techo (Texto / Lista desplegable): Concreto, Calamina, Eternit, Madera/Paja.

tiene_agua_red (Booleano: Sí/No)

tiene_desague_red (Booleano: Sí/No)

tiene_energia_electrica (Booleano: Sí/No)



NINGUN DATO DE ESTOS NO ES OBLIGATIRIO RELLENAR.