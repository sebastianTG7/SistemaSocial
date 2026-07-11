import asyncio
import flet as ft
from core.init_db import init_db
from views.login_view import LoginView
from views.dashboard_view import DashboardView
from views.components.sidebar import Sidebar
from views.registro_view import build_registro_view
from views.personas_view import build_personas_view
from views.evaluaciones_view import build_evaluaciones_view
from views.derivaciones_view import build_derivaciones_view
from views.config_view import build_config_view

from core.backup_manager import BackupManager

def main(page: ft.Page):
    init_db()
    page.title = "Sistema de Gestión Social"
    page.theme_mode = ft.ThemeMode.DARK
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE_700)
    page.window.width = 1200
    page.window.height = 800
    page.padding = 0

    state = {"user": None}
    main_container = ft.Container(expand=True)

    # ── Contenedor raíz único ──────────────────────────────────────────────
    root = ft.Container(expand=True)
    page.add(root)

    def navigate_to(index):
        sidebar.selected_index = index
        if index == 0:
            main_container.content = DashboardView(page, state["user"], logout)
        elif index == 1:
            main_container.content = build_registro_view(page)
        elif index == 2:
            main_container.content = build_personas_view(page, on_new_click=lambda: navigate_to(1))
        elif index == 3:
            main_container.content = build_evaluaciones_view(page)
        elif index == 4:
            main_container.content = build_derivaciones_view(page)
        elif index == 5:
            main_container.content = build_config_view(page)
        page.update()

    sidebar = Sidebar(on_change=lambda e: navigate_to(e.control.selected_index))

    def logout(e=None):
        state["user"] = None
        show_login()

    def login_success(user_data):
        state["user"] = user_data
        layout = ft.Row([
            sidebar,
            ft.VerticalDivider(width=1, color=ft.Colors.BLUE_900),
            ft.Container(content=main_container, expand=True, padding=20)
        ], expand=True)
        root.content = layout
        page.update()
        navigate_to(0)

    def show_login():
        login_view = LoginView(page, on_login_success=login_success)
        root.content = ft.Container(
            content=login_view, expand=True,
            alignment=ft.Alignment(0, 0), bgcolor=ft.Colors.BLUE_GREY_900
        )
        page.update()

    # ── Splash (page.run_task: compatible con Flet antiguo) ───────────────
    splash = ft.Container(
        expand=True,
        bgcolor="#0f111a",
        alignment=ft.Alignment(0, 0),
        content=ft.Column([
            ft.Image(src="logo_view.png", width=220, height=220),
            ft.Container(height=20),
            ft.Text("SERVICIO SOCIAL", size=30, weight="bold", color=ft.Colors.WHITE),
            ft.Text("Sistema de Gestión Universitaria", size=13, color=ft.Colors.BLUE_200),
            ft.Container(height=30),
            ft.ProgressRing(width=36, height=36, stroke_width=3, color=ft.Colors.BLUE_400),
            ft.Container(height=10),
            ft.Text("Cargando...", size=11, color=ft.Colors.WHITE38),
        ], horizontal_alignment="center", alignment="center"),
    )

    async def splash_task():
        root.content = splash
        page.update()
        await asyncio.sleep(2)
        show_login()

    # ── Backup automático al CERRAR la app (Máxima compatibilidad) ────────
    def on_window_event(e):
        if e.data == "close":
            try:
                cfg = BackupManager.get_config()
                if cfg.get("automatico", False):
                    BackupManager.hacer_respaldo()
            except Exception:
                pass
            page.window_destroy()

    page.window_prevent_close = True
    page.on_window_event      = on_window_event
    page.update()

    page.run_task(splash_task)

if __name__ == "__main__":
    import os
    if not os.path.exists("assets"):
        os.makedirs("assets")
    ft.run(main, assets_dir="assets")
