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

        # ── Estado de Filtros ──
        _hoy = datetime.now()
        self.sel_mes = str(_hoy.month)
        self.sel_anio = str(_hoy.year)

        # ── Contenedores Principales ──
        self.container_cards = ft.Row(spacing=15, alignment="start")
        self.container_charts = ft.ResponsiveRow(spacing=20)
        
        # ── Filtros Estilizados ──
        meses_n = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        self.dd_mes = ft.Dropdown(
            label="Mes", width=140, value=self.sel_mes,
            options=[ft.dropdown.Option("all", "Todo el Año")] + [ft.dropdown.Option(str(i+1), meses_n[i]) for i in range(12)],
            on_select=lambda _: self.actualizar_dashboard(),
            border_radius=10, border_color=ft.Colors.BLUE_900
        )
        self.dd_anio = ft.Dropdown(
            label="Año", width=110, value=self.sel_anio,
            options=[ft.dropdown.Option(str(a), str(a)) for a in range(2025, _hoy.year + 5)],
            on_select=lambda _: self.actualizar_dashboard(),
            border_radius=10, border_color=ft.Colors.BLUE_900
        )

        header = ft.Container(
            content=ft.Row([
                ft.Column([
                    ft.Text(f"Dashboard Social", size=24, weight="bold"),
                    ft.Text("Métricas de impacto y seguimiento académico.", size=12, color=ft.Colors.WHITE_54)
                ], spacing=2),
                ft.Container(expand=True),
                self.dd_mes, self.dd_anio,
                ft.IconButton(ft.Icons.LOGOUT_ROUNDED, on_click=on_logout, icon_color=ft.Colors.RED_400),
            ]), padding=ft.Padding(0, 0, 0, 10)
        )

        self.controls = [
            header, 
            ft.Divider(height=1, color=ft.Colors.WHITE10), 
            self.container_cards, 
            ft.Divider(height=1, color="transparent"),
            self.container_charts, 
            ft.Container(height=40)
        ]
        
        self.actualizar_dashboard(render_now=False)

    def _donut_chart(self, value, total, color, label):
        perc = (value / total) if total > 0 else 0
        return ft.Column([
            ft.Stack([
                ft.ProgressRing(value=1.0, width=70, height=70, stroke_width=8, color=ft.Colors.WHITE10),
                ft.ProgressRing(value=perc, width=70, height=70, stroke_width=8, color=color),
                ft.Container(content=ft.Text(f"{int(perc*100)}%", size=11, weight="bold"), width=70, height=70, alignment=ft.Alignment(0, 0))
            ]),
            ft.Text(label, size=10, color=ft.Colors.WHITE_54, text_align="center")
        ], horizontal_alignment="center", spacing=8)

    def _vert_bar(self, label, count, max_val):
        h_max = 120
        h_bar = (count / max_val * h_max) if max_val > 0 else 5
        return ft.Column([
            ft.Container(expand=True),
            ft.Container(width=20, height=h_bar, bgcolor=ft.Colors.BLUE_400, border_radius=ft.border_radius.only(top_left=5, top_right=5), tooltip=f"{label}: {count}"),
            ft.Text(label[:3].upper(), size=9, color=ft.Colors.WHITE_54)
        ], horizontal_alignment="center", spacing=5, height=h_max + 20)

    def actualizar_dashboard(self, render_now=True):
        mes = None if self.dd_mes.value == "all" else self.dd_mes.value
        anio = self.dd_anio.value
        data = PersonaController.get_analytics(mes=mes, anio=anio)

        # 1. ACTUALIZAR TARJETAS (Nombres reales de tu base de datos)
        categorias_reales = [
            "Evaluación",
            "Evaluación y Seguimiento",
            "Seguimiento",
            "Orientacion"
        ]
        
        casos = data["casos_periodo"]
        self.container_cards.controls = [
            self._card_premium("Total Atenciones", str(data["total_periodo"]), ft.Colors.BLUE_400)
        ]
        
        for cat in categorias_reales:
            # Buscamos el conteo exacto en el diccionario que viene del controlador
            conteo = casos.get(cat, 0)
            self.container_cards.controls.append(
                self._card_premium(cat, str(conteo), ft.Colors.GREEN_400)
            )

        # 2. Cálculos para Gráficos
        t_sexo = sum(data['sexo'].values()) or 1
        
        # Normalizamos y combinamos Alumno/Estudiante para compatibilidad con datos viejos
        tipos_raw = data['tipos']
        val_estudiante = 0
        val_egresado = 0
        
        for k, v in tipos_raw.items():
            key_up = str(k).upper()
            if key_up in ["ALUMNO", "ESTUDIANTE"]:
                val_estudiante += v
            elif key_up == "EGRESADO":
                val_egresado += v
        
        tipos_norm = {"ESTUDIANTE": val_estudiante, "EGRESADO": val_egresado}
        t_tipos = (val_estudiante + val_egresado) or 1
        
        max_esc = max([e['count'] for e in data['top_escuelas']]) if data['top_escuelas'] else 1

        self.container_charts.controls = [
            # PANEL 1: GÉNERO
            ft.Container(
                col={"sm": 12, "md": 4}, bgcolor=ft.Colors.with_opacity(0.04, ft.Colors.WHITE), 
                padding=20, border_radius=15, height=220,
                content=ft.Column([
                    ft.Text("Género", size=13, weight="bold"),
                    ft.Divider(height=20, color="transparent"),
                    ft.Row([
                        self._donut_chart(data['sexo'].get("M", 0), t_sexo, ft.Colors.BLUE_500, "Varones"),
                        self._donut_chart(data['sexo'].get("F", 0), t_sexo, ft.Colors.PINK_400, "Mujeres"),
                    ], alignment="spaceAround")
                ])
            ),
            # PANEL 2: CONDICIÓN (Egresados vs Estudiante)
            ft.Container(
                col={"sm": 12, "md": 4}, bgcolor=ft.Colors.with_opacity(0.04, ft.Colors.WHITE), 
                padding=20, border_radius=15, height=220,
                content=ft.Column([
                    ft.Text("Tipo de Usuario", size=13, weight="bold"),
                    ft.Divider(height=20, color="transparent"),
                    ft.Row([
                        self._donut_chart(tipos_norm.get("ESTUDIANTE", 0), t_tipos, ft.Colors.GREEN_600, "Estudiante"),
                        self._donut_chart(tipos_norm.get("EGRESADO", 0), t_tipos, ft.Colors.ORANGE_600, "Egresado"),
                    ], alignment="spaceAround")
                ])
            ),
            ft.Container(
                col={"sm": 12, "md": 4}, bgcolor=ft.Colors.with_opacity(0.04, ft.Colors.WHITE), 
                padding=20, border_radius=15, height=220,
                content=ft.Column([ft.Text("Top 5 Escuelas", size=13, weight="bold"),
                                   ft.Row([self._vert_bar(e['label'], e['count'], max_esc) for e in data['top_escuelas']], 
                                          alignment="spaceAround", vertical_alignment="end", expand=True)], expand=True)
            )
        ]

        if render_now: self.update()

    def _card_premium(self, title, value, color):
        return ft.Container(
            expand=True, bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.WHITE), 
            padding=ft.padding.all(15), border_radius=15, border=ft.border.all(1, ft.Colors.WHITE10),
            content=ft.Column([
                ft.Text(title, size=10, color=ft.Colors.WHITE_54, max_lines=1),
                ft.Text(value, size=24, weight="bold")
            ], spacing=5, alignment="center"),
            height=100
        )
