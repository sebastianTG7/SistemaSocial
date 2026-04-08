import flet as ft
from controllers.persona_controller import PersonaController
from datetime import datetime

class DashboardView(ft.Column):
    def __init__(self, page: ft.Page, user, on_logout):
        super().__init__()
        self.main_page = page
        self.spacing = 20
        self.expand = True
        self.scroll = ft.ScrollMode.AUTO

        # ── Estado ──
        _hoy = datetime.now()
        self.sel_mes = str(_hoy.month)
        self.sel_anio = str(_hoy.year)

        # ── Contenedores ──
        self.container_cards = ft.Row(spacing=20, alignment="start")
        self.container_top_charts = ft.ResponsiveRow(spacing=20)
        self.container_bottom_trend = ft.Container(padding=ft.padding.all(20), border_radius=20)
        
        # ── Filtros ──
        meses_lista = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        self.dd_mes = ft.Dropdown(
            label="Mes Actual", width=140, value=self.sel_mes,
            options=[ft.dropdown.Option("all", "Todo el Año")] + [ft.dropdown.Option(str(i+1), meses_lista[i]) for i in range(12)],
            on_select=lambda _: self.actualizar_dashboard(),
            border_radius=12
        )
        self.dd_anio = ft.Dropdown(
            label="Año", width=110, value=self.sel_anio,
            options=[ft.dropdown.Option(str(a), str(a)) for a in range(2025, _hoy.year + 5)],
            on_select=lambda _: self.actualizar_dashboard(),
            border_radius=12
        )

        # Botón de Cambio de Tema
        self.btn_theme = ft.IconButton(
            icon=ft.Icons.LIGHT_MODE_ROUNDED if page.theme_mode == ft.ThemeMode.DARK else ft.Icons.DARK_MODE_ROUNDED,
            on_click=self.toggle_theme,
            icon_color=ft.Colors.AMBER_400 if page.theme_mode == ft.ThemeMode.DARK else ft.Colors.BLACK
        )

        self.title_text = ft.Text(f"Dashboard Analítico v3.0", size=24, weight="bold")
        self.sub_text = ft.Text("Métricas de rendimiento e impacto social universitario.", size=12)

        header = ft.Container(
            content=ft.Row([
                ft.Column([self.title_text, self.sub_text], spacing=2),
                ft.Container(expand=True),
                self.btn_theme, self.dd_mes, self.dd_anio,
                ft.IconButton(ft.Icons.LOGOUT_ROUNDED, on_click=on_logout, icon_color=ft.Colors.RED_400),
            ]), padding=ft.Padding(0, 0, 0, 10)
        )

        self.trend_title = ft.Text("Evolución de Atenciones Mes a Mes", size=16, weight="bold")

        self.controls = [
            header,
            ft.Divider(height=1),
            self.container_cards,
            self.container_top_charts,
            self.trend_title,
            self.container_bottom_trend,
            ft.Container(height=40)
        ]
        self.actualizar_dashboard(render_now=False)

    def toggle_theme(self, e):
        self.main_page.theme_mode = ft.ThemeMode.LIGHT if self.main_page.theme_mode == ft.ThemeMode.DARK else ft.ThemeMode.DARK
        self.actualizar_dashboard()
        self.main_page.update()

    def _get_ui_colors(self):
        """Devuelve una paleta de colores según el modo actual."""
        is_dark = self.main_page.theme_mode == ft.ThemeMode.DARK
        return {
            "card_bg": ft.Colors.with_opacity(0.07, ft.Colors.WHITE) if is_dark else ft.Colors.WHITE,
            "panel_bg": ft.Colors.with_opacity(0.05, ft.Colors.WHITE) if is_dark else ft.Colors.GREY_50,
            "text_main": ft.Colors.WHITE if is_dark else ft.Colors.BLACK,
            "text_sub": ft.Colors.WHITE_54 if is_dark else ft.Colors.BLACK54,
            "shadow": ft.Colors.BLACK54 if is_dark else ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
            "ring_bg": ft.Colors.WHITE10 if is_dark else ft.Colors.BLACK12,
            "border": ft.Colors.WHITE10 if is_dark else ft.Colors.BLACK12,
            "trend_title": ft.Colors.BLUE_200 if is_dark else ft.Colors.BLUE_900
        }

    def _badge_donut(self, value, total, color, label, ui):
        perc = (value / total) if total > 0 else 0
        return ft.Column([
            ft.Stack([
                ft.ProgressRing(value=1.0, width=75, height=75, stroke_width=7, color=ui["ring_bg"]),
                ft.ProgressRing(value=perc, width=75, height=75, stroke_width=7, color=color),
                ft.Container(content=ft.Text(f"{int(perc*100)}%", size=12, weight="bold", color=ui["text_main"]), width=75, height=75, alignment=ft.Alignment(0, 0))
            ]),
            ft.Text(label, size=11, color=ui["text_sub"])
        ], horizontal_alignment="center", spacing=8)

    def _trend_bar(self, label, count, max_val, ui):
        h_max = 100
        h_bar = (count / max_val * h_max) if max_val > 0 else 2
        return ft.Column([
            ft.Container(expand=True),
            ft.Container(
                content=ft.Text(str(count) if count > 0 else "", size=9, weight="bold", color=ui["text_main"]),
                alignment=ft.Alignment(0, -1),
                padding=ft.padding.only(top=5),
                width=35, height=h_bar, 
                gradient=ft.LinearGradient(begin=ft.Alignment(0,-1), end=ft.Alignment(0,1), colors=[ft.Colors.GREEN_400, ft.Colors.BLUE_900]),
                border_radius=8,
                shadow=ft.BoxShadow(offset=ft.Offset(2, 4), blur_radius=10, color=ui["shadow"]),
                tooltip=f"{label}: {count}"
            ),
            ft.Text(label[:3].upper(), size=10, color=ui["text_sub"])
        ], horizontal_alignment="center", spacing=10, height=130)

    def actualizar_dashboard(self, render_now=True):
        ui = self._get_ui_colors()
        
        # Actualizar UI base
        self.btn_theme.icon = ft.Icons.LIGHT_MODE_ROUNDED if self.main_page.theme_mode == ft.ThemeMode.DARK else ft.Icons.DARK_MODE_ROUNDED
        self.btn_theme.icon_color = ft.Colors.AMBER_400 if self.main_page.theme_mode == ft.ThemeMode.DARK else ft.Colors.BLACK
        self.sub_text.color = ui["text_sub"]
        self.trend_title.color = ui["trend_title"]

        mes = None if self.dd_mes.value == "all" else self.dd_mes.value
        anio = self.dd_anio.value
        data = PersonaController.get_analytics(mes=mes, anio=anio)
        trend = PersonaController.get_trend(anio)

        # 1. Cards
        self.container_cards.controls = [self._card_3d("Total Atenciones", str(data["total_periodo"]), ft.Colors.BLUE_400, ui)]
        casos = data["casos_periodo"]
        for cat in ["Evaluación", "Evaluación y Seguimiento", "Seguimiento", "Orientacion"]:
            self.container_cards.controls.append(self._card_3d(cat, str(casos.get(cat,0)), ft.Colors.GREEN_400, ui))

        # 2. Charts
        v_est = 0
        for k, v in data['tipos'].items():
            if str(k).upper() in ["ALUMNO", "ESTUDIANTE"]: v_est += v
        v_egr = data['tipos'].get("Egresado", 0) + data['tipos'].get("EGRESADO", 0)
        
        t_sexo = sum(data['sexo'].values()) or 1
        t_sum = (v_est + v_egr) or 1

        self.container_top_charts.controls = [
            self._panel_base("Demografía por Género", 5, ui, ft.Row([
                self._badge_donut(data['sexo'].get("M", 0), t_sexo, ft.Colors.BLUE_400, "Varones", ui),
                self._badge_donut(data['sexo'].get("F", 0), t_sexo, ft.Colors.PINK_400, "Mujeres", ui),
            ], alignment="spaceAround")),
            self._panel_base("Tipología de Usuario", 7, ui, ft.Row([
                self._badge_donut(v_est, t_sum, ft.Colors.GREEN_400, "Estudiantes", ui),
                self._badge_donut(v_egr, t_sum, ft.Colors.ORANGE_400, "Egresados", ui),
            ], alignment="spaceAround"))
        ]

        # 3. Tendencia
        meses_n = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
        m_trend = max(trend.values()) if trend.values() else 1
        self.container_bottom_trend.bgcolor = ui["panel_bg"]
        self.container_bottom_trend.shadow = ft.BoxShadow(blur_radius=15, color=ui["shadow"], offset=ft.Offset(0,10))
        self.container_bottom_trend.content = ft.Row(
            [self._trend_bar(meses_n[m-1], trend[m], m_trend, ui) for m in range(1, 13)],
            alignment="spaceAround", vertical_alignment="end"
        )
        if render_now: self.update()

    def _card_3d(self, title, value, color, ui):
        return ft.Container(
            expand=True, bgcolor=ui["card_bg"], padding=20, border_radius=20, border=ft.border.all(1, ui["border"]),
            shadow=ft.BoxShadow(offset=ft.Offset(4, 6), blur_radius=12, color=ui["shadow"]),
            content=ft.Column([
                ft.Text(title, size=10, color=ui["text_sub"], max_lines=1),
                ft.Text(value, size=28, weight="bold", color=color)
            ], spacing=5, alignment="center"), height=110
        )

    def _panel_base(self, title, col_size, ui, content):
        return ft.Container(
            col={"sm": 12, "md": col_size}, bgcolor=ui["panel_bg"], padding=25, border_radius=25, 
            shadow=ft.BoxShadow(blur_radius=15, color=ui["shadow"], offset=ft.Offset(0,10)),
            content=ft.Column([ft.Text(title, size=14, weight="bold", color=ui["text_main"]), ft.Divider(height=10, color="transparent"), content])
        )
