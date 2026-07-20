import flet as ft
from controllers.persona_controller import PersonaController
from database.db_config import SessionLocal
from database.models import Persona, Atencion, FichaDerivacion
from core.ui_helpers import mostrar_exito, mostrar_snackbar
from views.components.derivacion_dialog import mostrar_ficha_derivacion_dialog

def build_derivaciones_view(page: ft.Page):
    """Vista de Gestión de Derivaciones."""

    # ── Filtros Multi-selección ───────────────────────────────────────────────────
    import datetime
    _hoy = datetime.datetime.now()
    
    meses_nombres = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
                     "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
                     
    opciones_mes = [(str(i), m) for i, m in enumerate(meses_nombres, 1)]
    
    # Filtro de Año de 2025 a 2030
    años_options = [str(a) for a in range(2025, 2031)]
    opciones_año = [(a, a) for a in años_options]
    
    selected_meses = {str(_hoy.month)}
    selected_años = {str(_hoy.year)}

    estado_p = {"pagina": 1, "por_pagina": 20}

    txt_paginacion = ft.Text("Página 1", size=13, weight="bold")
    
    def cambiar_pag(delta):
        estado_p["pagina"] += delta
        cargar_datos()

    def reset_pag_y_cargar():
        estado_p["pagina"] = 1
        cargar_datos()

    btn_prev = ft.IconButton(ft.Icons.NAVIGATE_BEFORE, on_click=lambda _: cambiar_pag(-1), disabled=True)
    btn_next = ft.IconButton(ft.Icons.NAVIGATE_NEXT, on_click=lambda _: cambiar_pag(1))

    dd_per_page = ft.Dropdown(
        value="20", width=93, height=45,
        options=[ft.dropdown.Option("10"), ft.dropdown.Option("20"), 
                 ft.dropdown.Option("30"), ft.dropdown.Option("50")],
        on_select=lambda e: (estado_p.update({"por_pagina": int(e.control.value)}), reset_pag_y_cargar()),
        content_padding=ft.Padding(10,2,10,2)   
    )
    
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

    # Funciones auxiliares para el formato de texto de los botones
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

    btn_mes_filtro = crear_filtro_boton(
        "Mes", 
        get_meses_text, 
        lambda _: toggle_dropdown("Mes", btn_mes_filtro, opciones_mes, selected_meses, 260, 140, 220), 
        120
    )
    btn_año_filtro = crear_filtro_boton(
        "Año", 
        get_años_text, 
        lambda _: toggle_dropdown("Año", btn_año_filtro, opciones_año, selected_años, 390, 140, 180), 
        90
    )

    buscador = ft.TextField(
        hint_text="Buscar por DNI o Nombre...", prefix_icon=ft.Icons.SEARCH, width=250, 
        on_change=lambda _: (close_all_dropdowns(), reset_pag_y_cargar())
    )

    def limpiar_filtros(_):
        selected_meses.clear()
        selected_años.clear()
        selected_meses.add(str(_hoy.month))
        selected_años.add(str(_hoy.year))
        buscador.value = ""
        buscador.update()
        for btn in [btn_mes_filtro, btn_año_filtro]:
            btn.data["update_text"]()
            btn.update()
        close_all_dropdowns()
        reset_pag_y_cargar()

    # ── Tabla ───────────────────────────────────────────────────────────────
    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("#", weight="bold")),
            ft.DataColumn(ft.Text("Fecha Atención", weight="bold")),
            ft.DataColumn(ft.Text("DNI", weight="bold")),
            ft.DataColumn(ft.Text("Apellidos y Nombres", weight="bold")),
            ft.DataColumn(ft.Text("Facultad", weight="bold")),
            ft.DataColumn(ft.Text("Estado Ficha", weight="bold")),
            ft.DataColumn(ft.Text("Acciones", weight="bold")),
        ],
        column_spacing=20,
        heading_row_color=ft.Colors.with_opacity(0.1, ft.Colors.BLUE_400),
    )

    # ── Spinner de carga ──────────────────────────────────────────────────────
    spinner = ft.Container(
        content=ft.Column([
            ft.ProgressRing(width=50, height=50, stroke_width=4),
            ft.Text("Cargando derivaciones...", size=12, color=ft.Colors.BLUE_200)
        ], horizontal_alignment="center", spacing=12),
        alignment=ft.Alignment(0, 0),
        expand=True,
        visible=False
    )

    # ── Cargar filas ─────────────────────────────────────────────────────────
    def cargar_datos(*args):
        spinner.visible = True
        try: spinner.update()
        except: pass

        db = SessionLocal()
        try:
            from sqlalchemy import or_, extract
            from database.models import CatCasoSocial
            
            casos_derivacion = db.query(CatCasoSocial.id).filter(CatCasoSocial.nombre.ilike("%derivaci%")).all()
            caso_ids = [c[0] for c in casos_derivacion]
            
            query = db.query(Atencion, Persona, FichaDerivacion.id.label("ficha_id")).select_from(Atencion).join(
                Persona, Atencion.persona_id == Persona.id
            ).outerjoin(
                FichaDerivacion, Atencion.id == FichaDerivacion.atencion_id
            ).filter(Atencion.activo == True).filter(
                or_(Atencion.caso_social_id.in_(caso_ids), FichaDerivacion.id != None)
            )
            
            filtro = buscador.value if buscador.value else ""
            if filtro:
                f = filtro.upper()
                query = query.filter(
                    or_(
                        Persona.dni.contains(f),
                        Persona.apellidos.contains(f),
                        Persona.nombres.contains(f)
                    )
                )
                
            if selected_meses:
                query = query.filter(extract('month', Atencion.fecha_atencion).in_([int(m) for m in selected_meses]))
                
            if selected_años:
                query = query.filter(extract('year', Atencion.fecha_atencion).in_([int(a) for a in selected_años]))
                
            query = query.order_by(Atencion.fecha_atencion.desc())
            resultados_totales = query.all()
            
            total = len(resultados_totales)
            ppp = estado_p["por_pagina"]
            max_pags = max(1, (total + ppp - 1) // ppp)
            
            if estado_p["pagina"] > max_pags: estado_p["pagina"] = max_pags
            
            inicio = (estado_p["pagina"] - 1) * ppp
            resultados = resultados_totales[inicio:inicio+ppp]
            
            txt_paginacion.value = f"Página {estado_p['pagina']} de {max_pags} ({total} registros)"
            btn_prev.disabled = estado_p["pagina"] <= 1
            btn_next.disabled = estado_p["pagina"] >= max_pags
            
            tabla.rows = []
            for i, (atencion, p, ficha_id) in enumerate(resultados, inicio + 1):
                estado_texto = "Completada" if ficha_id else "Pendiente"
                estado_color = ft.Colors.GREEN_400 if ficha_id else ft.Colors.ORANGE_400
                
                tabla.rows.append(ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(i), size=13)),
                    ft.DataCell(ft.Text(atencion.fecha_atencion.strftime("%d/%m/%Y"), size=12)),
                    ft.DataCell(ft.Text(p.dni or "-", size=12, weight="bold")),
                    ft.DataCell(ft.Text(f"{p.apellidos}, {p.nombres}", weight="bold", size=12)),
                    ft.DataCell(ft.Text(p.facultad.nombre if p.facultad else "-", size=12)),
                    ft.DataCell(ft.Text(estado_texto, size=12, color=estado_color, weight="bold")),
                    ft.DataCell(ft.Row([
                        ft.ElevatedButton(
                            "Ficha", 
                            icon=ft.Icons.ASSIGNMENT_IND, 
                            bgcolor=ft.Colors.BLUE_800 if not ficha_id else ft.Colors.GREEN_800,
                            color=ft.Colors.WHITE,
                            on_click=lambda _, aid=atencion.id: mostrar_ficha_derivacion_dialog(page, aid, cargar_datos)
                        )
                    ])),
                ]))
        finally:
            db.close()

        spinner.visible = False
        try:
            txt_paginacion.update()
            btn_prev.update()
            btn_next.update()
        except:
            pass
        page.update()

    cargar_datos()

    area_tabla = ft.Container(
        content=ft.Row(
            [ft.Column([tabla], scroll=ft.ScrollMode.AUTO)],
            scroll=ft.ScrollMode.ALWAYS,
            vertical_alignment=ft.CrossAxisAlignment.START
        ),
        expand=True,
    )
    
    zona_contenido = ft.Stack([area_tabla, spinner], expand=True)

    main_column = ft.Column([
        ft.Row([
            ft.Icon(ft.Icons.SHARE_ROUNDED, color=ft.Colors.BLUE_400, size=28),
            ft.Text("Derivación de Casos Sociales", size=24, weight="bold"),
        ], spacing=10),
        ft.Divider(color=ft.Colors.BLUE_900),
        ft.Row([
            buscador, 
            btn_mes_filtro, 
            btn_año_filtro,
            ft.IconButton(ft.Icons.RESTART_ALT_ROUNDED, tooltip="Limpiar Filtros", on_click=limpiar_filtros)
        ], alignment=ft.MainAxisAlignment.START, spacing=15),
        ft.Divider(height=5, color="transparent"),
        zona_contenido,
        pagination_bar
    ], expand=True, spacing=12)

    filters_and_table_stack = ft.Stack([
        main_column,
        overlay_layer
    ], expand=True)

    return ft.Container(
        padding=ft.padding.only(left=25, right=25, top=20, bottom=10),
        expand=True,
        content=filters_and_table_stack
    )
