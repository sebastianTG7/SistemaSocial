# Proceso de Normalización de la Base de Datos

En este documento se explica paso a paso cómo se organizó la base de datos del Sistema Social. El objetivo de la "Normalización" es aplicar una serie de reglas para evitar que los datos se repitan innecesariamente, asegurar que no haya errores al actualizar información y evitar tablas llenas de espacios vacíos.

A continuación, veremos la evolución desde un diseño desordenado (como un Excel) hasta llegar a la estructura óptima que tenemos hoy (Tercera Forma Normal).

---

## 1. Estado Inicial (Fase Cero o Tabla Plana)

Al principio, es común imaginar el sistema como una gran hoja de cálculo de Excel donde anotamos todo en una sola fila. A esto se le llama **Tabla Plana**.

**Ejemplo de cómo se veía la tabla `Registro_Atencion` al inicio:**

| DNI | Nombres | Facultad | Casos Sociales | Ficha_Ingreso_Familiar | Derivacion_Diagnostico |
|-----|---------|----------|----------------|------------------------|------------------------|
| 123 | Juan P. | Ingeniería | Orientación, Evaluación | 1500.00 | Ansiedad |
| 456 | Maria L.| Ingeniería | Seguimiento | *(Vacío / NULL)* | *(Vacío / NULL)* |
| 789 | Luis A. | Derecho | Orientación | *(Vacío / NULL)* | *(Vacío / NULL)* |

**¿Cuál era el problema aquí?**
1. **Redundancia (Repetición):** Si 500 alumnos son de "Ingeniería", la palabra se escribe 500 veces. Si luego la facultad cambia de nombre, hay que buscar y corregir 500 filas.
2. **Campos Combinados:** Juan P. vino por "Orientación" y "Evaluación" a la vez, todo metido en una sola celda.
3. **Muchos campos vacíos (NULL):** María y Luis solo vinieron a conversar (Orientación/Seguimiento), no necesitaron evaluación económica ni psicológica. Sin embargo, esas columnas existen y se quedan vacías, desperdiciando espacio y desordenando la base de datos.

---

## 2. Primera Forma Normal (1FN)

**¿Qué dice la regla (en palabras sencillas)?**
*Cada celda debe tener un solo valor (no podemos tener listas separadas por comas en una celda). Además, cada fila debe tener un identificador único (Llave Primaria o PK).*

**Lo que hicimos en nuestro sistema:**
- Separamos los casos de Juan P. en dos filas distintas.
- En lugar de usar el DNI como identificador único (lo cual no dejaría a Juan registrarse más de una vez en su vida), creamos un **`ID` autoincrementable**. 
- Al hacer esto, nuestra tabla dejó de ser un "registro de personas" y se convirtió en una **"Bitácora de Atenciones"** (cada fila es una visita al consultorio).

**Ejemplo de la tabla en 1FN:**

| ID (PK) | DNI | Nombres | Facultad | Caso Social | Ficha_Ingreso_Familiar | Derivacion_Diagnostico |
|---|-----|---------|----------|-------------|------------------------|------------------------|
| 1 | 123 | Juan P. | Ingeniería | Orientación | 1500.00 | Ansiedad |
| 2 | 123 | Juan P. | Ingeniería | Evaluación | 1500.00 | Ansiedad |
| 3 | 456 | Maria L.| Ingeniería | Seguimiento | *(Vacío)* | *(Vacío)* |

*(Notar que el DNI 123 se repite, porque Juan vino dos veces, cada visita tiene su propio ID).*

---

## 3. Segunda Forma Normal (2FN)

**¿Qué dice la regla (en palabras sencillas)?**
*Si tienes una tabla, todos los datos deben depender directamente del identificador principal (ID). Si hay datos que se repiten porque dependen de otra cosa (como el nombre de la facultad), debes sacarlos a su propia tabla.*

