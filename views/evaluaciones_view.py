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
    
    opciones_estado = [("completada", "Completada"), ("pendiente", "Pendiente")]
    opciones_mes = [(str(i+1), meses_nombres[i]) for i in range(12)]
    años_options = [str(a) for a in range(2026, _hoy.year + 5)]
    opciones_año = [(a, a) for a in años_options]
    
    selected_estados = {"completada", "pendiente"}
    selected_meses = {str(_hoy.month)}
    selected_años = {str(_hoy.year)}

    # Funciones auxiliares para el formato de texto de los botones
    def get_estados_text():
        if not selected_estados:
            return "Ninguno"
        if len(selected_estados) == 2:
            return "Todos"
        return ", ".join(e.capitalize() for e in selected_estados)

    def get_meses_text():
        if not selected_meses:
            return "Ninguno"
        if len(selected_meses) == 12:
            return "Todo el Año"
        names = [meses_nombres[int(m)-1] for m in sorted(list(selected_meses), key=int)]
        text = ", ".join(names)
        if len(text) > 12:
            return f"{len(selected_meses)} Meses"
        return text

    def get_años_text():
        if not selected_años:
            return "Ninguno"
        if len(selected_años) == len(años_options):
            return "Todos"
        text = ", ".join(sorted(list(selected_años)))
        if len(text) > 10:
            return f"{len(selected_años)} Años"
        return text

    # Auxiliar para construir botones estilizados de filtros estilo dropdown
    def crear_filtro_boton(label, get_text_func, on_click_func, width):
        text_control = ft.Text(get_text_func(), size=12, overflow=ft.TextOverflow.ELLIPSIS)
        
        def on_hover(e):
            e.control.border = ft.border.all(1, ft.Colors.BLUE_400 if e.data == "true" else ft.Colors.WHITE_38)
            e.control.update()
            
        btn = ft.Container(
            content=ft.Row([
                ft.Column([
                    ft.Text(label, size=9, color=ft.Colors.WHITE_54, weight="bold"),
                    text_control,
                ], spacing=2, alignment=ft.MainAxisAlignment.CENTER, expand=True),
                ft.Icon(ft.Icons.ARROW_DROP_DOWN, color=ft.Colors.WHITE_54, size=20)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment="center"),
            width=width,
            height=48,
            border=ft.border.all(1, ft.Colors.WHITE_38),
            border_radius=8,
            padding=ft.padding.symmetric(horizontal=10, vertical=4),
            on_click=on_click_func,
            on_hover=on_hover,
            ink=True,
        )
        
        btn.data = {"update_text": lambda: setattr(text_control, "value", get_text_func())}
        return btn

    # Capa superior de overlay para el selector flotante y barrera transparente
    active_dropdown = {"name": None}
    overlay_layer = ft.Stack(expand=True, visible=False)

    def close_all_dropdowns():
        overlay_layer.controls.clear()
        overlay_layer.visible = False
        active_dropdown["name"] = None
        try: overlay_layer.update()
        except: pass

    # Controlador de menú desplegable con checkmarks que no se cierra al hacer clic
    def toggle_dropdown(name, btn, opciones, selected_set, left_pos, width_val, height_val):
        if active_dropdown["name"] == name:
            close_all_dropdowns()
            return
            
        close_all_dropdowns()
        active_dropdown["name"] = name
        
        # 1. Barrera transparente hit-testable
        barrier = ft.Container(
            expand=True,
            bgcolor=ft.Colors.with_opacity(0.0, ft.Colors.BLACK),
            on_click=lambda _: close_all_dropdowns()
        )
        
        # 2. Contenedor de checkboxes
        checkboxes_col = ft.Column(scroll=ft.ScrollMode.AUTO, tight=True, spacing=5)
        
        def rebuild_dropdown_content():
            checkboxes_col.controls.clear()
            all_selected = len(selected_set) == len(opciones)
            
            def toggle_all(e):
                if all_selected:
                    selected_set.clear()
                else:
                    selected_set.clear()
                    selected_set.update(k for k, _ in opciones)
                btn.data["update_text"]()
                btn.update()
                rebuild_dropdown_content()
                card.update()
                reset_pag_y_cargar()
                
            chk_all = ft.Checkbox(
                label="Seleccionar Todos",
                value=all_selected,
                on_change=toggle_all,
                fill_color=ft.Colors.BLUE_400
            )
            checkboxes_col.controls.append(chk_all)
            checkboxes_col.controls.append(ft.Divider(height=5, color=ft.Colors.WHITE_24))
            
            for key, label in opciones:
                is_checked = key in selected_set
                
                def make_on_change(k):
                    def on_change(e):
                        if e.control.value:
                            selected_set.add(k)
                        else:
                            selected_set.discard(k)
                        btn.data["update_text"]()
                        btn.update()
                        rebuild_dropdown_content()
                        card.update()
                        reset_pag_y_cargar()
                    return on_change
                    
                chk = ft.Checkbox(
                    label=label,
                    value=is_checked,
                    on_change=make_on_change(key)
                )
                checkboxes_col.controls.append(chk)
                
        rebuild_dropdown_content()
        
        card = ft.Card(
            content=ft.Container(
                content=checkboxes_col,
                padding=10,
                width=width_val,
                height=height_val,
            ),
            left=left_pos,
            top=48, # Nacimiento exacto en el borde inferior del botón
            elevation=10,
            shadow_color=ft.Colors.BLACK
        )
        
        overlay_layer.controls.append(barrier)
        overlay_layer.controls.append(card)
        overlay_layer.visible = True
        overlay_layer.update()

    # Crear botones de filtro
    btn_estado_filtro = crear_filtro_boton(
        "Estado Ficha", 
        get_estados_text, 
        lambda _: toggle_dropdown("Estado Ficha", btn_estado_filtro, opciones_estado, selected_estados, 260, 150, 140), 
        150
    )
    btn_mes_filtro = crear_filtro_boton(
        "Mes", 
        get_meses_text, 
        lambda _: toggle_dropdown("Mes", btn_mes_filtro, opciones_mes, selected_meses, 420, 140, 220), 
        120
    )
    btn_año_filtro = crear_filtro_boton(
        "Año", 
        get_años_text, 
        lambda _: toggle_dropdown("Año", btn_año_filtro, opciones_año, selected_años, 550, 140, 180), 
        90
    )

    buscador = ft.TextField(
        hint_text="Buscar por DNI, Nombre o Código...", prefix_icon=ft.Icons.SEARCH, width=250, 
        on_change=lambda _: (close_all_dropdowns(), reset_pag_y_cargar())
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
        close_all_dropdowns()
        estado_p["pagina"] = 1
        cargar_datos()

    def cambiar_pag(delta):
        close_all_dropdowns()
        estado_p["pagina"] += delta
        cargar_datos()

    def limpiar_filtros(e):
        selected_estados.clear()
        selected_estados.update(["completada", "pendiente"])
        selected_meses.clear()
        selected_meses.add(str(datetime.now().month))
        selected_años.clear()
        selected_años.add(str(datetime.now().year))
        buscador.value = ""
        reset_pag_y_cargar()

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
        
        # Filtrar por período (mes y año)
        if selected_meses:
            p_all = [p for p in p_all if str(p["fecha_atencion"].month) in selected_meses]
        else:
            p_all = []
            
        if selected_años:
            p_all = [p for p in p_all if str(p["fecha_atencion"].year) in selected_años]
        else:
            p_all = []
            
        # Filtrar por estado Ficha
        def match_estado(p):
            tiene_f = p.get("tiene_ficha")
            if tiene_f:
                return "completada" in selected_estados
            else:
                return "pendiente" in selected_estados
                
        if selected_estados:
            p_all = [p for p in p_all if match_estado(p)]
        else:
            p_all = []
            
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
        
        # Actualizar textos de los botones de filtro
        try:
            for btn in [btn_estado_filtro, btn_mes_filtro, btn_año_filtro]:
                btn.data["update_text"]()
                btn.update()
        except: pass

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

    pagination_bar = ft.Container(
        padding=ft.padding.symmetric(horizontal=10, vertical=5),
        bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.BLUE_700),
        border_radius=8,
        content=ft.Row([
            ft.Row([
                ft.Text("Ver:", size=11, color=ft.Colors.WHITE_54),
                dd_per_page
            ], spacing=10),
            ft.VerticalDivider(width=20),
            txt_paginacion,
            ft.Container(expand=True),
            ft.Row([btn_prev, btn_next], spacing=5)
        ], alignment=ft.MainAxisAlignment.CENTER)
    )

    filters_row = ft.Row([
        buscador,
        btn_estado_filtro,
        btn_mes_filtro,
        btn_año_filtro,
        ft.IconButton(ft.Icons.RESTART_ALT_ROUNDED, tooltip="Limpiar Filtros", on_click=limpiar_filtros),
    ], spacing=10, wrap=False, vertical_alignment=ft.CrossAxisAlignment.CENTER)

    filters_and_table_stack = ft.Stack([
        ft.Column([
            filters_row,
            zona_contenido,
            pagination_bar
        ], expand=True, spacing=12),
        overlay_layer
    ], expand=True)

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
            
            # Filtros, Tabla y Paginación
            filters_and_table_stack
        ], expand=True, spacing=12)
    )
