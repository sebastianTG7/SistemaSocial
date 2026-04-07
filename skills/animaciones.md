Animaciones
Animaciones implícitas#
Con animaciones implícitas, puedes animar una propiedad de control estableciendo un valor objetivo; Cuando ese objetivo El valor cambia, el control anima la propiedad del valor antiguo al nuevo.

La animación produce valores interpolados entre el valor antiguo y el nuevo durante la duración dada.

Por defecto, la animación aumenta linealmente el valor de la animación, sin embargo, una curva puede ser aplicado a la animación, que cambia el valor según la curva proporcionada. Por ejemplo, AnimationCurve.EASE_OUT_CUBIC curva aumenta rápidamente el valor de animación en el Inicio de la animación y luego ralentizándose hasta alcanzar el valor objetivo:

LayoutControl (y sus subclases) proporciona varias propiedades, descritas a continuación, para permitir la animación implícita de su apariencia:animate_{something}

animate_opacity
animate_rotation
animate_scale
animate_offset
animate_position
animate (Container)
animate_* Las propiedades podrían tener uno de los siguientes valores:

Instancia de animación - permite configurar la duración y la curva del
animación, por ejemplo. Consulta esta documentación de Flutter sobre curvas de animación para posibles valores. Por defecto es AnimationCurve.LINEAR.animate_rotation=Animation(duration=300, curve=AnimationCurve.BOUNCE_OUT)
int valor - permite animación con duración especificada en milisegundos y AnimationCurve. Curva LINEAL.
bool valor - permite animación con una duración de 1000 milisegundos y AnimationCurve. Curva LINEAL.