import flet as ft
from core.init_db import init_db
from views.login_view import LoginView
from views.dashboard_view import DashboardView
from views.components.sidebar import Sidebar
from views.registro_view import build_registro_view
from views.personas_view import build_personas_view
from views.historial_view import build_historial_view
from views.config_view import build_config_view

def main(page: ft.Page):
    # Inicializar la base de datos en el primer arranque
    init_db()
    
    # Configuración de la página
    page.title = "Sistema de Gestión Social"
    page.theme_mode = ft.ThemeMode.DARK
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE_700)
    page.window.width = 1200
    page.window.height = 800
    page.padding = 0
    
    # Estado de la sesión
    state = {"user": None}
    main_container = ft.Container(expand=True)

    def navigate_to(index):
        """Maneja el cambio de pestañas del sidebar."""
        # Sincronizar el sidebar si se llama externamente
        sidebar.selected_index = index
        
        if index == 0:
            main_container.content = DashboardView(page, state["user"], logout)
        elif index == 1:
            main_container.content = build_registro_view(page)
        elif index == 2:
            main_container.content = build_personas_view(page, on_new_click=lambda: navigate_to(1))
        elif index == 3:
            main_container.content = build_historial_view(page)
        elif index == 4:
            main_container.content = build_config_view(page)
        page.update()

    # Sidebar
    sidebar = Sidebar(on_change=lambda e: navigate_to(e.control.selected_index))

    def logout(e=None):
        state["user"] = None
        page.clean()
        show_login()

    def login_success(user_data):
        state["user"] = user_data
        page.clean()
        
        layout = ft.Row(
            [
                sidebar,
                ft.VerticalDivider(width=1, color=ft.Colors.BLUE_900),
                ft.Container(content=main_container, expand=True, padding=20)
            ],
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.START
        )
        page.add(layout)
        navigate_to(0)

    def show_login():
        login_view = LoginView(page, on_login_success=login_success)
        page.add(ft.Container(
            content=login_view,
            expand=True,
            alignment=ft.alignment.Alignment(0, 0),
            bgcolor=ft.Colors.BLUE_GREY_900
        ))

    show_login()

if __name__ == "__main__":
    ft.run(main)
