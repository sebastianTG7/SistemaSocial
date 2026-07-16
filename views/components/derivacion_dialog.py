import flet as ft
from controllers.persona_controller import PersonaController
from database.db_config import SessionLocal
from database.models import Persona, Atencion
from core.ui_helpers import mostrar_exito, mostrar_snackbar
from core.pdf_generator import generar_html_derivacion
from datetime import datetime

def mostrar_ficha_derivacion_dialog(page: ft.Page, atencion_id: int, on_close=None):
    """
    Muestra el diálogo para rellenar la ficha de derivación.
    """
    
    # ── 1. Cargar Datos ──
    db = SessionLocal()
    atencion_db = db.query(Atencion).filter(Atencion.id == atencion_id).first()
    if not atencion_db:
        db.close()
        return
        
    persona_db = db.query(Persona).filter(Persona.id == atencion_db.persona_id).first()
    if not persona_db:
        db.close()
        return
        
    datos_base = {
        "id": atencion_db.persona_id,
        "apellido_paterno": (persona_db.apellidos or "").split()[0] if persona_db.apellidos else "",
        "apellido_materno": (persona_db.apellidos or "").split()[-1] if persona_db.apellidos and len(persona_db.apellidos.split()) > 1 else "",
        "nombres": persona_db.nombres or "",
        "codigo_estudiante": persona_db.codigo_estudiante or "",
        "dni": persona_db.dni or "",
        "celular": persona_db.celular or "",
        "direccion": persona_db.direccion or "",
        "correo": persona_db.correo or "",
        "facultad": persona_db.facultad.nombre if persona_db.facultad else ""
    }
    db.close()
    
    ficha = PersonaController.get_ficha_derivacion(atencion_id)
    if not ficha:
        ficha = {}

    # ── 2. Campos del Formulario ──
    
    # Organismos
    default_area = ficha.get("area_deriva")
    if not default_area:
        default_area = "Servicio Social"
        
    e_area_deriva = ft.TextField(label="Área que deriva", value=default_area, expand=True)
    e_area_derivada = ft.TextField(label="Área a la que se deriva", value=ficha.get("area_derivada", ""), expand=True)
    e_fecha_derivacion = ft.TextField(label="Fecha de Ficha (DD/MM/AAAA)", value=ficha.get("fecha_derivacion", datetime.now().strftime("%d/%m/%Y")) if isinstance(ficha.get("fecha_derivacion"), str) else (ficha.get("fecha_derivacion").strftime("%d/%m/%Y") if ficha.get("fecha_derivacion") else datetime.now().strftime("%d/%m/%Y")), expand=True)
    
    # Datos Personales
    e_fecha_nac = ft.TextField(label="Fecha de Nac. (DD/MM/AAAA)", value=ficha.get("fecha_nacimiento", ""), expand=True)
    e_lugar_nac = ft.TextField(label="Lugar de Nacimiento", value=ficha.get("lugar_nacimiento", ""), expand=True)
    e_ocupacion = ft.TextField(label="Ocupación", value=ficha.get("ocupacion", ""), expand=True)
    e_vive_con = ft.TextField(label="Vive con", value=ficha.get("vive_con", ""), expand=True)
    e_tel_fam = ft.TextField(label="Tel. Familiares", value=ficha.get("telefono_familiares", ""), expand=True)
    
    # Información de la Derivación
    e_motivo = ft.TextField(label="Motivo de la consulta", value=ficha.get("motivo_consulta", ""), multiline=True, min_lines=2, expand=True)
    e_tiene_previas = ft.Switch(label="¿Tiene derivaciones previas?", value=ficha.get("tiene_derivaciones_previas", False))
    e_detalle_previas = ft.TextField(label="Detalle Derivaciones (Opcional)", value=ficha.get("detalle_derivaciones_previas", ""), expand=True)
    
    e_condicion = ft.Dropdown(
        label="Condición", 
        value=ficha.get("condicion", ""), 
        options=[ft.dropdown.Option("Leve"), ft.dropdown.Option("Moderado"), ft.dropdown.Option("Grave")],
        expand=True
    )
    
    # Impactos (Checkboxes)
    chk_academico = ft.Checkbox(label="Académico", value=ficha.get("impacto_academico", False))
    chk_social = ft.Checkbox(label="Social", value=ficha.get("impacto_social", False))
    chk_familiar = ft.Checkbox(label="Familiar", value=ficha.get("impacto_familiar", False))
    chk_personal = ft.Checkbox(label="Personal", value=ficha.get("impacto_personal", False))
    
    e_diagnostico = ft.TextField(label="Diagnóstico del caso", value=ficha.get("diagnostico", ""), multiline=True, min_lines=3, expand=True)
    e_observaciones = ft.TextField(label="Observaciones", value=ficha.get("observaciones", ""), multiline=True, min_lines=3, expand=True)

    # ── 3. Layout del Diálogo ──
    contenido = ft.Column([
        ft.Text("Información de los Organismos", weight="bold", color=ft.Colors.BLUE_300),
        ft.Row([e_area_deriva, e_area_derivada, e_fecha_derivacion]),
        ft.Divider(),
        
        ft.Text("Datos Personales (Complementarios)", weight="bold", color=ft.Colors.BLUE_300),
        ft.Row([e_fecha_nac, e_lugar_nac]),
        ft.Row([e_ocupacion, e_vive_con, e_tel_fam]),
        ft.Divider(),
        
        ft.Text("Información de la Derivación", weight="bold", color=ft.Colors.BLUE_300),
        ft.Row([e_motivo]),
        ft.Row([e_tiene_previas, e_detalle_previas]),
        ft.Row([e_condicion]),
        ft.Text("Impacto en el funcionamiento diario:", size=12),
        ft.Row([chk_academico, chk_social, chk_familiar, chk_personal]),
        ft.Row([e_diagnostico]),
        ft.Row([e_observaciones]),
    ], scroll=ft.ScrollMode.AUTO, spacing=15, tight=True)
    
    dlg = ft.AlertDialog(
        modal=True,
        title=ft.Text("Ficha de Derivación de Caso Social"),
        content=ft.Container(width=700, content=contenido),
    )

    def guardar_datos():
        nuevos_datos = {
            "fecha_nacimiento": e_fecha_nac.value,
            "lugar_nacimiento": e_lugar_nac.value,
            "ocupacion": e_ocupacion.value,
            "vive_con": e_vive_con.value,
            "telefono_familiares": e_tel_fam.value,
            "area_deriva": e_area_deriva.value,
            "area_derivada": e_area_derivada.value,
            "fecha_derivacion": e_fecha_derivacion.value,
            "motivo_consulta": e_motivo.value,
            "tiene_derivaciones_previas": e_tiene_previas.value,
            "detalle_derivaciones_previas": e_detalle_previas.value,
            "condicion": e_condicion.value,
            "impacto_academico": chk_academico.value,
            "impacto_social": chk_social.value,
            "impacto_familiar": chk_familiar.value,
            "impacto_personal": chk_personal.value,
            "diagnostico": e_diagnostico.value,
            "observaciones": e_observaciones.value
        }
        return nuevos_datos

    def cmd_guardar(e):
        datos = guardar_datos()
        success, msg = PersonaController.guardar_ficha_derivacion(atencion_id, datos)
        if success:
            mostrar_exito(page, "Ficha de Derivación guardada")
            dlg.open = False
            page.update()
            if on_close:
                on_close()
        else:
            mostrar_snackbar(page, f"Error: {msg}", "red")

    def cmd_imprimir(e):
        # Primero guardamos
        datos = guardar_datos()
        success, msg = PersonaController.guardar_ficha_derivacion(atencion_id, datos)
        if success:
            mostrar_exito(page, "Generando PDF...")
            # Combinamos datos base con los datos del formulario para enviar al HTML
            datos_completos = {**datos_base, **datos}
            
            try:
                generar_html_derivacion(datos_completos)
            except Exception as ex:
                mostrar_snackbar(page, f"Error al generar: {str(ex)}", "red")
                
            dlg.open = False
            page.update()
            if on_close:
                on_close()
        else:
            mostrar_snackbar(page, f"Error al guardar: {msg}", "red")

    dlg.actions = [
        ft.TextButton("Cancelar", on_click=lambda _: (setattr(dlg, 'open', False), page.update())),
        ft.ElevatedButton("Guardar Ficha", icon=ft.Icons.SAVE, color=ft.Colors.WHITE, bgcolor=ft.Colors.BLUE_800, on_click=cmd_guardar),
        ft.ElevatedButton("Generar PDF", icon=ft.Icons.PRINT, color=ft.Colors.WHITE, bgcolor=ft.Colors.GREEN_700, on_click=cmd_imprimir),
    ]
    
    # ── Manejo de Overlay ──
    page.overlay.append(dlg)
    dlg.open = True
    page.update()
