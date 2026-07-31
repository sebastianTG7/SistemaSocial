# 4.7. Construcción y Desarrollo de Interfaces

## 4.7.1. Estándares de Codificación y Estructura del Proyecto

Para el desarrollo del sistema se han adoptado estándares de codificación reconocidos y mejores prácticas con el fin de asegurar la mantenibilidad y escalabilidad del código fuente. Dado que el proyecto está desarrollado en Python, se ha seguido el estándar **PEP 8**, garantizando un código limpio, legible y uniformemente estructurado en cuanto a indentación (4 espacios), nombres de variables en `snake_case`, clases en `PascalCase` y funciones descriptivas.

En cuanto a la arquitectura, el proyecto sigue un patrón de diseño orientado al **Modelo-Vista-Controlador (MVC)** estructurado en módulos, lo cual permite una clara separación de responsabilidades entre la interfaz gráfica, la lógica de negocio y la gestión de datos.

La estructura de directorios principal se compone de las siguientes carpetas clave:

| Carpeta | Descripción |
|---|---|
| `assets/` | Recursos estáticos: imágenes, íconos, logotipos y plantillas HTML para documentos exportados. |
| `config/` | Archivos de configuración global: parámetros de conexión y configuración de backup automático. |
| `controllers/` | Lógica de negocio. Contiene `auth_controller.py`, `persona_controller.py`, `catalog_controller.py`, entre otros. |
| `core/` | Utilidades compartidas: `init_db.py`, `ui_helpers.py`, `backup_manager.py`. |
| `database/` | Gestión de la base de datos: configuración de sesión (SQLAlchemy), modelos ORM y scripts de migración. |
| `views/` | Lógica de la interfaz de usuario (UI). Incluye subcomponentes reutilizables en `views/components/`. |

---

## 4.7.2. Desarrollo del Frontend

### 4.7.2.1. Framework Utilizado

El frontend del sistema ha sido desarrollado utilizando **Flet** (versión 0.83+), un framework de Python que permite construir aplicaciones de escritorio multiplataforma con interfaces modernas e interactivas, basadas internamente en **Flutter**. Esta elección técnica elimina la necesidad de usar HTML/CSS tradicional y permite diseñar interfaces altamente responsivas con componentes reutilizables, orientadas a ofrecer una excelente experiencia de usuario (UX). La aplicación corre de forma nativa en escritorio (Windows), garantizando rendimiento fluido sin dependencias externas de navegador.

---

### 4.7.2.2. Sistema de Temas: Modo Oscuro / Modo Claro

El sistema implementa un **tema dual** que el usuario puede alternar en tiempo real desde el botón de cambio de tema ubicado en el Dashboard. La configuración del tema raíz se define en `main.py` de la siguiente manera:

```python
page.theme_mode = ft.ThemeMode.DARK
page.theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE_700)
```

Esto establece **BLUE_700** como color semilla del esquema de colores de Material Design 3, a partir del cual Flet genera automáticamente una paleta complementaria para todos los componentes del sistema.

---

### 4.7.2.3. Paleta de Colores

La paleta de colores del sistema fue definida de forma manual en el código fuente, con colores específicos asignados por contexto funcional. A continuación se presenta el catálogo completo de colores utilizados:

#### Colores Base (Fondo y Superficies)

| Nombre / Rol | Código Hex / Constante Flet | Uso en el Sistema |
|---|---|---|
| **Fondo Principal (Dark)** | `#0f111a` | Fondo de la pantalla de Login y Splash Screen. |
| **Fondo Contenedor Login** | `ft.Colors.BLUE_GREY_900` | Contenedor raíz que envuelve la vista de Login. |
| **Superficie Tarjeta (Dark)** | `WHITE con opacidad 0.07` | Fondo de las tarjetas KPI en modo oscuro. |
| **Superficie Tarjeta (Light)** | `ft.Colors.WHITE` | Fondo de las tarjetas KPI en modo claro. |
| **Panel Gráfico (Dark)** | `WHITE con opacidad 0.05` | Fondo de los paneles analíticos en modo oscuro. |
| **Panel Gráfico (Light)** | `ft.Colors.GREY_50` | Fondo de los paneles analíticos en modo claro. |
| **Campo de Formulario** | `#1e293b` | Fondo de los `TextField` (usuario y contraseña en Login). |
| **Barra Lateral (Sidebar)** | `BLUE_900 con opacidad 0.10` | Fondo traslúcido de la barra de navegación lateral. |

#### Colores de Acento e Interacción

