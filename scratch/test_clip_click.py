import flet as ft

def main(page: ft.Page):
    page.title = "Test Stack Clip Click"
    page.theme_mode = ft.ThemeMode.DARK
    
    click_count = 0
    txt_info = ft.Text("Clics en elemento fuera de límites: 0")
    
    def on_btn_click(e):
        nonlocal click_count
        click_count += 1
        txt_info.value = f"Clics en elemento fuera de límites: {click_count}"
        page.update()

    # Stack of height 50, but with a button at top=60 (overflowing)
    stack = ft.Stack(
        controls=[
            ft.Container(
                content=ft.Text("Botón Padre (dentro de límites)", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.BLUE_900,
                width=200,
                height=50,
                alignment=ft.alignment.center
            ),
            ft.Container(
                content=ft.ElevatedButton("Botón Fuera (Hijo)", on_click=on_btn_click),
                top=60,
                width=200,
                height=50,
            )
        ],
        width=200,
        height=50,
        clip_behavior=ft.ClipBehavior.NONE
    )

    page.add(
        ft.Column([
            stack,
            ft.Container(height=80), # Spacer so the button doesn't overlap text
            txt_info
        ])
    )

if __name__ == "__main__":
    ft.run(main)
