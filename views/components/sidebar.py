import flet as ft

class Sidebar(ft.NavigationRail):
    def __init__(self, on_change, user_rol="operador"):
        super().__init__()
        self.selected_index = 0
        self.label_type = ft.NavigationRailLabelType.ALL
        self.min_width = 80
        self.min_extended_width = 180
        self.group_alignment = -0.9
        self.on_change = on_change
        self.bgcolor = ft.Colors.with_opacity(0.1, ft.Colors.BLUE_900)
        self.indicator_color = ft.Colors.GREEN_800

        # Destinos base (visibles para todos)
        destinos = [
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
                label="Atenciones",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.ASSIGNMENT_IND_OUTLINED,
                selected_icon=ft.Icons.ASSIGNMENT_IND_ROUNDED,
                label="Evaluaciones",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.SHARE_OUTLINED,
                selected_icon=ft.Icons.SHARE_ROUNDED,
                label="Derivaciones",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.PEOPLE_ALT_OUTLINED,
                selected_icon=ft.Icons.PEOPLE_ALT_ROUNDED,
                label="Usuarios",
            ),

            ft.NavigationRailDestination(
                icon=ft.Icons.SETTINGS_OUTLINED,
                selected_icon=ft.Icons.SETTINGS_ROUNDED,
                label="Config.",
            ),
        ]

        # Solo el administrador ve "Gestionar Cuentas"
        if user_rol == "administrador":
            destinos.append(
                ft.NavigationRailDestination(
                    icon=ft.Icons.ADMIN_PANEL_SETTINGS_OUTLINED,
                    selected_icon=ft.Icons.ADMIN_PANEL_SETTINGS_ROUNDED,
                    label="Cuentas",
                )
            )

        self.destinations = destinos
