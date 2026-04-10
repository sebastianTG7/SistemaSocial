import flet as ft
from controllers.auth_controller import AuthController

class LoginView(ft.Container):
    def __init__(self, page: ft.Page, on_login_success):
        super().__init__()
        self.main_page = page
        self.on_login_success = on_login_success
        
        self.expand = True
        self.bgcolor = "#0f111a"
        self.alignment = ft.Alignment(0, 0)

        # ── Campos de Entrada ─────────────────────────────────────────────────
        self.username_field = ft.TextField(
            label="Usuario",
            prefix_icon=ft.Icons.PERSON_OUTLINED,
            border_radius=15,
            border_color="#1e293b",
            focused_border_color="#0ea5e9",
            bgcolor="#1e293b",
            width=300,
            on_submit=self.handle_login,
        )
        
        self.password_field = ft.TextField(
            label="Contraseña",
            prefix_icon=ft.Icons.LOCK_OUTLINED,
            password=True,
            can_reveal_password=True,
            border_radius=15,
            border_color="#1e293b",
            focused_border_color="#0ea5e9",
            bgcolor="#1e293b",
            width=300,
            on_submit=self.handle_login,
        )

        self.login_button = ft.Container(
            content=ft.Text("Iniciar Sesión", weight="bold", color="#0ea5e9"),
            alignment=ft.Alignment(0, 0),
            width=300,
            height=50,
            bgcolor="#1e293b",
            border_radius=15,
            on_click=self.handle_login,
        )

        self.error_text = ft.Text("", color=ft.Colors.RED_400, weight="bold", size=12)

        # ── Panel Formulario (Izquierda) ──────────────────────────────────────
        form_panel = ft.Container(
            expand=1,
            content=ft.Column([
                ft.Column([
                    ft.Text("SERVICIO SOCIAL", size=32, weight="bold", color=ft.Colors.WHITE),
                    ft.Container(height=2, width=100, bgcolor="#0ea5e9"),
                ], horizontal_alignment="center", spacing=6),

                ft.Container(height=40),

                ft.Text("Iniciar Sesión", size=22, weight="bold", color=ft.Colors.WHITE),
                ft.Container(height=15),

                self.username_field,
                ft.Container(height=5),
                self.password_field,
                ft.Container(height=10),
                self.error_text,
                ft.Container(height=20),
                self.login_button,

            ], horizontal_alignment="center", alignment="center"),
        )

        # ── Panel Logo PNG (Derecha) ──────────────────────────────────────────
        image_panel = ft.Container(
            expand=1,
            alignment=ft.Alignment(0, 0),
            padding=ft.padding.only(right=40, top=20, bottom=20),
            content=ft.Image(
                src="logo_view.png",
                width=500,
                height=500,
            ),
        )

        self.content = ft.Row([
            form_panel,
            image_panel,
        ], alignment="center", expand=True)

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
