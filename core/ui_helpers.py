import flet as ft
import threading
import time


def mostrar_snackbar(page: ft.Page, mensaje: str, color=ft.Colors.GREEN_800, duracion_ms: int = 3000):
    """Muestra un SnackBar compatible en la parte inferior."""
    page.snack_bar = ft.SnackBar(
        content=ft.Text(mensaje, color=ft.Colors.WHITE),
        bgcolor=color,
        duration=duracion_ms,
    )
    page.snack_bar.open = True
    page.update()


def mostrar_exito(page: ft.Page, mensaje: str):
    """Muestra una notificación flotante estilo Toast ULTRA-DELGADA y compacta."""
    
    notif_container = ft.Ref[ft.Container]()

    def cerrar_notif(e=None):
        try:
            if notif_container.current:
                notif_container.current.opacity = 0
                page.update()
                time.sleep(0.3)
                if notif_container.current in page.overlay:
                    page.overlay.remove(notif_container.current)
                page.update()
        except: pass

    notif = ft.Container(
        ref=notif_container,
        width=240,
        content=ft.Column([
            # CABECERA ULTRA-DELGADA
            ft.Container(
                width=240,
                height=26, # Altura fija mínima
                content=ft.Row([
                    ft.Text(" Éxito", color=ft.Colors.GREEN_900, weight="bold", size=11),
                    ft.IconButton(
                        icon=ft.Icons.CLOSE, 
                        icon_color=ft.Colors.GREEN_900, 
                        icon_size=12,
                        on_click=cerrar_notif,
                        padding=0
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                bgcolor=ft.Colors.GREEN_100,
                padding=ft.Padding(10, 0, 5, 0),
                border_radius=ft.border_radius.only(top_left=6, top_right=6)
            ),
            # CUERPO ULTRA-DELGADO
            ft.Container(
                width=240,
                height=34, # Altura fija mínima
                content=ft.Text(f" {mensaje}", color=ft.Colors.WHITE, size=10, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                bgcolor=ft.Colors.GREEN_800,
                padding=ft.Padding(10, 0, 10, 0),
                alignment=ft.alignment.Alignment(-1, 0),
                border_radius=ft.border_radius.only(bottom_left=6, bottom_right=6)
            )
        ], spacing=0, tight=True),
        top=20,
        right=20,
        shadow=ft.BoxShadow(blur_radius=8, color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK)),
        animate_opacity=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
        opacity=0,
    )

    page.overlay.append(notif)
    page.update()
    
    notif.opacity = 1
    page.update()
    
    def timer_cerrar():
        time.sleep(1.5); cerrar_notif()
            
    threading.Thread(target=timer_cerrar, daemon=True).start()
