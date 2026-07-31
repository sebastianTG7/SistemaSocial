# Diccionario de Datos - Sistema Social

A continuacion se presenta el diccionario de datos exacto de la base de datos del Sistema Social, reflejando fielmente la estructura fisica SQL de la base de datos.

---

## Relaciones entre Entidades

Las siguientes relaciones describen como se vinculan las tablas entre si dentro del sistema:

### Tablas de Catalogo (Maestras)

- cat_facultades (1:N) cat_escuelas - Una facultad puede tener muchas escuelas profesionales.
- cat_escuelas (N:1) cat_facultades - Cada escuela pertenece a una unica facultad.

### Entidades Principales

- personas (N:1) cat_tipos_usuario - Cada persona tiene un unico tipo de usuario (Estudiante, Docente, etc.).
- personas (N:1) cat_facultades - Cada persona pertenece a una unica facultad.
- personas (N:1) cat_escuelas - Cada persona pertenece a una unica escuela profesional.
- personas (N:1) cat_modalidades - Cada persona tiene una unica modalidad de ingreso.
- personas (1:N) tenciones - Una persona puede tener multiples atenciones registradas a lo largo del tiempo.
- tenciones (N:1) cat_casos_sociales - Cada atencion esta clasificada bajo un unico caso social.

### Fichas Especializadas

- personas (1:1) ichas_socioeconomicas - Cada persona puede tener a lo sumo una ficha socioeconomica. Se actualiza periodicamente; no se crea una por cada atencion.
- tenciones (1:1) ichas_derivacion - Cada atencion puede tener a lo sumo una ficha de derivacion. Es exclusiva de cada atencion individual, a diferencia de la ficha socioeconomica.

---

## Diccionario de Datos

### 1. Tablas de Catalogo (Maestras)

#### Tabla: cat_tipos_usuario
Define los tipos de usuario (ej. Estudiante, Docente, Administrativo).

| Campo | Tipo SQL | Restriccion | Descripcion |
| :--- | :--- | :--- | :--- |
| id | INT | PK, INDEX | Identificador unico del tipo de usuario. |
| 
ombre | VARCHAR(50) | NOT NULL, UNIQUE | Nombre del tipo de usuario. |
| ctivo | BOOLEAN | DEFAULT 1 | Indica si el registro esta activo. |

#### Tabla: cat_facultades
Catalogo de facultades de la institucion.

| Campo | Tipo SQL | Restriccion | Descripcion |
| :--- | :--- | :--- | :--- |
| id | INT | PK, INDEX | Identificador unico de la facultad. |
| 
ombre | VARCHAR(100) | NOT NULL, UNIQUE | Nombre de la facultad. |
| ctivo | BOOLEAN | DEFAULT 1 | Indica si el registro esta activo. |

#### Tabla: cat_escuelas
Catalogo de escuelas profesionales. Cada escuela depende de una facultad.

| Campo | Tipo SQL | Restriccion | Descripcion |
| :--- | :--- | :--- | :--- |
| id | INT | PK, INDEX | Identificador unico de la escuela. |
| 
ombre | VARCHAR(100) | NOT NULL | Nombre de la escuela. |
| acultad_id | INT | FK | Referencia a cat_facultades.id. |
| ctivo | BOOLEAN | DEFAULT 1 | Indica si el registro esta activo. |

#### Tabla: cat_casos_sociales
Tipos de casos sociales que clasifican cada atencion (Orientacion, Evaluacion, Derivacion, etc.).

| Campo | Tipo SQL | Restriccion | Descripcion |
| :--- | :--- | :--- | :--- |
| id | INT | PK, INDEX | Identificador unico del caso social. |
| 
ombre | VARCHAR(50) | NOT NULL, UNIQUE | Nombre del caso social. |
| ctivo | BOOLEAN | DEFAULT 1 | Indica si el registro esta activo. |

#### Tabla: cat_modalidades
Modalidades de ingreso a la institucion (General, CEPREVAL, Discapacidad, etc.).

| Campo | Tipo SQL | Restriccion | Descripcion |
| :--- | :--- | :--- | :--- |
| id | INT | PK, INDEX | Identificador unico de la modalidad. |
| 
ombre | VARCHAR(50) | NOT NULL, UNIQUE | Nombre de la modalidad de ingreso. |
| ctivo | BOOLEAN | DEFAULT 1 | Indica si el registro esta activo. |

---

### 2. Entidades Principales

#### Tabla: usuarios
Credenciales de acceso para el personal del sistema (operadores y administradores).

