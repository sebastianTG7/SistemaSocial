# Diccionario de Datos - Sistema Social

A continuación se presenta el diccionario de datos exacto de la base de datos del Sistema Social, reflejando fielmente la estructura física SQL de la base de datos.

### 1. Tablas de Catálogo (Maestras)

#### Tabla: `cat_tipos_usuario`
Define los tipos de usuario (ej. Estudiante, Docente).

| Campo | Tipo SQL | Restricción | Descripción |
| :--- | :--- | :--- | :--- |
| `id` | INT | PK, INDEX | Identificador único del tipo de usuario. |
| `nombre` | VARCHAR(50) | NOT NULL, UNIQUE | Nombre del tipo de usuario. |
| `activo` | BOOLEAN | DEFAULT 1 | Indica si el registro está activo. |

#### Tabla: `cat_facultades`
Catálogo de facultades.

| Campo | Tipo SQL | Restricción | Descripción |
| :--- | :--- | :--- | :--- |
| `id` | INT | PK, INDEX | Identificador único de la facultad. |
| `nombre` | VARCHAR(100) | NOT NULL, UNIQUE | Nombre de la facultad. |
| `activo` | BOOLEAN | DEFAULT 1 | Indica si el registro está activo. |

#### Tabla: `cat_escuelas`
Catálogo de escuelas profesionales.

| Campo | Tipo SQL | Restricción | Descripción |
| :--- | :--- | :--- | :--- |
| `id` | INT | PK, INDEX | Identificador único de la escuela. |
| `nombre` | VARCHAR(100) | NOT NULL | Nombre de la escuela. |
| `facultad_id` | INT | FK | Referencia a `cat_facultades.id`. |
| `activo` | BOOLEAN | DEFAULT 1 | Indica si el registro está activo. |

#### Tabla: `cat_casos_sociales`
Tipos de casos sociales (Orientación, Evaluación, Seguimiento, etc).

| Campo | Tipo SQL | Restricción | Descripción |
| :--- | :--- | :--- | :--- |
| `id` | INT | PK, INDEX | Identificador único del caso social. |
| `nombre` | VARCHAR(50) | NOT NULL, UNIQUE | Nombre del caso social. |
| `activo` | BOOLEAN | DEFAULT 1 | Indica si el registro está activo. |

#### Tabla: `cat_modalidades`
Modalidades de ingreso (General, Cepreval, Discapacidad, etc).

| Campo | Tipo SQL | Restricción | Descripción |
| :--- | :--- | :--- | :--- |
| `id` | INT | PK, INDEX | Identificador único de la modalidad. |
| `nombre` | VARCHAR(50) | NOT NULL, UNIQUE | Nombre de la modalidad de ingreso. |
| `activo` | BOOLEAN | DEFAULT 1 | Indica si el registro está activo. |

---

### 2. Entidades Principales

#### Tabla: `usuarios`
Credenciales de acceso para el personal (operadores/administradores).

| Campo | Tipo SQL | Restricción | Descripción |
| :--- | :--- | :--- | :--- |
| `id` | INT | PK, INDEX | Identificador único del usuario. |
| `username` | VARCHAR(50) | NOT NULL, UNIQUE, INDEX | Nombre de usuario para el login. |
| `password_hash` | VARCHAR(255)| NOT NULL | Contraseña encriptada. |
| `nombre_completo`| VARCHAR(200)| - | Nombres y apellidos completos del personal. |
| `rol` | VARCHAR(20) | DEFAULT 'operador' | Rol del usuario en el sistema. |
| `activo` | BOOLEAN | DEFAULT 1 | Indica si la cuenta está activa. |

#### Tabla: `personas` (Catálogo de Beneficiarios)
Registro central de datos fijos de los individuos atendidos.

| Campo | Tipo SQL | Restricción | Descripción |
| :--- | :--- | :--- | :--- |
| `id` | INT | PK, INDEX | Identificador único de la persona. |
| `dni` | VARCHAR(20) | NOT NULL, UNIQUE, INDEX | DNI de la persona. |
| `nombres` | VARCHAR(100) | NOT NULL | Nombres de la persona. |
| `apellidos` | VARCHAR(100) | NOT NULL | Apellidos de la persona. |
| `fecha_nacimiento`| DATE | - | Fecha de nacimiento de la persona. |
| `edad` | INT | - | Edad de la persona. |
| `sexo` | VARCHAR(1) | - | Sexo (F/M). |
| `codigo_estudiante`| VARCHAR(20) | - | Código universitario (si aplica). |
| `año_estudio` | VARCHAR(10) | - | Año o ciclo de estudio actual. |
| `tipo_usuario_id`| INT | FK | Referencia a `cat_tipos_usuario.id`. |
| `facultad_id` | INT | FK | Referencia a `cat_facultades.id`. |
| `escuela_id` | INT | FK | Referencia a `cat_escuelas.id`. |
| `celular` | VARCHAR(20) | - | Número de celular. |
| `correo` | VARCHAR(100) | - | Correo electrónico. |
| `direccion` | VARCHAR(200) | - | Dirección domiciliaria. |
| `activo` | BOOLEAN | DEFAULT 1 | Estado lógico del registro. |
| `fecha_registro` | DATETIME | DEFAULT | Fecha en la que se guardó en el sistema. |

#### Tabla: `atenciones` (Historial de Visitas)
Registro de cada evento de atención a una persona (Relación 1:N con personas).

