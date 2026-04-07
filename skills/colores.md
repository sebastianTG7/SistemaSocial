Colores


Flet admite dos formas principales de definir colores:

Valores hexadecimales
Colores nombrados
Valores hexadecimales#
Los valores de color hexadecimal siguen cualquiera de estos formatos:

#aarrggbb o 0xaarrggbb
#rrggbb o (opacidad por defecto si se omite)0xrrggbbffaa

>>> ft.Container(bgcolor="#ff0000")
Ejemplo en vivo

Color Nombrado#
Flet utiliza los colores y paletas de colores temáticos de Material Design.

Puedes definir colores con nombre de dos maneras:

Como cadena (por ejemplo, , "blue""redAccent100")
Uso de los enums de or para mejorar la seguridad de los tipos y la autocompletaciónColorsCupertinoColors

>>> ft.Container(bgcolor="yellow")
>>> ft.Container(bgcolor=ft.Colors.YELLOW)
>>> ft.Container(bgcolor=ft.CupertinoColors.DESTRUCTIVE_RED)
Colores del tema#


Ejemplo en vivo

Hay 30 colores temáticos nombrados en Theme.color_scheme que se generan en función de el Theme.color_scheme_seed, que por defecto es Colors.BLUE.


>>> page.theme = ft.Theme(color_scheme_seed=ft.Colors.GREEN)
Cualquiera de los 30 colores del esquema temático puede ser anulado, en cuyo caso tendrán un valor absoluto Eso ya no dependerá del color de la semilla.


page.theme = ft.Theme(
    color_scheme=ft.ColorScheme(
        primary=ft.Colors.GREEN,
        error=ft.Colors.RED,
    ),
)


Los colores de los temas sirven como valores de respaldo para la mayoría de los controles Flet.

Paletas de colores#


Ejemplo en vivo

Originalmente introducidas por Material Design en 2014, las paletas de colores son colecciones de coordenadas colores diseñados para funcionar armoniosamente.

Cada muestra de color (paleta) incluye múltiples tonos de un color específico, donde los números son menores representan tonos claros y los números más altos indican los más oscuros. La mayoría de las paletas varían de hasta , en incrementos de , mientras que las muestras de acento (por ejemplo, Colors.RED_ACCENT) solo tienen , , , y .50900100100200400700

Además de las muestras de color, Flet ofrece variantes en blanco y negro con nombre y opacidades integradas, tales como: - Colors.BLACK_54 → negro con un 54% de opacidad - Colors.WHITE_70 → blanco con un 70% de opacidad

Estos colores de paleta pueden utilizarse: - directamente como valores para propiedades de color de control (por ejemplo, , ) - como colores semilla para generar esquemas de color dinámicos de temas usando Theme.color_scheme_seedbgcolorcolor

Opacidad del color#
Flet proporciona varias formas de establecer opacidad:

Usando with_opacity#
Este método está presente tanto en los enums de Colors como en CupertinoColors. Toma un color y una opacidad, y devuelve una cadena en el formato , entendido por Flet."color,opacity"


>>> ft.Colors.with_opacity(0.5, ft.Colors.RED)
"red,0.5"
>>> ft.CupertinoColors.with_opacity(0.8, ft.CupertinoColors.LINK)
"link,0.8"
Incrustación de opacidad en código hexadecimal#
Para colores en formato hexadecimal, puedes especificar el canal con valores entre y .aa00ff


>>> "#7fff6666"  # (1)!
Color rojo con opacidad del 50% ().7f
Definición de colores para los controles Flet#
La mayoría de los controles Flet tienen colores predeterminados definidos por el Theme.color_scheme, y estos pueden ser anulados en varios niveles.

Ejemplo en vivo



Nivel de control#
Si se proporciona un color como valor para la propiedad color similar a un control, se usará directamente.


>>> ft.Card(bgcolor=ft.Colors.GREEN_200)
Nota: No todos los controles Flet tienen una propiedad de color que se pueda establecer a nivel de control. Por ejemplo, FilledButton siempre tiene un color "primario" por defecto que está definido por el ancestro más cercano.theme

Nivel de tema de control#
El objeto Tema tiene muchas propiedades que pueden usarse para anular el valor predeterminado colores para los controles Flet.

Por ejemplo, el Theme.card_bgcolor más cercano se usará para el control de la Tarjeta.

Nota: Si necesitas cambiar el tema para ciertos descendientes, puedes envolver por ejemplo, en un contenedor, y personalizar su propiedad de tema, que se aplicará a todos sus descendientes.

Nivel de Tema de los Antepasados#
Flet busca hacia arriba en el árbol de widgets el ancestro más cercano con un , y tomará color de su Theme.color_scheme. En el ejemplo siguiente, el antecesor más cercano para el FilledButton es Container, y el color que se usa para el botón se tomará del tema Container..themeprimary


import flet as ft

def main(page: ft.Page):
    page.add(
        ft.Container(
            width=200,
            height=200,
            border=ft.border.all(1, ft.Colors.BLACK),
            content=ft.FilledButton("Primary color"),
            theme=ft.Theme(color_scheme=ft.ColorScheme(primary=ft.Colors.YELLOW))
        )
    )

ft.run(main)
Si no se define ningún tema para un control, su padre o sus antecesores, el control se vuelve por defecto a usando el tema del antepasado superior, que es Page.theme (o Page.dark_theme en modo oscuro).