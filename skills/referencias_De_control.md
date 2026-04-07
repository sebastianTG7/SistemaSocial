Referencias de control
Los controles Flet son objetos y para acceder a sus propiedades necesitamos mantener referencias (variables) a esos objetos.

Consideremos el siguiente ejemplo:


import flet as ft

def main(page):
    first_name = ft.TextField(label="First name", autofocus=True)
    last_name = ft.TextField(label="Last name")
    greetings = ft.Column()

    async def btn_click(e):
        greetings.controls.append(ft.Text(f"Hello, {first_name.value} {last_name.value}!"))
        first_name.value = ""
        last_name.value = ""
        page.update()
        await first_name.focus()

    page.add(
        first_name,
        last_name,
        ft.Button("Say hello!", on_click=btn_click),
        greetings,
    )

ft.run(main)
Al principio del método creamos tres controles que vamos a usar en el manejador de botón: dos para nombres y apellidos y un contenedor - para mensajes de saludo. Creamos controles con todas sus propiedades activadas y, al final del método, en llamada, Usamos sus referencias (variables).main()on_clickTextFieldColumnmain()page.add()

Cuando se añaden más controles y gestores de eventos, se vuelve complicado mantener todo el control definiciones en un solo lugar, así que se dispersan por todo el cuerpo. Al mirar los parámetros, es es difícil imaginar (sin saltos constantes a definiciones de variables en IDE) cómo sería la forma final:main()page.add()


    page.add(
        first_name,
        last_name,
        ft.Button("Say hello!", on_click=btn_click),
        greetings,
    )
¿Es un TextField, tiene el enfoque automático activado? ¿Saludos es a o un ?first_nameRowColumn

Ref Clase#
Flet proporciona una clase utility que permite definir una referencia al control, usar esa referencia en los gestores de eventos y establecer la referencia a un control real más adelante, mientras se construye un árbol. La idea viene de React.Ref

Para definir una nueva referencia de control tipada:


first_name = ft.Ref[ft.TextField]()
Para acceder a la propiedad de uso de control referenciado (control de desreferencia):Ref.current


# empty first name
first_name.current.value = ""
Para asignar control a una propiedad de conjunto de referencia a una referencia:Control.ref


page.add(
    ft.TextField(ref=first_name, label="First name", autofocus=True)
)
Nota

Todos los controles Flet tienen propiedades.ref

Podríamos reescribir nuestro programa para usar referencias:


import flet as ft


def main(page):

    first_name = ft.Ref[ft.TextField]()
    last_name = ft.Ref[ft.TextField]()
    greetings = ft.Ref[ft.Column]()

    async def btn_click(e):
        greetings.current.controls.append(
            ft.Text(f"Hello, {first_name.current.value} {last_name.current.value}!")
        )
        first_name.current.value = ""
        last_name.current.value = ""
        page.update()
        await first_name.current.focus()

    page.add(
        ft.TextField(ref=first_name, label="First name", autofocus=True),
        ft.TextField(ref=last_name, label="Last name"),
        ft.Button("Say hello!", on_click=btn_click),
        ft.Column(ref=greetings),
    )

ft.run(main)
Ahora podemos ver claramente la estructura de la página y todos los controles que la componen.page.add()

Sí, la lógica se vuelve un poco más extensa a medida que necesitas añadir al control de Access Ref, pero es cuestión de preferencia personal :).current.