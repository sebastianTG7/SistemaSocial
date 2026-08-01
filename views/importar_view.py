import flet as ft
import asyncio
import os
import sys
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog
from core.import_manager import ImportManager


def build_importar_view(page: ft.Page) -> ft.Column:
    """Vista del módulo de importación de base de datos SQLite."""

    # ── Estado interno ────────────────────────────────────────────────────────
    ruta_seleccionada = {"valor": None}

    # ── Controles de UI ───────────────────────────────────────────────────────
    icono_estado = ft.Icon(
        ft.Icons.CLOUD_UPLOAD_OUTLINED,
        size=56,
        color=ft.Colors.BLUE_300,
    )

    txt_titulo_archivo = ft.Text(
        "Ningún archivo seleccionado",
        size=13,
        color=ft.Colors.WHITE38,
        text_align=ft.TextAlign.CENTER,
    )

    card_resumen = ft.Container(visible=False)

    btn_seleccionar = ft.OutlinedButton(
        "Seleccionar archivo .db",
        icon=ft.Icons.FOLDER_OPEN_OUTLINED,
        style=ft.ButtonStyle(
            side=ft.BorderSide(1, ft.Colors.WHITE24),
            color=ft.Colors.WHITE,
            padding=ft.padding.symmetric(horizontal=24, vertical=12),
        ),
    )

    btn_importar = ft.FilledButton(
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
            padding=ft.padding.symmetric(horizontal=24, vertical=12),
        ),
    )

    # Mensaje de estado (reemplaza el "banner" de colores)
    txt_estado = ft.Text(
        "",
        size=12,
        color=ft.Colors.WHITE54,
        text_align=ft.TextAlign.CENTER,
    )
    icono_msg = ft.Icon(ft.Icons.INFO_OUTLINED, size=15, color=ft.Colors.WHITE38)
    fila_estado = ft.Row(
        [icono_msg, txt_estado],
        spacing=8,
        alignment=ft.MainAxisAlignment.CENTER,
        visible=False,
    )

    def mostrar_estado(mensaje: str, tipo: str = "info"):
        """tipos: 'info', 'error', 'success'"""
        colores_icon = {
            "info":    (ft.Icons.INFO_OUTLINED,                ft.Colors.WHITE54),
            "error":   (ft.Icons.ERROR_OUTLINE_ROUNDED,        ft.Colors.RED_300),
            "success": (ft.Icons.CHECK_CIRCLE_OUTLINE_ROUNDED, ft.Colors.GREEN_300),
        }
        icn, clr = colores_icon.get(tipo, colores_icon["info"])
        icono_msg.name  = icn
        icono_msg.color = clr
        txt_estado.value = mensaje
        txt_estado.color = clr
        fila_estado.visible = True
        page.update()

    def ocultar_estado():
        fila_estado.visible = False
        page.update()

    # ── FilePicker vía Tkinter ────────────────────────────────────────────────
    def seleccionar_archivo_tkinter(e):
        def abrir_dialogo():
            root = tk.Tk()
            root.withdraw()
            root.attributes("-topmost", True)
            file_path = filedialog.askopenfilename(
                title="Seleccionar base de datos",
                filetypes=[
                    ("Archivos de base de datos", "*.db"),
                    ("Todos los archivos", "*.*"),
                ],
            )
            root.destroy()
            if file_path:
                page.run_task(procesar_archivo_seleccionado, file_path)

        threading.Thread(target=abrir_dialogo, daemon=True).start()

    async def procesar_archivo_seleccionado(ruta):
        ocultar_estado()
        nombre = os.path.basename(ruta)

        txt_titulo_archivo.value = nombre
        txt_titulo_archivo.color = ft.Colors.WHITE70
        card_resumen.visible = False
        btn_importar.disabled = True
        ruta_seleccionada["valor"] = None
        icono_estado.name  = ft.Icons.CLOUD_UPLOAD_OUTLINED
        icono_estado.color = ft.Colors.BLUE_300
        page.update()
        await asyncio.sleep(0)

        # Validar
        valido, mensaje = ImportManager.validar_bd(ruta)

        if not valido:
            icono_estado.name  = ft.Icons.ERROR_OUTLINE_ROUNDED
            icono_estado.color = ft.Colors.RED_300
            mostrar_estado(mensaje, "error")
            return

        # Resumen de la BD
        resumen = ImportManager.obtener_resumen(ruta)
        ruta_seleccionada["valor"] = ruta

        icono_estado.name  = ft.Icons.CHECK_CIRCLE_OUTLINE_ROUNDED
        icono_estado.color = ft.Colors.GREEN_300

        card_resumen.visible = True
        card_resumen.content = ft.Column(
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
                        _stat_row(ft.Icons.PEOPLE_ALT_OUTLINED, "Personas",   resumen["personas"]),
                        ft.VerticalDivider(width=1, color=ft.Colors.WHITE12),
                        _stat_row(ft.Icons.EVENT_NOTE_OUTLINED,  "Atenciones", resumen["atenciones"]),
                    ],
                    spacing=24,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            spacing=12,
        )
        card_resumen.bgcolor       = ft.Colors.with_opacity(0.04, ft.Colors.WHITE)
        card_resumen.border_radius = 8
        card_resumen.padding       = ft.padding.symmetric(vertical=16, horizontal=20)
        card_resumen.border        = ft.border.all(1, ft.Colors.WHITE10)

        btn_importar.disabled = False
        mostrar_estado(
            "Archivo validado. Presiona 'Importar base de datos' para continuar.",
            "info",
        )
        page.update()

    btn_seleccionar.on_click = seleccionar_archivo_tkinter

    # ── Diálogo de confirmación ───────────────────────────────────────────────
    def confirmar_importacion(e):
        ruta = ruta_seleccionada["valor"]
        if not ruta:
            return

        def ejecutar_import(_):
            dlg.open = False
            page.update()
            _realizar_importacion(ruta)

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar importación", weight=ft.FontWeight.BOLD),
            content=ft.Column(
                [
                    ft.Text(
                        "Esta acción reemplazará todos los datos actuales del sistema "
                        "con los datos del archivo seleccionado.",
                        size=13,
                        color=ft.Colors.WHITE60,
                    ),
                    ft.Container(height=4),
                    ft.Text(
                        "Se creará un respaldo de la base de datos actual antes de continuar.",
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
                    on_click=lambda _: (setattr(dlg, "open", False), page.update()),
                ),
                ft.FilledButton(
                    "Confirmar importación",
                    icon=ft.Icons.DOWNLOAD_DONE_ROUNDED,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.BLUE_700,
                        color=ft.Colors.WHITE,
                    ),
                    on_click=ejecutar_import,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    btn_importar.on_click = confirmar_importacion

    # ── Lógica de importación ─────────────────────────────────────────────────
    def _realizar_importacion(ruta: str):
        btn_importar.disabled  = True
        btn_seleccionar.disabled = True
        icono_estado.name  = ft.Icons.HOURGLASS_TOP_ROUNDED
        icono_estado.color = ft.Colors.BLUE_300
        mostrar_estado("Importando base de datos, por favor espere...", "info")
        page.update()

        ok, resultado = ImportManager.importar_bd(ruta)

        if not ok:
            icono_estado.name  = ft.Icons.ERROR_OUTLINE_ROUNDED
            icono_estado.color = ft.Colors.RED_300
            btn_importar.disabled  = False
            btn_seleccionar.disabled = False
            mostrar_estado(resultado, "error")
            page.update()
            return

        # Exito
        icono_estado.name  = ft.Icons.CHECK_CIRCLE_ROUNDED
        icono_estado.color = ft.Colors.GREEN_300
        txt_titulo_archivo.value = "Importacion completada"
        txt_titulo_archivo.color = ft.Colors.GREEN_300
        ruta_seleccionada["valor"] = None
        card_resumen.visible = False
        mostrar_estado(
            f"Base de datos importada. Respaldo guardado en: {resultado}",
            "success",
        )

        btn_reiniciar = ft.OutlinedButton(
            "Reiniciar para aplicar los cambios",
            icon=ft.Icons.RESTART_ALT_ROUNDED,
            style=ft.ButtonStyle(
                side=ft.BorderSide(1, ft.Colors.WHITE24),
                color=ft.Colors.WHITE,
                padding=ft.padding.symmetric(horizontal=24, vertical=12),
            ),
            on_click=_reiniciar_sistema,
        )
        btn_importar.visible   = False
        btn_seleccionar.visible = False
        view_content.controls.append(
            ft.Container(content=btn_reiniciar, alignment=ft.Alignment(0, 0))
        )
        page.update()

    async def _reiniciar_sistema(_):
        """Lanza una nueva instancia y cierra la actual."""
        python = sys.executable
        script  = os.path.abspath(sys.argv[0])
        # Abrir nueva instancia sin ventana CMD
        flags = (subprocess.DETACHED_PROCESS | subprocess.CREATE_NO_WINDOW
                 if sys.platform == "win32" else 0)
        subprocess.Popen([python, script], creationflags=flags)
        # Cerrar la ventana actual
        try:
            await page.window.destroy()
        except Exception:
            pass
        os._exit(0)  # Salida directa sin propagar SystemExit

    # ── Helper: fila de estadística ───────────────────────────────────────────
    def _stat_row(icono, etiqueta, valor):
        return ft.Column(
            [
                ft.Icon(icono, color=ft.Colors.WHITE54, size=18),
                ft.Text(
                    str(valor),
                    size=20,
                    weight=ft.FontWeight.W_600,
                    color=ft.Colors.WHITE,
                ),
                ft.Text(etiqueta, size=11, color=ft.Colors.WHITE38),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=4,
        )

    # ── Ensamblado de la vista ────────────────────────────────────────────────
    view_content = ft.Column(
        controls=[
            # Zona de seleccion de archivo
            ft.Container(
                content=ft.Column(
                    [
                        icono_estado,
                        ft.Container(height=4),
                        ft.Text(
                            "Restaurar base de datos",
                            size=15,
                            weight=ft.FontWeight.W_600,
                            color=ft.Colors.WHITE,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Text(
                            "Selecciona un archivo .db generado por este sistema.",
                            size=12,
                            color=ft.Colors.WHITE38,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Container(height=10),
                        txt_titulo_archivo,
                        ft.Container(height=6),
                        btn_seleccionar,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=6,
                ),
                bgcolor=ft.Colors.with_opacity(0.04, ft.Colors.WHITE),
                border=ft.border.all(1, ft.Colors.WHITE10),
                border_radius=10,
                padding=ft.padding.symmetric(vertical=36, horizontal=30),
                alignment=ft.Alignment(0, 0),
            ),

            # Card resumen BD
            card_resumen,

            # Mensaje de estado
            fila_estado,

            # Boton importar
            ft.Container(
                content=btn_importar,
                alignment=ft.Alignment(0, 0),
            ),

            # Nota de seguridad
            ft.Row(
                [
                    ft.Icon(ft.Icons.LOCK_OUTLINE_ROUNDED, color=ft.Colors.WHITE24, size=13),
                    ft.Text(
                        "Se genera un respaldo automatico antes de cualquier reemplazo.",
                        size=11,
                        color=ft.Colors.WHITE24,
                    ),
                ],
                spacing=6,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ],
        spacing=16,
        scroll=ft.ScrollMode.AUTO,
    )

    return ft.Column(
        [
            # Encabezado
            ft.Row(
                [
                    ft.Icon(ft.Icons.UPLOAD_FILE_ROUNDED, color=ft.Colors.WHITE70, size=22),
                    ft.Column(
                        [
                            ft.Text(
                                "Importar base de datos",
                                size=18,
                                weight=ft.FontWeight.W_600,
                                color=ft.Colors.WHITE,
                            ),
                            ft.Text(
                                "Restaura el sistema cargando una copia de respaldo (.db)",
                                size=12,
                                color=ft.Colors.WHITE38,
                            ),
                        ],
                        spacing=1,
                    ),
                ],
                spacing=12,
            ),
            ft.Divider(height=1, color=ft.Colors.WHITE10),
            ft.Container(content=view_content, expand=True),
        ],
        spacing=16,
        expand=True,
    )
