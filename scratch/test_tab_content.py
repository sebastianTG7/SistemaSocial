import flet as ft

def test():
    try:
        t = ft.Tab(label="Tab A")
        # Asignar content después del init
        t.content = ft.Container(content=ft.Text("Hello World"))
        print("t.content assignment after init OK!")
    except Exception as e:
        print(f"t.content assignment failed: {e}")

if __name__ == "__main__":
    test()
