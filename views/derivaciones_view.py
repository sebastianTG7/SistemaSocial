import flet as ft
from controllers.persona_controller import PersonaController
from database.db_config import SessionLocal
from database.models import Persona, FichaDerivacion
from core.ui_helpers import mostrar_exito, mostrar_snackbar
from views.components.derivacion_dialog import mostrar_ficha_derivacion_dialog

def build_derivaciones_view(page: ft.Page):
    """Vista de Gestión de Derivaciones."""

    # ── Filtrado y Estado ───────────────────────────────────────────────────
    datos_actuales = []
    buscador = ft.TextField(
        hint_text="Buscar por DNI o Nombre...", prefix_icon=ft.Icons.SEARCH,
        width=300, on_change=lambda e: cargar_datos(e.control.value)
    )

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
    def cargar_datos(filtro=""):
        spinner.visible = True
        try: spinner.update()
        except: pass

        db = SessionLocal()
        try:
            # Obtener todas las personas cuyo caso social es "Derivación" O que ya tengan una ficha
            # Usaremos una consulta personalizada para mayor eficiencia
            from sqlalchemy import or_
            from database.models import CatCasoSocial
            
            casos_derivacion = db.query(CatCasoSocial.id).filter(CatCasoSocial.nombre.ilike("%derivaci%")).all()
            caso_ids = [c[0] for c in casos_derivacion]
            
            query = db.query(Persona, FichaDerivacion.id.label("ficha_id")).outerjoin(
                FichaDerivacion, Persona.id == FichaDerivacion.persona_id
            ).filter(Persona.activo == True).filter(
                or_(Persona.caso_social_id.in_(caso_ids), FichaDerivacion.id != None)
            )
            
            if filtro:
                f = filtro.upper()
                query = query.filter(
                    or_(
                        Persona.dni.contains(f),
                        Persona.apellidos.contains(f),
                        Persona.nombres.contains(f)
                    )
                )
                
            resultados = query.all()
            
            tabla.rows = []
            for i, (p, ficha_id) in enumerate(resultados, 1):
                estado_texto = "Completada" if ficha_id else "Pendiente"
                estado_color = ft.Colors.GREEN_400 if ficha_id else ft.Colors.ORANGE_400
                
                tabla.rows.append(ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(i), size=13)),
                    ft.DataCell(ft.Text(p.fecha_atencion.strftime("%d/%m/%Y"), size=12)),
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
                            on_click=lambda _, pid=p.id: mostrar_ficha_derivacion_dialog(page, pid, lambda: cargar_datos(buscador.value))
                        )
                    ])),
                ]))
        finally:
            db.close()

        spinner.visible = False
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
        ft.Row([buscador], alignment=ft.MainAxisAlignment.START),
        ft.Divider(height=5, color="transparent"),
        zona_contenido
    ], expand=True, spacing=12)

    return ft.Container(
        padding=ft.padding.only(left=25, right=25, top=20, bottom=10),
        expand=True,
        content=main_column
    )
