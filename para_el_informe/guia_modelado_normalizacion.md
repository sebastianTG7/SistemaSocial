# Guía de Modelado y Normalización de la Base de Datos
## Sistema de Gestión Social

Este documento contiene la especificación formal del modelo lógico, físico y el análisis de normalización de la base de datos relacional para el **Sistema de Gestión Social**, listo para su incorporación en el informe técnico o tesis.

---

### 1. Modelo Lógico (Esquema Relacional)

La base de datos utiliza una arquitectura de **Base de Datos Relacional (RDBMS)** basada en **SQLite 3**. El diseño está estructurado con un conjunto de **Tablas Maestras (Catálogos)** para garantizar la consistencia de los datos, las cuales alimentan a una **Tabla Operativa Principal (`personas`)** que funciona como bitácora de atenciones.

#### Entidades y Relaciones principales:
*   **`cat_tipos_usuario`**: Almacena las clasificaciones de las personas atendidas (ej. Estudiante, Docente, Administrativo, Externo).
*   **`cat_facultades`**: Listado de facultades académicas de la institución.
*   **`cat_escuelas`**: Escuelas profesionales asociadas a cada facultad mediante una relación de uno a muchos ($1:N$).
*   **`cat_casos_sociales`**: Tipos o categorías de asistencia social requeridos (ej. Salud, Económico, Alimentario, Familiar).
*   **`usuarios`**: Administradores y operadores con acceso credencializado al sistema.
*   **`personas`**: Entidad principal donde se registran las atenciones. Se comporta como una **bitácora histórica** permitiendo múltiples registros de DNI para documentar atenciones subsecuentes a un mismo usuario.

---

### 2. Modelo Físico (Diccionario de Datos)

A continuación, se detalla la estructura física de la base de datos con sus respectivos tipos de datos, restricciones y propósitos en el sistema SQLite.

#### 2.1 Tabla Principal: `personas` (Bitácora de Atenciones)
| Nombre del Campo | Tipo de Dato | Restricciones / Atributos | Descripción |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Identificador único y autoincremental de la atención. |
| `dni` | VARCHAR(20) | INDEX, NOT NULL | Documento Nacional de Identidad de la persona atendida. |
| `nombres` | VARCHAR(100) | NOT NULL | Nombres completos de la persona. |
| `apellidos` | VARCHAR(100) | NOT NULL | Apellidos paterno y materno. |
| `edad` | INTEGER | | Edad cronológica al momento de la atención. |
| `sexo` | VARCHAR(1) | | Sexo biológico ('M' para Masculino, 'F' para Femenino). |
| `fecha_atencion` | DATETIME | NOT NULL, DEFAULT `CURRENT_TIMESTAMP` | Fecha y hora en que se realizó la atención. |
| `codigo_estudiante` | VARCHAR(20) | | Código universitario (opcional, aplicable a estudiantes). |
| `año_estudio` | VARCHAR(10) | | Ciclo, año o semestre académico del estudiante. |
| `tipo_usuario_id` | INTEGER | FOREIGN KEY (`cat_tipos_usuario.id`) | Tipo de usuario (estudiante, docente, etc.). |
| `facultad_id` | INTEGER | FOREIGN KEY (`cat_facultades.id`) | Facultad a la que pertenece (si aplica). |
| `escuela_id` | INTEGER | FOREIGN KEY (`cat_escuelas.id`) | Escuela profesional a la que pertenece (si aplica). |
| `caso_social_id` | INTEGER | FOREIGN KEY (`cat_casos_sociales.id`) | Categoría del caso social atendido. |
| `celular` | VARCHAR(20) | | Número telefónico de contacto. |
| `correo` | VARCHAR(100) | | Dirección de correo electrónico. |
| `direccion` | VARCHAR(200) | | Dirección domiciliaria actual. |
| `observaciones` | TEXT | | Anotaciones, diagnósticos o notas detalladas del caso. |
| `activo` | BOOLEAN | DEFAULT `True` | Control para baja lógica (eliminación virtual). |
| `fecha_registro` | DATETIME | DEFAULT `CURRENT_TIMESTAMP` | Sello de tiempo automático de registro en el sistema. |

#### 2.2 Tabla de Catálogo: `cat_escuelas`
| Nombre del Campo | Tipo de Dato | Restricciones / Atributos | Descripción |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Identificador único del catálogo. |
| `nombre` | VARCHAR(100) | NOT NULL | Nombre de la escuela académica profesional. |
| `facultad_id` | INTEGER | FOREIGN KEY (`cat_facultades.id`) | Relación de pertenencia a una facultad maestra. |
| `activo` | BOOLEAN | DEFAULT `True` | Estado del registro en el catálogo (activo/inactivo). |

#### 2.3 Tabla de Seguridad: `usuarios`
| Nombre del Campo | Tipo de Dato | Restricciones / Atributos | Descripción |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Identificador único del usuario de sistema. |
| `username` | VARCHAR(50) | UNIQUE, INDEX, NOT NULL | Nombre de usuario para el inicio de sesión. |
| `password_hash` | VARCHAR(255) | NOT NULL | Contraseña encriptada para máxima seguridad. |
| `nombre_completo` | VARCHAR(200) | | Nombre y apellido del operador. |
| `rol` | VARCHAR(20) | DEFAULT 'operador' | Nivel de permisos ('administrador' o 'operador'). |
| `activo` | BOOLEAN | DEFAULT `True` | Habilitación de la cuenta. |

---

### 3. Sustento de Normalización (Tercera Forma Normal - 3FN)

El diseño de esta base de datos cumple rigurosamente con las **Formas Normales (FN)** clásicas de la teoría de bases de datos relacionales, lo que garantiza un almacenamiento óptimo y elimina anomalías de inserción, actualización y borrado:

#### 3.1 Primera Forma Normal (1FN) - Atomicidad de los Datos
*   **Regla:** Todos los valores almacenados en las columnas deben ser atómicos (indivisibles) y no deben existir filas o columnas repetitivas.
*   **Sustento:** Cada celda contiene un único valor. Por ejemplo, en lugar de guardar datos de contacto en una sola cadena, se dividen estructuralmente en `celular`, `correo` y `direccion`. De igual forma, los nombres y apellidos se registran por separado.

#### 3.2 Segunda Forma Normal (2FN) - Dependencia Funcional Completa
*   **Regla:** Cumplir con la 1FN y que todos los atributos que no forman parte de la clave primaria tengan una dependencia funcional completa respecto a ella.
*   **Sustento:** En la tabla `personas`, la clave primaria es `id` (número único de atención). Atributos como `observaciones`, `edad` o `fecha_atencion` no dependen de sub-claves intermedias; pertenecen exclusiva y enteramente a ese registro de atención particular.

#### 3.3 Tercera Forma Normal (3FN) - Eliminación de Dependencias Transitivas
*   **Regla:** Cumplir con la 2FN y asegurar que ninguna columna que no sea clave dependa transitivamente de otra columna no clave.
*   **Sustento:** Este es el punto fuerte del modelo. En lugar de almacenar directamente los nombres de las facultades o los tipos de casos sociales en la tabla de atenciones (lo cual causaría duplicaciones y problemas si una facultad cambia de nombre), se guardan únicamente llaves foráneas (`facultad_id`, `caso_social_id`) apuntando a sus respectivos catálogos. 
    Así, la descripción de la facultad depende únicamente del ID en la tabla `cat_facultades`, y no transita de forma redundante dentro de la tabla de personas.
