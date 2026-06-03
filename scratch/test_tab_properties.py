import inspect
import flet as ft

def inspect_tab():
    print("--- INSPECTING ft.Tab ---")
    try:
        # Imprimir la firma de __init__
        sig = inspect.signature(ft.Tab.__init__)
        print(f"Tab.__init__ signature: {sig}")
    except Exception as e:
        print(f"Error inspecting signature: {e}")
        
    print("\nAvailable attributes/properties of ft.Tab:")
    t = ft.Tab(label="Test")
    attrs = dir(t)
    for attr in sorted(attrs):
        if not attr.startswith("_"):
            print(f"  {attr}")

if __name__ == "__main__":
    inspect_tab()
