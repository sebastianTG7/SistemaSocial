import flet as ft
from datetime import datetime
from controllers.catalog_controller import CatalogController
from controllers.persona_controller import PersonaController
from core.ui_helpers import mostrar_snackbar, mostrar_exito


def build_registro_view(page: ft.Page):
    """Construye la vista de registro perfeccionada con Autofill por DNI y Historial."""

    # ── Cargar catálogos ─────────────────────────────────────────────────────
    tipos_usuario = CatalogController.get_tipos_usuario()
    casos_sociales = CatalogController.get_casos_sociales()
    facultades = CatalogController.get_facultades()

    # ── Campos con Lógica de Autocompletado ──────────────────────────────────
    def on_dni_change(e):
        if len(f_dni.value) == 8: # Cuando se completa el DNI de 8 dígitos
            p = PersonaController.buscar_por_dni(f_dni.value)
            if p:
                f_nombres.value = p["nombres"]
                f_apellidos.value = p["apellidos"]
                f_edad.value = str(p["edad"]) if p["edad"] else ""
                dd_sexo.value = p["sexo"]
                f_codigo.value = p["codigo_estudiante"] or ""
                f_año.value = p["año_estudio"] or ""
                dd_tipo.value = str(p["tipo_usuario_id"]) if p["tipo_usuario_id"] else None
                dd_facultad.value = str(p["facultad_id"]) if p["facultad_id"] else None
                
                # Cargar escuelas para esa facultad
                if dd_facultad.value:
                    on_facultad_change(None)
                    dd_escuela.value = str(p["escuela_id"]) if p["escuela_id"] else None
                
                f_celular.value = p["celular"] or ""
                f_correo.value = p["correo"] or ""
                f_direccion.value = p["direccion"] or ""
                
                status_text.value = "ℹ Registro previo encontrado. Datos actualizados."
                status_text.color = ft.Colors.BLUE_400
            page.update()

    # ── Elementos de Interfaz ────────────────────────────────────────────────
    f_dni = ft.TextField(label="DNI *", max_length=8, width=160, on_change=on_dni_change)
    f_fecha = ft.TextField(label="Fecha de Atención *", value=datetime.now().strftime("%d/%m/%Y"), width=180, hint_text="DD/MM/YYYY")
    f_nombres = ft.TextField(label="Nombres *", expand=True)
    f_apellidos = ft.TextField(label="Apellidos *", expand=True)
    f_edad = ft.TextField(label="Edad", width=90, max_length=3)
    f_codigo = ft.TextField(label="Código Estudiante", width=190)
    f_año = ft.TextField(label="Año de Estudio", width=140)
    f_celular = ft.TextField(label="Celular", width=180)
    f_correo = ft.TextField(label="Correo Electrónico", expand=True)
    f_direccion = ft.TextField(label="Dirección", expand=True)
    f_observaciones = ft.TextField(label="Observaciones", multiline=True, min_lines=3, expand=True)

    dd_escuela = ft.Dropdown(label="Escuela Profesional *", disabled=True, expand=True)
    
    def on_facultad_change(e):
        if dd_facultad.value:
            escuelas = CatalogController.get_escuelas_by_facultad(int(dd_facultad.value))
            dd_escuela.options = [ft.dropdown.Option(key=str(esc.id), text=esc.nombre) for esc in escuelas]
            dd_escuela.disabled = False
            dd_escuela.hint_text = "Seleccione una escuela"
        page.update()

    dd_sexo = ft.Dropdown(label="Sexo *", width=150, options=[ft.dropdown.Option("F", "Femenino"), ft.dropdown.Option("M", "Masculino")])
    dd_tipo = ft.Dropdown(label="Tipo de Usuario *", width=210, options=[ft.dropdown.Option(str(t.id), t.nombre) for t in tipos_usuario])
    dd_caso = ft.Dropdown(label="Caso Social *", width=200, options=[ft.dropdown.Option(str(c.id), c.nombre) for c in casos_sociales])
    dd_facultad = ft.Dropdown(label="Facultad *", expand=True, on_select=on_facultad_change, options=[ft.dropdown.Option(str(f.id), f.nombre) for f in facultades])
    
    status_text = ft.Text("", size=13, weight="bold")

    def registrar(e):
        # Validaciones
        for c in [f_dni, f_fecha, f_nombres, f_apellidos, dd_sexo, dd_tipo, dd_facultad, dd_escuela, dd_caso]:
            c.error_text = None
        
        hay_errores = False
        if not f_dni.value or len(f_dni.value) != 8: f_dni.error_text = "DNI Inválido"; hay_errores = True
        if not f_fecha.value: f_fecha.error_text = "Requerido"; hay_errores = True
        if not f_nombres.value: f_nombres.error_text = "Requerido"; hay_errores = True
        if not f_apellidos.value: f_apellidos.error_text = "Requerido"; hay_errores = True
        if not dd_caso.value: dd_caso.error_text = "Requerido"; hay_errores = True

        if hay_errores: 
            status_text.value = "⚠ Corrija los errores."; status_text.color = ft.Colors.RED_400; page.update(); return

        datos = {
            "dni": f_dni.value,
            "fecha_atencion": f_fecha.value,
            "nombres": f_nombres.value,
            "apellidos": f_apellidos.value,
            "edad": f_edad.value,
            "sexo": dd_sexo.value,
            "codigo_estudiante": f_codigo.value,
            "año_estudio": f_año.value,
            "tipo_usuario_id": int(dd_tipo.value),
            "facultad_id": int(dd_facultad.value),
            "escuela_id": int(dd_escuela.value),
            "caso_social_id": int(dd_caso.value),
            "celular": f_celular.value,
            "correo": f_correo.value,
            "direccion": f_direccion.value,
            "observaciones": f_observaciones.value,
        }

        exito, resultado = PersonaController.registrar(datos)
        if exito:
            mostrar_exito(page, "Registro de atención guardado")
            limpiar()
        else:
            mostrar_snackbar(page, f"Error: {resultado}", ft.Colors.RED_800)
        page.update()

    def limpiar(e=None):
        for campo in [f_dni, f_nombres, f_apellidos, f_edad, f_codigo, f_año, f_celular, f_correo, f_direccion, f_observaciones]:
            campo.value = ""
        for dd in [dd_sexo, dd_tipo, dd_caso, dd_facultad, dd_escuela]:
            dd.value = None
        f_fecha.value = datetime.now().strftime("%d/%m/%Y")
        dd_escuela.disabled = True
        status_text.value = ""
        page.update()

    btn_registrar = ft.ElevatedButton("Guardar Registro", bgcolor=ft.Colors.GREEN_800, color=ft.Colors.WHITE, on_click=registrar, icon=ft.Icons.SAVE_ROUNDED)

    return ft.Container(
        padding=30,
        content=ft.Column([
            ft.Row([ft.Icon(ft.Icons.PERSON_ADD_ROUNDED, color=ft.Colors.GREEN_400, size=28), ft.Text("Registrar Nueva Atención", size=22, weight="bold")]),
            ft.Divider(color=ft.Colors.BLUE_900),
            ft.Row([f_dni, f_fecha, status_text], spacing=20, vertical_alignment="center"),
            ft.Row([f_nombres, f_apellidos], spacing=20),
            ft.Row([f_edad, dd_sexo, f_codigo, f_año], spacing=20),
            ft.Row([dd_tipo, dd_caso], spacing=20),
            ft.Row([dd_facultad, dd_escuela], spacing=20),
            ft.Row([f_celular, f_correo], spacing=20),
            f_direccion,
            f_observaciones,
            ft.Row([btn_registrar, ft.TextButton("Limpiar Formulario", on_click=limpiar)], alignment="end")
        ], spacing=15, scroll=ft.ScrollMode.AUTO)
    )
