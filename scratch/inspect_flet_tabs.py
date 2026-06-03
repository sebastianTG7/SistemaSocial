import flet as ft
import inspect

print("ft.Tab file:", inspect.getfile(ft.Tab))
print("ft.Tabs file:", inspect.getfile(ft.Tabs))

# Let's inspect properties of Tab and Tabs via inspect.getmembers
print("\nProperties of ft.Tab:")
for name, prop in inspect.getmembers(ft.Tab, lambda o: isinstance(o, property)):
    print(f"  {name}")

print("\nProperties of ft.Tabs:")
for name, prop in inspect.getmembers(ft.Tabs, lambda o: isinstance(o, property)):
    print(f"  {name}")
