import flet as ft
from controllers.persona_controller import PersonaController
from core.ui_helpers import mostrar_snackbar, mostrar_exito


def mostrar_ficha_socioeconomica_dialog(page: ft.Page, persona_id, nombre_estudiante, on_save_callback=None):
    """Muestra un diálogo AlertDialog flotante premium para rellenar o editar la Ficha Socioeconómica."""
    
    # ── Cargar Ficha Existente si la hay ──────────────────────────────────────
    ficha = PersonaController.get_ficha_socioeconomica(persona_id)
    datos_previos = ficha or {}
    
    # ── Elementos de UI: Tab 1 (Contexto y Vulnerabilidad) ───────────────────
    motivo_opciones = ["Comedor Universitario", "Exoneración o Reducción de Pago", "Derivación a otra Área", "Caso Especial", "Modalidad de Ingreso"]
    dd_motivo = ft.Dropdown(
        label="Motivo de la Evaluación", expand=True,
        options=[ft.dropdown.Option(m, m) for m in motivo_opciones],
        value=datos_previos.get("motivo_evaluacion")
    )
    
    sisfoh_opciones = ["No Pobre", "Pobre", "Pobre Extremo"]
    dd_sisfoh = ft.Dropdown(
        label="Condición SISFOH", expand=True,
        options=[ft.dropdown.Option(s, s) for s in sisfoh_opciones],
        value=datos_previos.get("sisfoh_condicion")
    )
    
    seguro_opciones = ["SIS Gratuito", "EsSalud", "SIS Independiente", "Privado", "Ninguno"]
    dd_seguro = ft.Dropdown(
        label="Tipo de Seguro de Salud", expand=True,
        options=[ft.dropdown.Option(s, s) for s in seguro_opciones],
        value=datos_previos.get("tipo_seguro")
    )
    
    sw_discapacidad = ft.Switch(
        label="¿Tiene alguna discapacidad?",
        value=bool(datos_previos.get("tiene_discapacidad", False))
    )
    
    discapacidad_opciones = ["Ninguna", "Visual", "Motora", "Auditiva", "Mental", "Otro"]
    dd_discapacidad = ft.Dropdown(
        label="Tipo de Discapacidad", expand=True,
        options=[ft.dropdown.Option(d, d) for d in discapacidad_opciones],
        value=datos_previos.get("tipo_discapacidad") or "Ninguna",
        visible=bool(datos_previos.get("tiene_discapacidad", False))
    )
    
    def on_discapacidad_toggle(e):
        dd_discapacidad.visible = sw_discapacidad.value
        if not sw_discapacidad.value:
            dd_discapacidad.value = "Ninguna"
        dd_discapacidad.update()
        
    sw_discapacidad.on_change = on_discapacidad_toggle

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
        
    f_ingreso_fam = create_numeric_field("Ingreso Familiar Total (S/.)", datos_previos.get("ingreso_familiar_total"))
    f_ingreso_beca = create_numeric_field("Ingreso Becas/Bonos (S/.)", datos_previos.get("ingreso_becas_bonos"))
    f_egreso_alquiler = create_numeric_field("Gasto Vivienda/Alquiler (S/.)", datos_previos.get("egreso_alquiler"))
    f_egreso_alimentacion = create_numeric_field("Gasto Alimentación (S/.)", datos_previos.get("egreso_alimentacion"))
    f_egreso_servicios = create_numeric_field("Gasto Servicios Luz/Agua (S/.)", datos_previos.get("egreso_servicios"))
    f_egreso_educacion = create_numeric_field("Gasto Educación/Pasajes (S/.)", datos_previos.get("egreso_educacion_otros"))

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
            "tiene_discapacidad": sw_discapacidad.value,
            "tipo_discapacidad": dd_discapacidad.value,
            "tipo_seguro": dd_seguro.value,
            "estructura_familiar": dd_familia.value,
            "dinamica_familiar": dd_dinamica.value,
            "ingreso_familiar_total": parse_float(f_ingreso_fam),
            "ingreso_becas_bonos": parse_float(f_ingreso_beca),
            "egreso_alquiler": parse_float(f_egreso_alquiler),
            "egreso_alimentacion": parse_float(f_egreso_alimentacion),
            "egreso_servicios": parse_float(f_egreso_servicios),
            "egreso_educacion_otros": parse_float(f_egreso_educacion),
            "tipo_vivienda": dd_vivienda.value,
            "material_paredes": dd_paredes.value,
            "material_techo": dd_techos.value,
            "tiene_agua_red": sw_agua.value,
            "tiene_desague_red": sw_desague.value,
            "tiene_energia_electrica": sw_luz.value
        }
        
        exito, resultado = PersonaController.guardar_ficha_socioeconomica(persona_id, datos)
        if exito:
            mostrar_exito(page, "✔ Ficha Socioeconómica guardada correctamente")
            dlg.open = False
            page.update()
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
                                dd_seguro,
                                ft.Container(height=10),
                                ft.Row([sw_discapacidad, dd_discapacidad], spacing=20, vertical_alignment="center")
                            ], spacing=15)
                        ),
                        # Contenido Tab 2: Familia y Economía
                        ft.Container(
                            padding=20,
                            content=ft.Column([
                                ft.Row([dd_familia, dd_dinamica], spacing=15),
                                ft.Row([f_ingreso_fam, f_ingreso_beca], spacing=15),
                                ft.Row([f_egreso_alquiler, f_egreso_alimentacion], spacing=15),
                                ft.Row([f_egreso_servicios, f_egreso_educacion], spacing=15),
                            ], spacing=15)
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
    dlg.title = ft.Text(f"📝 Ficha Socioeconómica — {nombre_estudiante.upper()}", weight="bold", size=18)
    dlg.content = ft.Container(width=780, height=420, content=tabs)
    dlg.actions = [
        ft.TextButton("Cancelar", on_click=lambda _: (cerrar_dialogo_overlay(page, dlg))),
        ft.ElevatedButton("Guardar Ficha", on_click=guardar_ficha, bgcolor=ft.Colors.GREEN_800, color=ft.Colors.WHITE, icon=ft.Icons.SAVE_ROUNDED)
    ]
    dlg.actions_alignment = "end"
    
    # Registrar diálogo en el overlay y abrir
    page.overlay.clear()
    page.overlay.append(dlg)
    dlg.open = True
    page.update()


def cerrar_dialogo_overlay(page: ft.Page, dlg):
    dlg.open = False
    page.update()
