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
    modalidades = CatalogController.get_modalidades()

    # ── Campos con Lógica de Autocompletado ──────────────────────────────────
    def on_dni_change(e):
        if len(f_dni.value) == 8:
            p = PersonaController.buscar_por_dni(f_dni.value)
            if p:
                f_nombres.value = p["nombres"]
                f_apellidos.value = p["apellidos"]
                f_edad.value = str(p["edad"]) if p["edad"] else ""
                dd_sexo.value = p["sexo"]
                f_codigo.value = p["codigo_estudiante"] or ""
                dd_año.value = p["año_estudio"] or None
                dd_tipo.value = str(p["tipo_usuario_id"]) if p["tipo_usuario_id"] else None
                dd_facultad.value = str(p["facultad_id"]) if p["facultad_id"] else None

                if dd_facultad.value:
                    on_facultad_change(None)
                    dd_escuela.value = str(p["escuela_id"]) if p["escuela_id"] else None

                dd_modalidad.value = str(p["modalidad_id"]) if p["modalidad_id"] else "1"
                f_registro_modalidad.value = p["registro_modalidad"] or ""
                on_modalidad_change(None)

                f_celular.value = p["celular"] or ""
                f_correo.value = p["correo"] or ""
                f_direccion.value = p["direccion"] or ""

                if p.get("caso_social"):
                    casos_previos = [c.strip().lower() for c in p["caso_social"].split(",")]
                    for cb in cb_casos:
                        cb.value = any(cp in cb.label.lower() or cb.label.lower() in cp for cp in casos_previos)
                    _actualizar_texto_caso()

                mes_nombre = "N/A"
                if p.get("fecha_atencion"):
                    MESES = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]
                    mes_nombre = MESES[p["fecha_atencion"].month - 1]

                status_text.value = f"Registro previo encontrado ({mes_nombre}). Datos actualizados."
                status_text.color = ft.Colors.BLUE_400
            page.update()

    # ── Elementos de Interfaz ────────────────────────────────────────────────
    f_dni = ft.TextField(label="DNI *", max_length=8, width=160, on_change=on_dni_change)
    f_fecha = ft.TextField(label="Fecha de Atención *", value=datetime.now().strftime("%d/%m/%Y"), width=180, hint_text="DD/MM/YYYY")
    f_nombres = ft.TextField(label="Nombres *", expand=True)
    f_apellidos = ft.TextField(label="Apellidos *", expand=True)
    f_edad = ft.TextField(label="Edad", width=90, max_length=3)
    f_codigo = ft.TextField(label="Código Estudiante", width=190)
    dd_año = ft.Dropdown(
        label="Año de Estudio", width=140,
        options=[ft.dropdown.Option(str(i), f"{i}° Año") for i in range(1, 11)] + [ft.dropdown.Option("Egresado", "Egresado")]
    )
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

    # ── Casos Sociales Múltiples (Selector compacto desplegable) ──────────────
    nombres_casos_base = ["Orientación", "Evaluación", "Seguimiento", "Derivación"]
    for c in casos_sociales:
        if c.nombre not in nombres_casos_base and "," not in c.nombre:
            nombres_casos_base.append(c.nombre)

    cb_casos = [ft.Checkbox(label=nom, value=False) for nom in nombres_casos_base]
    lbl_caso_error = ft.Text("", color=ft.Colors.RED_400, size=11, visible=False)

    # Texto que muestra la selección actual dentro del campo
    txt_caso_display = ft.Text("Seleccionar...", size=13, color=ft.Colors.WHITE54, expand=True)

    def _actualizar_texto_caso():
        seleccionados = [cb.label for cb in cb_casos if cb.value]
        if seleccionados:
            txt_caso_display.value = ", ".join(seleccionados)
            txt_caso_display.color = ft.Colors.WHITE
        else:
            txt_caso_display.value = "Seleccionar..."
            txt_caso_display.color = ft.Colors.WHITE54

    # Panel desplegable oculto por defecto
    caso_panel_visible = {"val": False}
    caso_panel = ft.Container(
        visible=False,
        padding=ft.padding.only(left=12, right=12, top=6, bottom=6),
        border_radius=6,
        bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE),
        content=ft.Row(cb_casos, wrap=True, spacing=8, run_spacing=2)
    )

    def _toggle_caso_panel(e):
        caso_panel_visible["val"] = not caso_panel_visible["val"]
        caso_panel.visible = caso_panel_visible["val"]
        chevron_icon.name = ft.Icons.KEYBOARD_ARROW_UP_ROUNDED if caso_panel_visible["val"] else ft.Icons.KEYBOARD_ARROW_DOWN_ROUNDED
        page.update()

    def _on_caso_changed(e):
        _actualizar_texto_caso()
        lbl_caso_error.visible = False
        lbl_caso_error.value = ""
        page.update()

    for cb in cb_casos:
        cb.on_change = _on_caso_changed

    chevron_icon = ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN_ROUNDED, size=20, color=ft.Colors.WHITE54)

    cnt_caso_header = ft.Container(
        on_click=_toggle_caso_panel,
        padding=ft.padding.symmetric(horizontal=12, vertical=10),
        border=ft.border.all(1, ft.Colors.with_opacity(0.25, ft.Colors.WHITE)),
        border_radius=6,
        content=ft.Row([
            ft.Column([
                ft.Text("Caso Social *", size=11, color=ft.Colors.WHITE54),
                txt_caso_display
            ], spacing=1, expand=True),
            chevron_icon
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    )

    cnt_casos = ft.Column([
        cnt_caso_header,
        caso_panel,
        lbl_caso_error
    ], spacing=4, expand=True)

    dd_facultad = ft.Dropdown(label="Facultad *", expand=True, on_select=on_facultad_change, options=[ft.dropdown.Option(str(f.id), f.nombre) for f in facultades])

    # ── Modalidades ──
    dd_modalidad = ft.Dropdown(
        label="Modalidad de Ingreso *", width=240,
        options=[ft.dropdown.Option(str(m.id), m.nombre) for m in modalidades],
        value="1"
    )
    f_registro_modalidad = ft.TextField(
        label="Código/Registro de Modalidad",
        visible=False,
        expand=True
    )

    def on_modalidad_change(e):
        from database.db_config import SessionLocal
        from database.models import CatModalidad
        if dd_modalidad.value:
            db = SessionLocal()
            m = db.query(CatModalidad).filter(CatModalidad.id == int(dd_modalidad.value)).first()
            db.close()
            if m and m.nombre not in ["General", "CEPREVAL"]:
                if m.nombre == "Discapacidad":
                    f_registro_modalidad.label = "Código CONADIS"
                else:
                    f_registro_modalidad.label = f"N° Registro/Carnet {m.nombre} (Opcional)"
                f_registro_modalidad.visible = True
            else:
                f_registro_modalidad.visible = False
        else:
            f_registro_modalidad.visible = False
        page.update()

    dd_modalidad.on_select = on_modalidad_change

    status_text = ft.Text("", size=13, weight="bold")

    def registrar(e):
        # Validaciones
        for c in [f_dni, f_fecha, f_nombres, f_apellidos, dd_sexo, dd_tipo, dd_facultad, dd_escuela, dd_modalidad]:
            c.error_text = None
        lbl_caso_error.value = ""
        lbl_caso_error.visible = False

        hay_errores = False
        if not f_dni.value or len(f_dni.value) != 8: f_dni.error_text = "DNI Inválido"; hay_errores = True
        if not f_fecha.value: f_fecha.error_text = "Requerido"; hay_errores = True
        if not f_nombres.value: f_nombres.error_text = "Requerido"; hay_errores = True
        if not f_apellidos.value: f_apellidos.error_text = "Requerido"; hay_errores = True
        if not dd_sexo.value: dd_sexo.error_text = "Requerido"; hay_errores = True
        if not dd_tipo.value: dd_tipo.error_text = "Requerido"; hay_errores = True

        casos_seleccionados = [cb.label for cb in cb_casos if cb.value]
        if not casos_seleccionados:
            lbl_caso_error.value = "Seleccione al menos una opción"
            lbl_caso_error.visible = True
            hay_errores = True

        if not dd_facultad.value: dd_facultad.error_text = "Requerido"; hay_errores = True
        if not dd_escuela.value: dd_escuela.error_text = "Requerido"; hay_errores = True
        if not dd_modalidad.value: dd_modalidad.error_text = "Requerido"; hay_errores = True

        if hay_errores:
            status_text.value = "Corrija los campos marcados."; status_text.color = ft.Colors.RED_400; page.update(); return

        nombre_caso_consolidado = ", ".join(casos_seleccionados)
        caso_social_id = CatalogController.get_or_create_caso_social(nombre_caso_consolidado)

        datos = {
            "dni": f_dni.value,
            "fecha_atencion": f_fecha.value,
            "nombres": f_nombres.value,
            "apellidos": f_apellidos.value,
            "edad": f_edad.value,
            "sexo": dd_sexo.value,
            "codigo_estudiante": f_codigo.value,
            "año_estudio": dd_año.value,
            "tipo_usuario_id": int(dd_tipo.value) if dd_tipo.value else None,
            "facultad_id": int(dd_facultad.value) if dd_facultad.value else None,
            "escuela_id": int(dd_escuela.value) if dd_escuela.value else None,
            "caso_social_id": caso_social_id,
            "modalidad_id": int(dd_modalidad.value) if dd_modalidad.value else None,
            "registro_modalidad": f_registro_modalidad.value if f_registro_modalidad.visible else None,
            "celular": f_celular.value,
            "correo": f_correo.value,
            "direccion": f_direccion.value,
            "observaciones": f_observaciones.value,
        }

        def preguntar_ficha(p_id, nombres_completos, callback_siguiente=None):
            confirm_dlg = ft.AlertDialog(modal=True)

            def al_si(e):
                confirm_dlg.open = False
                page.update()
                from views.components.socioeconomic_dialog import mostrar_ficha_socioeconomica_dialog
                mostrar_ficha_socioeconomica_dialog(page, p_id, nombres_completos, on_save_callback=callback_siguiente)

            def al_no(e):
                confirm_dlg.open = False
                page.update()
                if callback_siguiente: callback_siguiente()

            confirm_dlg.title = ft.Text("Evaluación Socioeconómica Detectada")
            confirm_dlg.content = ft.Text("¿Deseas rellenar la Ficha Socioeconómica del estudiante ahora?")
            confirm_dlg.actions = [
                ft.TextButton("En otro momento", on_click=al_no),
                ft.ElevatedButton("Sí, Rellenar", on_click=al_si, bgcolor=ft.Colors.GREEN_800, color=ft.Colors.WHITE)
            ]
            confirm_dlg.actions_alignment = "end"

            if confirm_dlg not in page.overlay:
                page.overlay.append(confirm_dlg)
            confirm_dlg.open = True
            page.update()

        def preguntar_derivacion(p_id):
            confirm_dlg = ft.AlertDialog(modal=True)

            def al_si(e):
                confirm_dlg.open = False
                page.update()
                from views.components.derivacion_dialog import mostrar_ficha_derivacion_dialog
                mostrar_ficha_derivacion_dialog(page, p_id, on_close=None)

            def al_no(e):
                confirm_dlg.open = False
                page.update()

            confirm_dlg.title = ft.Text("Derivación Detectada")
            confirm_dlg.content = ft.Text("¿Deseas rellenar la Ficha de Derivación para esta atención ahora?")
            confirm_dlg.actions = [
                ft.TextButton("En otro momento", on_click=al_no),
                ft.ElevatedButton("Sí, Rellenar", on_click=al_si, bgcolor=ft.Colors.GREEN_800, color=ft.Colors.WHITE)
            ]
            confirm_dlg.actions_alignment = "end"

            if confirm_dlg not in page.overlay:
                page.overlay.append(confirm_dlg)
            confirm_dlg.open = True
            page.update()


        exito, resultado = PersonaController.registrar(datos)
        if exito:
            p_id = resultado
            nombres_completos = f"{f_apellidos.value}, {f_nombres.value}"
            mostrar_exito(page, "Registro de atención guardado")

            tiene_evaluacion = any("evaluaci" in c.lower() for c in casos_seleccionados)
            tiene_derivacion = any("derivaci" in c.lower() for c in casos_seleccionados)

            limpiar()

            if tiene_evaluacion and tiene_derivacion:
                preguntar_ficha(p_id, nombres_completos, callback_siguiente=lambda: preguntar_derivacion(p_id))
            elif tiene_evaluacion:
                preguntar_ficha(p_id, nombres_completos)
            elif tiene_derivacion:
                preguntar_derivacion(p_id)
        else:
            mostrar_snackbar(page, f"Error: {resultado}", ft.Colors.RED_800)
        page.update()

    def limpiar(e=None):
        for campo in [f_dni, f_nombres, f_apellidos, f_edad, f_codigo, f_celular, f_correo, f_direccion, f_observaciones, f_registro_modalidad]:
            campo.value = ""
        for dd in [dd_sexo, dd_tipo, dd_facultad, dd_escuela, dd_año]:
            dd.value = None
        for cb in cb_casos:
            cb.value = False
        _actualizar_texto_caso()
        lbl_caso_error.value = ""
        lbl_caso_error.visible = False
        caso_panel.visible = False
        caso_panel_visible["val"] = False
        chevron_icon.name = ft.Icons.KEYBOARD_ARROW_DOWN_ROUNDED
        dd_modalidad.value = "1"
        f_registro_modalidad.visible = False
        f_fecha.value = datetime.now().strftime("%d/%m/%Y")
        dd_escuela.disabled = True
        status_text.value = ""
        page.update()

    btn_registrar = ft.ElevatedButton("Guardar Registro", bgcolor=ft.Colors.GREEN_800, color=ft.Colors.WHITE, on_click=registrar)
    btn_limpiar = ft.TextButton("Limpiar Formulario", on_click=limpiar)

    # ── Helper: Separador de sección ─────────────────────────────────────────
    def seccion(titulo):
        return ft.Container(
            padding=ft.padding.only(top=10, bottom=2),
            content=ft.Text(titulo, size=13, weight="w600", color=ft.Colors.BLUE_200)
        )

    return ft.Container(
        padding=30,
        content=ft.Column([
            ft.Text("Registrar Nueva Atención", size=22, weight="bold"),
            ft.Divider(color=ft.Colors.with_opacity(0.15, ft.Colors.WHITE)),

            # — Sección: Identificación
            seccion("Identificación"),
            ft.Row([f_dni, f_fecha, status_text], spacing=15, vertical_alignment="center"),
            ft.Row([f_nombres, f_apellidos], spacing=15),
            ft.Row([f_edad, dd_sexo], spacing=15),

            # — Sección: Datos Académicos
            seccion("Datos Académicos"),
            ft.Row([dd_tipo, f_codigo, dd_año], spacing=15),
            ft.Row([dd_facultad, dd_escuela], spacing=15),
            ft.Row([dd_modalidad, f_registro_modalidad], spacing=15),

            # — Sección: Caso Social
            seccion("Caso Social"),
            cnt_casos,

            # — Sección: Contacto
            seccion("Contacto"),
            ft.Row([f_celular, f_correo], spacing=15),
            f_direccion,
            f_observaciones,

            ft.Divider(color=ft.Colors.with_opacity(0.1, ft.Colors.WHITE)),
            ft.Row([btn_registrar, btn_limpiar], alignment="end", spacing=10)
        ], spacing=10, scroll=ft.ScrollMode.AUTO)
    )
