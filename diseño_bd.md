# Diseño y Modelado de Base de Datos - Sistema Social

## 1. Fase de Análisis y Conceptualización (Pre-Normalización)

Para el diseño de la base de datos, el flujo se inició con un **Modelo Conceptual (Diagrama Entidad-Relación inicial)** orientado a capturar la totalidad de los datos requeridos por el sistema. Inicialmente, la abstracción partió de una gran macro-entidad de "Registro o Atención" donde se pretendía agrupar toda la información personal del estudiante, sus datos académicos (facultad, escuela), el tipo de caso social y los múltiples detalles que componen las fichas. 

Para que el modelo llegara al estado consolidado que tenemos ahora, fue necesario aplicar **reglas de normalización**. Este proceso evolutivo nos permitió:
- **Separar datos repetitivos** y estáticos (como Facultades, Escuelas, Modalidades de Ingreso y Tipos de Casos Sociales) en **tablas de catálogo (maestras)** para evitar redundancia e inconsistencias (Primera y Segunda Forma Normal).
- **Desacoplar las fichas de evaluación** (`FichaSocioeconomica` y `FichaDerivacion`) de la tabla principal `Persona`. Si no hubiéramos normalizado, la tabla `Persona` tendría demasiados campos vacíos (nulos) cuando un estudiante no requiriera una ficha específica, violando los principios de un buen diseño.

---

## 2. Definición de Relaciones (Cardinalidad)

Una vez normalizado el modelo, las entidades se conectan entre sí mediante las siguientes relaciones específicas. Estas relaciones son clave para que puedas armar tu diagrama final:

### Relaciones de Uno a Muchos (1:N)
- **Facultad a Escuela (1:N):** Una facultad puede tener múltiples escuelas profesionales, pero una escuela pertenece a una única facultad.
- **Catálogo a Persona (1:N):** 
  - **CatTipoUsuario a Persona:** Un tipo de usuario (ej. Estudiante) es asignado a muchas personas.
  - **CatFacultad a Persona:** Una facultad alberga a muchos estudiantes (personas registradas).
  - **CatEscuela a Persona:** Una escuela alberga a muchos estudiantes (personas registradas).
  - **CatCasoSocial a Persona:** Un tipo de caso social puede estar asociado a muchas atenciones (personas).
  - **CatModalidad a Persona:** Una modalidad de ingreso puede estar presente en muchos estudiantes (personas).

### Relaciones de Uno a Uno (1:1)
- **Persona a FichaSocioeconomica (1:1):** Un registro de atención de una persona tiene, como máximo, una sola Ficha Socioeconómica (una persona tiene solo una ficha socioeconómica).
- **Persona a FichaDerivacion (1:1):** Un registro de atención de una persona tiene, como máximo, una sola Ficha de Derivación (una persona tiene solo una ficha de derivación).

---

## 3. Modelo Relacional Normalizado (Diccionario de Datos Actual)

A continuación, se detalla el esquema exacto consolidado tras la normalización. Incluye las entidades, sus atributos, llaves (PK/FK) y los tipos de datos listos para tu informe.

### 3.1 Entidades de Catálogo (Tablas Maestras)

**Entidad: CatTipoUsuario**
*Descripción:* Define el tipo de público que está recibiendo la atención (ej. Estudiante, Docente, Administrativo, Egresado). Sirve para categorizar a la `Persona` atendida.
- `id` : INT(11) [PK]
- `nombre` : VARCHAR(50)
- `activo` : BOOLEAN (o TINYINT(1))

**Entidad: CatFacultad**
- `id` : INT(11) [PK]
- `nombre` : VARCHAR(100)
- `activo` : BOOLEAN

**Entidad: CatEscuela**
- `id` : INT(11) [PK]
- `nombre` : VARCHAR(100)
- `facultad_id` : INT(11) [FK -> CatFacultad.id]
- `activo` : BOOLEAN

**Entidad: CatCasoSocial**
- `id` : INT(11) [PK]
- `nombre` : VARCHAR(50)
- `activo` : BOOLEAN

**Entidad: CatModalidad**
- `id` : INT(11) [PK]
- `nombre` : VARCHAR(50)
- `activo` : BOOLEAN

### 3.2 Entidades Principales y Transaccionales

