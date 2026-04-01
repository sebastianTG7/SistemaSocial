import flet as ft
from controllers.persona_controller import PersonaController
from datetime import datetime


class DashboardView(ft.Column):
    def __init__(self, page: ft.Page, user, on_logout):
        super().__init__()
        self.main_page = page
        self.user = user
        self.on_logout = on_logout
        self.spacing = 15
        self.expand = True
        self.scroll = ft.ScrollMode.AUTO

        # ── Contenedores que se actualizarán ──
        self.seccion_tarjetas = ft.Row(wrap=True, spacing=15)
        self.seccion_graficos = ft.Column(spacing=15, expand=True)
        self.txt_periodo = ft.Text("Periodo: Actual", size=12, color=ft.Colors.BLUE_200)

        # ── Filtros ──
        _hoy = datetime.now()
        meses_n = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        
        self.dd_mes = ft.Dropdown(
            label="Mes", width=140, value=str(_hoy.month),
            options=[ft.dropdown.Option("all", "Todo el Año")] + [ft.dropdown.Option(str(i+1), meses_n[i]) for i in range(12)],
            on_select=lambda _: self.cargar_datos(),
            content_padding=ft.Padding(10,2,10,2)
        )
        self.dd_anio = ft.Dropdown(
            label="Año", width=110, value=str(_hoy.year),
            options=[ft.dropdown.Option(str(a), str(a)) for a in range(2025, _hoy.year + 5)],
            on_select=lambda _: self.cargar_datos(),
            content_padding=ft.Padding(10,2,10,2)
        )

        # ── Layout Inicial ──
        encabezado = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.DASHBOARD_ROUNDED, color=ft.Colors.GREEN_400, size=28),
                ft.Column([
                    ft.Text(f"Bienvenido, {user['nombre_completo']}", size=20, weight="bold"),
                    self.txt_periodo,
                ], spacing=1),
                ft.Container(expand=True),
                self.dd_mes, 
                self.dd_anio,
                ft.IconButton(ft.Icons.LOGOUT_ROUNDED, on_click=on_logout, icon_color=ft.Colors.RED_400),
            ], vertical_alignment="center"),
            padding=ft.Padding(0, 0, 0, 8)
        )

        self.controls = [
            encabezado,
            ft.Divider(color=ft.Colors.BLUE_900),
            self.seccion_tarjetas,
            ft.Divider(color=ft.Colors.BLUE_900),
            self.seccion_graficos,
            ft.Container(height=30)
        ]
        
        # Carga inicial de datos (SIN forzar update, ya que aún no está en la página)
        self.cargar_datos(force_update=False)

    def cargar_datos(self, force_update=True):
        # 1. Obtener valores de filtros
        mes = None if self.dd_mes.value == "all" else self.dd_mes.value
        anio = self.dd_anio.value
        
        # 2. Llamar al controlador con filtros
        data = PersonaController.get_analytics(mes=mes, anio=anio)
        
        # 3. Actualizar Texto de Periodo
        m_str = "Todo el Año" if not mes else f"Mes {mes}"
        self.txt_periodo.value = f"Visualizando: {m_str} / {anio}"

        # 4. Reconstruir Tarjetas
        self.seccion_tarjetas.controls = [
            self._card("Total Atenciones", str(data["total_periodo"]), ft.Icons.PEOPLE_ROUNDED, ft.Colors.BLUE_400),
            *[self._card(n, str(c), self._get_icon_for_case(n), ft.Colors.GREEN_400) for n, c in data["casos_periodo"].items()]
        ]

        # 5. Reconstruir Gráficos (Barras de Progreso)
        def _stat_bar(label, count, total, color):
            perc = (count / total) if total > 0 else 0
            return ft.Column([
                ft.Row([ft.Text(label, size=11, weight="bold"), ft.Container(expand=True), ft.Text(f"{count} ({perc*100:.1f}%)", size=10, color=ft.Colors.WHITE_54)], spacing=10),
                ft.ProgressBar(value=perc, color=color, bgcolor=ft.Colors.with_opacity(0.1, color), height=8, border_radius=4)
            ], spacing=4)

        t_sexo = sum(data['sexo'].values())
        b_sexo = ft.Column([_stat_bar("Masculino", data['sexo'].get("M", 0), t_sexo, ft.Colors.BLUE_500), _stat_bar("Femenino", data['sexo'].get("F", 0), t_sexo, ft.Colors.PINK_400)], spacing=12)

        t_tipos = sum(data['tipos'].values())
        b_tipos = ft.Column([_stat_bar(k, v, t_tipos, ft.Colors.GREEN_600 if "Alum" in k else ft.Colors.ORANGE_600) for k, v in data['tipos'].items()], spacing=12)

        max_esc = max([e['count'] for e in data['top_escuelas']]) if data['top_escuelas'] else 1
        b_escuelas = ft.Column([_stat_bar(e['label'], e['count'], max_esc, ft.Colors.CYAN_700) for e in data['top_escuelas']], spacing=10)

        self.seccion_graficos.controls = [
            ft.Text("Métricas de Estudiantes y Escuelas (Periodo Seleccionado)", size=16, weight="bold", color=ft.Colors.GREEN_400),
            ft.Row([
                ft.Container(expand=True, padding=20, border_radius=12, bgcolor=ft.Colors.with_opacity(0.04, ft.Colors.WHITE), content=ft.Column([ft.Text("Distribución por Sexo", size=13, weight="bold"), ft.Divider(height=10, color=ft.Colors.TRANSPARENT), b_sexo])),
                ft.Container(expand=True, padding=20, border_radius=12, bgcolor=ft.Colors.with_opacity(0.04, ft.Colors.WHITE), content=ft.Column([ft.Text("Condición de Usuario", size=13, weight="bold"), ft.Divider(height=10, color=ft.Colors.TRANSPARENT), b_tipos]))
            ], spacing=15),
            ft.Container(padding=20, border_radius=12, bgcolor=ft.Colors.with_opacity(0.04, ft.Colors.WHITE), content=ft.Column([ft.Text("Top 5 Escuelas con más atenciones", size=13, weight="bold"), ft.Divider(height=10, color=ft.Colors.TRANSPARENT), b_escuelas]))
        ]
        
        if force_update:
            self.update()

    def _get_icon_for_case(self, name):
        n = name.lower()
        if "orient" in n: return ft.Icons.FORUM_ROUNDED
        if "seguim" in n: return ft.Icons.TRACK_CHANGES_ROUNDED
        if "monit" in n: return ft.Icons.QUERY_STATS_ROUNDED
        return ft.Icons.ASSIGNMENT_ROUNDED

    def _card(self, title, value, icon, color):
        return ft.Container(
            content=ft.Column([
                ft.Icon(icon, color=color, size=24),
                ft.Text(value, size=22, weight="bold"),
                ft.Text(title, size=10, color=ft.Colors.WHITE_54, text_align="center"),
            ], horizontal_alignment="center", spacing=2),
            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLUE_700),
            padding=15, border_radius=10,
            border=ft.border.all(1, ft.Colors.with_opacity(0.2, color)),
            width=145
        )
