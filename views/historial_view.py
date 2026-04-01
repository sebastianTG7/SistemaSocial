import flet as ft
from datetime import datetime
from controllers.persona_controller import PersonaController
from core.ui_helpers import mostrar_snackbar, mostrar_exito
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill
import os


def build_historial_view(page: ft.Page):
    """Vista de Historial: Generación de Informe Mensual en Excel."""
    
    # ── Estado de Datos ──────────────────────────────────────────────────────
    datos_actuales = [] # Para exportar lo mismo que se ve en la tabla

    # ── Componentes de la Tabla ───────────────────────────────────────────────
    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("#", weight="bold")),
            ft.DataColumn(ft.Text("Fecha", weight="bold")),
            ft.DataColumn(ft.Text("DNI/Código", weight="bold")),
            ft.DataColumn(ft.Text("Apellidos y Nombres", weight="bold")),
            ft.DataColumn(ft.Text("Cel./Correo", weight="bold")),
            ft.DataColumn(ft.Text("Tipo/Caso", weight="bold")),
            ft.DataColumn(ft.Text("Facultad/Escuela", weight="bold")),
            ft.DataColumn(ft.Text("Obs./Dirección", weight="bold")),
        ],
        column_spacing=18,
        heading_row_color=ft.Colors.with_opacity(0.1, ft.Colors.BLUE_400),
    )

    # ── Filtros de Fecha (Por defecto: Mes Actual) ─────────────────────────
    _hoy = datetime.now()
    meses_nombres = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    
    dd_mes = ft.Dropdown(
        label="Mes", width=140, value=str(_hoy.month),
        options=[ft.dropdown.Option(key=str(i+1), text=meses_nombres[i]) for i in range(12)],
        on_select=lambda _: cargar_datos()
    )
    
    anios_lista = [str(a) for a in range(2023, _hoy.year + 3)]
    dd_año = ft.Dropdown(
        label="Año", width=110, value=str(_hoy.year),
        options=[ft.dropdown.Option(key=str(a), text=str(a)) for a in anios_lista],
        on_select=lambda _: cargar_datos()
    )

    buscador = ft.TextField(
        label="Buscar por DNI o Nombres...", 
        prefix_icon=ft.Icons.SEARCH, 
        expand=True, 
        on_change=lambda _: cargar_datos()
    )

    # ── Función de Exportación Excel ─────────────────────────────────────────
    def exportar_excel(e):
        if not datos_actuales:
            mostrar_snackbar(page, "No hay datos para exportar", "red")
            return
            
        try:
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Informe Social"
            
            # Cabeceras (Las que pediste exactamente)
            headers = [
                "N°", "DNI", "APELLIDOS Y NOMBRES", "EDAD", "SEXO", 
                "TIPO DE USUARIO", "CODIGO EST", "AÑO DE ESTUDIOS", 
                "FACULTAD", "ESCUELA", "CASO SOCIAL"
            ]
            
            # Estilo de cabeceras
            fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
            font = Font(color="FFFFFF", bold=True)
            
            for col, header in enumerate(headers, 1):
                cell = ws.cell(row=1, column=col, value=header)
                cell.fill = fill
                cell.font = font
                cell.alignment = Alignment(horizontal="center")

            # Insertar Datos
            for i, p in enumerate(datos_actuales, 1):
                row = [
                    i,
                    p.get("dni", "-"),
                    f"{p['apellidos']}, {p['nombres']}".upper(),
                    p.get("edad", "-"),
                    p.get("sexo", "-"),
                    p.get("tipo_usuario", "-"),
                    p.get("codigo_estudiante", "-"),
                    p.get("año_estudio", "-"),
                    p.get("facultad", "-"),
                    p.get("escuela", "-"),
                    p.get("caso_social", "-")
                ]
                ws.append(row)

            # Ajustar anchos
            for col in ws.columns:
                max_length = 0
                column = col[0].column_letter
                for cell in col:
                    try:
                        if len(str(cell.value)) > max_length: max_length = len(str(cell.value))
                    except: pass
                ws.column_dimensions[column].width = max_length + 2

            # Guardar archivo
            filename = f"Informe_Social_{meses_nombres[int(dd_mes.value)-1]}_{dd_año.value}.xlsx"
            filepath = os.path.join(os.path.expanduser("~"), "Downloads", filename)
            
            # Si falla la descarga a Downloads, guardamos en la carpeta actual
            try:
                wb.save(filepath)
                mostrar_exito(page, f"✔ Excel guardado en Descargas: {filename}")
            except:
                wb.save(filename)
                mostrar_exito(page, f"✔ Excel guardado en carpeta del programa: {filename}")
                
        except Exception as ex:
            mostrar_snackbar(page, f"Error al generar Excel: {str(ex)}", "red")

    def cargar_datos():
        nonlocal datos_actuales
        # Obtener TODOS pero filtrar solo ACTÍVOS (los que van pal informe)
        p_all = PersonaController.get_all(solo_activos=False)
        p_all = [p for p in p_all if p["activo"]] # Solo activos en el informe
        
        if dd_mes.value:
            p_all = [p for p in p_all if p["fecha_atencion"].month == int(dd_mes.value)]
        if dd_año.value:
            p_all = [p for p in p_all if p["fecha_atencion"].year == int(dd_año.value)]
            
        f = buscador.value.upper() if buscador.value else ""
        if f:
            p_all = [p for p in p_all if f in (p["dni"] or "") or f in (p["apellidos"] or "").upper() or f in (p["nombres"] or "").upper()]
            
        # Orden alfabético
        p_all.sort(key=lambda p: ((p["apellidos"] or "").upper(), (p["nombres"] or "").upper()))
        datos_actuales = p_all

        tabla.rows = []
        for i, p in enumerate(p_all, 1):
            tabla.rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(str(i), size=13)),
                ft.DataCell(ft.Text(p["fecha_atencion"].strftime("%d/%m/%Y"), size=12)),
                ft.DataCell(ft.Column([
                    ft.Text(p["dni"] or "-", size=12, weight="bold"),
                    ft.Text(p["codigo_estudiante"] or "-", size=12, color=ft.Colors.BLUE_200, weight="bold")
                ], spacing=0)),
                ft.DataCell(ft.Column([
                    ft.Text(f"{p['apellidos']}, {p['nombres']}", weight="bold", size=12),
                    ft.Text(f"{p['edad'] or '-'} años, {p['sexo'] or '-'}", size=10, color=ft.Colors.WHITE_54)
                ], spacing=0, width=260)),
                ft.DataCell(ft.Column([
                    ft.Text(p["celular"] or "-", size=12),
                    ft.Text(p["correo"] or "-", size=11, color=ft.Colors.BLUE_200)
                ], spacing=0, width=120)),
                ft.DataCell(ft.Column([
                    ft.Text(p["tipo_usuario"], size=11),
                    ft.Text(p["caso_social"], size=11, color=ft.Colors.GREEN_400, weight="bold")
                ], spacing=0, width=100)),
                ft.DataCell(ft.Column([
                    ft.Text(p["facultad"], size=11),
                    ft.Text(p["escuela"], size=10, color=ft.Colors.WHITE_54)
                ], spacing=0, width=140)),
                ft.DataCell(ft.Column([
                    ft.Text(p["observaciones"] or "-", size=11, italic=True),
                    ft.Text(p["direccion"] or "-", size=10, color=ft.Colors.WHITE_54)
                ], spacing=0, width=200)),
            ]))
        page.update()

    def limpiar_filtros(e):
        dd_mes.value = str(_hoy.month)
        dd_año.value = str(_hoy.year)
        buscador.value = ""
        cargar_datos()

    cargar_datos()

    # ── Layout de la Vista ─────────────────────────────────────────────────
    # OFFSET para el scroll acotado
    OFFSET = 260
    tabla_col = ft.Column(
        controls=[tabla],
        scroll=ft.ScrollMode.AUTO,
        height=max(300, page.window.height - OFFSET)
    )

    def on_page_resize(e):
        tabla_col.height = max(300, page.window.height - OFFSET)
        tabla_col.update()

    page.on_resized = on_page_resize

    return ft.Container(
        padding=ft.padding.only(left=25, right=25, top=20, bottom=0),
        expand=True,
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.HISTORY_ROUNDED, color=ft.Colors.BLUE_400, size=28), 
                ft.Text("Historial de Atenciones", size=24, weight="bold"),
                ft.Container(expand=True),
                ft.ElevatedButton(
                    "Descargar Excel", 
                    icon=ft.Icons.FILE_DOWNLOAD, 
                    bgcolor=ft.Colors.GREEN_800, 
                    color=ft.Colors.WHITE,
                    on_click=exportar_excel
                )
            ]),
            ft.Divider(color=ft.Colors.BLUE_900),
            ft.Row([buscador, dd_mes, dd_año, ft.IconButton(ft.Icons.RESTART_ALT_ROUNDED, on_click=limpiar_filtros)], spacing=10),
            # Scroll 2D con altura acotada
            ft.Row(
                [tabla_col],
                scroll=ft.ScrollMode.ALWAYS,
                vertical_alignment=ft.CrossAxisAlignment.START
            ),
        ], expand=True, spacing=12)
    )