| Campo | Tipo SQL | Restriccion | Descripcion |
| :--- | :--- | :--- | :--- |
| id | INT | PK, INDEX | Identificador unico del usuario del sistema. |
| username | VARCHAR(50) | NOT NULL, UNIQUE, INDEX | Nombre de usuario para el login. |
| password_hash | VARCHAR(255) | NOT NULL | Contrasena almacenada de forma encriptada. |
| 
ombre_completo | VARCHAR(200) | - | Nombres y apellidos completos del personal. |
| 
ol | VARCHAR(20) | DEFAULT operador | Rol del usuario: administrador u operador. |
| ctivo | BOOLEAN | DEFAULT 1 | Indica si la cuenta esta activa. |

#### Tabla: personas
Registro central y permanente de datos de los individuos atendidos (beneficiarios). Un mismo registro de persona se reutiliza en todas sus atenciones.

| Campo | Tipo SQL | Restriccion | Descripcion |
| :--- | :--- | :--- | :--- |
| id | INT | PK, INDEX | Identificador unico de la persona. |
| dni | VARCHAR(20) | NOT NULL, UNIQUE, INDEX | DNI de la persona. Clave natural de identificacion. |
| 
ombres | VARCHAR(100) | NOT NULL | Nombres de la persona. |
| pellidos | VARCHAR(100) | NOT NULL | Apellidos de la persona. |
| echa_nacimiento | DATE | - | Fecha de nacimiento. |
| edad | INT | - | Edad de la persona. |
| sexo | VARCHAR(1) | - | Sexo: F (Femenino) o M (Masculino). |
| codigo_estudiante | VARCHAR(20) | - | Codigo universitario (si aplica). |
| nio_estudio | VARCHAR(10) | - | Anio o ciclo de estudio actual. |
| 	ipo_usuario_id | INT | FK | Referencia a cat_tipos_usuario.id. |
| acultad_id | INT | FK | Referencia a cat_facultades.id. |
| escuela_id | INT | FK | Referencia a cat_escuelas.id. |
| modalidad_id | INT | FK | Referencia a cat_modalidades.id. |
| 
egistro_modalidad | VARCHAR(100) | - | Detalle o codigo asociado a la modalidad de ingreso. |
| celular | VARCHAR(20) | - | Numero de celular. |
| correo | VARCHAR(100) | - | Correo electronico. |
| direccion | VARCHAR(200) | - | Direccion domiciliaria. |
| ctivo | BOOLEAN | DEFAULT 1 | Estado logico del registro. |
| echa_registro | DATETIME | DEFAULT | Fecha en la que el registro fue creado en el sistema. |

#### Tabla: tenciones
Historial de eventos de atencion. Cada fila representa una visita o contacto de una persona con el servicio social. Una persona puede tener multiples atenciones.

| Campo | Tipo SQL | Restriccion | Descripcion |
| :--- | :--- | :--- | :--- |
| id | INT | PK, INDEX | Identificador unico de la atencion. |
| persona_id | INT | FK, NOT NULL | Referencia a personas.id. No es UNIQUE (permite multiples atenciones por persona). |
| echa_atencion | DATETIME | NOT NULL, DEFAULT | Fecha y hora del evento de atencion. |
| caso_social_id | INT | FK | Referencia a cat_casos_sociales.id. |
| observaciones | TEXT | - | Anotaciones generales sobre la visita. |
| ctivo | BOOLEAN | DEFAULT 1 | Estado logico del registro. |
| echa_registro | DATETIME | DEFAULT | Fecha de creacion del registro en el sistema. |

---

### 3. Fichas Especializadas

#### Tabla: ichas_socioeconomicas
Recopila el perfil economico, familiar y de vivienda del beneficiario. Relacion 1:1 con personas; existe a lo sumo una ficha por persona. Se actualiza periodicamente y no se crea una nueva por cada atencion.