**Entidad: Usuario** (Credenciales del sistema)
*Nota para tu Diagrama ER:* Esta tabla representa al **personal (trabajadores sociales, operadores, administradores)** que ingresa al sistema, NO a los estudiantes. Es normal que en tu diagrama quede como una "entidad aislada" (sin líneas hacia las otras tablas), ya que su único fin es el acceso al software.
- `id` : INT(11) [PK]
- `username` : VARCHAR(50)
- `password_hash` : VARCHAR(255)
- `nombre_completo` : VARCHAR(200)
- `rol` : VARCHAR(20)
- `activo` : BOOLEAN

**Entidad: Persona** (Bitácora central de atención)
*Nota de diseño (Justificación para el informe):* La llave primaria de esta tabla es el `id` y **no el `dni`**. Se diseñó como una "bitácora": si usáramos el DNI como llave, el estudiante solo podría registrarse una vez en la vida. Al usar un `id` interno, el sistema permite que un mismo DNI se registre múltiples veces en diferentes fechas, manteniendo un historial de atenciones.
- `id` : INT(11) [PK]
- `dni` : VARCHAR(20)
- `nombres` : VARCHAR(100)
- `apellidos` : VARCHAR(100)
- `edad` : INT(3)
- `sexo` : VARCHAR(1)
- `fecha_atencion` : DATETIME
- `codigo_estudiante` : VARCHAR(20)
- `año_estudio` : VARCHAR(10)
- `tipo_usuario_id` : INT(11) [FK -> CatTipoUsuario.id]
- `facultad_id` : INT(11) [FK -> CatFacultad.id]
- `escuela_id` : INT(11) [FK -> CatEscuela.id]
- `caso_social_id` : INT(11) [FK -> CatCasoSocial.id]
- `modalidad_id` : INT(11) [FK -> CatModalidad.id]
- `registro_modalidad` : VARCHAR(100)
- `celular` : VARCHAR(20)
- `correo` : VARCHAR(100)
- `direccion` : VARCHAR(200)
- `observaciones` : TEXT
- `activo` : BOOLEAN
- `fecha_registro` : DATETIME

### 3.3 Entidades de Fichas Especializadas

**Entidad: FichaSocioeconomica** 
- `id` : INT(11) [PK]
- `persona_id` : INT(11) [FK -> Persona.id] *(Relación 1:1 con Persona)*
- `motivo_evaluacion` : VARCHAR(100)
- `sisfoh_condicion` : VARCHAR(50)
- `tiene_discapacidad` : BOOLEAN
- `tipo_discapacidad` : VARCHAR(50)
- `nivel_de_discapacidad` : VARCHAR(50)
- `tipo_seguro` : VARCHAR(50)
- `estructura_familiar` : VARCHAR(50)
- `dinamica_familiar` : VARCHAR(50)
- `ingreso_familiar_total` : FLOAT (o DECIMAL(10,2))
- `ingreso_becas_bonos` : FLOAT (o DECIMAL(10,2))
- `egreso_alquiler` : FLOAT (o DECIMAL(10,2))
- `egreso_alimentacion` : FLOAT (o DECIMAL(10,2))
- `egreso_servicios` : FLOAT (o DECIMAL(10,2))
- `egreso_educacion_otros` : FLOAT (o DECIMAL(10,2))
- `tipo_vivienda` : VARCHAR(50)
- `material_paredes` : VARCHAR(50)
- `material_techo` : VARCHAR(50)
- `tiene_agua_red` : BOOLEAN
- `tiene_desague_red` : BOOLEAN
- `tiene_energia_electrica` : BOOLEAN

**Entidad: FichaDerivacion**
- `id` : INT(11) [PK]
- `persona_id` : INT(11) [FK -> Persona.id] *(Relación 1:1 con Persona)*
- `fecha_nacimiento` : DATE
- `lugar_nacimiento` : VARCHAR(100)
- `ocupacion` : VARCHAR(100)
- `vive_con` : VARCHAR(100)
- `telefono_familiares` : VARCHAR(50)
- `area_deriva` : VARCHAR(100)
- `area_derivada` : VARCHAR(100)
- `fecha_derivacion` : DATETIME
- `motivo_consulta` : TEXT
- `tiene_derivaciones_previas` : BOOLEAN
- `detalle_derivaciones_previas` : TEXT
- `condicion` : VARCHAR(50)
- `impacto_academico` : BOOLEAN
- `impacto_social` : BOOLEAN
- `impacto_familiar` : BOOLEAN
- `impacto_personal` : BOOLEAN
- `diagnostico` : TEXT
- `observaciones` : TEXT