| Campo | Tipo SQL | Restricción | Descripción |
| :--- | :--- | :--- | :--- |
| `id` | INT | PK, INDEX | Identificador único de la atención. |
| `persona_id` | INT | FK, NOT NULL | Referencia a `personas.id` (NO UNIQUE). |
| `fecha_atencion` | DATETIME | NOT NULL, DEFAULT | Fecha y hora de la atención. |
| `caso_social_id` | INT | FK | Referencia a `cat_casos_sociales.id`. |
| `modalidad_id` | INT | FK | Referencia a `cat_modalidades.id`. |
| `registro_modalidad`| VARCHAR(100)| - | Detalle extra sobre la modalidad. |
| `observaciones` | TEXT | - | Anotaciones generales sobre la visita. |
| `activo` | BOOLEAN | DEFAULT 1 | Estado lógico del registro. |
| `fecha_registro` | DATETIME | DEFAULT | Fecha de registro en el sistema. |

---

### 3. Fichas Especializadas

#### Tabla: `fichas_socioeconomicas`
Detalle económico, familiar y de vivienda (Relación 1:1 con `personas`).

| Campo | Tipo SQL | Restricción | Descripción |
| :--- | :--- | :--- | :--- |
| `id` | INT | PK, INDEX | Identificador único de la ficha. |
| `persona_id` | INT | FK, NOT NULL, UNIQUE| Referencia a `personas.id`. |
| `motivo_evaluacion` | VARCHAR(100) | - | Contexto de la evaluación. |
| `sisfoh_condicion` | VARCHAR(50) | - | Clasificación socioeconómica (SISFOH). |
| `tiene_discapacidad`| BOOLEAN | DEFAULT 0 | Si el estudiante tiene discapacidad. |
| `tipo_discapacidad` | VARCHAR(50) | - | Especificación del tipo de discapacidad. |
| `nivel_de_discapacidad`| VARCHAR(50)| - | Nivel de severidad de la discapacidad. |
| `tipo_seguro` | VARCHAR(50) | - | Seguro de salud con el que cuenta. |
| `estructura_familiar` | VARCHAR(50) | - | Tipo de familia. |
| `dinamica_familiar` | VARCHAR(50) | - | Calidad de relaciones familiares. |
| `ingreso_familiar_total`| FLOAT | DEFAULT 0.0 | Ingresos totales de la familia. |
| `ingreso_becas_bonos` | FLOAT | DEFAULT 0.0 | Ingresos adicionales por becas/bonos. |
| `egreso_alquiler` | FLOAT | DEFAULT 0.0 | Gastos en alquiler. |
| `egreso_alimentacion` | FLOAT | DEFAULT 0.0 | Gastos en alimentación. |
| `egreso_servicios` | FLOAT | DEFAULT 0.0 | Gastos en servicios básicos. |
| `egreso_educacion_otros`| FLOAT | DEFAULT 0.0 | Gastos en educación u otros. |
| `tipo_vivienda` | VARCHAR(50) | - | Condición de la vivienda. |
| `material_paredes`| VARCHAR(50) | - | Material principal de paredes. |
| `material_techo` | VARCHAR(50) | - | Material principal del techo. |
| `tiene_agua_red` | BOOLEAN | DEFAULT 0 | Acceso a red de agua. |
| `tiene_desague_red` | BOOLEAN | DEFAULT 0 | Acceso a red de desagüe. |
| `tiene_energia_electrica`| BOOLEAN| DEFAULT 0 | Acceso a energía eléctrica. |

#### Tabla: `fichas_derivacion`
Detalles para derivación a otras áreas y evaluación de impacto (Relación 1:1 con `atenciones`).

| Campo | Tipo SQL | Restricción | Descripción |
| :--- | :--- | :--- | :--- |
| `id` | INT | PK, INDEX | Identificador único de la ficha. |
| `atencion_id` | INT | FK, NOT NULL, UNIQUE| Referencia a `atenciones.id`. |
| `lugar_nacimiento`| VARCHAR(100)| - | Lugar de nacimiento. |
| `ocupacion` | VARCHAR(100)| - | Ocupación laboral o académica extra. |
| `vive_con` | VARCHAR(100)| - | Personas con las que convive. |
| `telefono_familiares`| VARCHAR(50) | - | Contacto en caso de emergencia/familia. |
| `area_deriva` | VARCHAR(100)| - | Área desde donde se origina la derivación. |
| `area_derivada` | VARCHAR(100)| - | Área destino de la derivación. |
| `fecha_derivacion`| DATETIME | DEFAULT | Fecha y hora de derivación. |
| `motivo_consulta` | TEXT | - | Motivo de la consulta y derivación. |
| `tiene_derivaciones_previas`| BOOLEAN| DEFAULT 0 | Si fue derivado anteriormente. |
| `detalle_derivaciones_previas`| TEXT| - | Detalles de derivaciones pasadas. |
| `condicion` | VARCHAR(50) | - | Nivel de condición (ej. Leve, Grave). |
| `impacto_academico`| BOOLEAN | DEFAULT 0 | Si el caso afecta su rendimiento académico. |
| `impacto_social` | BOOLEAN | DEFAULT 0 | Si afecta a sus relaciones sociales. |
| `impacto_familiar`| BOOLEAN | DEFAULT 0 | Si afecta a su entorno familiar. |
| `impacto_personal`| BOOLEAN | DEFAULT 0 | Si afecta de manera personal/psicológica. |
| `diagnostico` | TEXT | - | Diagnóstico presuntivo o definido. |
| `observaciones` | TEXT | - | Observaciones finales. |