| Campo | Tipo SQL | Restriccion | Descripcion |
| :--- | :--- | :--- | :--- |
| id | INT | PK, INDEX | Identificador unico de la ficha. |
| persona_id | INT | FK, NOT NULL, UNIQUE | Referencia a personas.id. UNIQUE garantiza maxima una ficha por persona. |
| motivo_evaluacion | VARCHAR(100) | - | Motivo principal de la evaluacion socioeconomica. |
| sisfoh_condicion | VARCHAR(50) | - | Clasificacion segun el SISFOH (No Pobre, Pobre, Pobre Extremo). |
| 	iene_discapacidad | BOOLEAN | DEFAULT 0 | Indica si el beneficiario tiene alguna discapacidad. |
| 	ipo_discapacidad | VARCHAR(50) | - | Tipo de discapacidad. |
| 
ivel_de_discapacidad | VARCHAR(50) | - | Nivel de severidad de la discapacidad. |
| 	ipo_seguro | VARCHAR(50) | - | Tipo de seguro de salud (SIS, EsSalud, etc.). |
| estructura_familiar | VARCHAR(50) | - | Tipo de estructura familiar (Nuclear, Monoparental, Extendida, etc.). |
| dinamica_familiar | VARCHAR(50) | - | Calidad de las relaciones en el hogar (Funcional, Disfuncional, etc.). |
| ingreso_economico_miembros | FLOAT | DEFAULT 0.0 | Suma de ingresos de todos los miembros del hogar. |
| ingreso_becas | FLOAT | DEFAULT 0.0 | Ingresos provenientes de becas. |
| ingreso_otros | FLOAT | DEFAULT 0.0 | Otros ingresos (alquileres, pensiones, envios del exterior, etc.). |
| egreso_agua | FLOAT | DEFAULT 0.0 | Gasto mensual en servicio de agua. |
| egreso_luz | FLOAT | DEFAULT 0.0 | Gasto mensual en servicio de energia electrica. |
| egreso_educacion_pasajes | FLOAT | DEFAULT 0.0 | Gasto mensual en educacion y pasajes. |
| egreso_alimentacion | FLOAT | DEFAULT 0.0 | Gasto mensual en alimentacion. |
| egreso_alquiler | FLOAT | DEFAULT 0.0 | Gasto mensual en alquiler de vivienda. |
| estudiante_trabaja | VARCHAR(50) | - | Situacion laboral del estudiante (Si tiempo completo, Si tiempo parcial, No, Eventualmente). |
| lugar_trabajo | VARCHAR(150) | - | Lugar de trabajo del estudiante (opcional). |
| 
emuneracion_estudiante | FLOAT | DEFAULT 0.0 | Remuneracion mensual si el estudiante trabaja. |
| 	ipo_vivienda | VARCHAR(50) | - | Condicion de tenencia de la vivienda (Propia, Alquilada, etc.). |
| material_paredes | VARCHAR(50) | - | Material principal de construccion de las paredes. |
| material_techo | VARCHAR(50) | - | Material principal de construccion del techo. |
| 	iene_agua_red | BOOLEAN | DEFAULT 0 | Acceso a agua por red publica. |
| 	iene_desague_red | BOOLEAN | DEFAULT 0 | Acceso a desaguee por red publica. |
| 	iene_energia_electrica | BOOLEAN | DEFAULT 0 | Acceso a energia electrica. |

#### Tabla: ichas_derivacion
Registra los detalles de un proceso de derivacion a otra area especializada. Relacion 1:1 con atenciones. Es propia de cada evento de atencion individual.

| Campo | Tipo SQL | Restriccion | Descripcion |
| :--- | :--- | :--- | :--- |
| id | INT | PK, INDEX | Identificador unico de la ficha de derivacion. |
| tencion_id | INT | FK, NOT NULL, UNIQUE | Referencia a atenciones.id. UNIQUE garantiza maxima una ficha por atencion. |
| lugar_nacimiento | VARCHAR(100) | - | Lugar de nacimiento del beneficiario. |
| ocupacion | VARCHAR(100) | - | Ocupacion laboral o academica. |
| ive_con | VARCHAR(100) | - | Personas con las que convive el beneficiario. |
| 	elefono_familiares | VARCHAR(50) | - | Telefono de contacto familiar o de emergencia. |
| rea_deriva | VARCHAR(100) | - | Area desde donde se origina la derivacion. |
| rea_derivada | VARCHAR(100) | - | Area destino a la que se deriva al beneficiario. |
| echa_derivacion | DATETIME | DEFAULT | Fecha y hora en que se realiza la derivacion. |
| motivo_consulta | TEXT | - | Descripcion del motivo de la consulta y derivacion. |
| 	iene_derivaciones_previas | BOOLEAN | DEFAULT 0 | Indica si el beneficiario tuvo derivaciones anteriores. |
| detalle_derivaciones_previas | TEXT | - | Detalle narrativo de derivaciones anteriores. |
| condicion | VARCHAR(50) | - | Nivel de condicion del caso (Leve, Moderado, Grave). |
| impacto_academico | BOOLEAN | DEFAULT 0 | Afecta el rendimiento academico. |
| impacto_social | BOOLEAN | DEFAULT 0 | Afecta sus relaciones sociales. |
| impacto_familiar | BOOLEAN | DEFAULT 0 | Afecta su entorno familiar. |
| impacto_personal | BOOLEAN | DEFAULT 0 | Afecta de manera personal o psicologica. |
| diagnostico | TEXT | - | Diagnostico presuntivo o definido del caso. |
| observaciones | TEXT | - | Observaciones y notas finales del evaluador. |
