import flet as ft


class Sidebar(ft.NavigationRail):
    def __init__(self, on_change):
        super().__init__()
        self.selected_index = 0
        self.label_type = ft.NavigationRailLabelType.ALL
        self.min_width = 80
        self.min_extended_width = 180
        self.group_alignment = -0.9
        self.on_change = on_change
        self.bgcolor = ft.Colors.with_opacity(0.1, ft.Colors.BLUE_900)
        self.indicator_color = ft.Colors.GREEN_800

        self.destinations = [
            ft.NavigationRailDestination(
                icon=ft.Icons.DASHBOARD_OUTLINED,
                selected_icon=ft.Icons.DASHBOARD_ROUNDED,
                label="Inicio",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.PERSON_ADD_ALT_OUTLINED,
                selected_icon=ft.Icons.PERSON_ADD_ALT_1_ROUNDED,
                label="Registrar",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.LIST_ALT_OUTLINED,
                selected_icon=ft.Icons.LIST_ALT_ROUNDED,
                label="Personas",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.HISTORY_ROUNDED,
                selected_icon=ft.Icons.HISTORY_ROUNDED,
                label="Historial",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.SETTINGS_OUTLINED,
                selected_icon=ft.Icons.SETTINGS_ROUNDED,
                label="Config.",
            ),
        ]
