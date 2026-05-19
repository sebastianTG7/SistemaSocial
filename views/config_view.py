import flet as ft
import os
from database.db_config import SessionLocal
from database.models import CatFacultad, CatEscuela, CatCasoSocial, CatTipoUsuario
from core.ui_helpers import mostrar_snackbar, mostrar_exito
from core.backup_manager import BackupManager


# ══════════════════════════════════════════════════════════════════════════════
#  Helper: Tabla CRUD genérica para catálogos simples (sin relaciones)
# ══════════════════════════════════════════════════════════════════════════════
def _tabla_crud_simple(page, modelo, nombre_campo="nombre", titulo="Catálogo"):
    """
    Genera una vista completa CRUD para un catálogo simple (solo 'nombre').
    Muestra tabla con botones Editar/Eliminar y formulario inline para Agregar/Editar.
    """
    # ── Estado ───────────────────────────────────────────────────────────────
    estado = {
        "editando_id": None,   # None = estamos en modo Agregar
        "formulario_visible": False,
    }

    # ── Elementos del formulario ──────────────────────────────────────────────
    campo_nombre = ft.TextField(
        label=f"Nombre del {titulo[:-1] if titulo.endswith('s') else titulo}",
        expand=True,
        border_color=ft.Colors.BLUE_700,
        focused_border_color=ft.Colors.GREEN_400,
    )
    form_titulo = ft.Text("", size=16, weight="bold", color=ft.Colors.GREEN_400)
    form_mensaje = ft.Text("", color=ft.Colors.RED_400, size=12)

    # ── Tabla ─────────────────────────────────────────────────────────────────
    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", weight="bold")),
            ft.DataColumn(ft.Text("Nombre", weight="bold")),
            ft.DataColumn(ft.Text("Estado", weight="bold")),
            ft.DataColumn(ft.Text("Acciones", weight="bold")),
        ],
        rows=[],
        column_spacing=24,
        heading_row_color=ft.Colors.with_opacity(0.15, ft.Colors.BLUE_700),
        border=ft.border.all(1, ft.Colors.BLUE_900),
        border_radius=8,
    )

    # ── Contenedor del formulario (inicialmente oculto) ───────────────────────
    form_container = ft.Container(visible=False)
    contador_text = ft.Text("", size=12, color=ft.Colors.BLUE_200)

    def recargar():
        """Recarga los datos de la tabla desde la DB."""
        db = SessionLocal()
        registros = db.query(modelo).order_by(modelo.id).all()
        db.close()

        tabla.rows = []
        total_activos = 0
        for r in registros:
            nombre_val = getattr(r, nombre_campo)
            activo = r.activo
            if activo:
                total_activos += 1

            def hacer_editar(reg_id=r.id, reg_nombre=nombre_val):
                def on_editar(e):
                    estado["editando_id"] = reg_id
                    estado["formulario_visible"] = True
                    campo_nombre.value = reg_nombre
                    campo_nombre.error_text = None
                    form_mensaje.value = ""
                    form_titulo.value = f"✏ Editando: {reg_nombre}"
                    form_container.visible = True
                    page.update()
                return on_editar

            def hacer_toggle(reg_id=r.id, reg_activo=activo):
                def on_toggle(e):
                    db = SessionLocal()
                    reg = db.query(modelo).filter(modelo.id == reg_id).first()
                    if reg:
                        reg.activo = not reg_activo
                        db.commit()
                    db.close()
                    color = ft.Colors.GREEN_800 if not reg_activo else ft.Colors.ORANGE_800
                    texto = f"{'✔ Activado' if not reg_activo else '✖ Desactivado'}"
                    mostrar_snackbar(page, texto, color)
                    recargar()
                return on_toggle

            color_estado = ft.Colors.GREEN_400 if activo else ft.Colors.RED_400
            texto_estado = "Activo" if activo else "Inactivo"
            texto_toggle = "Desactivar" if activo else "Activar"

            tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(r.id))),  # Sin color fijo
                        ft.DataCell(ft.Text(nombre_val)),
                        ft.DataCell(ft.Container(
                            content=ft.Text(texto_estado, size=12, weight="bold", color=color_estado),
                            bgcolor=ft.Colors.with_opacity(0.12, color_estado),
                            padding=ft.Padding(8, 4, 8, 4),
                            border_radius=20,
                        )),
                        ft.DataCell(
                            ft.Row([
                                ft.ElevatedButton(
                                    content=ft.Row([ft.Icon(ft.Icons.EDIT, size=14), ft.Text("Editar", size=12)], tight=True, spacing=4),
                                    bgcolor=ft.Colors.BLUE_700,
                                    color=ft.Colors.WHITE,
                                    on_click=hacer_editar(),
                                ),
                                ft.OutlinedButton(
                                    content=ft.Row([ft.Icon(ft.Icons.BLOCK if activo else ft.Icons.CHECK_CIRCLE, size=14), ft.Text(texto_toggle, size=12)], tight=True, spacing=4),
                                    on_click=hacer_toggle(),
                                ),
                            ], spacing=8)
                        ),
                    ]
                )
            )

        contador_text.value = f"Total: {len(registros)} registros ({total_activos} activos)"
        page.update()

    def guardar(e):
        nombre_val = campo_nombre.value.strip() if campo_nombre.value else ""
        if not nombre_val:
            campo_nombre.error_text = "El nombre es requerido"
            page.update()
            return
        campo_nombre.error_text = None

        db = SessionLocal()
        # Verificar si ya existe con ese nombre (solo entre los activos)
        ya_existe = db.query(modelo).filter(
            getattr(modelo, nombre_campo) == nombre_val,
            modelo.id != (estado["editando_id"] or -1)
        ).first()

        if ya_existe:
            form_mensaje.value = f"⚠ Ya existe un registro con el nombre '{nombre_val}'"
            db.close()
            page.update()
            return

        if estado["editando_id"]:
            # EDITAR
            reg = db.query(modelo).filter(modelo.id == estado["editando_id"]).first()
            if reg:
                setattr(reg, nombre_campo, nombre_val)
                db.commit()
                db.close()
                mostrar_snackbar(page, f"✔ '{nombre_val}' actualizado")
        else:
            # AGREGAR
            nuevo = modelo(**{nombre_campo: nombre_val})
            db.add(nuevo)
            db.commit()
            db.close()
            mostrar_snackbar(page, f"✔ '{nombre_val}' agregado")

        cancelar(None)
        recargar()

    def cancelar(e):
        estado["editando_id"] = None
        estado["formulario_visible"] = False
        campo_nombre.value = ""
        campo_nombre.error_text = None
        form_mensaje.value = ""
        form_container.visible = False
        page.update()

    def nuevo_registro(e):
        estado["editando_id"] = None
        estado["formulario_visible"] = True
        campo_nombre.value = ""
        campo_nombre.error_text = None
        form_mensaje.value = ""
        form_titulo.value = f"➕ Nuevo Registro"
        form_container.visible = True
        page.update()

    # ── Formulario inline ─────────────────────────────────────────────────────
    form_container.content = ft.Container(
        content=ft.Column([
            form_titulo,
            ft.Divider(color=ft.Colors.BLUE_900),
            ft.Row([campo_nombre], spacing=12),
            form_mensaje,
            ft.Row([
                ft.ElevatedButton(
                    content=ft.Row([ft.Icon(ft.Icons.SAVE, size=16), ft.Text("Guardar Cambios", size=13)], tight=True, spacing=6),
                    bgcolor=ft.Colors.GREEN_800, color=ft.Colors.WHITE, on_click=guardar,
                ),
                ft.OutlinedButton(
                    content=ft.Row([ft.Icon(ft.Icons.CANCEL, size=16), ft.Text("Cancelar", size=13)], tight=True, spacing=6),
                    on_click=cancelar,
                ),
            ], spacing=12),
        ], spacing=12),
        bgcolor=ft.Colors.with_opacity(0.08, ft.Colors.BLUE_700),
        padding=20,
        border_radius=10,
        border=ft.border.all(1, ft.Colors.GREEN_900),
    )

    # Carga inicial
    recargar()

    return ft.Column([
        ft.Row([
            ft.Text(titulo, size=18, weight="bold"),
            ft.Container(expand=True),
            contador_text,
            ft.ElevatedButton(
                content=ft.Row([ft.Icon(ft.Icons.ADD, size=16), ft.Text("Agregar Nuevo", size=13)], tight=True, spacing=6),
                bgcolor=ft.Colors.GREEN_800, color=ft.Colors.WHITE, on_click=nuevo_registro,
            ),
        ]),
        form_container,
        ft.Container(
            content=ft.Column([tabla], scroll=ft.ScrollMode.AUTO),
            expand=True,
        ),
    ], spacing=16, expand=True)


