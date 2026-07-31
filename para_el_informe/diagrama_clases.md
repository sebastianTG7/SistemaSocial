# Diagrama de Clases Lógico - Sistema Social

A diferencia de un diagrama de base de datos (que solo muestra tablas y llaves foráneas), el **diagrama de clases** modela la estructura lógica del software. En él definimos no solo las propiedades (atributos) que tiene una entidad, sino también los comportamientos (métodos/operaciones) que puede realizar en el sistema.

Dado que tu sistema es un gestor de Casos Sociales, hemos agrupado las clases por **Módulos Lógicos** e inferido los métodos típicos que cada clase ejecutaría en el backend (por ejemplo, registrar una atención, evaluar una ficha, etc.).

Puedes usar estos diagramas directamente en tu informe, o copiarlos en herramientas como [Mermaid Live](https://mermaid.live/) o Draw.io.

---

## 1. Módulo de Seguridad y Accesos

Este módulo gestiona a los operadores y administradores del sistema.

```mermaid
classDiagram
    class Usuario {
        -Integer id
        -String username
        -String passwordHash
        -String nombreCompleto
        -String rol
        -Boolean activo
        +iniciarSesion(username: String, pass: String): Boolean
        +cerrarSesion(): Void
        +cambiarPassword(newPass: String): Boolean
        +verificarRol(): String
    }
```

**Explicación:**
* La clase `Usuario` representa a las personas que operan el sistema (trabajadoras sociales, administradores). Sus métodos reflejan acciones lógicas como validarse en el sistema o cambiar su contraseña.

---

## 2. Módulo de Beneficiarios (Personas)

Gestiona la información central de los estudiantes o personas que reciben asistencia social.

```mermaid
classDiagram
    class Persona {
        -Integer id
        -String dni
        -String nombres
        -String apellidos
        -Date fechaNacimiento
        -String sexo
        -String codigoEstudiante
        -String celular
        -Boolean activo
        +registrarPersona(datos: Object): Persona
        +actualizarDatosContacto(): Boolean
        +obtenerHistorialAtenciones(): List~Atencion~
        +calcularEdadActual(): Integer
    }

    class CatFacultad {
        -Integer id
        -String nombre
        -Boolean activo
        +listarEscuelas(): List~CatEscuela~
    }

    class CatEscuela {
        -Integer id
        -String nombre
        -Boolean activo
    }

    class CatModalidad {
        -Integer id
        -String nombre
    }

    Persona "1" --> "1" CatFacultad : pertenece a
    Persona "1" --> "1" CatEscuela : matriculado en
    Persona "1" --> "1" CatModalidad : ingresó por
    CatFacultad "1" *-- "many" CatEscuela : contiene
```

**Explicación:**
* `Persona` es la clase central. Los métodos `obtenerHistorialAtenciones()` o `calcularEdadActual()` son lógica de negocio.
* Se relaciona con catálogos (Facultad, Escuela, Modalidad) para tipificar su perfil académico.

---

## 3. Módulo de Atenciones y Evaluación Social

Este es el núcleo de tu sistema, donde se registran las visitas, se hacen evaluaciones socioeconómicas y se derivan casos psicológicos o médicos.

```mermaid
classDiagram
    class Atencion {
        -Integer id
        -DateTime fechaAtencion
        -String observaciones
        -Boolean activo
        +registrarAtencion(personaId: Integer, casoId: Integer): Atencion
        +actualizarObservaciones(texto: String): Boolean
        +obtenerFichaAsociada(): FichaDerivacion
    }

    class FichaSocioeconomica {
        -Integer id
        -String motivoEvaluacion
        -String sisfohCondicion
        -Float ingresoTotal
        -Float egresoTotal
        -Boolean tieneDiscapacidad
        +evaluarVulnerabilidad(): String
        +calcularBalanceEconomico(): Float
        +generarReporteSocioeconomico(): File
    }

    class FichaDerivacion {
        -Integer id
        -String areaDeriva
        -String areaDerivada
        -DateTime fechaDerivacion
        -String motivoConsulta
        -String condicion
        -String diagnostico
        +derivarCaso(areaTarget: String): Boolean
        +evaluarImpactoAcademico(): String
        +actualizarDiagnostico(diagnostico: String): Void
    }

    class CatCasoSocial {
        -Integer id
        -String nombre
    }

    Persona "1" *-- "many" Atencion : recibe
    Atencion "many" --> "1" CatCasoSocial : clasificada como
    Persona "1" -- "0..1" FichaSocioeconomica : posee
    Atencion "1" -- "0..1" FichaDerivacion : genera
```

**Explicación:**
* **`Atencion`**: Es el registro de cada visita de una `Persona` a la oficina de servicio social. Tiene métodos para registrar el evento y consultar datos.
* **`FichaSocioeconomica`**: Se asocia directamente a la `Persona` (relación 1 a 1). Contiene lógica crítica como `calcularBalanceEconomico()` (ingresos - egresos) y `evaluarVulnerabilidad()`.
* **`FichaDerivacion`**: Se genera a partir de una `Atencion` específica. Sus métodos incluyen la acción de derivar a un paciente y actualizar diagnósticos médicos/psicológicos.

---

## Recomendaciones para tu Informe

1. **Uso de UML**: Lo que te he generado utiliza la sintaxis **Mermaid** (que es un estándar muy usado para diagramar por código). Puedes tomar captura de estos diagramas visuales generados para ponerlos en tu Word/PDF.
2. **Separar por Módulos**: Tal como lo hice arriba, es mucho más profesional explicar el diagrama de clases **por módulos** (Seguridad, Beneficiarios, Fichas) que poner un diagrama gigante e incomprensible de 15 clases todas cruzadas.
3. **Inferencia de Métodos**: En Python (SQLAlchemy) solemos poner las clases de base de datos (`models.py`) solo con atributos. Sin embargo, en un diagrama de clases lógico (UML), **sí** debes poner los métodos (la lógica que hará tu API o tus controladores). Los métodos que he colocado (`calcularBalanceEconomico`, `derivarCaso`, `registrarAtencion`) son ejemplos perfectos de lo que los jurados o profesores esperan ver en un diagrama de clases.