| Nombre / Rol | Código Hex / Constante Flet | Uso en el Sistema |
|---|---|---|
| **Acento Principal (Sky Blue)** | `#0ea5e9` | Bordes activos en Login, texto del botón "Iniciar Sesión", separador decorativo bajo el título. |
| **Acento Azul (Datos)** | `ft.Colors.BLUE_400` | KPIs de total de atenciones, gráfico de género masculino, barras de tendencia mensual. |
| **Acento Verde (Datos)** | `ft.Colors.GREEN_400` | KPI de categorías de atención, barras de tendencia. |
| **Acento Rosa (Datos)** | `ft.Colors.PINK_400` | Gráfico de distribución de género femenino. |
| **Acento Naranja (Datos)** | `ft.Colors.ORANGE_400` | Gráfico de tipología: egresados. |
| **Acento Púrpura (Datos)** | `ft.Colors.PURPLE_400` | Ítem de ranking de facultades (color rotatorio). |
| **Acento Cian (Datos)** | `ft.Colors.CYAN_400` | Ítem de ranking de facultades (color rotatorio). |
| **Indicador de Navegación** | `ft.Colors.GREEN_800` | Color del indicador del ítem seleccionado en el Sidebar. |
| **Títulos de Panel (Dark)** | `ft.Colors.BLUE_200` | Títulos de sección del Dashboard en modo oscuro. |
| **Títulos de Panel (Light)** | `ft.Colors.BLUE_900` | Títulos de sección del Dashboard en modo claro. |
| **Encabezado de Tabla** | `BLUE_400 con opacidad 0.10` | Fondo de la fila de encabezado en las tablas de datos. |

#### Colores de Estado y Retroalimentación

| Nombre / Rol | Código Hex / Constante Flet | Uso en el Sistema |
|---|---|---|
| **Error / Alerta** | `ft.Colors.RED_400` | Mensaje de error en Login, ícono del botón de Cerrar Sesión. |
| **Información / Autocompletado** | `ft.Colors.BLUE_400` | Mensaje al detectar un registro previo por DNI en el formulario. |
| **Éxito / Confirmación** | `ft.Colors.GREEN` (snackbar) | Notificaciones de éxito al registrar o guardar datos. |
| **Toggle Tema (Sol)** | `ft.Colors.AMBER_400` | Ícono del botón de cambio de tema en modo oscuro. |
| **Toggle Tema (Luna)** | `ft.Colors.BLACK` | Ícono del botón de cambio de tema en modo claro. |

---

### 4.7.2.4. Tipografía

La tipografía del sistema utiliza la **fuente del sistema por defecto de Flet/Flutter**, que en entornos Windows corresponde a **Segoe UI**, y en otras plataformas utiliza la fuente nativa de Material Design. No se cargó ninguna fuente externa dado que Flet hereda el sistema tipográfico de Material Design 3, garantizando legibilidad y coherencia en todas las resoluciones y densidades de pantalla.

La jerarquía tipográfica aplicada en el sistema es la siguiente:

| Nivel | Tamaño | Peso | Color | Uso Principal |
|---|---|---|---|---|
| **Título Principal** | `32 pt` | `bold` | `WHITE` | Nombre del sistema en la pantalla de Login (`"SERVICIO SOCIAL"`). |
| **Splash / Marca** | `30 pt` | `bold` | `WHITE` | Nombre del sistema en la pantalla de carga inicial. |
| **Título de Pantalla** | `24 pt` | `bold` | Tema | Título del Dashboard (`"Dashboard Analítico v3.0"`). |
| **Subtítulo Formulario** | `22 pt` | `bold` | `WHITE` | Encabezado del formulario de Login (`"Iniciar Sesión"`). |
| **Título de Panel** | `16 pt` | `bold` | `BLUE_200/900` | Títulos de los paneles analíticos del Dashboard. |
| **Cuerpo de Panel** | `14 pt` | `bold` | Tema | Títulos internos dentro de paneles del Dashboard. |
| **Splash Secundario** | `13 pt` | normal | `BLUE_200` | Eslogan debajo del título en la pantalla de carga. |
| **Datos de Tabla** | `12 pt` | normal | Tema | Contenido de filas en tablas de personas y atenciones. |
| **Encabezado Tabla** | `12 pt` | `bold` | Tema | Cabeceras de columnas de las tablas de datos. |
| **Etiqueta de Categoría** | `12 pt` | normal | `text_sub` | Etiquetas en gráficos de donuts (ej. "Varones", "Mujeres"). |
| **Valor de KPI** | `28 pt` | `bold` | Color acento | Valor numérico destacado en las tarjetas KPI. |
| **Etiqueta de KPI** | `10 pt` | normal | `text_sub` | Descripción del indicador en las tarjetas KPI. |
| **Texto Auxiliar** | `11–12 pt` | normal | `text_sub` | Subtítulos, anotaciones y textos de soporte. |
| **Error / Validación** | `12 pt` | `bold` | `RED_400` | Mensajes de error en formularios. |
| **Cargando** | `11 pt` | normal | `WHITE38` | Texto "Cargando…" en la pantalla de splash. |

