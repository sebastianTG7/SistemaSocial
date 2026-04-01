import flet as ft
from database.db_config import SessionLocal
from database.models import CatFacultad, CatEscuela, CatCasoSocial, CatTipoUsuario
from core.ui_helpers import mostrar_snackbar


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
                        ft.DataCell(ft.Text(str(r.id), color=ft.Colors.WHITE_54)),
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
