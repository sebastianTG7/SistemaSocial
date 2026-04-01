import flet as ft

def try_tab(kw="label"):
    try:
        t = ft.Tab(**{kw: "Test"})
        print(f"Tab({kw}='Test') OK")
    except Exception as e:
        print(f"Tab({kw}='Test') FAILED: {e}")

if __name__ == "__main__":
    try_tab("label")
    try_tab("text")
    try_tab("hint")
    try_tab("name")
