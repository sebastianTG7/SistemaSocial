import flet as ft

def main(page: ft.Page):
    t = ft.Tabs(
        length=2,
        content=[
            ft.Tab(text="Hola"),
            ft.Tab(text="Mundo")
        ]
    )
    page.add(t)

if __name__ == "__main__":
    try:
        # Solo para ver si falla el init
        ft.Tabs(length=2, content=[ft.Tab(text="A"), ft.Tab(text="B")])
        print("Standard init OK")
    except Exception as e:
        print(f"Standard init FAILED: {e}")
