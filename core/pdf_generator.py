import os
import webbrowser
from datetime import datetime

def generar_html_derivacion(datos_ficha, output_filename="ficha_derivacion_temp.html"):
    """
    Toma los datos de la ficha, reemplaza las variables en la plantilla HTML
    y abre el archivo en el navegador para impresión.
    """
    # Ruta de la plantilla
    template_path = os.path.join(os.path.dirname(__file__), "..", "assets", "derivacion_template.html")
    
    # Asegurarnos de que las rutas de los logos existan (relativas o absolutas para el HTML)
    # Usaremos rutas relativas porque el archivo HTML temporal se guarda en la misma carpeta assets/
    assets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets"))
    logo_unheval_path = "logo_unheval.png"
    logo_servicio_path = "logo_servicio_social.png"
    
    # Diccionario de mapeo
    data = {
        "{{ logo_unheval }}": logo_unheval_path,
        "{{ logo_servicio }}": logo_servicio_path,
        "{{ numero_ficha }}": str(datos_ficha.get("id", "001")),
        "{{ fecha }}": datos_ficha.get("fecha_derivacion", datetime.now().strftime("%d/%m/%Y")),
        "{{ area_deriva }}": datos_ficha.get("area_deriva", ""),
        "{{ area_derivada }}": datos_ficha.get("area_derivada", ""),
        "{{ apellido_paterno }}": datos_ficha.get("apellido_paterno", ""),
        "{{ apellido_materno }}": datos_ficha.get("apellido_materno", ""),
        "{{ nombres }}": datos_ficha.get("nombres", ""),
        "{{ fecha_nacimiento }}": datos_ficha.get("fecha_nacimiento", ""),
        "{{ codigo_estudiante }}": datos_ficha.get("codigo_estudiante", ""),
        "{{ dni }}": datos_ficha.get("dni", ""),
        "{{ lugar_nacimiento }}": datos_ficha.get("lugar_nacimiento", ""),
        "{{ celular }}": datos_ficha.get("celular", ""),
        "{{ direccion }}": datos_ficha.get("direccion", ""),
        "{{ correo }}": datos_ficha.get("correo", ""),
        "{{ ocupacion }}": datos_ficha.get("ocupacion", ""),
        "{{ facultad }}": datos_ficha.get("facultad", ""),
        "{{ vive_con }}": datos_ficha.get("vive_con", ""),
        "{{ telefono_familiares }}": datos_ficha.get("telefono_familiares", ""),
        "{{ motivo_consulta }}": datos_ficha.get("motivo_consulta", ""),
        "{{ detalle_derivaciones_previas }}": datos_ficha.get("detalle_derivaciones_previas", ""),
        "{{ diagnostico }}": datos_ficha.get("diagnostico", ""),
        "{{ observaciones }}": datos_ficha.get("observaciones", ""),
    }

    # Leer plantilla
    with open(template_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Reemplazo de variables simples
    for key, value in data.items():
        html_content = html_content.replace(key, str(value) if value else "")

    # Reemplazos lógicos (Checkboxes de jinja simulados)
    tiene_previas = datos_ficha.get("tiene_derivaciones_previas", False)
    html_content = html_content.replace("{{ 'X' if tiene_derivaciones_previas else '&nbsp;&nbsp;' }}", "X" if tiene_previas else "&nbsp;&nbsp;")
    html_content = html_content.replace("{{ '&nbsp;&nbsp;' if tiene_derivaciones_previas else 'X' }}", "&nbsp;&nbsp;" if tiene_previas else "X")

    condicion = datos_ficha.get("condicion", "")
    html_content = html_content.replace("{{ 'X' if condicion == 'Leve' else '&nbsp;&nbsp;' }}", "X" if condicion == "Leve" else "&nbsp;&nbsp;")
    html_content = html_content.replace("{{ 'X' if condicion == 'Moderado' else '&nbsp;&nbsp;' }}", "X" if condicion == "Moderado" else "&nbsp;&nbsp;")
    html_content = html_content.replace("{{ 'X' if condicion == 'Grave' else '&nbsp;&nbsp;' }}", "X" if condicion == "Grave" else "&nbsp;&nbsp;")

    impactos = [
        ("impacto_academico", "impacto_academico"),
        ("impacto_social", "impacto_social"),
        ("impacto_familiar", "impacto_familiar"),
        ("impacto_personal", "impacto_personal"),
    ]
    for key, var in impactos:
        val = datos_ficha.get(key, False)
        html_content = html_content.replace(f"{{{{ 'X' if {var} else '&nbsp;&nbsp;' }}}}", "X" if val else "&nbsp;&nbsp;")

    # Guardar archivo temporal
    temp_path = os.path.join(assets_dir, output_filename)
    with open(temp_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    # Abrir en el navegador
    file_url = f"file:///{temp_path.replace(chr(92), '/')}"
    webbrowser.open(file_url)
    
    return temp_path
