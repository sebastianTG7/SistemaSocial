2. Consulta de Base de Datos: ¿SQLite o migrar a MySQL / Postgres / MongoDB?
📊 Mi recomendación definitiva: Quédate en SQLite
Para el tipo de aplicación que estás construyendo (uso personal, ejecutable local, registro individual), SQLite es la mejor base de datos posible. Te explico por qué:

Portabilidad sin dolores de cabeza (Serverless):
Si usas MySQL o PostgreSQL, tendrías que instalar un servidor de base de datos en cada computadora donde lleves tu aplicación. Con SQLite, toda la base de datos vive dentro del archivo servicio_social.db. Si copias tu proyecto en un USB o en la nube, ¡te llevas tus datos contigo al instante!
Rendimiento de sobra:
SQLite es increíblemente rápido. Puede almacenar hasta 281 Terabytes de datos y manejar millones de filas. Para los miles de registros que tú harás en tu gestión social, el archivo apenas pesará unos pocos Megabytes y tus búsquedas se resolverán en milisegundos.
Es una base de datos relacional real:
Usa SQL estándar, tiene llaves primarias, llaves foráneas y soporta integridad referencial. Es tan robusta que es la base de datos por defecto en todos los teléfonos móviles (Android/iOS), navegadores web (Chrome/Firefox) y sistemas de escritorio.
¿Cuándo deberías migrar a Postgres o MySQL?
Únicamente si el día de mañana decides hacer una página web donde 5 o más personas deban registrar datos al mismo tiempo desde diferentes lugares. Mientras seas solo tú en tu aplicación de escritorio, SQLite es el rey indiscutible.

3. Guía de Modelado y Normalización para tu Informe de Tesis
¡Haber iniciado con la base de datos sin un diagrama es normal en el desarrollo ágil! No te preocupes. Tu estructura actual es muy limpia y sigue excelentes prácticas. A continuación, tienes toda la documentación formal de tu base de datos lista para copiar a tu informe técnico o diapositivas.

📐 A. Modelo Lógico (Esquema Relacional)
Tu base de datos está organizada bajo una arquitectura de Tablas Maestras (Catálogos) que nutren a una Tabla Operativa Principal (personas).

NOTE

Detalle clave de diseño: La tabla personas actúa en realidad como una Bitácora de Atenciones. Permite DNI duplicados intencionalmente, lo cual es excelente porque permite registrar a una misma persona en diferentes fechas, manteniendo su historial completo de visitas.

cat_tipos_usuario (Almacena categorías como "Estudiante", "Docente", "Externo").
cat_facultades (Listado de facultades de la universidad).
cat_escuelas (Escuelas profesionales, asociadas a una facultad mediante Llave Foránea).
cat_casos_sociales (Tipos de atención: "Salud", "Ayuda alimentaria", "Familiar", etc.).
usuarios (Credenciales del sistema para el login).
personas (Atenciones registradas).
💻 B. Modelo Físico (Diccionario de Datos)
Aquí tienes el detalle técnico de las tablas principales para tu informe:

1. Tabla Principal: personas (Registro de Atenciones)
Campo	Tipo	Restricción	Descripción
id	INTEGER	Primary Key, Autoincrement	Identificador único de la atención.
dni	VARCHAR(20)	INDEX	DNI de la persona atendida.
nombres	VARCHAR(100)	NOT NULL	Nombres del usuario.
apellidos	VARCHAR(100)	NOT NULL	Apellidos del usuario.
edad	INTEGER		Edad.
sexo	VARCHAR(1)		'M' o 'F'.
fecha_atencion	DATETIME	NOT NULL	Fecha de la atención.
codigo_estudiante	VARCHAR(20)		Código universitario (opcional).
año_estudio	VARCHAR(10)		Ciclo/Año de estudio.
tipo_usuario_id	INTEGER	Foreign Key (cat_tipos_usuario.id)	Tipo de usuario.
facultad_id	INTEGER	Foreign Key (cat_facultades.id)	Facultad.
escuela_id	INTEGER	Foreign Key (cat_escuelas.id)	Escuela Profesional.
caso_social_id	INTEGER	Foreign Key (cat_casos_sociales.id)	Categoría del caso.
celular	VARCHAR(20)		Teléfono de contacto.
correo	VARCHAR(100)		Correo electrónico.
direccion	VARCHAR(200)		Dirección de domicilio.
observaciones	TEXT		Detalles adicionales de la atención.
activo	BOOLEAN	DEFAULT True	Estado de baja lógica del registro.
fecha_registro	DATETIME	DEFAULT Now()	Fecha y hora en que se creó en sistema.
2. Tabla Maestras (Ejemplo: cat_escuelas)
Campo	Tipo	Restricción	Descripción
id	INTEGER	Primary Key, Autoincrement	Identificador único.
nombre	VARCHAR(100)	NOT NULL	Nombre de la escuela.
facultad_id	INTEGER	Foreign Key (cat_facultades.id)	Relación con la facultad.
activo	BOOLEAN	DEFAULT True	Estado del catálogo.
🎓 C. Demostración de Normalización (Tu sustento académico)
En tu informe debes explicar que tu base de datos cumple con las Tres Formas Normales (3FN) para demostrar que es un diseño eficiente y libre de redundancias:

Primera Forma Normal (1FN) - Atomicidad:

Regla: Todos los atributos deben ser atómicos (valores indivisibles) y no deben existir grupos repetitivos.
Sustento: Tu diseño cumple plenamente. Por ejemplo, en lugar de guardar teléfono y correo juntos, tienes columnas separadas (celular, correo). Tampoco hay listas de datos dentro de una celda.
Segunda Forma Normal (2FN) - Dependencia Completa:

Regla: Debe cumplir con 1FN y todas las columnas que no sean llaves primarias deben depender directamente de la clave primaria de la tabla (id).
Sustento: Cumple. Cada fila representa una atención única (personas.id). Campos como edad, observaciones o fecha_atencion dependen por completo de ese registro de atención particular.
Tercera Forma Normal (3FN) - Sin Dependencias Transitivas:

Regla: Debe cumplir con 2FN y no deben existir dependencias transitivas entre campos que no son llaves (las columnas no clave deben depender únicamente de la clave primaria, no de otras columnas).
Sustento: Aquí es donde brilla tu base de datos. En lugar de guardar el texto "Facultad de Ingeniería de Sistemas" o "Salud Mental" en cada celda de la tabla personas (lo cual generaría redundancia excesiva, errores de escritura y pesadez), tu base de datos almacena números identificadores (facultad_id, caso_social_id) apuntando a tablas maestras. Si el día de mañana la Facultad cambia de nombre, solo lo modificas en la tabla cat_facultades una sola vez, y automáticamente se actualiza en todas las atenciones sin alterar la integridad de tus datos.