import flet as ft
from controllers.auth_controller import AuthController

class LoginView(ft.Column):
    def __init__(self, page: ft.Page, on_login_success):
        super().__init__()
        self.main_page = page
        self.on_login_success = on_login_success

        self.username_field = ft.TextField(
            label="Usuario",
            prefix_icon=ft.Icons.PERSON,
            border_color=ft.Colors.BLUE_700,
            focused_border_color=ft.Colors.GREEN_400,
            on_submit=self.handle_login,
            width=320,
        )
        self.password_field = ft.TextField(
            label="Contraseña",
            prefix_icon=ft.Icons.LOCK,
            password=True,
            can_reveal_password=True,
            border_color=ft.Colors.BLUE_700,
            focused_border_color=ft.Colors.GREEN_400,
            on_submit=self.handle_login,
            width=320,
        )
        self.login_button = ft.ElevatedButton(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.LOGIN, size=18),
                    ft.Text("Iniciar Sesión", weight=ft.FontWeight.BOLD),
                ],
                tight=True,
                spacing=8,
            ),
            width=320,
            on_click=self.handle_login,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.BLUE_800,
                color=ft.Colors.WHITE,
            ),
        )
        self.error_text = ft.Text(
            "", color=ft.Colors.RED_400, weight=ft.FontWeight.BOLD
        )

        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.alignment = ft.MainAxisAlignment.CENTER
        self.expand = True

        self.controls = [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.ACCOUNT_BALANCE, size=70, color=ft.Colors.BLUE_400),
                        ft.Text(
                            "Servicio Social",
                            size=26,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.WHITE,
                        ),
                        ft.Text(
                            "Sistema de Gestión Universitaria",
                            size=14,
                            color=ft.Colors.BLUE_200,
                        ),
                        ft.Divider(height=24, color=ft.Colors.TRANSPARENT),
                        self.username_field,
                        self.password_field,
                        ft.Container(height=4),
                        self.error_text,
                        ft.Container(height=4),
                        self.login_button,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=12,
                ),
                bgcolor=ft.Colors.with_opacity(0.15, ft.Colors.BLUE_700),
                padding=40,
                border_radius=16,
                border=ft.border.all(1, ft.Colors.BLUE_900),
                width=420,
            )
        ]

    def handle_login(self, e):
        self.login_button.disabled = True
        self.main_page.update()

        user = AuthController.login(
            self.username_field.value, self.password_field.value
        )
        if user:
            self.error_text.value = ""
            self.on_login_success(user)
        else:
            self.error_text.value = "⚠ Usuario o contraseña incorrectos"
            self.login_button.disabled = False
            self.main_page.update()
