import flet as ft
from controllers.persona_controller import PersonaController
from controllers.catalog_controller import CatalogController
from database.db_config import SessionLocal
from database.models import Persona
from core.ui_helpers import mostrar_exito
from datetime import datetime


def build_personas_view(page: ft.Page, on_new_click=None):
    """Vista de Gestión de Personas — Diálogos via page.overlay (compatible Flet 0.83)."""

    estado = {"mostrar_activos": True}
    txt_activos = ft.Ref[ft.Text]()
    txt_inactivos = ft.Ref[ft.Text]()

    # ── Helper: mostrar cualquier AlertDialog via overlay ──────────────────
    def mostrar_dialogo(dlg):
        """Agrega el diálogo al overlay y lo abre. Compatible con Flet 0.83."""
        # Limpiar diálogos previos del overlay
        page.overlay.clear()
        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    def cerrar_dialogo(dlg):
        dlg.open = False
        page.update()

    # ── Estado de Ordenación ────────────────────────────────────────────────
    sort_info = {"index": None, "ascending": True}

    def al_ordenar(col_idx, ascending):
        sort_info["index"] = col_idx
        sort_info["ascending"] = ascending
        tabla.sort_column_index = col_idx
        tabla.sort_ascending = ascending
        cargar_datos(buscador.value)

    # ── Tabla ───────────────────────────────────────────────────────────────
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
            ft.DataColumn(ft.Text("Acciones", weight="bold")),
        ],
        column_spacing=18,
        heading_row_color=ft.Colors.with_opacity(0.1, ft.Colors.BLUE_400),
    )
    buscador = ft.TextField(
        label="Buscar por DNI, Nombre o Código...", prefix_icon=ft.Icons.SEARCH,
        width=300, on_change=lambda e: cargar_datos(e.control.value)
    )

    # ── Filtros de Mes y Año (por defecto: mes actual) ────────────────────────
    _hoy = datetime.now()
    MESES = ["Enero","Febrero","Marzo","Abril","Mayo","Junio",
             "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
    dd_mes = ft.Dropdown(
        label="Mes", width=155,
        value=str(_hoy.month),
        options=[
            ft.dropdown.Option(key="all", text="Todo el Año")
        ] + [ft.dropdown.Option(key=str(i+1), text=MESES[i]) for i in range(12)],
        on_select=lambda _: cargar_datos(buscador.value)
    )
    dd_año = ft.Dropdown(
        label="Año", width=110,
        value=str(_hoy.year),
        options=[ft.dropdown.Option(key=str(a), text=str(a)) for a in range(2026, _hoy.year + 5)],
        on_select=lambda _: cargar_datos(buscador.value)
    )
    def limpiar_mes(e):
        dd_mes.value = str(datetime.now().month)
        dd_año.value = str(datetime.now().year)
        buscador.value = ""
        cargar_datos()
        page.update()

    # ── Edición ─────────────────────────────────────────────────────────────
    def abrir_edicion(p_id):
        db_s = SessionLocal()
        p = db_s.query(Persona).filter(Persona.id == p_id).first()
        if not p:
            db_s.close(); return
        tipos = CatalogController.get_tipos_usuario()
        casos = CatalogController.get_casos_sociales()
        facultades = CatalogController.get_facultades()

        e_nombres  = ft.TextField(label="Nombres",    value=p.nombres,           expand=1)
        e_apellidos= ft.TextField(label="Apellidos",  value=p.apellidos,          expand=1)
        e_dni      = ft.TextField(label="DNI",        value=p.dni,                expand=1)
        e_codigo   = ft.TextField(label="Código",     value=p.codigo_estudiante or "", expand=1)
        e_edad     = ft.TextField(label="Edad",       value=str(p.edad) if p.edad else "", expand=1)
        e_fecha    = ft.TextField(label="Fecha",      value=p.fecha_atencion.strftime("%d/%m/%Y"), expand=1)
        e_celular  = ft.TextField(label="Celular",    value=p.celular or "",      expand=1)
        e_correo   = ft.TextField(label="Correo",     value=p.correo or "",       expand=1)
        e_año      = ft.TextField(label="Año Est.",   value=p.año_estudio or "",  expand=1)
        e_direccion= ft.TextField(label="Dirección",  value=p.direccion or "",    expand=True)
        e_obs      = ft.TextField(label="Observaciones", value=p.observaciones or "", expand=True, multiline=True)
        e_sexo = ft.Dropdown(label="Sexo", value=p.sexo, expand=1,
            options=[ft.dropdown.Option("F","Femenino"), ft.dropdown.Option("M","Masculino")])
        e_tipo = ft.Dropdown(label="Tipo Usuario", value=str(p.tipo_usuario_id), expand=1,
            options=[ft.dropdown.Option(str(t.id), t.nombre) for t in tipos])
        e_caso = ft.Dropdown(label="Caso Social", value=str(p.caso_social_id), expand=1,
            options=[ft.dropdown.Option(str(c.id), c.nombre) for c in casos])
        e_facu = ft.Dropdown(label="Facultad", value=str(p.facultad_id), expand=1,
            options=[ft.dropdown.Option(str(f.id), f.nombre) for f in facultades])
        e_escu = ft.Dropdown(label="Escuela", value=str(p.escuela_id), expand=1)
        db_s.close()

        def ue(ev):
            if e_facu.value:
                esc = CatalogController.get_escuelas_by_facultad(int(e_facu.value))
                e_escu.options = [ft.dropdown.Option(str(es.id), es.nombre) for es in esc]
            if ev: e_escu.update()
        e_facu.on_select = ue; ue(None); e_escu.value = str(p.escuela_id)

        dlg = ft.AlertDialog(modal=True)   # se define antes para poder referenciarla

        def guardar(e):
            db = SessionLocal()
            r = db.query(Persona).filter(Persona.id == p_id).first()
            if r:
                r.nombres = e_nombres.value.upper(); r.apellidos = e_apellidos.value.upper()
                r.dni = e_dni.value; r.codigo_estudiante = e_codigo.value
                r.edad = int(e_edad.value) if e_edad.value.isdigit() else None
                r.sexo = e_sexo.value; r.tipo_usuario_id = int(e_tipo.value)
                r.caso_social_id = int(e_caso.value); r.facultad_id = int(e_facu.value)
                r.escuela_id = int(e_escu.value); r.celular = e_celular.value
                r.correo = e_correo.value; r.direccion = e_direccion.value
                r.año_estudio = e_año.value; r.observaciones = e_obs.value
                try: r.fecha_atencion = datetime.strptime(e_fecha.value, "%d/%m/%Y")
                except: pass
                db.commit()
            db.close()
            mostrar_exito(page, "✔ Registro actualizado")
            cerrar_dialogo(dlg)
            cargar_datos(buscador.value)

        dlg.title = ft.Text("✏ Editar Registro", weight="bold", size=18)
        dlg.content = ft.Container(width=750, content=ft.Column([
            ft.Row([e_dni, e_fecha, e_edad], spacing=10),
            ft.Row([e_nombres, e_apellidos], spacing=10),
            ft.Row([e_sexo, e_codigo, e_año], spacing=10),
            ft.Row([e_tipo, e_caso], spacing=10),
            ft.Row([e_facu, e_escu], spacing=10),
            ft.Row([e_celular, e_correo], spacing=10),
            e_direccion, e_obs,
        ], spacing=14, scroll=ft.ScrollMode.AUTO, tight=True))
        dlg.actions = [
            ft.TextButton("Cancelar", on_click=lambda _: cerrar_dialogo(dlg)),
            ft.ElevatedButton("Guardar Todo", on_click=guardar,
                bgcolor=ft.Colors.GREEN_800, color=ft.Colors.WHITE, icon=ft.Icons.SAVE),
        ]
        dlg.actions_alignment = "end"
        mostrar_dialogo(dlg)

    # ── Borrado ──────────────────────────────────────────────────────────────
    def abrir_borrado(p_id):
        dlg = ft.AlertDialog(modal=True)
        def confirmar(e):
            PersonaController.eliminar_permanente(p_id)
            mostrar_exito(page, "✔ Registro eliminado")
            cerrar_dialogo(dlg); cargar_datos(buscador.value)
        dlg.title   = ft.Text("⚠ Confirmar Eliminación")
        dlg.content = ft.Text("¿Borrar definitivamente? Esta acción no se puede deshacer.")
        dlg.actions = [
            ft.TextButton("Cancelar", on_click=lambda _: cerrar_dialogo(dlg)),
            ft.ElevatedButton("Sí, Borrar", on_click=confirmar,
                bgcolor=ft.Colors.RED_800, color=ft.Colors.WHITE),
        ]
        dlg.actions_alignment = "end"
        mostrar_dialogo(dlg)

    # ── Estado de Paginación ──────────────────────────────────────────────────
    estado_p = {
        "pagina": 1,
        "por_pagina": 20,
        "total_registros": 0
    }
    
    txt_paginacion = ft.Text("Página 1", size=13, weight="bold")
    btn_prev = ft.IconButton(ft.Icons.NAVIGATE_BEFORE, on_click=lambda _: cambiar_pag(-1), disabled=True)
    btn_next = ft.IconButton(ft.Icons.NAVIGATE_NEXT, on_click=lambda _: cambiar_pag(1))
    
    def on_per_page_change(e):
        estado_p["por_pagina"] = int(e.control.value)
        estado_p["pagina"] = 1
        cargar_datos(buscador.value)

    dd_per_page = ft.Dropdown(
        value="20", width=93, height=45,
        options=[ft.dropdown.Option("10"), ft.dropdown.Option("20"), 
                 ft.dropdown.Option("50"), ft.dropdown.Option("100")],
        on_select=on_per_page_change,
        content_padding=ft.padding.all(10)
    )

    def cambiar_pag(delta):
        estado_p["pagina"] += delta
        cargar_datos(buscador.value)

    # ── Cargar filas ─────────────────────────────────────────────────────────
    def cargar_datos(filtro=""):
        p_all = PersonaController.get_all(solo_activos=False)
        
        # 1. Filtrar por mes/año
        if dd_mes.value and dd_mes.value != "all":
            p_all = [p for p in p_all if p["fecha_atencion"].month == int(dd_mes.value)]
        if dd_año.value:
            p_all = [p for p in p_all if p["fecha_atencion"].year == int(dd_año.value)]
            
        # 2. Filtrar por pestaña Activo/Inactivo
        p_filtered  = [p for p in p_all if p["activo"] == estado["mostrar_activos"]]
        
        # 3. Filtrar por buscador
        if filtro:
            f = filtro.upper()
            p_filtered = [p for p in p_filtered if
                f in (p["dni"] or "") or
                f in (p["apellidos"] or "").upper() or
                f in (p["nombres"] or "").upper() or
                f in (p["codigo_estudiante"] or "").upper()]
        
        # 4. Ordenación Dinámica según cabecera
        if sort_info["index"] is not None:
            idx = sort_info["index"]
            asc = sort_info["ascending"]
            
            if idx == 1: # Fecha
                p_filtered.sort(key=lambda p: p["fecha_atencion"], reverse=not asc)
            elif idx == 2: # DNI
                p_filtered.sort(key=lambda p: (p["dni"] or ""), reverse=not asc)
            elif idx == 3: # Apellidos
                p_filtered.sort(key=lambda p: ((p["apellidos"] or "").upper(), (p["nombres"] or "").upper()), reverse=not asc)
            elif idx == 5: # Tipo de Usuario
                p_filtered.sort(key=lambda p: (p["tipo_usuario"] or ""), reverse=not asc)
            elif idx == 6: # Facultad/Escuela
                p_filtered.sort(key=lambda p: ((p["facultad"] or "").upper(), (p["escuela"] or "").upper()), reverse=not asc)
            elif idx == 0: # # Correlativo
                p_filtered.sort(key=lambda p: p["id"], reverse=not asc)
        else:
            # Orden por defecto: alfabético ascendente
            p_filtered.sort(key=lambda p: ((p["apellidos"] or "").upper(), (p["nombres"] or "").upper()))
        
        # 5. Lógica de Paginación (Slicing)
        total = len(p_filtered)
        estado_p["total_registros"] = total
        max_pags = max(1, (total + estado_p["por_pagina"] - 1) // estado_p["por_pagina"])
        
        if estado_p["pagina"] > max_pags: estado_p["pagina"] = max_pags
        if estado_p["pagina"] < 1: estado_p["pagina"] = 1
        
        inicio = (estado_p["pagina"] - 1) * estado_p["por_pagina"]
        fin = inicio + estado_p["por_pagina"]
        
        datos_paginados = p_filtered[inicio:fin]
        
        # Actualizar UI de paginación
        txt_paginacion.value = f"Página {estado_p['pagina']} de {max_pags} ({total} registros)"
        btn_prev.disabled = estado_p["pagina"] <= 1
        btn_next.disabled = estado_p["pagina"] >= max_pags
        
        # Actualizar contadores de pestañas
        if txt_activos.current:
            txt_activos.current.value  = f"Activos ({sum(1 for p in p_all if p.get('activo'))})"
        if txt_inactivos.current:
            txt_inactivos.current.value= f"Inactivos ({sum(1 for p in p_all if not p.get('activo'))})"

        # 6. Dibujar Tabla
        tabla.rows = []
        for i, p in enumerate(datos_paginados, inicio + 1):
            pid = p["id"]
            tabla.rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(str(i), size=13)),
                ft.DataCell(ft.Text(p["fecha_atencion"].strftime("%d/%m/%Y"), size=12)),
                ft.DataCell(ft.Column([
                    ft.Text(p["dni"] or "-", size=12, weight="bold"),
                    ft.Text(p["codigo_estudiante"] or "-", size=12, color=ft.Colors.BLUE_200, weight="bold")
                ], spacing=0)),
                ft.DataCell(ft.Column([
                    ft.Text(f"{p['apellidos']}, {p['nombres']}", weight="bold", size=12),
                    ft.Text(f"{p['edad'] or '-'} años, {p['sexo'] or '-'} ", size=10, color=ft.Colors.WHITE_54)
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
                ], spacing=0, width=150)),
                ft.DataCell(ft.Column([
                    ft.Text(p["observaciones"] or "-", size=11, italic=True),
                    ft.Text(p["direccion"] or "-", size=10, color=ft.Colors.WHITE_54)
                ], spacing=0, width=200)),
                ft.DataCell(ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.EDIT_ROUNDED, icon_color=ft.Colors.BLUE_400,
                        icon_size=20, tooltip="Editar",
                        visible=estado["mostrar_activos"],
                        on_click=lambda _, p=pid: abrir_edicion(p)
                    ),
                    ft.IconButton(
                        icon=ft.Icons.BLOCK_ROUNDED, icon_color=ft.Colors.RED_400,
                        icon_size=20, tooltip="Desactivar",
                        visible=estado["mostrar_activos"],
                        on_click=lambda _, p=pid: (PersonaController.desactivar(p), mostrar_exito(page,"Desactivado"), cargar_datos(buscador.value))
                    ),
                    ft.IconButton(
                        icon=ft.Icons.CHECK_CIRCLE_ROUNDED, icon_color=ft.Colors.GREEN_400,
                        icon_size=20, tooltip="Volver de Inactivo",
                        visible=not estado["mostrar_activos"],
                        on_click=lambda _, p=pid: (PersonaController.activar(p), mostrar_exito(page,"Activado"), cargar_datos(buscador.value))
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DELETE_FOREVER_ROUNDED, icon_color=ft.Colors.RED_900,
                        icon_size=20, tooltip="Borrar Definitivo",
                        visible=not estado["mostrar_activos"],
                        on_click=lambda _, p=pid: abrir_borrado(p)
                    ),
                ], spacing=0)),
            ]))
        page.update()

    # ── Tabs ─────────────────────────────────────────────────────────────────
    ia = ft.Container(height=3, bgcolor=ft.Colors.BLUE_400,     border_radius=5)
    ii = ft.Container(height=3, bgcolor=ft.Colors.TRANSPARENT, border_radius=5)

    def ctab(act):
        estado["mostrar_activos"] = act
        ia.bgcolor = ft.Colors.BLUE_400     if act  else ft.Colors.TRANSPARENT
        ii.bgcolor = ft.Colors.BLUE_400     if not act else ft.Colors.TRANSPARENT
        cargar_datos(buscador.value or "")

    cargar_datos()

    # ── Scroll 2D: Contenedor Elástico ──────────────────────────────────────
    # Usamos expand=True para que el área de la tabla tome todo el espacio 
    # sobrante y deje la paginación pegada abajo.
    area_tabla = ft.Container(
        content=ft.Row(
            [ft.Column([tabla], scroll=ft.ScrollMode.AUTO)],
            scroll=ft.ScrollMode.ALWAYS,
            vertical_alignment=ft.CrossAxisAlignment.START
        ),
        expand=True, # <--- ESTO es el secreto para que no se oculte la paginación
    )

    return ft.Container(padding=ft.padding.only(left=25, right=25, top=20, bottom=10), expand=True, content=ft.Column([
        ft.Row([
            ft.Icon(ft.Icons.SCHOOL_ROUNDED, color=ft.Colors.GREEN_400, size=28),
            ft.Text("Gestión de Estudiantes", size=24, weight="bold"),
            ft.Container(expand=True),
            ft.ElevatedButton("+ Nuevo", bgcolor=ft.Colors.GREEN_800, color=ft.Colors.WHITE,
                              on_click=lambda _: on_new_click()),
        ]),
        ft.Divider(color=ft.Colors.BLUE_900),
        ft.Row([
            ft.Column([ft.TextButton(content=ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, size=16),
                                                     ft.Text("Activos", ref=txt_activos)]),
                                     on_click=lambda _: ctab(True)), ia], spacing=2),
            ft.Column([ft.TextButton(content=ft.Row([ft.Icon(ft.Icons.BLOCK_OUTLINED, size=16),
                                                     ft.Text("Inactivos", ref=txt_inactivos)]),
                                     on_click=lambda _: ctab(False)), ii], spacing=2),
            ft.Container(expand=True),
            dd_mes, dd_año,
            ft.IconButton(ft.Icons.RESTART_ALT_ROUNDED, tooltip="Mes actual", on_click=limpiar_mes),
        ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        buscador,

        # El área de la tabla ahora es EXPANDIBLE
        area_tabla,
        
        # ── Barra de Paginación ──────────────────────────────────────────────
        ft.Container(
            padding=ft.padding.symmetric(horizontal=10, vertical=5),
            bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.BLUE_700),
            border_radius=8,
            content=ft.Row([
                ft.Row([
                    ft.Text("Ver:", size=12, color=ft.Colors.WHITE_54),
                    dd_per_page
                ], spacing=10),
                ft.VerticalDivider(width=20),
                txt_paginacion,
                ft.Container(expand=True),
                ft.Row([
                    btn_prev,
                    btn_next
                ], spacing=5)
            ], alignment=ft.MainAxisAlignment.CENTER)
        )
    ], expand=True, spacing=12))