# ══════════════════════════════════════════════════════════════════════════════
#  Sección de Respaldos de Base de Datos
# ══════════════════════════════════════════════════════════════════════════════
def _build_respaldos(page: ft.Page):
    cfg = BackupManager.get_config()

    # ── Controles ────────────────────────────────────────────────────────────
    txt_ultimo = ft.Text(BackupManager.ultimo_respaldo_texto(), size=13, weight="bold")
    txt_carpeta = ft.TextField(
        label="Carpeta de respaldo", value=cfg.get("carpeta", ""),
        expand=True, read_only=False,
        hint_text="Ej: C:/Respaldos/ServicioSocial"
    )
    txt_estado = ft.Text("", size=12, color=ft.Colors.GREEN_400)

    swt_auto = ft.Switch(
        value=cfg.get("automatico", False),
        active_color=ft.Colors.BLUE_400,
        label="Respaldo automático al iniciar",
    )

    INTERVALOS = [
        ("1",  "Diario (cada 1 día)"),
        ("7",  "Semanal (cada 7 días)"),
        ("14", "Quincenal (cada 14 días)"),
        ("30", "Mensual (cada 30 días)"),
    ]
    dd_intervalo = ft.Dropdown(
        label="Intervalo", width=260,
        value=str(cfg.get("intervalo_dias", 7)),
        options=[ft.dropdown.Option(key=k, text=t) for k, t in INTERVALOS],
    )

    panel_auto = ft.Container(
        visible=cfg.get("automatico", False),
        content=ft.Column([
            ft.Text("Frecuencia del respaldo automático:", size=12, color=ft.Colors.WHITE54),
            dd_intervalo,
        ], spacing=8),
        padding=ft.padding.only(left=10, top=8),
    )

    def on_toggle_auto(e):
        panel_auto.visible = swt_auto.value
        page.update()

    swt_auto.on_change = on_toggle_auto

    # ── Selector de carpeta nativo (tkinter) ──────────────────────────────────
    import threading
    import tkinter as tk
    from tkinter import filedialog

    def elegir_carpeta(e):
        def abrir_dialogo():
            root = tk.Tk()
            root.withdraw()                     # Ocultar ventana principal de tk
            root.attributes("-topmost", True)   # Diálogo encima de todo
            carpeta = filedialog.askdirectory(
                title="Seleccionar carpeta de respaldo"
            )
            root.destroy()
            if carpeta:
                txt_carpeta.value = carpeta.replace("/", "\\")
                page.update()

        threading.Thread(target=abrir_dialogo, daemon=True).start()

    # ── Guardar config ────────────────────────────────────────────────────────
    def guardar_config(e):
        nuevo_cfg = BackupManager.get_config()
        nuevo_cfg["automatico"]    = swt_auto.value
        nuevo_cfg["intervalo_dias"] = int(dd_intervalo.value or 7)
        nuevo_cfg["carpeta"]        = txt_carpeta.value.strip() or nuevo_cfg["carpeta"]
        BackupManager.save_config(nuevo_cfg)
        txt_estado.value  = "✔ Configuración guardada"
        txt_estado.color  = ft.Colors.GREEN_400
        page.update()

    # ── Respaldo manual ───────────────────────────────────────────────────────
    def hacer_respaldo_manual(e):
        carpeta = txt_carpeta.value.strip() or None
        try:
            ruta = BackupManager.hacer_respaldo(carpeta)
            txt_estado.value = f"✔ Respaldo creado en:\n{ruta}"
            txt_estado.color = ft.Colors.GREEN_400
            txt_ultimo.value = BackupManager.ultimo_respaldo_texto()
        except Exception as ex:
            txt_estado.value = f"✖ Error: {str(ex)}"
            txt_estado.color = ft.Colors.RED_400
        page.update()

    # ── Layout ────────────────────────────────────────────────────────────────
    return ft.Column([
        ft.Row([
            ft.Icon(ft.Icons.BACKUP_ROUNDED, color=ft.Colors.BLUE_400, size=24),
            ft.Text("Respaldo de Base de Datos", size=18, weight="bold"),
        ], spacing=10),
        ft.Divider(color=ft.Colors.BLUE_900),

        # Card: Último respaldo
        ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.HISTORY_ROUNDED, color=ft.Colors.BLUE_400, size=20),
                ft.Column([
                    ft.Text("Último respaldo", size=11, weight="bold"),
                    txt_ultimo,
                ], spacing=2),
            ], spacing=12),
            bgcolor=ft.Colors.with_opacity(0.07, ft.Colors.BLUE_700),
            padding=16, border_radius=10,
        ),

        # Card: Carpeta destino
        ft.Container(
            content=ft.Column([
                ft.Text("Carpeta de destino", size=13, weight="bold"),
                ft.Row([
                    txt_carpeta,
                    ft.IconButton(
                        ft.Icons.FOLDER_OPEN_ROUNDED,
                        tooltip="Buscar carpeta",
                        icon_color=ft.Colors.BLUE_400,
                        on_click=elegir_carpeta,
                    ),
                ], spacing=8),
            ], spacing=8),
            bgcolor=ft.Colors.with_opacity(0.07, ft.Colors.BLUE_700),
            padding=16, border_radius=10,
        ),

        # Card: Automático
        ft.Container(
            content=ft.Column([
                swt_auto,
                panel_auto,
            ], spacing=4),
            bgcolor=ft.Colors.with_opacity(0.07, ft.Colors.BLUE_700),
            padding=16, border_radius=10,
        ),

        # Acciones
        ft.Row([
            ft.ElevatedButton(
                content=ft.Row([ft.Icon(ft.Icons.SAVE_ROUNDED, size=16), ft.Text("Guardar configuración", size=13)], tight=True, spacing=6),
                bgcolor=ft.Colors.BLUE_800, color=ft.Colors.WHITE,
                on_click=guardar_config,
            ),
            ft.ElevatedButton(
                content=ft.Row([ft.Icon(ft.Icons.BACKUP_ROUNDED, size=16), ft.Text("Hacer Respaldo Ahora", size=13)], tight=True, spacing=6),
                bgcolor=ft.Colors.GREEN_800, color=ft.Colors.WHITE,
                on_click=hacer_respaldo_manual,
            ),
        ], spacing=12),
        txt_estado,
    ], spacing=16, scroll=ft.ScrollMode.AUTO)