---

### 4.7.2.5. Componentes de Interfaz Implementados

El sistema fue construido con los siguientes componentes de Flet/Material Design, organizados por su función:

#### Componentes de Entrada de Datos

| Componente | Configuración Clave | Vistas Donde Aparece |
|---|---|---|
| `TextField` | `border_radius=15`, fondo `#1e293b`, borde activo `#0ea5e9` | Login, Registro, Evaluaciones, Derivaciones |
| `Dropdown` | `border_radius=12`, opciones dinámicas desde la base de datos | Registro (Tipo, Facultad, Escuela, Modalidad), Dashboard (Mes, Año) |
| `DataTable` | `heading_row_color` con opacidad, soporte para ordenación por columna | Personas, Evaluaciones, Derivaciones, Usuarios |
| `AlertDialog` | Gestionado vía `page.overlay` para compatibilidad con Flet 0.83 | Formularios de edición y eliminación en todas las vistas |

#### Componentes de Visualización y Navegación

| Componente | Configuración Clave | Vistas Donde Aparece |
|---|---|---|
| `NavigationRail` (Sidebar) | `min_width=80`, `indicator_color=GREEN_800`, etiquetas siempre visibles | Barra lateral persistente en toda la aplicación |
| `ProgressRing` (Donut) | Anillos apilados con `ft.Stack`, `value` proporcional al porcentaje | Dashboard (gráfico de género y tipo de usuario) |
| `Container` con `LinearGradient` | Gradiente `GREEN_400 → BLUE_900` y `color → BLUE_900` | Barras de tendencia mensual y ranking de facultades |
| `BoxShadow` | `blur_radius=12–15`, `offset=(4,6)` o `(0,10)` | Tarjetas KPI y paneles del Dashboard |
| `SnackBar` | Mensajes de éxito/error con cierre automático | Todas las vistas con operaciones CRUD |
| `ProgressRing` (Loading) | `width=36`, `stroke_width=3`, `color=BLUE_400` | Pantalla de carga (Splash Screen) |
| `IconButton` | Íconos de Material Icons (outlined vs. rounded para seleccionado) | Botones de acción en tablas, cambio de tema, logout |

#### Componentes de Layout

| Componente | Uso |
|---|---|
| `Row` / `Column` | Composición de layouts horizontales y verticales en todas las vistas. |
| `ResponsiveRow` | Panel superior del Dashboard con rejilla adaptable por breakpoints (`sm`, `md`). |
| `Stack` | Superposición de anillos de progreso y barras de gráficos. |
| `Container` | Unidad principal de diseño: maneja `padding`, `border_radius`, `bgcolor`, `shadow`. |
| `VerticalDivider` / `Divider` | Separadores visuales entre la barra lateral y el contenido principal. |

---

### 4.7.2.6. Vistas Principales Implementadas

#### Vista de Splash (Carga Inicial)

Pantalla de presentación que se muestra durante 2 segundos al iniciar la aplicación. Muestra el logotipo institucional, el nombre del sistema ("SERVICIO SOCIAL"), un eslogan descriptivo ("Sistema de Gestión Universitaria") y un indicador de progreso animado (`ProgressRing`). El fondo es `#0f111a`. Se implementa como una tarea asíncrona (`page.run_task`) para no bloquear el hilo principal de la aplicación.

#### Vista de Inicio de Sesión (Login)

Pantalla de autenticación con diseño en dos columnas: a la izquierda, el formulario con campos de usuario y contraseña (con opción de revelar la contraseña), separador decorativo en color `#0ea5e9`; a la derecha, el logotipo institucional. El formulario incluye validación de credenciales y muestra mensajes de error en `RED_400`. El botón de login se deshabilita durante el proceso de autenticación para evitar dobles envíos.

#### Vista de Dashboard (Panel Analítico)