**Lo que hicimos en nuestro sistema:**
- La palabra "Ingeniería" no depende de la visita de Juan, es un dato fijo de la universidad. 
- Creamos **Tablas de Catálogo (Maestras)** para Facultades, Escuelas, Casos Sociales, etc.
- En nuestra tabla principal, en lugar de escribir "Ingeniería", ponemos un número (Llave Foránea o FK) que apunta al catálogo.

**Ejemplo de cómo quedó en 2FN:**

*Tabla: `CatFacultad` (El Catálogo)*
| ID (PK) | Nombre_Facultad |
|---|---|
| 1 | Ingeniería |
| 2 | Derecho |

*Tabla principal `Persona` (La Bitácora):*
| ID (PK)| DNI | Nombres | facultad_id (FK) | caso_social_id (FK)| Ficha_Ingreso | Derivacion_Diag |
|---|---|---|---|---|---|---|
| 1 | 123 | Juan P. | 1 *(Apunta a Ing)* | 1 *(Apunta a Orient.)* | 1500.00 | Ansiedad |

*¡Ahora ya no repetimos texto, solo números!*

---

## 4. Tercera Forma Normal (3FN)

**¿Qué dice la regla (en palabras sencillas)?**
*Si hay columnas que dependen de otra columna que NO es la llave primaria, debes separarlas. En nuestro caso, evitar tener campos de otras evaluaciones mezclados en la atención general.*

**Lo que hicimos en nuestro sistema:**
- Los campos `Ficha_Ingreso` y `Derivacion_Diag` no son propios de "anotar que alguien vino a la oficina". Dependen de si se le hizo una Ficha Socioeconómica o una Ficha de Derivación.
- Para evitar tener campos vacíos cuando un estudiante no requiere esas fichas (como María o Luis), **sacamos esos campos a sus propias tablas**.
- Relacionamos estas nuevas tablas de forma **1 a 1** (Una atención tiene máximo una ficha).

**Ejemplo final de nuestro sistema en 3FN (Base de Datos Consolidada Actual):**

*Tabla principal: `Persona` (Limpia, sin campos vacíos extraños)*
| ID (PK)| DNI | Nombres | facultad_id (FK)|
|---|---|---|---|
| 1 | 123 | Juan P. | 1 |
| 3 | 456 | Maria L.| 1 |

*Tabla: `FichaSocioeconomica` (Solo se crea si se necesita)*
| ID (PK)| persona_id (FK) | Ingreso_Familiar | Tipo_Vivienda |
|---|---|---|---|
| 1 | 1 *(Apunta a Juan)* | 1500.00 | Material Noble |

*Tabla: `FichaDerivacion` (Solo se crea si se necesita)*
| ID (PK)| persona_id (FK) | Diagnostico |
|---|---|---|
| 1 | 1 *(Apunta a Juan)* | Ansiedad |

---

## 5. Explicación extra: ¿Por qué no usamos una relación "Muchos a Muchos"?

En el diseño de bases de datos, cuando "A tiene muchos B" y "B tiene muchos A", se genera una relación "Muchos a Muchos" (N:M). Para solucionarlo, las reglas obligan a crear una tercera tabla intermedia engorrosa.

En la vida real: *"Juan (persona) puede tener muchos problemas sociales con el tiempo, y un problema (ej. Orientación) lo sufren muchas personas".*

**Nuestra solución de diseño:**
Como vimos en la 1FN, nosotros NO guardamos a "Juan" como una sola fila inamovible (usando su DNI como ID). Nosotros usamos la tabla principal como una **Bitácora**. 
Cada vez que Juan viene, creamos una **nueva visita (nueva fila, nuevo ID)**. 
En **esa visita específica**, a Juan solo se le atiende por **un solo caso social**. 

De esta manera, evitamos crear complejas tablas intermedias. Convertimos el problema en una relación limpia de **Uno a Muchos (1:N)**: El catálogo de Casos Sociales reparte sus casos a múltiples "Visitas" registradas en la tabla Persona.
