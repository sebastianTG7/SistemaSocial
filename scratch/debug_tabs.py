import flet as ft

def main(page: ft.Page):
    # Vamos a probar la creación de ft.Tabs
    try:
        print("Testing basic tabs construction...")
        t1 = ft.Tab(label="Tab A")
        t1.content = ft.Container(content=ft.Text("Content A"))
        
        t2 = ft.Tab(label="Tab B")
        t2.content = ft.Container(content=ft.Text("Content B"))
        
        tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            length=2,
            content=[t1, t2],
            expand=True
        )
        print("Tabs created successfully. Let's inspect their properties:")
        print("tabs.content:", tabs.content)
        print("tabs.length:", tabs.length)
        print("tab1.content:", t1.content)
        
        # Intentemos agregarlo a la página para ver si se queja al hacer update
        page.add(tabs)
        print("Added to page successfully!")
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    ft.app(target=main)