# ══════════════════════════════════════════════════════════════════════════════
#  Helper: Tabla CRUD para escuelas profesionales (con relaciones)
# ══════════════════════════════════════════════════════════════════════════════
def _tabla_crud_escuelas(page):
    """
    Genera una vista completa CRUD para Escuelas Profesionales.
    Muestra tabla con columnas: ID, Nombre, Facultad, Estado, Acciones.
    """
    estado = {
        "editando_id": None,
        "formulario_visible": False,
    }

    # ── Elementos del formulario ──────────────────────────────────────────────
    campo_nombre = ft.TextField(
        label="Nombre de la Escuela Profesional",
        expand=True,
        border_color=ft.Colors.BLUE_700,
        focused_border_color=ft.Colors.GREEN_400,
    )
    
    dropdown_facultad = ft.Dropdown(
        label="Facultad",
        expand=True,
        border_color=ft.Colors.BLUE_700,
        focused_border_color=ft.Colors.GREEN_400,
    )
    
    form_titulo = ft.Text("", size=16, weight="bold", color=ft.Colors.GREEN_400)
    form_mensaje = ft.Text("", color=ft.Colors.RED_400, size=12)

    # ── Tabla ─────────────────────────────────────────────────────────────────
    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", weight="bold")),
            ft.DataColumn(ft.Text("Nombre", weight="bold")),
            ft.DataColumn(ft.Text("Facultad", weight="bold")),
            ft.DataColumn(ft.Text("Estado", weight="bold")),
            ft.DataColumn(ft.Text("Acciones", weight="bold")),
        ],
        rows=[],
        column_spacing=24,
        heading_row_color=ft.Colors.with_opacity(0.15, ft.Colors.BLUE_700),
        border=ft.border.all(1, ft.Colors.BLUE_900),
        border_radius=8,
    )

    form_container = ft.Container(visible=False)
    contador_text = ft.Text("", size=12)

    def cargar_facultades():
        db = SessionLocal()
        facs = db.query(CatFacultad).filter(CatFacultad.activo == True).order_by(CatFacultad.nombre).all()
        db.close()
        dropdown_facultad.options = [ft.dropdown.Option(str(f.id), f.nombre) for f in facs]

    def recargar():
        db = SessionLocal()
        registros = db.query(CatEscuela).outerjoin(CatFacultad).order_by(CatEscuela.nombre).all()
        
        tabla.rows = []
        total_activos = 0
        for r in registros:
            nombre_val = r.nombre
            fac_nombre = r.facultad.nombre if r.facultad else "Sin Facultad"
            activo = r.activo
            if activo:
                total_activos += 1

            def hacer_editar(reg_id=r.id, reg_nombre=nombre_val, fac_id=r.facultad_id):
                def on_editar(e):
                    cargar_facultades()
                    estado["editando_id"] = reg_id
                    estado["formulario_visible"] = True
                    campo_nombre.value = reg_nombre
                    dropdown_facultad.value = str(fac_id) if fac_id else None
                    campo_nombre.error_text = None
                    dropdown_facultad.error_text = None
                    form_mensaje.value = ""
                    form_titulo.value = f"✏ Editando Escuela: {reg_nombre}"
                    form_container.visible = True
                    page.update()
                return on_editar

            def hacer_toggle(reg_id=r.id, reg_activo=activo):
                def on_toggle(e):
                    db = SessionLocal()
                    reg = db.query(CatEscuela).filter(CatEscuela.id == reg_id).first()
                    if reg:
                        reg.activo = not reg_activo
                        db.commit()
                    db.close()
                    color = ft.Colors.GREEN_800 if not reg_activo else ft.Colors.ORANGE_800
                    texto = f"{'✔ Activado' if not reg_activo else '✖ Desactivado'}"
                    mostrar_snackbar(page, texto, color)
                    recargar()
                return on_toggle

            color_estado = ft.Colors.GREEN_400 if activo else ft.Colors.RED_400
            texto_estado = "Activo" if activo else "Inactivo"
            texto_toggle = "Desactivar" if activo else "Activar"

            tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(r.id))),
                        ft.DataCell(ft.Text(nombre_val)),
                        ft.DataCell(ft.Text(fac_nombre)),
                        ft.DataCell(ft.Container(
                            content=ft.Text(texto_estado, size=12, weight="bold", color=color_estado),
                            bgcolor=ft.Colors.with_opacity(0.12, color_estado),
                            padding=ft.Padding(8, 4, 8, 4),
                            border_radius=20,
                        )),
                        ft.DataCell(
                            ft.Row([
                                ft.ElevatedButton(
                                    content=ft.Row([ft.Icon(ft.Icons.EDIT, size=14), ft.Text("Editar", size=12)], tight=True, spacing=4),
                                    bgcolor=ft.Colors.BLUE_700,
                                    color=ft.Colors.WHITE,
                                    on_click=hacer_editar(),
                                ),
                                ft.OutlinedButton(
                                    content=ft.Row([ft.Icon(ft.Icons.BLOCK if activo else ft.Icons.CHECK_CIRCLE, size=14), ft.Text(texto_toggle, size=12)], tight=True, spacing=4),
                                    on_click=hacer_toggle(),
                                ),
                            ], spacing=8)
                        ),
                    ]
                )
            )
        db.close()
        contador_text.value = f"Total: {len(registros)} escuelas ({total_activos} activas)"
        page.update()

    def guardar(e):
        nombre_val = campo_nombre.value.strip() if campo_nombre.value else ""
        fac_id_val = dropdown_facultad.value
        
        has_error = False
        if not nombre_val:
            campo_nombre.error_text = "El nombre es requerido"
            has_error = True
        else:
            campo_nombre.error_text = None
            
        if not fac_id_val:
            dropdown_facultad.error_text = "Debe seleccionar una facultad"
            has_error = True
        else:
            dropdown_facultad.error_text = None

        if has_error:
            page.update()
            return

        db = SessionLocal()
        ya_existe = db.query(CatEscuela).filter(
            CatEscuela.nombre == nombre_val,
            CatEscuela.facultad_id == int(fac_id_val),
            CatEscuela.id != (estado["editando_id"] or -1)
        ).first()

        if ya_existe:
            form_mensaje.value = f"⚠ Ya existe la escuela '{nombre_val}' en la facultad seleccionada"
            db.close()
            page.update()
            return

        if estado["editando_id"]:
            # EDITAR
            reg = db.query(CatEscuela).filter(CatEscuela.id == estado["editando_id"]).first()
            if reg:
                reg.nombre = nombre_val
                reg.facultad_id = int(fac_id_val)
                db.commit()
                db.close()
                mostrar_snackbar(page, f"✔ '{nombre_val}' actualizada")
        else:
            # AGREGAR
            nuevo = CatEscuela(nombre=nombre_val, facultad_id=int(fac_id_val))
            db.add(nuevo)
            db.commit()
            db.close()
            mostrar_snackbar(page, f"✔ '{nombre_val}' agregada")

        cancelar(None)
        recargar()

    def cancelar(e):
        estado["editando_id"] = None
        estado["formulario_visible"] = False
        campo_nombre.value = ""
        dropdown_facultad.value = None
        campo_nombre.error_text = None
        dropdown_facultad.error_text = None
        form_mensaje.value = ""
        form_container.visible = False
        page.update()

    def nuevo_registro(e):
        cargar_facultades()
        estado["editando_id"] = None
        estado["formulario_visible"] = True
        campo_nombre.value = ""
        dropdown_facultad.value = None
        campo_nombre.error_text = None
        dropdown_facultad.error_text = None
        form_mensaje.value = ""
        form_titulo.value = f"➕ Nueva Escuela Profesional"
        form_container.visible = True
        page.update()

    form_container.content = ft.Container(
        content=ft.Column([
            form_titulo,
            ft.Divider(color=ft.Colors.BLUE_900),
            ft.Row([campo_nombre, dropdown_facultad], spacing=12),
            form_mensaje,
            ft.Row([
                ft.ElevatedButton(
                    content=ft.Row([ft.Icon(ft.Icons.SAVE, size=16), ft.Text("Guardar Cambios", size=13)], tight=True, spacing=6),
                    bgcolor=ft.Colors.GREEN_800, color=ft.Colors.WHITE, on_click=guardar,
                ),
                ft.OutlinedButton(
                    content=ft.Row([ft.Icon(ft.Icons.CANCEL, size=16), ft.Text("Cancelar", size=13)], tight=True, spacing=6),
                    on_click=cancelar,
                ),
            ], spacing=12),
        ], spacing=12),
        bgcolor=ft.Colors.with_opacity(0.08, ft.Colors.BLUE_700),
        padding=20,
        border_radius=10,
        border=ft.border.all(1, ft.Colors.GREEN_900),
    )

    recargar()

    return ft.Column([
        ft.Row([
            ft.Text("Escuelas Profesionales", size=18, weight="bold"),
            ft.Container(expand=True),
            contador_text,
            ft.ElevatedButton(
                content=ft.Row([ft.Icon(ft.Icons.ADD, size=16), ft.Text("Agregar Nuevo", size=13)], tight=True, spacing=6),
                bgcolor=ft.Colors.GREEN_800, color=ft.Colors.WHITE, on_click=nuevo_registro,
            ),
        ]),
        form_container,
        ft.Container(
            content=ft.Column([tabla], scroll=ft.ScrollMode.AUTO),
            expand=True,
        ),
    ], spacing=16, expand=True)


