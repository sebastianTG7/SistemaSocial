# Análisis Exploratorio de Datos (EDA) vs. Diseño de Base de Datos

El presente documento tiene como objetivo aclarar la naturaleza del Análisis Exploratorio de Datos (EDA, por sus siglas en inglés), distinguirlo del diseño y construcción de una base de datos, y establecer el lugar adecuado para su documentación dentro de la estructura de un proyecto de software o de análisis de información.

## 1. Definición y Diferencias Conceptuales

Existe a menudo una confusión entre el análisis de la información existente y la estructuración de la misma para su almacenamiento. Es fundamental separar ambos conceptos:

*   **Análisis Exploratorio de Datos (EDA):** Es una fase analítica enfocada en **entender la naturaleza de los datos crudos**. El EDA busca responder preguntas como: ¿Qué calidad tienen los datos?, ¿Existen valores nulos o atípicos (outliers)?, ¿Cuáles son las distribuciones y correlaciones entre las variables? Su propósito es descubrir patrones, identificar riesgos (como sesgos o datos faltantes) y determinar qué transformaciones son necesarias antes de procesar la información o alimentar un modelo. El EDA "escucha" a los datos para saber qué historia cuentan en su estado actual.

*   **Diseño de la Base de Datos (y su construcción):** Es una fase de ingeniería de software enfocada en **estructurar cómo se almacenarán los datos** en el sistema futuro. Involucra la creación de diagramas Entidad-Relación, la normalización (1FN, 2FN, 3FN), la definición de tipos de datos estrictos, restricciones (constraints) y la arquitectura de almacenamiento. Su propósito es garantizar la integridad, eficiencia y disponibilidad de la información. El Diseño de la Base de Datos "dicta" las reglas de cómo debe comportarse y guardarse la información en el sistema.

**En resumen:** El EDA analiza los datos que *ya existen* para entenderlos; el Diseño de Base de Datos crea la estructura (los "cajones") donde los datos *vivirán* de manera organizada y eficiente en el futuro. El EDA puede influir en el diseño de la base de datos (por ejemplo, si el EDA revela que un campo asume muchos valores nulos, el diseño de la BD contemplará permitir nulos en esa columna), pero son disciplinas distintas.

## 2. Ubicación del EDA en la Estructura del Informe

Considerando la estructura de documentación proporcionada:

1. Generalidades
2. Plan de trabajo
3. Marco teórico
4. Desarrollo del informe
    4.1 Análisis del sistema
    4.2 Recolección y análisis de requerimientos
    4.3 Análisis y diseño del sistema
    4.4 Diseño de la base de datos
    4.5 Modelado del sistema - UML
    4.6 Diseño del sistema

El EDA, al ser una etapa de comprensión y preparación, no encaja en la sección de "Diseño de la base de datos" (4.4). Dependiendo del enfoque principal del proyecto, el EDA debe ubicarse en una etapa temprana del desarrollo. Se recomiendan las siguientes alternativas:

**Alternativa A: Como subsección del Análisis del Sistema (Recomendada)**
Si el sistema a construir depende de procesar o migrar datos existentes, el EDA es parte de entender la situación actual.
> **4. Desarrollo del informe**
> **4.1 Análisis del sistema**
> *4.1.1 Análisis Exploratorio de Datos (EDA)* <-- (AQUÍ: Se documenta qué se encontró en los datos de origen, riesgos y transformaciones necesarias).
> 4.2 Recolección y análisis de requerimientos
> ...

**Alternativa B: Como una fase independiente (Para proyectos centrados en datos)**
Si el proyecto tiene un fuerte componente de ciencia de datos, machine learning o analítica (donde el entendimiento del dato es tan importante como el software en sí), el EDA merece su propio apartado principal dentro de "Desarrollo del informe".
> **4. Desarrollo del informe**
> 4.1 Análisis del sistema
> 4.2 Recolección y análisis de requerimientos
> **4.3 Análisis Exploratorio de Datos (EDA)** <-- (AQUÍ: Antes de diseñar el sistema, analizamos la materia prima).
> 4.4 Análisis y diseño del sistema
> 4.5 Diseño de la base de datos
> ...

## 3. ¿Qué se debe redactar en la sección de EDA del informe?

Cuando se redacte el apartado del EDA en el documento final, se debe mantener un tono formal y objetivo, documentando los siguientes hallazgos:

1.  **Origen y Descripción del Dataset:** De dónde provienen los datos analizados, su volumen (número de registros, columnas) y su formato original.
2.  **Identificación de Anomalías y Calidad del Dato:** Un resumen de los problemas encontrados (ej. "Se detectó que el 15% de los registros carecían de fecha de nacimiento", "Se identificaron valores atípicos en el campo X").
3.  **Transformaciones y Limpieza (Data Cleaning):** Qué decisiones se tomaron para corregir las anomalías (ej. "Los valores nulos fueron imputados mediante la media", "Se estandarizó el formato de las fechas a YYYY-MM-DD").
4.  **Hallazgos Clave (Insights):** Cualquier patrón relevante descubierto que impacte los requerimientos o el diseño del sistema.
5.  **Riesgos Prevenidos:** Cómo el análisis previo evitó posibles fallos en el sistema futuro.

Este enfoque asegura que quede evidencia de que el modelado y diseño del sistema se basaron en un entendimiento profundo y objetivo de la información real, garantizando la robustez de la solución final.
