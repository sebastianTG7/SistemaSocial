import flet as ft
from controllers.persona_controller import PersonaController
from core.ui_helpers import mostrar_snackbar, mostrar_exito


def mostrar_ficha_socioeconomica_dialog(page: ft.Page, atencion_id, nombre_estudiante, on_save_callback=None):
    """Muestra un diálogo AlertDialog flotante premium para rellenar o editar la Ficha Socioeconómica."""
    
    # ── Cargar Ficha Existente si la hay ──────────────────────────────────────
    # Intentamos obtener la ficha (esto buscará la persona correcta usando el atencion_id)
    ficha = PersonaController.get_ficha_socioeconomica(atencion_id)
    datos_previos = ficha or {}
    
    # ── Elementos de UI: Tab 1 (Contexto y Vulnerabilidad) ───────────────────
    motivo_opciones = ["Comedor Universitario", "Exoneración o Reducción de Pago", "Derivación a otra Área", "Caso Especial", "Modalidad de Ingreso"]
    dd_motivo = ft.Dropdown(
        label="Motivo de la Evaluación", expand=True,
        options=[ft.dropdown.Option(m, m) for m in motivo_opciones],
        value=datos_previos.get("motivo_evaluacion")
    )
    
    sisfoh_opciones = ["No Pobre", "Pobre", "Pobre Extremo", "No tiene / No registrado"]
    dd_sisfoh = ft.Dropdown(
        label="Condición SISFOH", expand=True,
        options=[ft.dropdown.Option(s, s) for s in sisfoh_opciones],
        value=datos_previos.get("sisfoh_condicion")
    )
    
    seguro_opciones = ["SIS Gratuito", "EsSalud", "SIS Independiente", "Privado", "Ninguno", "Otro"]
    tipo_seg_prev = datos_previos.get("tipo_seguro")
    es_otro_seguro = tipo_seg_prev and tipo_seg_prev not in seguro_opciones and tipo_seg_prev != "Ninguno"
    
    dd_seguro = ft.Dropdown(
        label="Tipo de Seguro de Salud", expand=True,
        options=[ft.dropdown.Option(s, s) for s in seguro_opciones],
        value="Otro" if es_otro_seguro else tipo_seg_prev
    )
    
    txt_otro_seguro = ft.TextField(
        label="Especifique el seguro de salud", 
        expand=True, 
        visible=bool(es_otro_seguro),
        value=tipo_seg_prev if es_otro_seguro else ""
    )
    
    def on_seguro_change(e):
        txt_otro_seguro.visible = (dd_seguro.value == "Otro")
        if not txt_otro_seguro.visible:
            txt_otro_seguro.value = ""
        txt_otro_seguro.update()
        
    dd_seguro.on_change = on_seguro_change
    
    rg_discapacidad = ft.RadioGroup(
        content=ft.Row([
            ft.Text("¿Tiene alguna discapacidad?"),
            ft.Radio(value="Si", label="Sí"),
            ft.Radio(value="No", label="No")
        ]),
        value="Si" if datos_previos.get("tiene_discapacidad", False) else "No"
    )
    
    discapacidad_opciones = ["Visual", "Motora", "Auditiva", "Mental", "Otro"]
    dd_discapacidad = ft.Dropdown(
        label="Tipo de Discapacidad", expand=True,
        options=[ft.dropdown.Option(d, d) for d in discapacidad_opciones],
        value=datos_previos.get("tipo_discapacidad") if datos_previos.get("tipo_discapacidad") in discapacidad_opciones else None,
        visible=bool(datos_previos.get("tiene_discapacidad", False))
    )
    
    nivel_discapacidad_opciones = ["Leve", "Moderada", "Severa"]
    dd_nivel_discapacidad = ft.Dropdown(
        label="Nivel de Discapacidad", expand=True,
        options=[ft.dropdown.Option(n, n) for n in nivel_discapacidad_opciones],
        value=datos_previos.get("nivel_de_discapacidad") if datos_previos.get("nivel_de_discapacidad") in nivel_discapacidad_opciones else None,
        visible=bool(datos_previos.get("tiene_discapacidad", False))
    )
    
    def on_discapacidad_change(e):
        tiene = (rg_discapacidad.value == "Si")
        dd_discapacidad.visible = tiene
        dd_nivel_discapacidad.visible = tiene
        if not tiene:
            dd_discapacidad.value = None
            dd_nivel_discapacidad.value = None
        dd_discapacidad.update()
        dd_nivel_discapacidad.update()
        
    rg_discapacidad.on_change = on_discapacidad_change

    # ── Elementos de UI: Tab 2 (Familia y Economía) ──────────────────────────
    familia_opciones = ["Nuclear", "Monoparental", "Extendida", "Unipersonal", "Ensamblada"]
    dd_familia = ft.Dropdown(
        label="Estructura Familiar", expand=True,
        options=[ft.dropdown.Option(f, f) for f in familia_opciones],
        value=datos_previos.get("estructura_familiar")
    )
    
    dinamica_opciones = ["Armonioso", "Moderadamente Armonioso", "Conflictiva", "Altamente Conflictiva"]
    dd_dinamica = ft.Dropdown(
        label="Dinámica Familiar", expand=True,
        options=[ft.dropdown.Option(d, d) for d in dinamica_opciones],
        value=datos_previos.get("dinamica_familiar")
    )
    
    # TextFields Numéricos
    def on_focus_numeric(e):
        if e.control.value:
            e.control.selection = ft.TextSelection(0, len(e.control.value))
            e.control.update()

    def on_blur_numeric(e):
        if not e.control.value or not e.control.value.strip():
            e.control.value = "0.00"
            e.control.update()

    def create_numeric_field(label, val):
        return ft.TextField(
            label=label, value=f"{val:.2f}" if val is not None else "0.00",
            expand=True, input_filter=ft.InputFilter(regex_string=r"^[0-9]*\.?[0-9]*$"),
            keyboard_type=ft.KeyboardType.NUMBER,
            hint_text="0.00",
            on_focus=on_focus_numeric,
            on_blur=on_blur_numeric
        )
        
    f_ingreso_economico_miembros = create_numeric_field("Ingresos Económicos de Miembros (S/.)", datos_previos.get("ingreso_economico_miembros"))
    f_ingreso_becas = create_numeric_field("Ingreso por Becas (S/.)", datos_previos.get("ingreso_becas"))
    f_ingreso_otros = create_numeric_field("Otros Ingresos (alquileres, etc.) (S/.)", datos_previos.get("ingreso_otros"))

    f_egreso_agua = create_numeric_field("Gasto de Agua (S/.)", datos_previos.get("egreso_agua"))
    f_egreso_luz = create_numeric_field("Gasto de Luz (S/.)", datos_previos.get("egreso_luz"))
    f_egreso_educacion = create_numeric_field("Gasto Educación/Pasajes (S/.)", datos_previos.get("egreso_educacion_pasajes"))
    f_egreso_alimentacion = create_numeric_field("Gasto Alimentación (S/.)", datos_previos.get("egreso_alimentacion"))
    f_egreso_alquiler = create_numeric_field("Gasto Alquiler (S/.)", datos_previos.get("egreso_alquiler"))

    # Estudiante trabaja
    trabaja_opciones = ["Sí, tiempo completo", "Sí, tiempo parcial", "No", "Eventualmente"]
    dd_trabaja = ft.Dropdown(
        label="¿El estudiante trabaja?", expand=True,
        options=[ft.dropdown.Option(t, t) for t in trabaja_opciones],
        value=datos_previos.get("estudiante_trabaja") or "No"
    )

    txt_lugar_trabajo = ft.TextField(
        label="Lugar donde trabaja (Opcional)", expand=True,
        value=datos_previos.get("lugar_trabajo"),
        visible=datos_previos.get("estudiante_trabaja") in ["Sí, tiempo completo", "Sí, tiempo parcial", "Eventualmente"]
    )
    
    f_remuneracion = create_numeric_field("Remuneración (S/.)", datos_previos.get("remuneracion_estudiante"))
    f_remuneracion.visible = datos_previos.get("estudiante_trabaja") in ["Sí, tiempo completo", "Sí, tiempo parcial", "Eventualmente"]

    def on_trabaja_change(e):
        trabaja = dd_trabaja.value in ["Sí, tiempo completo", "Sí, tiempo parcial", "Eventualmente"]
        txt_lugar_trabajo.visible = trabaja
        f_remuneracion.visible = trabaja
        txt_lugar_trabajo.update()
        f_remuneracion.update()

    dd_trabaja.on_change = on_trabaja_change

    # ── Elementos de UI: Tab 3 (Vivienda y Servicios) ────────────────────────
    vivienda_opciones = ["Propia", "Alquilada", "Hipotecada", "Alojado por familiares", "Cuidador"]
    dd_vivienda = ft.Dropdown(
        label="Tipo de Vivienda", expand=True,
        options=[ft.dropdown.Option(v, v) for v in vivienda_opciones],
        value=datos_previos.get("tipo_vivienda")
    )
    
    paredes_opciones = ["Ladrillo/Cemento", "Adobe/Tapia", "Madera", "Otros"]
    dd_paredes = ft.Dropdown(
        label="Material de Paredes", expand=True,
        options=[ft.dropdown.Option(p, p) for p in paredes_opciones],
        value=datos_previos.get("material_paredes")
    )
    
    techo_opciones = ["Concreto", "Calamina", "Eternit", "Madera/Paja"]
    dd_techos = ft.Dropdown(
        label="Material de Techos", expand=True,
        options=[ft.dropdown.Option(t, t) for t in techo_opciones],
        value=datos_previos.get("material_techo")
    )
    
    sw_agua = ft.Switch(label="Agua por red", value=bool(datos_previos.get("tiene_agua_red", False)))
    sw_desague = ft.Switch(label="Desagüe por red", value=bool(datos_previos.get("tiene_desague_red", False)))
    sw_luz = ft.Switch(label="Energía Eléctrica", value=bool(datos_previos.get("tiene_energia_electrica", False)))

    # ── Diálogo e Interacciones ──────────────────────────────────────────────
    dlg = ft.AlertDialog(modal=True)
    
    def guardar_ficha(e):
        # Captura y parseo de datos
        def parse_float(tf):
            val = tf.value.strip() if tf.value else ""
            if not val:
                return 0.0
            try: return float(val)
            except: return 0.0
            
        datos = {
            "motivo_evaluacion": dd_motivo.value,
            "sisfoh_condicion": dd_sisfoh.value,
            "tiene_discapacidad": (rg_discapacidad.value == "Si"),
            "tipo_discapacidad": dd_discapacidad.value,
            "nivel_de_discapacidad": dd_nivel_discapacidad.value if (rg_discapacidad.value == "Si") else None,
            "tipo_seguro": txt_otro_seguro.value.strip() if dd_seguro.value == "Otro" else dd_seguro.value,
            "estructura_familiar": dd_familia.value,
            "dinamica_familiar": dd_dinamica.value,
            "ingreso_economico_miembros": parse_float(f_ingreso_economico_miembros),
            "ingreso_becas": parse_float(f_ingreso_becas),
            "ingreso_otros": parse_float(f_ingreso_otros),
            "egreso_agua": parse_float(f_egreso_agua),
            "egreso_luz": parse_float(f_egreso_luz),
            "egreso_educacion_pasajes": parse_float(f_egreso_educacion),
            "egreso_alimentacion": parse_float(f_egreso_alimentacion),
            "egreso_alquiler": parse_float(f_egreso_alquiler),
            "estudiante_trabaja": dd_trabaja.value,
            "lugar_trabajo": txt_lugar_trabajo.value,
            "remuneracion_estudiante": parse_float(f_remuneracion),
            "tipo_vivienda": dd_vivienda.value,
            "material_paredes": dd_paredes.value,
            "material_techo": dd_techos.value,
            "tiene_agua_red": sw_agua.value,
            "tiene_desague_red": sw_desague.value,
            "tiene_energia_electrica": sw_luz.value
        }
        
        # Guardar en base de datos
        exito, resultado = PersonaController.guardar_ficha_socioeconomica(atencion_id, datos)
        if exito:
            dlg.open = False
            page.update()
            # Luego mostrar notificación y ejecutar callback
            mostrar_exito(page, "Ficha Socioeconomica guardada correctamente")
            if on_save_callback:
                on_save_callback()
        else:
            mostrar_snackbar(page, f"Error al guardar: {resultado}", ft.Colors.RED_800)
            
    # Armado de la estructura de Flet Tabs (compatible con Flet 0.83.1)
    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        length=3,
        expand=True,
        content=ft.Column(
            expand=True,
            controls=[
                ft.TabBar(
                    tabs=[
                        ft.Tab(label="Salud y SISFOH", icon=ft.Icons.VACCINES_ROUNDED),
                        ft.Tab(label="Familia y Economía", icon=ft.Icons.MONETIZATION_ON_ROUNDED),
                        ft.Tab(label="Vivienda y Servicios", icon=ft.Icons.HOUSE_ROUNDED),
                    ]
                ),
                ft.TabBarView(
                    expand=True,
                    controls=[
                        # Contenido Tab 1: Salud y SISFOH
                        ft.Container(
                            padding=20,
                            content=ft.Column([
                                dd_motivo,
                                dd_sisfoh,
                                ft.Row([dd_seguro, txt_otro_seguro], spacing=15),
                                ft.Container(height=10),
                                rg_discapacidad,
                                ft.Row([dd_discapacidad, dd_nivel_discapacidad], spacing=20, vertical_alignment="center")
                            ], spacing=15)
                        ),
                        # Contenido Tab 2: Familia y Economía
                        ft.Container(
                            padding=20,
                            content=ft.Column([
                                ft.Row([dd_familia, dd_dinamica], spacing=15),
                                ft.Text("Ingresos", size=14, weight="bold", color=ft.Colors.BLUE_200),
                                ft.Row([f_ingreso_economico_miembros, f_ingreso_becas, f_ingreso_otros], spacing=15),
                                ft.Text("Egresos", size=14, weight="bold", color=ft.Colors.RED_200),
                                ft.Row([f_egreso_agua, f_egreso_luz, f_egreso_educacion], spacing=15),
                                ft.Row([f_egreso_alimentacion, f_egreso_alquiler], spacing=15),
                                ft.Text("Situación Laboral del Estudiante", size=14, weight="bold", color=ft.Colors.GREEN_200),
                                ft.Row([dd_trabaja, txt_lugar_trabajo, f_remuneracion], spacing=15),
                            ], spacing=10, scroll=ft.ScrollMode.AUTO)
                        ),
                        # Contenido Tab 3: Vivienda y Servicios
                        ft.Container(
                            padding=20,
                            content=ft.Column([
                                dd_vivienda,
                                ft.Row([dd_paredes, dd_techos], spacing=15),
                                ft.Container(height=10),
                                ft.Text("Servicios Básicos Disponibles:", size=13, weight="bold", color=ft.Colors.BLUE_200),
                                ft.Row([sw_agua, sw_desague, sw_luz], spacing=30, alignment="center")
                            ], spacing=15)
                        )
                    ]
                )
            ]
        )
    )
    
    # Configuración final del AlertDialog
    es_actualizacion = bool(datos_previos)
    dlg.title = ft.Text(
        f"{'Actualizar' if es_actualizacion else 'Nueva'} Ficha Socioeconomica -- {nombre_estudiante.upper()}", 
        weight="bold", size=18
    )
    dlg.content = ft.Container(width=780, height=420, content=tabs)
    dlg.actions = [
        ft.TextButton("Cancelar", on_click=lambda _: (cerrar_dialogo_overlay(page, dlg))),
        ft.ElevatedButton(
            "Actualizar Ficha" if es_actualizacion else "Guardar Ficha", 
            on_click=guardar_ficha, 
            bgcolor=ft.Colors.BLUE_800 if es_actualizacion else ft.Colors.GREEN_800, 
            color=ft.Colors.WHITE, 
            icon=ft.Icons.UPDATE_ROUNDED if es_actualizacion else ft.Icons.SAVE_ROUNDED
        )
    ]
    dlg.actions_alignment = "end"
    
    # Registrar diálogo en el overlay y abrir
    if dlg not in page.overlay:
        page.overlay.append(dlg)
    dlg.open = True
    page.update()


def cerrar_dialogo_overlay(page: ft.Page, dlg):
    dlg.open = False
    page.update()
    page.update()
