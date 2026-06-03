import flet as ft
from datetime import datetime
from controllers.persona_controller import PersonaController
from views.components.socioeconomic_dialog import mostrar_ficha_socioeconomica_dialog


def build_evaluaciones_view(page: ft.Page):
    """Vista de Evaluaciones Socioeconómicas: Dashboard de Impacto y Listado de Fichas."""
    
    # ── Estado de Datos y Paginación ──────────────────────────────────────────
    datos_actuales = []
    estado_p = {
        "pagina": 1,
        "por_pagina": 15,
        "total_registros": 0
    }
    
    # ── Estado de Ordenación ────────────────────────────────────────────────
    sort_info = {"index": None, "ascending": True}

    def al_ordenar(col_idx, ascending):
        sort_info["index"] = col_idx
        sort_info["ascending"] = ascending
        tabla.sort_column_index = col_idx
        tabla.sort_ascending = ascending
        cargar_datos()

    # ── Elementos de UI ──────────────────────────────────────────────────────
    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("#", weight="bold"), on_sort=lambda e: al_ordenar(e.column_index, e.ascending)),
            ft.DataColumn(ft.Text("Fecha", weight="bold"), on_sort=lambda e: al_ordenar(e.column_index, e.ascending)),
            ft.DataColumn(ft.Text("DNI/Código", weight="bold"), on_sort=lambda e: al_ordenar(e.column_index, e.ascending)),
            ft.DataColumn(ft.Text("Estudiante", weight="bold"), on_sort=lambda e: al_ordenar(e.column_index, e.ascending)),
            ft.DataColumn(ft.Text("Caso Social", weight="bold"), on_sort=lambda e: al_ordenar(e.column_index, e.ascending)),
            ft.DataColumn(ft.Text("Condición SISFOH", weight="bold")),
            ft.DataColumn(ft.Text("Ingreso Familiar", weight="bold")),
            ft.DataColumn(ft.Text("Estado Ficha", weight="bold")),
            ft.DataColumn(ft.Text("Acciones", weight="bold")),
        ],
        column_spacing=18,
        heading_row_color=ft.Colors.with_opacity(0.1, ft.Colors.BLUE_400),
    )

    _hoy = datetime.now()
    meses_nombres = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    
    dd_mes = ft.Dropdown(
        label="Mes", width=155, value=str(_hoy.month),
        options=[
            ft.dropdown.Option(key="all", text="Todo el Año")
        ] + [ft.dropdown.Option(key=str(i+1), text=meses_nombres[i]) for i in range(12)],
        on_select=lambda _: reset_pag_y_cargar()
    )
    
    dd_año = ft.Dropdown(
        label="Año", width=110, value=str(_hoy.year),
        options=[ft.dropdown.Option(key="all", text="Todos")] + [ft.dropdown.Option(key=str(a), text=str(a)) for a in range(2026, _hoy.year + 5)],
        on_select=lambda _: reset_pag_y_cargar()
    )

    dd_estado = ft.Dropdown(
        label="Estado Ficha", width=160, value="all",
        options=[
            ft.dropdown.Option(key="all", text="Todos"),
            ft.dropdown.Option(key="completada", text="Completada"),
            ft.dropdown.Option(key="pendiente", text="Pendiente")
        ],
        on_select=lambda _: reset_pag_y_cargar()
    )

    buscador = ft.TextField(
        hint_text="Buscar por DNI, Nombre o Código...", prefix_icon=ft.Icons.SEARCH, width=350, 
        on_change=lambda _: reset_pag_y_cargar()
    )

    txt_paginacion = ft.Text("Página 1", size=13, weight="bold")
    btn_prev = ft.IconButton(ft.Icons.NAVIGATE_BEFORE, on_click=lambda _: cambiar_pag(-1), disabled=True)
    btn_next = ft.IconButton(ft.Icons.NAVIGATE_NEXT, on_click=lambda _: cambiar_pag(1))
    
    dd_per_page = ft.Dropdown(
        value="15", width=93, height=45,
        options=[ft.dropdown.Option("10"), ft.dropdown.Option("15"), 
                 ft.dropdown.Option("30"), ft.dropdown.Option("50")],
        on_select=lambda e: (estado_p.update({"por_pagina": int(e.control.value)}), reset_pag_y_cargar()),
        content_padding=ft.Padding(10,2,10,2)   
    )

    def reset_pag_y_cargar():
        estado_p["pagina"] = 1
        cargar_datos()

    def cambiar_pag(delta):
        estado_p["pagina"] += delta
        cargar_datos()

    # ── Contenedores de Dashboard Socioeconómico ──────────────────────────────
    container_stats = ft.Row(spacing=20, alignment="start")
    container_donut_sisf = ft.Container(padding=15, border_radius=15)
    container_serv_vivi = ft.Container(padding=15, border_radius=15)
    
    # ── Spinner de carga ──────────────────────────────────────────────────────
    spinner = ft.Container(
        content=ft.Column([
            ft.ProgressRing(width=50, height=50, stroke_width=4),
            ft.Text("Cargando datos...", size=12, color=ft.Colors.BLUE_200)
        ], horizontal_alignment="center", spacing=12),
        alignment=ft.Alignment(0, 0),
        expand=True,
        visible=False
    )

    def _get_ui_colors():
        is_dark = page.theme_mode == ft.ThemeMode.DARK
        return {
            "card_bg": ft.Colors.with_opacity(0.07, ft.Colors.WHITE) if is_dark else ft.Colors.WHITE,
            "panel_bg": ft.Colors.with_opacity(0.05, ft.Colors.WHITE) if is_dark else ft.Colors.GREY_50,
            "text_main": ft.Colors.WHITE if is_dark else ft.Colors.BLACK,
            "text_sub": ft.Colors.WHITE_54 if is_dark else ft.Colors.BLACK54,
            "ring_bg": ft.Colors.WHITE10 if is_dark else ft.Colors.BLACK12,
            "border": ft.Colors.WHITE10 if is_dark else ft.Colors.BLACK12,
            "shadow": ft.Colors.BLACK54 if is_dark else ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
        }

    def _badge_donut(value, total, color, label, ui):
        perc = (value / total) if total > 0 else 0
        anillo = ft.Stack([
            ft.ProgressRing(value=1.0, width=65, height=65, stroke_width=5, color=ui["ring_bg"]),
            ft.ProgressRing(value=perc, width=65, height=65, stroke_width=5, color=color),
            ft.Container(
                content=ft.Text(f"{int(perc*100)}%", size=10, weight="bold", color=ui["text_main"]),
                width=65, height=65, alignment=ft.Alignment(0, 0)
            ),
        ])
        return ft.Column([
            anillo,
            ft.Text(f"{label} ({value})", size=10, color=ui["text_sub"], text_align="center")
        ], horizontal_alignment="center", spacing=6)

    def _service_row(label, value, total, color, ui):
        perc = (value / total) if total > 0 else 0
        return ft.Column([
            ft.Row([
                ft.Text(label, size=11, color=ui["text_main"]),
                ft.Container(expand=True),
                ft.Text(f"{value}/{total} ({int(perc*100)}%)", size=11, weight="bold", color=color)
            ]),
            ft.Stack([
                ft.Container(height=10, border_radius=5, bgcolor=ui["ring_bg"]),
                ft.Container(height=10, border_radius=5, width=max(4, int(perc*200)), bgcolor=color)
            ])
        ], spacing=5)

    def actualizar_socioeconomic_dashboard():
        ui = _get_ui_colors()
        
        # Obtener métricas consolidadas
        stats = PersonaController.get_socioeconomic_analytics()
        total_eval = stats["total"]
        
        # 1. Cards superiores
        container_stats.controls = [
            ft.Container(
                expand=True, bgcolor=ui["card_bg"], padding=15, border_radius=15, border=ft.border.all(1, ui["border"]),
                shadow=ft.BoxShadow(offset=ft.Offset(2, 4), blur_radius=8, color=ui["shadow"]),
                content=ft.Column([
                    ft.Text("Evaluaciones Socioeconómicas", size=9, color=ui["text_sub"]),
                    ft.Text(str(total_eval), size=24, weight="bold", color=ft.Colors.BLUE_400)
                ], spacing=3, alignment="center"), height=85
            ),
            ft.Container(
                expand=True, bgcolor=ui["card_bg"], padding=15, border_radius=15, border=ft.border.all(1, ui["border"]),
                shadow=ft.BoxShadow(offset=ft.Offset(2, 4), blur_radius=8, color=ui["shadow"]),
                content=ft.Column([
                    ft.Text("Ingreso Familiar Promedio", size=9, color=ui["text_sub"]),
                    ft.Text(f"S/. {stats['avg_ingreso_familiar']:.2f}", size=22, weight="bold", color=ft.Colors.GREEN_400)
                ], spacing=3, alignment="center"), height=85
            ),
            ft.Container(
                expand=True, bgcolor=ui["card_bg"], padding=15, border_radius=15, border=ft.border.all(1, ui["border"]),
                shadow=ft.BoxShadow(offset=ft.Offset(2, 4), blur_radius=8, color=ui["shadow"]),
                content=ft.Column([
                    ft.Text("Gasto Alimentación Promedio", size=9, color=ui["text_sub"]),
                    ft.Text(f"S/. {stats['avg_egreso_alimentacion']:.2f}", size=22, weight="bold", color=ft.Colors.AMBER_400)
                ], spacing=3, alignment="center"), height=85
            )
        ]
        
        # 2. Condición SISFOH
        sisf_data = stats["sisfoh"]
        t_sisf = sum(sisf_data.values()) or 1
        container_donut_sisf.bgcolor = ui["panel_bg"]
        container_donut_sisf.shadow = ft.BoxShadow(blur_radius=10, color=ui["shadow"], offset=ft.Offset(0,5))
        container_donut_sisf.content = ft.Column([
            ft.Text("Clasificación de Vulnerabilidad (SISFOH)", size=13, weight="bold", color=ui["text_main"]),
            ft.Divider(height=10, color="transparent"),
            ft.Row([
                _badge_donut(sisf_data.get("No Pobre", 0), t_sisf, ft.Colors.BLUE_400, "No Pobre", ui),
                _badge_donut(sisf_data.get("Pobre", 0), t_sisf, ft.Colors.ORANGE_400, "Pobre", ui),
                _badge_donut(sisf_data.get("Pobre Extremo", 0), t_sisf, ft.Colors.RED_400, "Pobre Ext.", ui),
            ], alignment="spaceAround")
        ])
        
        # 3. Servicios Básicos
        container_serv_vivi.bgcolor = ui["panel_bg"]
        container_serv_vivi.shadow = ft.BoxShadow(blur_radius=10, color=ui["shadow"], offset=ft.Offset(0,5))
        container_serv_vivi.content = ft.Column([
            ft.Text("Acceso a Servicios Básicos en Vivienda", size=13, weight="bold", color=ui["text_main"]),
            ft.Divider(height=10, color="transparent"),
            ft.Column([
                _service_row("Agua por red pública", stats["agua_red"], total_eval, ft.Colors.CYAN_400, ui),
                _service_row("Desagüe por red pública", stats["desague_red"], total_eval, ft.Colors.BLUE_400, ui),
                _service_row("Energía Eléctrica", stats["energia_electrica"], total_eval, ft.Colors.AMBER_400, ui)
            ], spacing=12)
        ])

    def cargar_datos():
        nonlocal datos_actuales
        spinner.visible = True
        try: spinner.update()
        except: pass
        
        # Obtener todas las personas
        p_all = PersonaController.get_all(solo_activos=False)
        p_all = [p for p in p_all if p["activo"]]
        
        # Filtrar únicamente Casos de "Evaluación" o "Evaluación y Seguimiento" (que contengan evaluaci)
        p_all = [p for p in p_all if "evaluaci" in (p.get("caso_social") or "").lower()]
        
        # Filtrar por período
        if dd_mes.value and dd_mes.value != "all": 
            p_all = [p for p in p_all if p["fecha_atencion"].month == int(dd_mes.value)]
        if dd_año.value and dd_año.value != "all": 
            p_all = [p for p in p_all if p["fecha_atencion"].year == int(dd_año.value)]
            
        # Filtrar por estado Ficha
        if dd_estado.value == "completada":
            p_all = [p for p in p_all if p.get("tiene_ficha")]
        elif dd_estado.value == "pendiente":
            p_all = [p for p in p_all if not p.get("tiene_ficha")]
            
        # Buscador por texto
        f = buscador.value.upper() if buscador.value else ""
        if f: 
            p_all = [p for p in p_all if
                f in (p["dni"] or "") or
                f in (p["apellidos"] or "").upper() or
                f in (p["nombres"] or "").upper() or
                f in (p["codigo_estudiante"] or "").upper() or
                f in (p["modalidad"] or "").upper()]

        # Ordenación Dinámica según cabecera
        if sort_info["index"] is not None:
            idx = sort_info["index"]
            asc = sort_info["ascending"]
            if idx == 1: # Fecha
                p_all.sort(key=lambda p: p["fecha_atencion"], reverse=not asc)
            elif idx == 2: # DNI
                p_all.sort(key=lambda p: (p["dni"] or ""), reverse=not asc)
            elif idx == 3: # Apellidos
                p_all.sort(key=lambda p: ((p["apellidos"] or "").upper(), (p["nombres"] or "").upper()), reverse=not asc)
            elif idx == 4: # Caso Social
                p_all.sort(key=lambda p: (p["caso_social"] or ""), reverse=not asc)
            elif idx == 0: # Correlativo
                p_all.sort(key=lambda p: p["id"], reverse=not asc)
        else:
            p_all.sort(key=lambda p: ((p["apellidos"] or "").upper(), (p["nombres"] or "").upper()))
            
        datos_actuales = p_all
        
        # Paginación
        total = len(p_all)
        ppp = int(dd_per_page.value) if dd_per_page.value else 15
        estado_p["por_pagina"] = ppp

        max_pags = max(1, (total + ppp - 1) // ppp)
        if estado_p["pagina"] > max_pags: estado_p["pagina"] = max_pags
        
        inicio = (estado_p["pagina"] - 1) * ppp
        datos_paginados = p_all[inicio:inicio+ppp]
        
        txt_paginacion.value = f"Página {estado_p['pagina']} de {max_pags} ({total} registros)"
        btn_prev.disabled = estado_p["pagina"] <= 1
        btn_next.disabled = estado_p["pagina"] >= max_pags

        # Rellenar Tabla
        tabla.rows = []
        for i, p in enumerate(datos_paginados, inicio + 1):
            pid = p["id"]
            
            # Obtener datos de la ficha si ya existe
            sisfoh_val = "Pendiente"
            ingreso_val = "-"
            tiene_f = p.get("tiene_ficha")
            
            if tiene_f:
                ficha_det = PersonaController.get_ficha_socioeconomica(pid)
                if ficha_det:
                    sisfoh_val = ficha_det.get("sisfoh_condicion") or "Registrado"
                    ingreso_val = f"S/. {ficha_det.get('ingreso_familiar_total'):.2f}"
            
            sisfoh_color = ft.Colors.GREEN_400 if tiene_f else ft.Colors.AMBER_400
            ingreso_color = ft.Colors.GREEN_300 if tiene_f else ft.Colors.WHITE_54
            
            # Badges de estado de Ficha
            badge_bg = ft.Colors.with_opacity(0.12, ft.Colors.GREEN_400) if tiene_f else ft.Colors.with_opacity(0.12, ft.Colors.AMBER_400)
            badge_text = "COMPLETADA" if tiene_f else "PENDIENTE"
            badge_color = ft.Colors.GREEN_400 if tiene_f else ft.Colors.AMBER_400
            
            badge = ft.Container(
                content=ft.Text(badge_text, size=10, weight="bold", color=badge_color),
                bgcolor=badge_bg,
                padding=ft.padding.symmetric(horizontal=8, vertical=4),
                border_radius=10,
                alignment=ft.Alignment(0,0)
            )
            
            # Formato de año estudios
            anio_est = p.get("año_estudio") or "-"
            if anio_est.isdigit():
                anio_est = f"{anio_est}° Año"

            tabla.rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(str(i), size=13)),
                ft.DataCell(ft.Text(p["fecha_atencion"].strftime("%d/%m/%Y"), size=12)),
                ft.DataCell(ft.Column([ft.Text(p["dni"] or "-", size=12, weight="bold"), ft.Text(p["codigo_estudiante"] or "-", size=12, color=ft.Colors.BLUE_200, weight="bold")], spacing=0)),
                ft.DataCell(ft.Column([ft.Text(f"{p['apellidos']}, {p['nombres']}", weight="bold", size=12), ft.Text(f"{p['edad'] or '-'} años, {p['sexo'] or '-'}, {anio_est}", size=10, color=ft.Colors.WHITE_54)], spacing=0, width=220)),
                ft.DataCell(ft.Column([ft.Text(p["caso_social"], size=11, color=ft.Colors.GREEN_400, weight="bold"), ft.Text(p["facultad"], size=10, color=ft.Colors.WHITE_54)], spacing=0, width=150)),
                ft.DataCell(ft.Text(sisfoh_val, size=11, weight="bold", color=sisfoh_color)),
                ft.DataCell(ft.Text(ingreso_val, size=11, weight="bold", color=ingreso_color)),
                ft.DataCell(badge),
                ft.DataCell(ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.ASSIGNMENT_IND_ROUNDED if tiene_f else ft.Icons.ASSIGNMENT_IND_OUTLINED,
                        icon_color=ft.Colors.PURPLE_400 if tiene_f else ft.Colors.PURPLE_200,
                        icon_size=20,
                        tooltip="Editar Ficha Socioeconómica" if tiene_f else "Rellenar Ficha Socioeconómica",
                        on_click=lambda _, p=pid, n=f"{p['apellidos']}, {p['nombres']}": mostrar_ficha_socioeconomica_dialog(
                            page, p, n, on_save_callback=lambda: (cargar_datos(), actualizar_socioeconomic_dashboard())
                        )
                    )
                ], spacing=0)),
            ]))
            
        # Recargar Dashboard
        actualizar_socioeconomic_dashboard()
        
        spinner.visible = False
        page.update()

    cargar_datos()

    # ── Layout Flexible ──────────────────────────────────────────────
    area_tabla = ft.Container(
        content=ft.Row(
            [ft.Column([tabla], scroll=ft.ScrollMode.AUTO)],
            scroll=ft.ScrollMode.ALWAYS,
            vertical_alignment=ft.CrossAxisAlignment.START
        ),
        expand=True,
    )
    zona_contenido = ft.Stack([area_tabla, spinner], expand=True)

    # Dashboard Superior en un Row responsivo de dos paneles
    dashboard_row = ft.ResponsiveRow([
        ft.Container(col={"sm": 12, "md": 6}, content=container_donut_sisf),
        ft.Container(col={"sm": 12, "md": 6}, content=container_serv_vivi)
    ], spacing=20)

    return ft.Container(
        padding=ft.padding.only(left=25, right=25, top=20, bottom=10), expand=True,
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.ASSIGNMENT_IND_ROUNDED, color=ft.Colors.PURPLE_300, size=28), 
                ft.Text("Módulo de Evaluaciones Socioeconómicas", size=24, weight="bold"),
            ]),
            ft.Divider(color=ft.Colors.BLUE_900),
            
            # Estadísticas y Dashboard superior
            container_stats,
            dashboard_row,
            ft.Divider(height=10, color="transparent"),
            
            # Buscador y filtros
            ft.Row([buscador, dd_estado, dd_mes, dd_año, ft.IconButton(ft.Icons.RESTART_ALT_ROUNDED, on_click=lambda _: reset_pag_y_cargar())], spacing=10, wrap=True),
            
            # Tabla / Spinner
            zona_contenido,
            
            # Barra de Paginación
            ft.Container(
                padding=ft.padding.symmetric(horizontal=10, vertical=5), bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.BLUE_700), border_radius=8,
                content=ft.Row([
                    ft.Row([ft.Text("Ver:", size=11, color=ft.Colors.WHITE_54), dd_per_page], spacing=10),
                    ft.VerticalDivider(width=20),
                    txt_paginacion,
                    ft.Container(expand=True),
                    ft.Row([btn_prev, btn_next], spacing=5)
                ], alignment=ft.MainAxisAlignment.CENTER)
            )
        ], expand=True, spacing=12)
    )