# ══════════════════════════════════════════════════════════════════════════════
#  Vista de Configuración Principal
# ══════════════════════════════════════════════════════════════════════════════
def build_config_view(page: ft.Page):

    """Vista con 3 secciones de gestión de catálogos."""

    contenido = ft.Container(expand=True)

    def cargar_seccion(seccion):
        if seccion == "tipos":
            contenido.content = _tabla_crud_simple(
                page, CatTipoUsuario, nombre_campo="nombre", titulo="Tipos de Usuario"
            )
        elif seccion == "casos":
            contenido.content = _tabla_crud_simple(
                page, CatCasoSocial, nombre_campo="nombre", titulo="Casos Sociales"
            )
        elif seccion == "facultades":
            contenido.content = _tabla_crud_simple(
                page, CatFacultad, nombre_campo="nombre", titulo="Facultades"
            )
        elif seccion == "escuelas":
            contenido.content = _tabla_crud_escuelas(page)
        elif seccion == "respaldos":
            contenido.content = _build_respaldos(page)
        page.update()

    # Botones de navegación entre secciones (reemplazo a Tabs)
    def btn_nav(label, seccion, icon):
        def on_click(e):
            cargar_seccion(seccion)
        return ft.ElevatedButton(
            content=ft.Row([ft.Icon(icon, size=16), ft.Text(label, size=13)], tight=True, spacing=6),
            bgcolor=ft.Colors.BLUE_900,
            color=ft.Colors.WHITE,
            on_click=on_click,
        )

    # Cargar sección por defecto
    cargar_seccion("tipos")

    return ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.SETTINGS_ROUNDED, color=ft.Colors.GREEN_400, size=26),
                ft.Text("Configuración de Catálogos", size=20, weight="bold"),
            ], spacing=10),
            ft.Divider(color=ft.Colors.BLUE_900),

            # Navegación por secciones
            ft.Container(
                content=ft.Row([
                    btn_nav("Tipos de Usuario", "tipos", ft.Icons.PERSON_ROUNDED),
                    btn_nav("Casos Sociales", "casos", ft.Icons.LABEL_ROUNDED),
                    btn_nav("Facultades", "facultades", ft.Icons.SCHOOL_ROUNDED),
                    btn_nav("Escuelas", "escuelas", ft.Icons.CLASS_ROUNDED),
                    btn_nav("Respaldos", "respaldos", ft.Icons.BACKUP_ROUNDED),
                ], spacing=12),
                bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.BLUE_700),
                padding=12,
                border_radius=8,
            ),

            contenido,
        ], spacing=16, expand=True),
        padding=20,
        expand=True,
    )
