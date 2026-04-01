import flet as ft

def main(page: ft.Page):
    print(f"Overlay type: {type(page.overlay)}")
    try:
        page.overlay.add(ft.Container())
        print("overlay.add exists")
    except AttributeError:
        print("overlay does NOT have .add, it is likely a list")
    except Exception as e:
        print(f"Error adding: {e}")
    page.window.close()

if __name__ == "__main__":
    ft.app(target=main)