Panel principal con los siguientes elementos:
- **Tarjetas KPI**: 5 tarjetas mostrando total de atenciones y distribución por tipo de caso, con valores en `28 pt` y color acento.
- **Gráficos de donuts**: Distribución por género y por tipo de usuario (Estudiante/Egresado), implementados con `ProgressRing` apilados.
- **Ranking de Facultades**: Lista expandible (acordeón) con barras horizontales de progreso y gradiente de color.
- **Gráfico de Tendencia**: Barras verticales mensuales con gradiente `GREEN_400 → BLUE_900`.
- **Filtros de período**: Selectores de mes y año para filtrar todos los indicadores simultáneamente.
- **Botón de cambio de tema**: Alterna entre modo oscuro y claro afectando a toda la aplicación.

#### Vista de Registro de Atenciones

Formulario completo para registrar nuevas atenciones. Implementa **autofill inteligente por DNI**: al ingresar 8 dígitos, el sistema consulta la base de datos y completa automáticamente los campos del beneficiario si ya existe un registro previo, informando al usuario con un mensaje en `BLUE_400`.

#### Vista de Gestión de Personas / Atenciones

Interfaz de listado con tabla ordenable por columna. Incluye buscador en tiempo real por DNI, nombre o código, y filtros combinables por mes, año y modalidad. Permite alternar entre registros activos e inactivos. Ofrece acciones de edición, eliminación y exportación de datos a Excel (`.xlsx`).

#### Vista de Evaluaciones y Derivaciones

Pantallas especializadas para el registro y gestión de evaluaciones psicológicas/sociales y las derivaciones a servicios externos, cada una con su propia tabla de datos con acciones CRUD y modales de detalle.

#### Vista de Configuración y Usuarios

Módulos administrativos para la gestión de usuarios del sistema (creación, edición, cambio de contraseña, activación/desactivación) y la configuración de parámetros generales como la ruta de backup y la programación del respaldo automático.

**Capturas de pantalla de las vistas:**
*(Insertar aquí las capturas de pantalla)*
- *[Captura de la pantalla de carga (Splash)]*
- *[Captura de la vista Login]*
- *[Captura del Dashboard en modo oscuro]*
- *[Captura del Dashboard en modo claro]*
- *[Captura del listado de atenciones con buscador activo]*
- *[Captura del formulario de registro con autofill por DNI activo]*
- *[Captura del módulo de evaluaciones]*
- *[Captura del módulo de derivaciones]*

---

### 4.7.2.7. Navegación y Flujo de la Aplicación

La navegación principal del sistema se realiza a través de un componente `NavigationRail` (barra lateral izquierda) que permanece visible en todas las pantallas una vez autenticado el usuario. Este componente está implementado en `views/components/sidebar.py` y cuenta con 7 destinos:

| Índice | Ícono Material | Etiqueta | Vista Asociada |
|---|---|---|---|
| 0 | `DASHBOARD` | Inicio | `DashboardView` |
| 1 | `PERSON_ADD` | Registrar | `registro_view` |
| 2 | `LIST_ALT` | Atenciones | `personas_view` |
| 3 | `ASSIGNMENT_IND` | Evaluaciones | `evaluaciones_view` |
| 4 | `SHARE` | Derivaciones | `derivaciones_view` |
| 5 | `PEOPLE_ALT` | Usuarios | `usuarios_view` |
| 6 | `SETTINGS` | Config. | `config_view` |

El flujo completo de la aplicación sigue la siguiente secuencia:

```
Inicio del programa
       │
       ▼
  Splash Screen (2 seg.)
       │
       ▼
  Vista de Login ─── Credenciales incorrectas ──► Mensaje de error en rojo
       │
  Autenticación exitosa
       │
       ▼
  Layout Principal (Sidebar + Área de Contenido)
       │
       ├──► [0] Dashboard (vista por defecto al ingresar)
       ├──► [1] Registro de Atención (nuevo beneficiario)
       ├──► [2] Gestión de Atenciones (listado, búsqueda, exportación)
       ├──► [3] Evaluaciones
       ├──► [4] Derivaciones
       ├──► [5] Gestión de Usuarios (solo administradores)
       └──► [6] Configuración del Sistema
```

---

### 4.7.2.8. Reutilización y Modularidad de Componentes

El sistema fue diseñado con un alto grado de **modularidad y reutilización** de componentes:

- **`views/components/sidebar.py`**: Barra de navegación lateral (`NavigationRail`), reutilizada en toda la aplicación post-login.
- **`views/components/socioeconomic_dialog.py`**: Diálogo modal reutilizable para la visualización y edición de la ficha socioeconómica de cada beneficiario.
- **`views/components/derivacion_dialog.py`**: Componente modal especializado para el registro y visualización de derivaciones a servicios externos.
- **`core/ui_helpers.py`**: Contiene las funciones `mostrar_snackbar()` y `mostrar_exito()`, utilizadas en todas las vistas para emitir notificaciones de retroalimentación al usuario de forma consistente.

---

## 4.7.3. Desarrollo del Backend y Seguridad

El desarrollo del backend reside en el mismo ecosistema Python, operando bajo la estructura de los controladores (`controllers/`) y la conexión a la base de datos (`database/`). La lógica central manipula las peticiones del usuario provenientes de Flet y realiza las transacciones de datos de forma segura mediante **SQLAlchemy** como ORM (Object-Relational Mapper).

En materia de **seguridad y control de acceso**:

- **Autenticación**: A través de `auth_controller.py`, se gestiona el inicio de sesión validando las contraseñas de los usuarios, las cuales se almacenan de forma encriptada en la base de datos.
- **Validación de Datos**: Los controladores actúan como filtro que verifica la integridad de los datos ingresados antes de insertarlos (por ejemplo, validación de duplicados de DNI y formato de fechas).
- **Gestión de Sesiones y Roles**: El sistema restringe el acceso a ciertas vistas o funciones dependiendo del rol del usuario autenticado (administrador vs. operador), protegiendo la información sensible.
- **Backup Automático**: A través de `core/backup_manager.py`, el sistema puede configurarse para realizar copias de seguridad automáticas al cerrar la aplicación, protegiendo la integridad de los datos ante fallos inesperados.
- **Gestión segura de diálogos**: Para compatibilidad con Flet 0.83+, todos los `AlertDialog` se gestionan a través de `page.overlay`, evitando conflictos de estado entre ventanas modales.

---

## 4.7.4. Módulo Analítico (Dashboard)

El módulo analítico se encuentra implementado principalmente en la vista de Dashboard (`views/dashboard_view.py`). Este panel de control tiene como objetivo consolidar y visualizar la información más relevante del sistema para facilitar la toma de decisiones del personal del Servicio Social.

### Indicadores Clave (KPIs)

Las tarjetas KPI muestran 5 métricas principales en tiempo real:

| KPI | Descripción | Color de Acento |
|---|---|---|
| Total de Atenciones | Número total de atenciones registradas en el período filtrado. | `BLUE_400` |
| Evaluación | Casos categorizados como "Evaluación" pura. | `GREEN_400` |
| Evaluación y Seguimiento | Casos con evaluación inicial y seguimiento continuado. | `GREEN_400` |
| Seguimiento | Casos en etapa de seguimiento activo. | `GREEN_400` |
| Orientación | Casos resueltos mediante orientación directa. | `GREEN_400` |

### Visualizaciones Implementadas

- **Gráficos de anillo (Donut Charts)**: Implementados con `ProgressRing` apilados en un `ft.Stack`, mostrando porcentaje y cantidad superpuestos. Se usan para la distribución de género y tipo de usuario.
- **Barras horizontales de progreso**: Ranking de facultades con mayor número de atendidos, con gradiente de color y expansión mediante acordeón ("Ver más / Ver menos").
- **Barras verticales de tendencia**: Histograma mensual con gradiente `GREEN_400 → BLUE_900`, sombras para efecto de profundidad (`BoxShadow`) y tooltip al pasar el cursor.

### Procesamiento de Datos

Al cargar o actualizar el Dashboard, los controladores realizan consultas optimizadas a través de `PersonaController.get_analytics()` y `PersonaController.get_trend()` para recuperar y agregar los datos en tiempo real, filtrando por mes y año seleccionados.

---

## 4.7.5. Exportación de Reportes

El sistema incluye funcionalidad de exportación de datos a formato **Excel (`.xlsx`)** desde la vista de Gestión de Atenciones (`personas_view.py`). Esta funcionalidad utiliza la librería **`openpyxl`** con estilos personalizados:

- **`Font(bold=True)`**: Texto en negrita para los encabezados de columna.
- **`PatternFill`**: Relleno de color para diferenciar visualmente la fila de encabezados del resto de los datos.
- **`Alignment`**: Alineación de celdas para centrar el contenido en cada celda.

Los reportes generados incluyen todos los campos del beneficiario y su atención, filtrados según el estado activo/inactivo y los filtros de período aplicados en la vista en el momento de la exportación.
