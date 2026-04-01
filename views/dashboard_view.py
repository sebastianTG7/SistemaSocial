import flet as ft
from controllers.persona_controller import PersonaController
from controllers.catalog_controller import CatalogController


class DashboardView(ft.Column):
    def __init__(self, page: ft.Page, user, on_logout):
        super().__init__()
        self.main_page = page
        self.spacing = 20
        self.expand = True

        # Obtener conteos principales
        total_personas = PersonaController.contar_activos()
        total_facultades = len(CatalogController.get_facultades())
        
        # Obtener desglose por Caso Social
        casos_stats = PersonaController.contar_por_caso_social()

        self.controls = [
            # Encabezado
            ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.DASHBOARD_ROUNDED, size=28, color=ft.Colors.GREEN_400),
                        ft.Column(
                            [
                                ft.Text(f"Bienvenido, {user['nombre_completo']}", size=20, weight="bold", color=ft.Colors.WHITE),
                                ft.Text(f"Rol: {user['rol'].capitalize()}", size=12, color=ft.Colors.BLUE_200),
                            ],
                            spacing=2,
                        ),
                        ft.Container(expand=True),
                        ft.IconButton(ft.Icons.LOGOUT_ROUNDED, on_click=on_logout, tooltip="Cerrar Sesión", icon_color=ft.Colors.RED_400),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=12,
                ),
                padding=ft.Padding(0, 0, 0, 10),
            ),
            ft.Divider(color=ft.Colors.BLUE_900),
            
            # Subtítulo principal
            ft.Text("Resumen del Sistema de Servicio Social", size=16, color=ft.Colors.BLUE_200, weight="bold"),
            
            # Fila 1: Estadísticas Generales
            ft.Row(
                [
                    self._card("Total Personas Activas", str(total_personas), ft.Icons.PEOPLE_ROUNDED, ft.Colors.BLUE_400),
                    self._card("Facultades", str(total_facultades), ft.Icons.SCHOOL_ROUNDED, ft.Colors.ORANGE_400),
                ],
                spacing=16,
                wrap=True,
            ),
            
            ft.Divider(color=ft.Colors.BLUE_900),
            
            # Sección: Desglose de Casos Sociales
            ft.Text("Desglose por Caso Social", size=15, color=ft.Colors.GREEN_300, weight="bold"),
            ft.Row(
                [
                    self._card(nombre, str(cantidad), self._get_icon_for_case(nombre), ft.Colors.GREEN_400)
                    for nombre, cantidad in casos_stats.items()
                ],
                spacing=16,
                wrap=True,
            ),
            
            ft.Divider(color=ft.Colors.BLUE_900),
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.INFO_OUTLINED, color=ft.Colors.BLUE_300, size=36),
                    ft.Text("Use el menú lateral para gestionar la información.", color=ft.Colors.WHITE_54, italic=True, size=14),
                ], horizontal_alignment="center", spacing=8),
                alignment=ft.alignment.Alignment(0, 0),
                padding=20,
            ),
        ]

    def _get_icon_for_case(self, name):
        """Devuelve un icono descriptivo según el nombre del caso social."""
        n = name.lower()
        if "orient" in n: return ft.Icons.FORUM_ROUNDED
        if "seguim" in n: return ft.Icons.TRACK_CHANGES_ROUNDED
        if "monit" in n: return ft.Icons.QUERY_STATS_ROUNDED
        if "inic" in n: return ft.Icons.PLAY_ARROW_ROUNDED
        return ft.Icons.ASSIGNMENT_ROUNDED

    def _card(self, title, value, icon, color):
        """Genera una tarjeta de estadística con diseño premium."""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(icon, color=color, size=34),
                    ft.Text(value, size=28, weight="bold", color=ft.Colors.WHITE),
                    ft.Text(title, size=11, color=ft.Colors.WHITE_54, text_align="center", max_lines=2),
                ],
                horizontal_alignment="center",
                spacing=4,
            ),
            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLUE_700),
            padding=20,
            border_radius=12,
            border=ft.border.all(1, ft.Colors.with_opacity(0.2, color)),
            width=180, # Ancho uniforme para las tarjetas
        )
