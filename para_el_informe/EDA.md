## 4.3. Análisis Exploratorio de Datos y Arquitectura del Sistema

Esta sección detalla la transición desde el análisis y diagnóstico de la información histórica (gestionada físicamente y en hojas de cálculo por la Oficina de Servicio Social), hasta la definición de la arquitectura y las tecnologías de software seleccionadas para la construcción del nuevo sistema de información.

### 4.3.1. Análisis Exploratorio y Preparación de Datos (EDA)

Como fase fundamental y previa al diseño arquitectónico del sistema, se llevó a cabo un Análisis Exploratorio de Datos (EDA) sobre el repositorio de información histórica de la oficina. El objetivo fue diagnosticar exhaustivamente el estado de los registros y determinar las estrategias de limpieza y transformación necesarias para migrar esta información hacia un modelo estructurado y relacional.

#### 4.3.1.1. Origen y descripción del dataset original
El repositorio de datos original con el que operaba la oficina constaba de un total aproximado de 200 registros de atenciones a estudiantes. Durante la recolección de requerimientos, se identificó que esta información presentaba un alto grado de dispersión, ya que se encontraba almacenada en dos formatos principales:
*   **Archivos físicos (Papeles):** Un volumen significativo de expedientes, fichas socioeconómicas y registros de derivación se encontraban archivados físicamente. Esta dependencia del papel dificultaba el acceso rápido a la información histórica, el seguimiento de casos recurrentes y el cruce estadístico para la elaboración de reportes mensuales.
*   **Hoja de cálculo (Excel):** La información que había logrado ser digitalizada residía en un archivo Excel consolidado de forma empírica. Este archivo presentaba una estructura completamente plana, donde todos los datos personales (DNI, nombres), académicos (facultad, escuela) y de atención socioeconómica (tipo de caso) convivían en una única tabla matriz, careciendo por completo de llaves primarias, foráneas o reglas de integridad referencial.
    > `[📸 AQUI PUEDES AGREGAR: Una fotografía de un expediente físico censurado/difuminado, al lado de una captura del Excel plano original para contrastar la precariedad del manejo manual vs digital básico].`

#### 4.3.1.2. Identificación de anomalías y calidad de datos
Al someter la hoja de cálculo a un escrutinio analítico y estadístico básico, se evidenciaron deficiencias estructurales críticas que imposibilitaban la escalabilidad y fiabilidad de la información para la toma de decisiones:
*   **Valores Nulos (Missing Data):** Se cuantificó una pérdida significativa de trazabilidad en identificadores clave. De los 200 registros consolidados, cerca de 50 carecían del Documento Nacional de Identidad (DNI) y aproximadamente 60 no contaban con el Código Universitario. Asimismo, 30 expedientes omitían el número de teléfono celular, limitando drásticamente la capacidad de la oficina para realizar acciones de seguimiento.
*   **Redundancia y falta de normalización:** El uso de una tabla plana forzó la digitación manual y repetitiva de variables categóricas. Esto generó una alta inconsistencia tipográfica (por ejemplo, el registro de una facultad podía figurar simultáneamente como "Ingeniería de Sistemas", "Ing. Sistemas" o "Sistemas"), lo que invalida cualquier intento de agrupación o filtrado estadístico automatizado.
*   **Duplicidad y mezcla de entidades:** Al no existir una separación lógica entre la entidad "Estudiante" y la entidad "Atención", el registro de un estudiante recurrente provocaba la sobrescritura de sus datos de contacto anteriores, o bien, la clonación innecesaria de toda su información personal en una nueva fila, inflando el tamaño del archivo y distorsionando el conteo real de personas únicas atendidas.
    > `[📸 AQUI PUEDES AGREGAR: Un gráfico de barras generado a partir de tu EDA que muestre visualmente la tasa de datos faltantes (DNI, Código, Celular) sobre el total de 200 registros].`

#### 4.3.1.3. Transformación, Limpieza y Justificación del Diseño (Data Cleaning)
Los hallazgos del diagnóstico exploratorio evidenciaron que mantener una estructura de datos plana, dispersa y no estandarizada era insostenible. Por consiguiente, se determinó que la construcción del nuevo sistema no solo requería una interfaz de usuario para agilizar el registro, sino obligatoriamente **la migración de los datos hacia una Base de Datos Relacional normalizada**.

Para garantizar que los registros históricos (tanto en papel como en Excel) pudieran ser importados al nuevo sistema sin corromper la integridad de la base de datos, se aplicó un proceso de *Data Cleaning* sobre el archivo original:
1.  **Tratamiento de valores nulos:** Se establecieron reglas de negocio transitorias para los campos obligatorios faltantes detectados en el EDA. Por ejemplo, a los registros sin DNI o Código se les asignaron valores de control, y el diseño de la base de datos se flexibilizó temporalmente para no perder la evidencia de la atención social histórica.
2.  **Extracción de diccionarios (Catálogos):** Se identificaron los valores únicos de las variables categóricas redundantes (facultades, escuelas, modalidades de ingreso y tipos de casos sociales). Estos valores fueron limpiados, unificados y abstraídos para conformar las tablas de catálogos independientes (Tablas maestras) en el nuevo modelo lógico.
3.  **Desacoplamiento de entidades:** Se dividió lógicamente el dataset original, separando de manera definitiva la información demográfica permanente (Persona) de los eventos transaccionales temporales (Atenciones, Fichas Socioeconómicas, Derivaciones).

Esta ardua fase de preparación y entendimiento de los datos sirvió como puente directo y justificación técnica para el diseño de la base de datos relacional (SQLite), el desarrollo del backend en Python y la construcción de los formularios de validación en la arquitectura del sistema que se detallan a continuación.

---

### 4.3.2. Arquitectura del sistema de gestión
*(Aquí insertas tu texto de Arquitectura original)*

### 4.3.3. Frontend
*(Aquí insertas tu texto original sobre Frontend, haciendo notar que la interfaz ahora exige y valida los campos para no repetir los errores del Excel)*

### 4.3.4. Backend
*(Aquí insertas tu texto original sobre Backend, explicando cómo Python maneja la lógica)*

### 4.3.5. Base de Datos
*(Aquí insertas tu texto original sobre SQLite, enfatizando que el modelo relacional implementado soluciona definitivamente la redundancia y duplicidad demostrada en el EDA)*
