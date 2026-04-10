import flet as ft
from datetime import datetime
from controllers.persona_controller import PersonaController
from core.ui_helpers import mostrar_snackbar, mostrar_exito
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill
import os


def build_historial_view(page: ft.Page):
    """Vista de Historial: Informe Mensual con Paginación y Excel."""
    
    # ── Estado de Datos y Paginación ──────────────────────────────────────────
    datos_actuales = [] # Lista completa filtrada para Excel
    estado_p = {
        "pagina": 1,
        "por_pagina": 20,
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
            ft.DataColumn(ft.Text("Apellidos y Nombres", weight="bold"), on_sort=lambda e: al_ordenar(e.column_index, e.ascending)),
            ft.DataColumn(ft.Text("Cel./Correo", weight="bold")),
            ft.DataColumn(ft.Text("Tipo/Caso", weight="bold"), on_sort=lambda e: al_ordenar(e.column_index, e.ascending)),
            ft.DataColumn(ft.Text("Facultad/Escuela", weight="bold"), on_sort=lambda e: al_ordenar(e.column_index, e.ascending)),
            ft.DataColumn(ft.Text("Obs./Dirección", weight="bold")),
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
        options=[ft.dropdown.Option(key=str(a), text=str(a)) for a in range(2026, _hoy.year + 5)],
        on_select=lambda _: reset_pag_y_cargar()
    )

    buscador = ft.TextField(
        label="Buscar...", prefix_icon=ft.Icons.SEARCH, expand=True, 
        on_change=lambda _: reset_pag_y_cargar()
    )

    txt_paginacion = ft.Text("Página 1", size=13, weight="bold")
    btn_prev = ft.IconButton(ft.Icons.NAVIGATE_BEFORE, on_click=lambda _: cambiar_pag(-1), disabled=True)
    btn_next = ft.IconButton(ft.Icons.NAVIGATE_NEXT, on_click=lambda _: cambiar_pag(1))
    
    dd_per_page = ft.Dropdown(
        value="20", width=93, height=45,
        options=[ft.dropdown.Option("10"), ft.dropdown.Option("20"), 
                 ft.dropdown.Option("50"), ft.dropdown.Option("100")],
        on_select=lambda e: (estado_p.update({"por_pagina": int(e.control.value)}), reset_pag_y_cargar()),
        content_padding=ft.Padding(10,2,10,2)   
    )

    def reset_pag_y_cargar():
        estado_p["pagina"] = 1
        cargar_datos()

    def cambiar_pag(delta):
        estado_p["pagina"] += delta
        cargar_datos()

    # ── Exportación Excel ────────────────────────────────────────────────────
    def exportar_excel(e):
        if not datos_actuales:
            mostrar_snackbar(page, "No hay datos para exportar", "red")
            return
        try:
            wb = openpyxl.Workbook()
            ws = wb.active
            headers = ["N°", "DNI", "APELLIDOS Y NOMBRES", "EDAD", "SEXO", "TIPO DE USUARIO", "CODIGO EST", "AÑO DE ESTUDIOS", "FACULTAD", "ESCUELA", "CASO SOCIAL"]
            fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
            font = Font(color="FFFFFF", bold=True)
            for col, h in enumerate(headers, 1):
                cell = ws.cell(row=1, column=col, value=h)
                cell.fill = fill; cell.font = font; cell.alignment = Alignment(horizontal="center")
            for i, p in enumerate(datos_actuales, 1):
                ws.append([i, p.get("dni","-"), f"{p['apellidos']}, {p['nombres']}".upper(), p.get("edad","-"), p.get("sexo","-"), p.get("tipo_usuario","-"), p.get("codigo_estudiante","-"), p.get("año_estudio","-"), p.get("facultad","-"), p.get("escuela","-"), p.get("caso_social","-")])
            periodo = "Anual" if dd_mes.value == "all" else meses_nombres[int(dd_mes.value)-1]
            filename = f"Informe_{periodo}_{dd_año.value}.xlsx"
            filepath = os.path.join(os.path.expanduser("~"), "Downloads", filename)
            try: wb.save(filepath); mostrar_exito(page, f"✔ en Descargas")
            except: wb.save(filename); mostrar_exito(page, f"✔ en CarpetaLocal")
        except Exception as ex: mostrar_snackbar(page, f"Error: {str(ex)}", "red")

    def cargar_datos():
        nonlocal datos_actuales
        p_all = PersonaController.get_all(solo_activos=False)
        p_all = [p for p in p_all if p["activo"]]
        if dd_mes.value and dd_mes.value != "all": p_all = [p for p in p_all if p["fecha_atencion"].month == int(dd_mes.value)]
        if dd_año.value: p_all = [p for p in p_all if p["fecha_atencion"].year == int(dd_año.value)]
        f = buscador.value.upper() if buscador.value else ""
        if f: p_all = [p for p in p_all if f in (p["dni"] or "") or f in (p["apellidos"] or "").upper() or f in (p["nombres"] or "").upper()]

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
            elif idx == 5: # Tipo de Usuario
                p_all.sort(key=lambda p: (p["tipo_usuario"] or ""), reverse=not asc)
            elif idx == 6: # Facultad/Escuela
                p_all.sort(key=lambda p: ((p["facultad"] or "").upper(), (p["escuela"] or "").upper()), reverse=not asc)
            elif idx == 0: # # Correlativo
                p_all.sort(key=lambda p: p["id"], reverse=not asc)
        else:
            p_all.sort(key=lambda p: ((p["apellidos"] or "").upper(), (p["nombres"] or "").upper()))
        datos_actuales = p_all # Guardar para Excel
        
        total = len(p_all)
        # Ajuste de combo por_pagina
        ppp = int(dd_per_page.value) if dd_per_page.value else 20
        estado_p["por_pagina"] = ppp

        max_pags = max(1, (total + ppp - 1) // ppp)
        if estado_p["pagina"] > max_pags: estado_p["pagina"] = max_pags
        
        inicio = (estado_p["pagina"] - 1) * ppp
        datos_paginados = p_all[inicio:inicio+ppp]
        
        txt_paginacion.value = f"Página {estado_p['pagina']} de {max_pags} ({total} registros)"
        btn_prev.disabled = estado_p["pagina"] <= 1
        btn_next.disabled = estado_p["pagina"] >= max_pags

        tabla.rows = []
        for i, p in enumerate(datos_paginados, inicio + 1):
            tabla.rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(str(i), size=13)),
                ft.DataCell(ft.Text(p["fecha_atencion"].strftime("%d/%m/%Y"), size=12)),
                ft.DataCell(ft.Column([ft.Text(p["dni"] or "-", size=12, weight="bold"), ft.Text(p["codigo_estudiante"] or "-", size=12, color=ft.Colors.BLUE_200, weight="bold")], spacing=0)),
                ft.DataCell(ft.Column([ft.Text(f"{p['apellidos']}, {p['nombres']}", weight="bold", size=12), ft.Text(f"{p['edad'] or '-'} años, {p['sexo'] or '-'} ", size=10, color=ft.Colors.WHITE_54)], spacing=0, width=260)),
                ft.DataCell(ft.Column([ft.Text(p["celular"] or "-", size=12), ft.Text(p["correo"] or "-", size=11, color=ft.Colors.BLUE_200)], spacing=0, width=120)),
                ft.DataCell(ft.Column([ft.Text(p["tipo_usuario"], size=11), ft.Text(p["caso_social"], size=11, color=ft.Colors.GREEN_400, weight="bold")], spacing=0, width=100)),
                ft.DataCell(ft.Column([ft.Text(p["facultad"], size=11), ft.Text(p["escuela"], size=10, color=ft.Colors.WHITE_54)], spacing=0, width=150)),
                ft.DataCell(ft.Column([ft.Text(p["observaciones"] or "-", size=11, italic=True), ft.Text(p["direccion"] or "-", size=10, color=ft.Colors.WHITE_54)], spacing=0, width=200)),
            ]))
        page.update()

    cargar_datos()

    # ── Layout Flexible ──────────────────────────────────────────────────────
    area_tabla = ft.Container(
        content=ft.Row(
            [ft.Column([tabla], scroll=ft.ScrollMode.AUTO)],
            scroll=ft.ScrollMode.ALWAYS,
            vertical_alignment=ft.CrossAxisAlignment.START
        ),
        expand=True,
    )

    return ft.Container(
        padding=ft.padding.only(left=25, right=25, top=20, bottom=10), expand=True,
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.HISTORY_ROUNDED, color=ft.Colors.BLUE_400, size=28), ft.Text("Historial de Atenciones", size=24, weight="bold"),
                ft.Container(expand=True),
                ft.ElevatedButton("Excel", icon=ft.Icons.FILE_DOWNLOAD, bgcolor=ft.Colors.GREEN_800, color=ft.Colors.WHITE, on_click=exportar_excel)
            ]),
            ft.Divider(color=ft.Colors.BLUE_900),
            ft.Row([buscador, dd_mes, dd_año, ft.IconButton(ft.Icons.RESTART_ALT_ROUNDED, on_click=lambda _: reset_pag_y_cargar())], spacing=10),
            
            # Tabla Expandible
            area_tabla,
            
            # Barra de Paginacion fija abajo
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
