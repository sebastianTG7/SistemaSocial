import flet as ft
from database.db_config import SessionLocal
from database.models import User
from core.security import hash_password, verify_password
from core.ui_helpers import mostrar_exito, mostrar_snackbar


def build_cuentas_view(page: ft.Page):
    """Vista de Gestión de Cuentas del Sistema (solo para administradores)."""

    # ── Helpers Diálogos ─────────────────────────────────────────────────────
    def mostrar_dialogo(dlg):
        for c in list(page.overlay):
            if isinstance(c, ft.AlertDialog):
                page.overlay.remove(c)
        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    def cerrar_dialogo(dlg):
        dlg.open = False
        page.update()

    # ── Tabla ────────────────────────────────────────────────────────────────
    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", weight="bold")),
            ft.DataColumn(ft.Text("Usuario", weight="bold")),
            ft.DataColumn(ft.Text("Nombre Completo", weight="bold")),
            ft.DataColumn(ft.Text("Cargo", weight="bold")),
            ft.DataColumn(ft.Text("Rol", weight="bold")),
            ft.DataColumn(ft.Text("Estado", weight="bold")),
            ft.DataColumn(ft.Text("Acciones", weight="bold")),
        ],
        rows=[],
        column_spacing=20,
        heading_row_color=ft.Colors.with_opacity(0.15, ft.Colors.BLUE_700),
        border=ft.border.all(1, ft.Colors.BLUE_900),
        border_radius=8,
    )

    estado_form = {"visible": False, "editando_id": None}

    # ── Campos del formulario ────────────────────────────────────────────────
    campo_usuario = ft.TextField(
        label="Usuario (login)", width=200,
        border_color=ft.Colors.BLUE_700, focused_border_color=ft.Colors.GREEN_400,
    )
    campo_nombre = ft.TextField(
        label="Nombre Completo", width=250,
        border_color=ft.Colors.BLUE_700, focused_border_color=ft.Colors.GREEN_400,
    )
    campo_cargo = ft.TextField(
        label="Cargo", width=200,
        border_color=ft.Colors.BLUE_700, focused_border_color=ft.Colors.GREEN_400,
    )
    campo_password = ft.TextField(
        label="Contraseña", width=200, password=True, can_reveal_password=True,
        border_color=ft.Colors.BLUE_700, focused_border_color=ft.Colors.GREEN_400,
    )
    campo_rol = ft.Dropdown(
        label="Rol", width=180,
        options=[
            ft.dropdown.Option("operador", "Operador"),
            ft.dropdown.Option("administrador", "Administrador"),
        ],
        value="operador",
        border_color=ft.Colors.BLUE_700, focused_border_color=ft.Colors.GREEN_400,
    )
    form_titulo = ft.Text("", size=16, weight="bold", color=ft.Colors.GREEN_400)
    form_mensaje = ft.Text("", color=ft.Colors.RED_400, size=12)

    form_container = ft.Container(visible=False)

    # ── Cargar datos ─────────────────────────────────────────────────────────
    def cargar_datos():
        db = SessionLocal()
        cuentas = db.query(User).order_by(User.id).all()
        db.close()

        tabla.rows = []
        for c in cuentas:
            estado_txt = "Activo" if c.activo else "Inactivo"
            estado_color = ft.Colors.GREEN_400 if c.activo else ft.Colors.RED_400
            rol_txt = "Administrador" if c.rol == "administrador" else "Operador"

            # Crear closures para las acciones
            def hacer_editar(cid=c.id, usr=c.username, nom=c.nombre_completo,
                             car=c.cargo or "", rol=c.rol):
                def on_click(e):
                    abrir_formulario_editar(cid, usr, nom, car, rol)
                return on_click

            def hacer_cambiar_pass(cid=c.id, usr=c.username):
                def on_click(e):
                    abrir_dialogo_password(cid, usr)
                return on_click

            def hacer_toggle(cid=c.id, nom=c.nombre_completo, act=c.activo):
                def on_click(e):
                    toggle_estado(cid, nom, act)
                return on_click

            # Botones de acción: editar y cambiar contraseña siempre visibles
            botones_acciones = [
                ft.IconButton(
                    ft.Icons.EDIT_ROUNDED, icon_size=18,
                    icon_color=ft.Colors.BLUE_400,
                    tooltip="Editar cuenta",
                    on_click=hacer_editar(),
                ),
                ft.IconButton(
                    ft.Icons.KEY_ROUNDED, icon_size=18,
                    icon_color=ft.Colors.ORANGE_400,
                    tooltip="Cambiar contraseña",
                    on_click=hacer_cambiar_pass(),
                ),
            ]

            # El botón de activar/desactivar NO se muestra para administradores
            if c.rol != "administrador":
                botones_acciones.append(
                    ft.IconButton(
                        ft.Icons.TOGGLE_ON_ROUNDED if c.activo else ft.Icons.TOGGLE_OFF_ROUNDED,
                        icon_size=18,
                        icon_color=ft.Colors.GREEN_400 if c.activo else ft.Colors.RED_400,
                        tooltip="Desactivar" if c.activo else "Activar",
                        on_click=hacer_toggle(),
                    )
                )

            acciones = ft.Row(botones_acciones, spacing=0)

            tabla.rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(str(c.id))),
                ft.DataCell(ft.Text(c.username, weight="bold")),
                ft.DataCell(ft.Text(c.nombre_completo or "")),
                ft.DataCell(ft.Text(c.cargo or "")),
                ft.DataCell(ft.Text(rol_txt)),
                ft.DataCell(ft.Text(estado_txt, color=estado_color)),
                ft.DataCell(acciones),
            ]))

        page.update()

    # ── Formulario: Nueva cuenta ─────────────────────────────────────────────
    def abrir_formulario_nuevo(e=None):
        estado_form["editando_id"] = None
        form_titulo.value = "➕ Nueva Cuenta del Sistema"
        campo_usuario.value = ""
        campo_usuario.disabled = False
        campo_nombre.value = ""
        campo_cargo.value = ""
        campo_password.value = ""
        campo_password.visible = True
        campo_rol.value = "operador"
        form_mensaje.value = ""
        form_container.visible = True
        page.update()

    # ── Formulario: Editar cuenta ────────────────────────────────────────────
    def abrir_formulario_editar(cid, username, nombre, cargo, rol):
        estado_form["editando_id"] = cid
        form_titulo.value = f"✏️ Editando cuenta: {username}"
        campo_usuario.value = username
        campo_usuario.disabled = True  # No se puede cambiar el username
        campo_nombre.value = nombre
        campo_cargo.value = cargo
        campo_password.value = ""
        campo_password.visible = False  # No se edita la contraseña aquí
        campo_rol.value = rol
        form_mensaje.value = ""
        form_container.visible = True
        page.update()

    # ── Guardar (crear o editar) ─────────────────────────────────────────────
    def guardar(e):
        nombre = (campo_nombre.value or "").strip()
        cargo = (campo_cargo.value or "").strip()
        rol = campo_rol.value

        if not nombre:
            form_mensaje.value = "⚠ El nombre completo es obligatorio."
            page.update()
            return

        db = SessionLocal()
        try:
            if estado_form["editando_id"] is None:
                # ── Crear nueva cuenta ──
                username = (campo_usuario.value or "").strip().lower()
                password = (campo_password.value or "").strip()

                if not username:
                    form_mensaje.value = "⚠ El usuario es obligatorio."
                    page.update()
                    return
                if not password:
                    form_mensaje.value = "⚠ La contraseña es obligatoria."
                    page.update()
                    return
                if len(password) < 4:
                    form_mensaje.value = "⚠ La contraseña debe tener al menos 4 caracteres."
                    page.update()
                    return

                # Verificar duplicado
                existente = db.query(User).filter(User.username == username).first()
                if existente:
                    form_mensaje.value = f"⚠ Ya existe una cuenta con el usuario '{username}'."
                    page.update()
                    return

                nuevo = User(
                    username=username,
                    password_hash=hash_password(password),
                    nombre_completo=nombre,
                    cargo=cargo,
                    rol=rol,
                )
                db.add(nuevo)
                db.commit()
                mostrar_exito(page, f"Cuenta '{username}' creada correctamente.")

            else:
                # ── Editar cuenta existente ──
                user = db.query(User).filter(User.id == estado_form["editando_id"]).first()
                if user:
                    user.nombre_completo = nombre
                    user.cargo = cargo
                    user.rol = rol
                    db.commit()
                    mostrar_exito(page, f"Cuenta '{user.username}' actualizada.")
        finally:
            db.close()

        form_container.visible = False
        cargar_datos()

    def cancelar_form(e):
        form_container.visible = False
        page.update()

    # ── Diálogo: Cambiar contraseña ──────────────────────────────────────────
    def abrir_dialogo_password(user_id, username):
        campo_nueva_pass = ft.TextField(
            label="Nueva contraseña", password=True, can_reveal_password=True,
            width=300, border_color=ft.Colors.BLUE_700,
        )
        campo_confirmar_pass = ft.TextField(
            label="Confirmar contraseña", password=True, can_reveal_password=True,
            width=300, border_color=ft.Colors.BLUE_700,
        )
        msg_error = ft.Text("", color=ft.Colors.RED_400, size=12)

        dlg = ft.AlertDialog(modal=True)

        def al_guardar(e):
            nueva = (campo_nueva_pass.value or "").strip()
            confirmar = (campo_confirmar_pass.value or "").strip()

            if not nueva:
                msg_error.value = "⚠ Ingrese la nueva contraseña."
                page.update()
                return
            if len(nueva) < 4:
                msg_error.value = "⚠ Mínimo 4 caracteres."
                page.update()
                return
            if nueva != confirmar:
                msg_error.value = "⚠ Las contraseñas no coinciden."
                page.update()
                return

            db = SessionLocal()
            try:
                user = db.query(User).filter(User.id == user_id).first()
                if user:
                    user.password_hash = hash_password(nueva)
                    db.commit()
                    cerrar_dialogo(dlg)
                    mostrar_exito(page, f"Contraseña de '{username}' cambiada correctamente.")
            finally:
                db.close()

        def al_cancelar(e):
            cerrar_dialogo(dlg)

        dlg.title = ft.Text(f"🔑 Cambiar Contraseña: {username}")
        dlg.content = ft.Column([
            ft.Text("Ingrese la nueva contraseña para esta cuenta.", size=13),
            ft.Container(height=10),
            campo_nueva_pass,
            campo_confirmar_pass,
            msg_error,
        ], tight=True, spacing=10)
        dlg.actions = [
            ft.TextButton("Cancelar", on_click=al_cancelar),
            ft.ElevatedButton("Guardar", on_click=al_guardar,
                              bgcolor=ft.Colors.GREEN_700, color=ft.Colors.WHITE),
        ]
        dlg.actions_alignment = "end"
        mostrar_dialogo(dlg)

    # ── Toggle activar/desactivar ────────────────────────────────────────────
    def toggle_estado(user_id, nombre, activo_actual):
        accion = "desactivar" if activo_actual else "activar"
        dlg = ft.AlertDialog(modal=True)

        def al_si(e):
            db = SessionLocal()
            try:
                user = db.query(User).filter(User.id == user_id).first()
                if user:
                    user.activo = not activo_actual
                    db.commit()
            finally:
                db.close()
            cerrar_dialogo(dlg)
            estado_txt = "activada" if not activo_actual else "desactivada"
            mostrar_exito(page, f"Cuenta de '{nombre}' {estado_txt}.")
            cargar_datos()

        def al_no(e):
            cerrar_dialogo(dlg)

        dlg.title = ft.Text(f"Confirmar {accion.capitalize()}")
        dlg.content = ft.Text(
            f"¿Está seguro de {accion} la cuenta de '{nombre}'?\n\n"
            + ("La cuenta no podrá iniciar sesión." if activo_actual
               else "La cuenta podrá iniciar sesión nuevamente.")
        )
        dlg.actions = [
            ft.TextButton("Cancelar", on_click=al_no),
            ft.ElevatedButton(
                f"Sí, {accion.capitalize()}",
                on_click=al_si,
                bgcolor=ft.Colors.RED_700 if activo_actual else ft.Colors.GREEN_700,
                color=ft.Colors.WHITE,
            ),
        ]
        dlg.actions_alignment = "end"
        mostrar_dialogo(dlg)

    # ── Construir formulario ─────────────────────────────────────────────────
    form_container.content = ft.Container(
        content=ft.Column([
            form_titulo,
            ft.Divider(color=ft.Colors.BLUE_900),
            ft.ResponsiveRow([
                ft.Container(campo_usuario, col={"sm": 12, "md": 4}),
                ft.Container(campo_nombre, col={"sm": 12, "md": 4}),
                ft.Container(campo_cargo, col={"sm": 12, "md": 4}),
            ]),
            ft.ResponsiveRow([
                ft.Container(campo_password, col={"sm": 12, "md": 4}),
                ft.Container(campo_rol, col={"sm": 12, "md": 4}),
            ]),
            form_mensaje,
            ft.Row([
                ft.ElevatedButton("Guardar", icon=ft.Icons.SAVE_ROUNDED,
                                  on_click=guardar,
                                  bgcolor=ft.Colors.GREEN_700, color=ft.Colors.WHITE),
                ft.OutlinedButton("Cancelar", icon=ft.Icons.CANCEL_ROUNDED,
                                  on_click=cancelar_form),
            ], spacing=10),
        ], spacing=12),
        padding=20,
        border=ft.border.all(1, ft.Colors.GREEN_900),
        border_radius=10,
        bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.GREEN_700),
    )

    # ── Carga inicial ────────────────────────────────────────────────────────
    cargar_datos()

    # ── Layout final ─────────────────────────────────────────────────────────
    return ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.ADMIN_PANEL_SETTINGS_ROUNDED,
                        color=ft.Colors.GREEN_400, size=26),
                ft.Text("Gestionar Cuentas del Sistema", size=20, weight="bold"),
                ft.Container(expand=True),
                ft.ElevatedButton(
                    "Nueva Cuenta",
                    icon=ft.Icons.PERSON_ADD_ALT_1_ROUNDED,
                    on_click=abrir_formulario_nuevo,
                    bgcolor=ft.Colors.BLUE_700,
                    color=ft.Colors.WHITE,
                ),
            ], spacing=10),
            ft.Divider(color=ft.Colors.BLUE_900),
            form_container,
            ft.Container(
                content=ft.Column([tabla], scroll=ft.ScrollMode.AUTO),
                expand=True,
            ),
        ], spacing=16, expand=True),
        padding=20,
        expand=True,
    )
