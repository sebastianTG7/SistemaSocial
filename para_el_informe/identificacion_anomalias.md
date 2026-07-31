# Identificación de Anomalías en el Dataset Original

## Tabla de Anomalías Detectadas por Variable

| **Variable** | **Tipo de Anomalía** | **Valores encontrados** | **Valor esperado** |
|---|---|---|---|
| **SEXO** | Inconsistencia en formato | `M`, `Masculino`, `masculino`, `MASCULINO`, `Masc`, `H`, `Hombre`, `m`, `F`, `Femenino`, `femenino`, `FEMENINO`, `Fem`, `Mujer`, `f` | `M` o `F` |
| **EDAD** | Tipos de dato mixtos | `17`, `"17"` (texto), `"21 años"` (texto con unidad), valores nulos | Valor numérico entero |
| **DNI** | Formato inconsistente | `60932248`, `6093 2248` (con espacio), `6093-2248` (con guión) | 8 dígitos sin separadores |
| **CELULAR** | Formato inconsistente | `993955379`, `+51 993955379`, `51993955379`, `993-955-379` | 9 dígitos sin prefijo |
| **NOMBRES** | Capitalización mixta | `DANNY ANDRE` (mayúsculas), `danny andre` (minúsculas), `Danny Andre` (Title Case) | Formato uniforme |
| **NOMBRES** | Datos cruzados | `CHICLOTE MONTEBLANCO, DANNY ANDRE` (apellido y nombre pegados en una sola columna, dejando APELLIDOS vacío) | Solo nombres |
| **APELLIDOS** | Valores vacíos | Registros con apellido en blanco porque se pegó todo en NOMBRES | Siempre con valor |
| **ESCUELA / CARRERA** | Inconsistencia en nomenclatura | `Enfermería`, `ENFERMERÍA`, `enfermeria`, `Enf.`, `Enferm.` | Nombre estandarizado |
| **ESCUELA / CARRERA** | Abreviaciones no estándar | `ING. CIVIL`, `Ing Civil`, `ING. SISTEMAS`, `CC. CONTABLES`, `Med. Humana`, `Arq.`, `Psico.` | Nombre completo |
| **CASO SOCIAL** | Inconsistencia en formato | `Seguimiento`, `seguimiento`, `SEGUIMIENTO`, `Seg.`, `seguim.` | Valor del catálogo |
| **CASO SOCIAL** | Variantes de tildes | `Orientación`, `orientacion`, `Evaluación y Seguimiento`, `Evaluacion y Seguimiento`, `EVALUACION Y SEGUIMIENTO`, `Eval. y Seg.` | Valor estandarizado con tildes |
| **FECHA ATENCION** | Formatos múltiples | `24 de marzo`, `24 de Marzo`, `24 de marzo del 2026`, `24/03/2026`, `24-marzo-2026`, `marzo 24`, `24/03` | Formato de fecha uniforme |
| **FECHA ATENCION** | Información incompleta | `24/03` (sin año), `marzo 24` (sin año) | Fecha completa con año |
| **SISFOH** | Inconsistencia en formato | `Pobre Extremo`, `POBRE EXTREMO`, `pobre extremo`, `Extrema Pobreza`, `PE`, `Pobre`, `POBRE`, `P`, `No Pobre`, `NO POBRE`, `NP` | Valor del catálogo (`No Pobre`, `Pobre`, `Pobre Extremo`) |
| **SEGURO** | Inconsistencia en formato | `SIS`, `sis`, `S.I.S.`, `SIS Gratuito`, `SIS gratuito`, `Sis` | Valor estandarizado |
| **SEGURO** | Variantes de seguro social | `ESSALUD`, `EsSalud`, `essalud`, `Es Salud`, `ESSALUD HUANUCO` | `EsSalud` |
| **SEGURO** | Valores ambiguos para "sin seguro" | `NINGUNO`, `Ninguno`, `ninguno`, `No tiene`, `Sin seguro`, `N/A`, vacío | Valor estandarizado o nulo |
| **TIPO VIVIENDA** | Inconsistencia en formato | `Propia`, `PROPIA`, `propia`, `Casa propia`, `Prop.`, `Alquilada`, `ALQUILADA`, `Alquiler`, `Alq.` | Valor del catálogo |
| **INGRESO FAMILIAR** | Tipos de dato mixtos | `2000.0` (numérico), `S/. 500` (con símbolo), `S/350` (con símbolo abreviado), `800,5` (coma decimal) | Valor numérico decimal |
| **GASTO ALQUILER** | Tipos de dato mixtos | `0.0` (numérico), `S/. 200`, `S/170`, `100,0` (coma decimal) | Valor numérico decimal |
| **GASTO ALIMENTACION** | Tipos de dato mixtos | `300.0` (numérico), `S/. 800`, `60,0` (coma decimal) | Valor numérico decimal |
| **MATERIAL PAREDES** | Inconsistencia en formato | `Noble`, `noble`, `NOBLE`, `Ladrillo`, `LADRILLO`, `Material noble`, `ladrillo/cemento`, `Mixto`, `mixto`, `MIXTO` | Valor del catálogo |
| **ESTRUCTURA FAMILIAR** | Términos no estandarizados | `Organizada`, `organizada`, `ORGANIZADA`, `Nuclear`, `Familia organizada`, `Desintegrada`, `desintegrada`, `Monoparental` | Valor del catálogo |
| **Booleanos** (Discapacidad, Agua, Desagüe, Luz) | Representación inconsistente | `1`, `0`, `Sí`, `SI`, `si`, `VERDADERO`, `Verdadero`, `TRUE`, `True`, `V`, `X`, `No`, `NO`, `FALSO`, `FALSE`, `-` | `Sí` / `No` o `1` / `0` |
| **Registros duplicados** | Filas repetidas | 8 registros duplicados con variaciones menores (ej. nombre en minúscula vs mayúscula) | Registros únicos por DNI |
| **Valores nulos** | Campos sin completar | CORREO (96% vacío), DIRECCIÓN (45% vacío), OBSERVACIONES (80% vacío), campos socioeconómicos (78% vacío) | Completitud esperada |

## Resumen de Tipos de Anomalías

| **Tipo de Anomalía** | **Cantidad de Variables Afectadas** |
|---|---|
| Inconsistencia de formato/capitalización | 14 |
| Tipos de dato mixtos (texto vs numérico) | 4 |
| Valores nulos o campos vacíos | 8 |
| Formatos de fecha múltiples | 1 |
| Abreviaciones no estándar | 2 |
| Registros duplicados | 8 filas |
| Datos cruzados entre columnas | 1 |
