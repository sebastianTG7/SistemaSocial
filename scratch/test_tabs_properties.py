import flet as ft
import inspect

def inspect_tabs():
    print("--- INSPECTING ft.Tabs ---")
    try:
        sig = inspect.signature(ft.Tabs.__init__)
        print(f"Tabs.__init__ signature: {sig}")
    except Exception as e:
        print(f"Error signature: {e}")
        
    t = ft.Tabs(length=0, content=[])
    attrs = dir(t)
    print("Attributes:")
    for attr in sorted(attrs):
        if not attr.startswith("_"):
            print(f"  {attr}")

if __name__ == "__main__":
    inspect_tabs()
