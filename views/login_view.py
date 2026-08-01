import flet as ft
import asyncio
import os
import sys
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog
from controllers.auth_controller import AuthController
from core.import_manager import ImportManager


class LoginView(ft.Container):
    def __init__(self, page: ft.Page, on_login_success):
        super().__init__()
        self.main_page   = page
        self.on_login_success = on_login_success

        self.expand    = True
        self.bgcolor   = "#0f111a"
        self.alignment = ft.Alignment(0, 0)

        # ── Campos de login ───────────────────────────────────────────────────
        self.username_field = ft.TextField(
            label="Usuario",
            prefix_icon=ft.Icons.PERSON_OUTLINED,
            border_radius=15,
            border_color="#1e293b",
            focused_border_color="#0ea5e9",
            bgcolor="#1e293b",
            color=ft.Colors.WHITE,
            label_style=ft.TextStyle(color=ft.Colors.WHITE70),
            width=300,
            on_submit=self.handle_login,
        )

        self.password_field = ft.TextField(
            label="Contrasena",
            prefix_icon=ft.Icons.LOCK_OUTLINED,
            password=True,
            can_reveal_password=True,
            border_radius=15,
            border_color="#1e293b",
            focused_border_color="#0ea5e9",
            bgcolor="#1e293b",
            color=ft.Colors.WHITE,
            label_style=ft.TextStyle(color=ft.Colors.WHITE70),
            width=300,
            on_submit=self.handle_login,
        )

        self.login_button = ft.Container(
            content=ft.Text("Iniciar Sesion", weight="bold", color="#0ea5e9"),
            alignment=ft.Alignment(0, 0),
            width=300,
            height=50,
            bgcolor="#1e293b",
            border_radius=15,
            on_click=self.handle_login,
        )

        self.error_text = ft.Text("", color=ft.Colors.RED_400, weight="bold", size=12)

        # ── Botón de restaurar base de datos ──────────────────────────────────
        btn_restaurar = ft.TextButton(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.UPLOAD_FILE_OUTLINED, size=14, color=ft.Colors.WHITE38),
                    ft.Text(
                        "Restaurar base de datos",
                        size=12,
                        color=ft.Colors.WHITE38,
                    ),
                ],
                spacing=6,
                tight=True,
            ),
            on_click=self._abrir_importar,
        )

        # ── Panel formulario (izquierda) ──────────────────────────────────────
        form_panel = ft.Container(
            expand=1,
            content=ft.Column(
                [
                    ft.Column(
                        [
                            ft.Text(
                                "SERVICIO SOCIAL",
                                size=32,
                                weight="bold",
                                color=ft.Colors.WHITE,
                            ),
                            ft.Container(height=2, width=100, bgcolor="#0ea5e9"),
                        ],
                        horizontal_alignment="center",
                        spacing=6,
                    ),
                    ft.Container(height=40),
                    ft.Text("Iniciar Sesion", size=22, weight="bold", color=ft.Colors.WHITE),
                    ft.Container(height=15),
                    self.username_field,
                    ft.Container(height=5),
                    self.password_field,
                    ft.Container(height=10),
                    self.error_text,
                    ft.Container(height=20),
                    self.login_button,
                    ft.Container(height=12),
                    btn_restaurar,
                ],
                horizontal_alignment="center",
                alignment="center",
            ),
        )

        # ── Panel logo (derecha) ──────────────────────────────────────────────
        image_panel = ft.Container(
            expand=1,
            alignment=ft.Alignment(0, 0),
            padding=ft.padding.only(right=40, top=20, bottom=20),
            content=ft.Image(src="logo_view.png", width=500, height=500),
        )

        self.content = ft.Row(
            [form_panel, image_panel],
            alignment="center",
            expand=True,
        )

    # ── Login ─────────────────────────────────────────────────────────────────
    def handle_login(self, e):
        self.login_button.disabled = True
        self.main_page.update()

        user = AuthController.login(
            self.username_field.value, self.password_field.value
        )
        if user:
            self.error_text.value = ""
            # Detectar si el admin ingreso con la contrasena por defecto
            if (user.get("username") == "admin"
                    and self._es_clave_defecto(self.password_field.value)):
                self._pedir_cambio_contrasena(user)
            else:
                self.on_login_success(user)
        else:
            self.error_text.value = "Usuario o contrasena incorrectos"
            self.login_button.disabled = False
            self.main_page.update()

    @staticmethod
    def _es_clave_defecto(password: str) -> bool:
        return password == "admin123"

    def _pedir_cambio_contrasena(self, user: dict):
        """Modal obligatorio: el admin debe cambiar la contrasena antes de entrar."""
        nueva_field = ft.TextField(
            label="Nueva contrasena",
            prefix_icon=ft.Icons.LOCK_OUTLINED,
            password=True,
            can_reveal_password=True,
            border_radius=10,
            border_color=ft.Colors.WHITE12,
            focused_border_color=ft.Colors.BLUE_400,
            bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE),
            color=ft.Colors.WHITE,
            label_style=ft.TextStyle(color=ft.Colors.WHITE54),
        )
        confirmar_field = ft.TextField(
            label="Confirmar contrasena",
            prefix_icon=ft.Icons.LOCK_OUTLINED,
            password=True,
            can_reveal_password=True,
            border_radius=10,
            border_color=ft.Colors.WHITE12,
            focused_border_color=ft.Colors.BLUE_400,
            bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE),
            color=ft.Colors.WHITE,
            label_style=ft.TextStyle(color=ft.Colors.WHITE54),
        )
        txt_error = ft.Text("", size=12, color=ft.Colors.RED_300)

        def guardar(_):
            nueva     = nueva_field.value.strip()
            confirmar = confirmar_field.value.strip()

            if len(nueva) < 6:
                txt_error.value = "La contrasena debe tener al menos 6 caracteres."
                self.main_page.update()
                return
            if nueva != confirmar:
                txt_error.value = "Las contrasenas no coinciden."
                self.main_page.update()
                return

            # Guardar nueva contrasena en la BD activa
            from controllers.auth_controller import AuthController as AC
            ok = AC.cambiar_password(user["id"], nueva)
            if not ok:
                txt_error.value = "Error al guardar la contrasena. Intenta de nuevo."
                self.main_page.update()
                return

            dlg.open = False
            self.main_page.update()
            self.on_login_success(user)

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Column(
                [
                    ft.Text(
                        "Cambio de contrasena requerido",
                        size=16,
                        weight=ft.FontWeight.W_600,
                        color=ft.Colors.WHITE,
                    ),
                    ft.Text(
                        "Estas ingresando con la contrasena por defecto. "
                        "Por seguridad debes establecer una nueva contrasena antes de continuar.",
                        size=12,
                        color=ft.Colors.WHITE54,
                    ),
                ],
                spacing=4,
                tight=True,
            ),
            content=ft.Column(
                [
                    ft.Divider(height=1, color=ft.Colors.WHITE10),
                    nueva_field,
                    confirmar_field,
                    txt_error,
                ],
                spacing=12,
                tight=True,
            ),
            actions=[
                ft.FilledButton(
                    "Guardar y continuar",
                    icon=ft.Icons.CHECK_ROUNDED,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.BLUE_700,
                        color=ft.Colors.WHITE,
                    ),
                    on_click=guardar,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.main_page.overlay.append(dlg)
        dlg.open = True
        self.login_button.disabled = False
        self.main_page.update()

    # ── Importar desde login ──────────────────────────────────────────────────
    def _abrir_importar(self, e):
        """Abre el overlay de importacion sobre la pantalla de login."""
        overlay = _ImportarOverlay(self.main_page, on_close=self._cerrar_importar)
        self.main_page.overlay.append(overlay)
        self.main_page.update()
        self._overlay_ref = overlay

    def _cerrar_importar(self):
        try:
            self.main_page.overlay.remove(self._overlay_ref)
        except Exception:
            pass
        self.main_page.update()


# ── Overlay de importacion ────────────────────────────────────────────────────
class _ImportarOverlay(ft.Container):
    """
    Panel modal que se pone encima del login para seleccionar e importar
    un archivo .db. Al completar la importacion, reinicia la aplicacion.
    """

    def __init__(self, page: ft.Page, on_close):
        super().__init__()
        self._page    = page
        self._on_close = on_close
        self._ruta    = {"valor": None}

        # Ocupa toda la pantalla con fondo semitransparente
        self.expand        = True
        self.bgcolor       = ft.Colors.with_opacity(0.88, "#0f111a")
        self.alignment     = ft.Alignment(0, 0)

        # ── Controles internos ────────────────────────────────────────────────
        self._icono = ft.Icon(ft.Icons.CLOUD_UPLOAD_OUTLINED, size=48, color=ft.Colors.BLUE_300)
        self._txt_archivo = ft.Text(
            "Ningun archivo seleccionado",
            size=13,
            color=ft.Colors.WHITE38,
            text_align=ft.TextAlign.CENTER,
        )
        self._card_resumen  = ft.Container(visible=False)
        self._icono_estado  = ft.Icon(ft.Icons.INFO_OUTLINED, size=14, color=ft.Colors.WHITE38)
        self._txt_estado    = ft.Text("", size=12, color=ft.Colors.WHITE38)
        self._fila_estado   = ft.Row(
            [self._icono_estado, self._txt_estado],
            spacing=8,
            alignment=ft.MainAxisAlignment.CENTER,
            visible=False,
        )

        self._btn_seleccionar = ft.OutlinedButton(
            "Seleccionar archivo .db",
            icon=ft.Icons.FOLDER_OPEN_OUTLINED,
            style=ft.ButtonStyle(
                side=ft.BorderSide(1, ft.Colors.WHITE24),
                color=ft.Colors.WHITE,
                padding=ft.padding.symmetric(horizontal=20, vertical=10),
            ),
            on_click=self._seleccionar,
        )

        self._btn_importar = ft.FilledButton(
            "Importar base de datos",
            icon=ft.Icons.DOWNLOAD_DONE_ROUNDED,
            disabled=True,
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.DEFAULT:  ft.Colors.BLUE_700,
                    ft.ControlState.DISABLED: ft.Colors.with_opacity(0.12, ft.Colors.WHITE),
                },
                color={
                    ft.ControlState.DEFAULT:  ft.Colors.WHITE,
                    ft.ControlState.DISABLED: ft.Colors.WHITE38,
                },
                padding=ft.padding.symmetric(horizontal=20, vertical=10),
            ),
            on_click=self._confirmar,
        )

        # Panel central
        panel = ft.Container(
            width=440,
            bgcolor="#0f111a",
            border=ft.border.all(1, ft.Colors.WHITE10),
            border_radius=12,
            padding=ft.padding.symmetric(vertical=36, horizontal=32),
            content=ft.Column(
                [
                    # Cabecera
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.UPLOAD_FILE_ROUNDED, color=ft.Colors.WHITE54, size=20),
                            ft.Column(
                                [
                                    ft.Text(
                                        "Restaurar base de datos",
                                        size=16,
                                        weight=ft.FontWeight.W_600,
                                        color=ft.Colors.WHITE,
                                    ),
                                    ft.Text(
                                        "Selecciona un respaldo (.db) para restaurar el sistema",
                                        size=11,
                                        color=ft.Colors.WHITE38,
                                    ),
                                ],
                                spacing=1,
                                expand=True,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.CLOSE,
                                icon_color=ft.Colors.WHITE38,
                                icon_size=18,
                                on_click=lambda _: self._on_close(),
                            ),
                        ],
                        spacing=10,
                    ),
                    ft.Divider(height=1, color=ft.Colors.WHITE10),

                    # Zona de seleccion
                    ft.Column(
                        [
                            self._icono,
                            ft.Container(height=4),
                            self._txt_archivo,
                            ft.Container(height=8),
                            self._btn_seleccionar,
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=4,
                    ),

                    # Resumen BD
                    self._card_resumen,

                    # Estado
                    self._fila_estado,

                    # Boton importar
                    ft.Container(
                        content=self._btn_importar,
                        alignment=ft.Alignment(0, 0),
                    ),

                    # Nota seguridad
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.LOCK_OUTLINE_ROUNDED, color=ft.Colors.WHITE24, size=12),
                            ft.Text(
                                "Se genera un respaldo automatico antes de reemplazar la base de datos actual.",
                                size=11,
                                color=ft.Colors.WHITE24,
                            ),
                        ],
                        spacing=6,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                spacing=16,
            ),
        )

        self.content = panel

    # ── Helpers de estado ─────────────────────────────────────────────────────
    def _mostrar_estado(self, mensaje: str, tipo: str = "info"):
        mapa = {
            "info":    (ft.Icons.INFO_OUTLINED,                ft.Colors.WHITE54),
            "error":   (ft.Icons.ERROR_OUTLINE_ROUNDED,        ft.Colors.RED_300),
            "success": (ft.Icons.CHECK_CIRCLE_OUTLINE_ROUNDED, ft.Colors.GREEN_300),
        }
        icn, clr = mapa.get(tipo, mapa["info"])
        self._icono_estado.name  = icn
        self._icono_estado.color = clr
        self._txt_estado.value   = mensaje
        self._txt_estado.color   = clr
        self._fila_estado.visible = True
        self._page.update()

    # ── Seleccion de archivo ──────────────────────────────────────────────────
    def _seleccionar(self, e):
        def dialogo():
            root = tk.Tk()
            root.withdraw()
            root.attributes("-topmost", True)
            path = filedialog.askopenfilename(
                title="Seleccionar base de datos",
                filetypes=[
                    ("Archivos de base de datos", "*.db"),
                    ("Todos los archivos", "*.*"),
                ],
            )
            root.destroy()
            if path:
                self._page.run_task(self._procesar, path)

        threading.Thread(target=dialogo, daemon=True).start()

    async def _procesar(self, ruta: str):
        self._fila_estado.visible = False
        self._txt_archivo.value   = os.path.basename(ruta)
        self._txt_archivo.color   = ft.Colors.WHITE70
        self._card_resumen.visible = False
        self._btn_importar.disabled = True
        self._ruta["valor"] = None
        self._icono.name  = ft.Icons.CLOUD_UPLOAD_OUTLINED
        self._icono.color = ft.Colors.BLUE_300
        self._page.update()
        await asyncio.sleep(0)

        valido, mensaje = ImportManager.validar_bd(ruta)
        if not valido:
            self._icono.name  = ft.Icons.ERROR_OUTLINE_ROUNDED
            self._icono.color = ft.Colors.RED_300
            self._mostrar_estado(mensaje, "error")
            return

        resumen = ImportManager.obtener_resumen(ruta)
        self._ruta["valor"] = ruta
        self._icono.name  = ft.Icons.CHECK_CIRCLE_OUTLINE_ROUNDED
        self._icono.color = ft.Colors.GREEN_300

        self._card_resumen.visible = True
        self._card_resumen.content = ft.Column(
            [
                ft.Text(
                    "Contenido del archivo seleccionado",
                    size=11,
                    weight=ft.FontWeight.W_500,
                    color=ft.Colors.WHITE38,
                ),
                ft.Divider(height=1, color=ft.Colors.WHITE10),
                ft.Row(
                    [
                        self._stat("Personas",   resumen["personas"],   ft.Icons.PEOPLE_ALT_OUTLINED),
                        ft.VerticalDivider(width=1, color=ft.Colors.WHITE12),
                        self._stat("Atenciones", resumen["atenciones"], ft.Icons.EVENT_NOTE_OUTLINED),
                    ],
                    spacing=24,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            spacing=10,
        )
        self._card_resumen.bgcolor       = ft.Colors.with_opacity(0.04, ft.Colors.WHITE)
        self._card_resumen.border_radius = 8
        self._card_resumen.padding       = ft.padding.symmetric(vertical=14, horizontal=18)
        self._card_resumen.border        = ft.border.all(1, ft.Colors.WHITE10)

        self._btn_importar.disabled = False
        self._mostrar_estado(
            "Archivo validado. Presiona 'Importar base de datos' para continuar.",
            "info",
        )
        self._page.update()

    def _stat(self, etiqueta, valor, icono):
        return ft.Column(
            [
                ft.Icon(icono, color=ft.Colors.WHITE54, size=16),
                ft.Text(str(valor), size=18, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE),
                ft.Text(etiqueta, size=11, color=ft.Colors.WHITE38),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=3,
        )

    # ── Confirmacion ──────────────────────────────────────────────────────────
    def _confirmar(self, e):
        ruta = self._ruta["valor"]
        if not ruta:
            return

        def ejecutar(_):
            dlg.open = False
            self._page.update()
            self._ejecutar_importacion(ruta)

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar importacion", weight=ft.FontWeight.BOLD),
            content=ft.Column(
                [
                    ft.Text(
                        "Esta accion reemplazara todos los datos actuales del sistema "
                        "con los datos del archivo seleccionado.",
                        size=13,
                        color=ft.Colors.WHITE60,
                    ),
                    ft.Container(height=4),
                    ft.Text(
                        "Se creara un respaldo de la base de datos actual antes de continuar.",
                        size=12,
                        color=ft.Colors.WHITE38,
                    ),
                ],
                tight=True,
                spacing=6,
            ),
            actions=[
                ft.TextButton(
                    "Cancelar",
                    on_click=lambda _: (setattr(dlg, "open", False), self._page.update()),
                ),
                ft.FilledButton(
                    "Confirmar importacion",
                    icon=ft.Icons.DOWNLOAD_DONE_ROUNDED,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.BLUE_700,
                        color=ft.Colors.WHITE,
                    ),
                    on_click=ejecutar,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self._page.overlay.append(dlg)
        dlg.open = True
        self._page.update()

    def _ejecutar_importacion(self, ruta: str):
        self._btn_importar.disabled    = True
        self._btn_seleccionar.disabled = True
        self._icono.name  = ft.Icons.HOURGLASS_TOP_ROUNDED
        self._icono.color = ft.Colors.BLUE_300
        self._mostrar_estado("Importando base de datos, por favor espere...", "info")

        ok, resultado = ImportManager.importar_bd(ruta)

        if not ok:
            self._icono.name  = ft.Icons.ERROR_OUTLINE_ROUNDED
            self._icono.color = ft.Colors.RED_300
            self._btn_importar.disabled    = False
            self._btn_seleccionar.disabled = False
            self._mostrar_estado(resultado, "error")
            self._page.update()
            return

        self._icono.name  = ft.Icons.CHECK_CIRCLE_ROUNDED
        self._icono.color = ft.Colors.GREEN_300
        self._mostrar_estado(
            f"Importacion completada. Reiniciando el sistema...",
            "success",
        )
        self._page.update()

        # Reiniciar
        threading.Timer(1.5, self._reiniciar).start()

    def _reiniciar(self):
        python = sys.executable
        script  = os.path.abspath(sys.argv[0])
        flags   = (subprocess.DETACHED_PROCESS | subprocess.CREATE_NO_WINDOW
                   if sys.platform == "win32" else 0)
        subprocess.Popen([python, script], creationflags=flags)
        # Delegar el cierre al event loop de Flet para poder hacer await
        self._page.run_task(self._cerrar_y_salir)

    async def _cerrar_y_salir(self):
        try:
            await self._page.window.destroy()
        except Exception:
            pass
        os._exit(0)
