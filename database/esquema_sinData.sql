CREATE TABLE cat_tipos_usuario (
	id INTEGER NOT NULL, 
	nombre VARCHAR(50) NOT NULL, 
	activo BOOLEAN, 
	PRIMARY KEY (id), 
	UNIQUE (nombre)
);

CREATE INDEX ix_cat_tipos_usuario_id ON cat_tipos_usuario (id);

CREATE TABLE cat_facultades (
	id INTEGER NOT NULL, 
	nombre VARCHAR(100) NOT NULL, 
	activo BOOLEAN, 
	PRIMARY KEY (id), 
	UNIQUE (nombre)
);

CREATE INDEX ix_cat_facultades_id ON cat_facultades (id);

CREATE TABLE cat_casos_sociales (
	id INTEGER NOT NULL, 
	nombre VARCHAR(50) NOT NULL, 
	activo BOOLEAN, 
	PRIMARY KEY (id), 
	UNIQUE (nombre)
);

CREATE INDEX ix_cat_casos_sociales_id ON cat_casos_sociales (id);

CREATE TABLE usuarios (
	id INTEGER NOT NULL, 
	username VARCHAR(50) NOT NULL, 
	password_hash VARCHAR(255) NOT NULL, 
	nombre_completo VARCHAR(200), 
	rol VARCHAR(20), 
	activo BOOLEAN, 
	PRIMARY KEY (id)
);

CREATE UNIQUE INDEX ix_usuarios_username ON usuarios (username);

CREATE INDEX ix_usuarios_id ON usuarios (id);

CREATE TABLE cat_escuelas (
	id INTEGER NOT NULL, 
	nombre VARCHAR(100) NOT NULL, 
	facultad_id INTEGER, 
	activo BOOLEAN, 
	PRIMARY KEY (id), 
	FOREIGN KEY(facultad_id) REFERENCES cat_facultades (id)
);

CREATE INDEX ix_cat_escuelas_id ON cat_escuelas (id);

CREATE TABLE cat_modalidades (
        id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
        nombre VARCHAR(50) NOT NULL UNIQUE,
        activo BOOLEAN DEFAULT 1
    );



CREATE TABLE fichas_derivacion (
	id INTEGER NOT NULL, 
	atencion_id INTEGER NOT NULL, 
	lugar_nacimiento VARCHAR(100), 
	ocupacion VARCHAR(100), 
	vive_con VARCHAR(100), 
	telefono_familiares VARCHAR(50), 
	area_deriva VARCHAR(100), 
	area_derivada VARCHAR(100), 
	fecha_derivacion DATETIME, 
	motivo_consulta TEXT, 
	tiene_derivaciones_previas BOOLEAN, 
	detalle_derivaciones_previas TEXT, 
	condicion VARCHAR(50), 
	impacto_academico BOOLEAN, 
	impacto_social BOOLEAN, 
	impacto_familiar BOOLEAN, 
	impacto_personal BOOLEAN, 
	diagnostico TEXT, 
	observaciones TEXT, 
	PRIMARY KEY (id), 
	UNIQUE (atencion_id), 
	FOREIGN KEY(atencion_id) REFERENCES atenciones (id)
);

CREATE INDEX ix_fichas_derivacion_id ON fichas_derivacion (id);

CREATE TABLE personas (
	id INTEGER NOT NULL, 
	dni VARCHAR(20) NOT NULL, 
	nombres VARCHAR(100) NOT NULL, 
	apellidos VARCHAR(100) NOT NULL, 
	fecha_nacimiento DATE, 
	edad INTEGER, 
	sexo VARCHAR(1), 
	codigo_estudiante VARCHAR(20), 
	"año_estudio" VARCHAR(10), 
	tipo_usuario_id INTEGER, 
	facultad_id INTEGER, 
	escuela_id INTEGER, 
	modalidad_id INTEGER, 
	registro_modalidad VARCHAR(100), 
	celular VARCHAR(20), 
	correo VARCHAR(100), 
	direccion VARCHAR(200), 
	activo BOOLEAN, 
	fecha_registro DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(tipo_usuario_id) REFERENCES cat_tipos_usuario (id), 
	FOREIGN KEY(facultad_id) REFERENCES cat_facultades (id), 
	FOREIGN KEY(escuela_id) REFERENCES cat_escuelas (id), 
	FOREIGN KEY(modalidad_id) REFERENCES cat_modalidades (id)
);

CREATE UNIQUE INDEX ix_personas_dni ON personas (dni);

CREATE INDEX ix_personas_id ON personas (id);

CREATE TABLE atenciones (
	id INTEGER NOT NULL, 
	persona_id INTEGER NOT NULL, 
	fecha_atencion DATETIME NOT NULL, 
	caso_social_id INTEGER, 
	observaciones TEXT, 
	activo BOOLEAN, 
	fecha_registro DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(persona_id) REFERENCES personas (id), 
	FOREIGN KEY(caso_social_id) REFERENCES cat_casos_sociales (id)
);

CREATE INDEX ix_atenciones_id ON atenciones (id);

CREATE TABLE fichas_socioeconomicas (
	id INTEGER NOT NULL, 
	persona_id INTEGER NOT NULL, 
	motivo_evaluacion VARCHAR(100), 
	sisfoh_condicion VARCHAR(50), 
	tiene_discapacidad BOOLEAN, 
	tipo_discapacidad VARCHAR(50), 
	nivel_de_discapacidad VARCHAR(50), 
	tipo_seguro VARCHAR(50), 
	estructura_familiar VARCHAR(50), 
	dinamica_familiar VARCHAR(50), 
	ingreso_economico_miembros FLOAT, 
	ingreso_becas FLOAT, 
	ingreso_otros FLOAT, 
	egreso_agua FLOAT, 
	egreso_luz FLOAT, 
	egreso_educacion_pasajes FLOAT, 
	egreso_alimentacion FLOAT, 
	egreso_alquiler FLOAT, 
	estudiante_trabaja VARCHAR(50), 
	lugar_trabajo VARCHAR(150), 
	remuneracion_estudiante FLOAT, 
	tipo_vivienda VARCHAR(50), 
	material_paredes VARCHAR(50), 
	material_techo VARCHAR(50), 
	tiene_agua_red BOOLEAN, 
	tiene_desague_red BOOLEAN, 
	tiene_energia_electrica BOOLEAN, 
	PRIMARY KEY (id), 
	UNIQUE (persona_id), 
	FOREIGN KEY(persona_id) REFERENCES personas (id)
);

CREATE INDEX ix_fichas_socioeconomicas_id ON fichas_socioeconomicas (id);

