import flet as ft

def test():
    try:
        t = ft.Tabs(
            length=3,
            content=[
                ft.Tab(label="Tab 1"),
                ft.Tab(label="Tab 2"),
                ft.Tab(label="Tab 3")
            ]
        )
        print("Tabs with Tab list inside content OK!")
    except Exception as e:
        print(f"Tabs failed: {e}")

if __name__ == "__main__":
    test()
