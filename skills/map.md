Map
Inherits: LayoutControl

An interactive map that displays various layers.

Properties

animation_curve(AnimationCurve) – The default animation curve to be used for map-animations
animation_duration(DurationValue) – The default animation duration to be used for map-animations
bgcolor(ColorValue) – The background color of this control.
initial_camera_fit(CameraFit | None) – Defines the visible bounds when the map is first loaded.
initial_center(MapLatitudeLongitude) – The initial center of the map.
initial_rotation(Number) – The rotation (in degrees) when the map is first loaded.
initial_zoom(Number) – The zoom when the map is first loaded.
interaction_configuration(InteractionConfiguration) – The interaction configuration.
keep_alive(bool) – Whether to enable the built in keep-alive functionality.
layers(list[MapLayer]) – A list of layers to be displayed (stack-like) on the map.
max_zoom(Number | None) – The maximum (highest) zoom level of every layer.
min_zoom(Number | None) – The minimum (smallest) zoom level of every layer.
Events

on_event(EventHandler[MapEvent] | None) – Fires when any map events occurs.
on_hover(EventHandler[MapHoverEvent] | None) – Fires when a hover event occurs.
on_init(ControlEventHandler[Map] | None) – Fires when the map is initialized.
on_long_press(EventHandler[MapTapEvent] | None) – Fires when a long press event occurs.
on_pointer_cancel(EventHandler[MapPointerEvent] | None) – Fires when a pointer cancel event occurs.
on_pointer_down(EventHandler[MapPointerEvent] | None) – Fires when a pointer down event occurs.
on_pointer_up(EventHandler[MapPointerEvent] | None) – Fires when a pointer up event occurs.
on_position_change(EventHandler[MapPositionChangeEvent] | None) – Fires when the map position changes, e.g. when the user pans or zooms the map.
on_secondary_tap(EventHandler[MapTapEvent] | None) – Fires when a secondary tap event occurs.
on_tap(EventHandler[MapTapEvent] | None) – Fires when a tap event occurs.
Methods

center_on – Centers the map on the given point.
get_camera – Gets the current camera snapshot of the map.
move_to – Moves to a specific location.
reset_rotation – Resets the map's rotation to 0 degrees.
rotate_from – Applies a rotation of degree to the current rotation.
zoom_in – Zooms in by one zoom-level from the current one.
zoom_out – Zooms out by one zoom-level from the current one.
zoom_to – Zoom the map to a specific zoom level.
Properties#
 animation_curve class-attribute instance-attribute #

animation_curve: AnimationCurve = FAST_OUT_SLOWIN
The default animation curve to be used for map-animations when calling instance methods like zoom_in(), rotate_from(), move_to() etc.

 animation_duration class-attribute instance-attribute #

animation_duration: DurationValue = field(
    default_factory=lambda: Duration(milliseconds=500)
)
The default animation duration to be used for map-animations when calling instance methods like zoom_in(), rotate_from(), move_to() etc.

 bgcolor class-attribute instance-attribute #

bgcolor: ColorValue = GREY_300
The background color of this control.

 initial_camera_fit class-attribute instance-attribute #

initial_camera_fit: CameraFit | None = None
Defines the visible bounds when the map is first loaded. Takes precedence over initial_center/initial_zoom.

 initial_center class-attribute instance-attribute #

initial_center: MapLatitudeLongitude = field(
    default_factory=lambda: MapLatitudeLongitude(
        latitude=50.5, longitude=30.51
    )
)
The initial center of the map.

 initial_rotation class-attribute instance-attribute #

initial_rotation: Number = 0.0
The rotation (in degrees) when the map is first loaded.

 initial_zoom class-attribute instance-attribute #

initial_zoom: Number = 13.0
The zoom when the map is first loaded. If initial_camera_fit is defined this has no effect.

 interaction_configuration class-attribute instance-attribute #

interaction_configuration: InteractionConfiguration = field(
    default_factory=lambda: InteractionConfiguration()
)
The interaction configuration.

 keep_alive class-attribute instance-attribute #

keep_alive: bool = False
Whether to enable the built in keep-alive functionality.

If the map is within a complex layout, such as a ListView, the map will reset to its initial position after it appears back into view. To ensure this doesn't happen, enable this flag to prevent it from rebuilding.

 layers instance-attribute #

layers: list[MapLayer]
A list of layers to be displayed (stack-like) on the map.

 max_zoom class-attribute instance-attribute #

max_zoom: Number | None = None
The maximum (highest) zoom level of every layer. Each layer can specify additional zoom level restrictions.

 min_zoom class-attribute instance-attribute #

min_zoom: Number | None = None
The minimum (smallest) zoom level of every layer. Each layer can specify additional zoom level restrictions.

Events#
 on_event class-attribute instance-attribute #

on_event: EventHandler[MapEvent] | None = None
Fires when any map events occurs.

 on_hover class-attribute instance-attribute #

on_hover: EventHandler[MapHoverEvent] | None = None
Fires when a hover event occurs.

 on_init class-attribute instance-attribute #

on_init: ControlEventHandler[Map] | None = None
Fires when the map is initialized.

 on_long_press class-attribute instance-attribute #

on_long_press: EventHandler[MapTapEvent] | None = None
Fires when a long press event occurs.

 on_pointer_cancel class-attribute instance-attribute #

on_pointer_cancel: EventHandler[MapPointerEvent] | None = (
    None
)
Fires when a pointer cancel event occurs.

 on_pointer_down class-attribute instance-attribute #

on_pointer_down: EventHandler[MapPointerEvent] | None = None
Fires when a pointer down event occurs.

 on_pointer_up class-attribute instance-attribute #

on_pointer_up: EventHandler[MapPointerEvent] | None = None
Fires when a pointer up event occurs.

 on_position_change class-attribute instance-attribute #

on_position_change: (
    EventHandler[MapPositionChangeEvent] | None
) = None
Fires when the map position changes, e.g. when the user pans or zooms the map.

 on_secondary_tap class-attribute instance-attribute #

on_secondary_tap: EventHandler[MapTapEvent] | None = None
Fires when a secondary tap event occurs.

 on_tap class-attribute instance-attribute #

on_tap: EventHandler[MapTapEvent] | None = None
Fires when a tap event occurs.

Methods#
 center_on async #

center_on(
    point: MapLatitudeLongitude,
    zoom: Number | None,
    animation_curve: AnimationCurve | None = None,
    animation_duration: DurationValue | None = None,
    cancel_ongoing_animations: bool = False,
) -> None
Centers the map on the given point.

Parameters:

point (MapLatitudeLongitude) – The point on which to center the map.
zoom (Number | None) – The zoom level to be applied.
animation_curve (AnimationCurve | None, default: None ) – The curve of the animation. If None (the default), Map.animation_curve will be used.
animation_duration (DurationValue | None, default: None ) – The duration of the animation. If None (the default), Map.animation_duration will be used.
cancel_ongoing_animations (bool, default: False ) – Whether to cancel/stop all ongoing map-animations before starting this new one.
 get_camera async #

get_camera() -> Camera
Gets the current camera snapshot of the map.

Returns:

Camera – Current Camera state.
 move_to async #

move_to(
    destination: MapLatitudeLongitude | None = None,
    zoom: Number | None = None,
    rotation: Number | None = None,
    animation_curve: AnimationCurve | None = None,
    animation_duration: DurationValue | None = None,
    offset: OffsetValue = (0, 0),
    cancel_ongoing_animations: bool = False,
) -> None
Moves to a specific location.

Parameters:

destination (MapLatitudeLongitude | None, default: None ) – The destination point to move to.
zoom (Number | None, default: None ) – The zoom level to be applied. If provided, must be greater than or equal to 0.0.
rotation (Number | None, default: None ) – Rotation (in degrees) to be applied.
offset (OffsetValue, default: (0, 0) ) – The offset to be used. Only works when rotation is None.
animation_curve (AnimationCurve | None, default: None ) – The curve of the animation. If None (the default), Map.animation_curve will be used.
animation_duration (DurationValue | None, default: None ) – The duration of the animation. If None (the default), Map.animation_duration will be used.
cancel_ongoing_animations (bool, default: False ) – Whether to cancel/stop all ongoing map-animations before starting this new one.
Raises:

ValueError – If zoom is not None and is negative.
 reset_rotation async #

reset_rotation(
    animation_curve: AnimationCurve | None = None,
    animation_duration: DurationValue | None = None,
    cancel_ongoing_animations: bool = False,
) -> None
Resets the map's rotation to 0 degrees.

Parameters:

animation_curve (AnimationCurve | None, default: None ) – The curve of the animation. If None (the default), Map.animation_curve will be used.
animation_duration (DurationValue | None, default: None ) – The duration of the animation. If None (the default), Map.animation_duration will be used.
cancel_ongoing_animations (bool, default: False ) – Whether to cancel/stop all ongoing map-animations before starting this new one.
 rotate_from async #

rotate_from(
    degree: Number,
    animation_curve: AnimationCurve | None = None,
    animation_duration: DurationValue | None = None,
    cancel_ongoing_animations: bool = False,
) -> None
Applies a rotation of degree to the current rotation.

Parameters:

degree (Number) – The number of degrees to increment to the current rotation.
animation_curve (AnimationCurve | None, default: None ) – The curve of the animation. If None (the default), Map.animation_curve will be used.
animation_duration (DurationValue | None, default: None ) – The duration of the animation. If None (the default), Map.animation_duration will be used.
cancel_ongoing_animations (bool, default: False ) – Whether to cancel/stop all ongoing map-animations before starting this new one.
 zoom_in async #

zoom_in(
    animation_curve: AnimationCurve | None = None,
    animation_duration: DurationValue | None = None,
    cancel_ongoing_animations: bool = False,
) -> None
Zooms in by one zoom-level from the current one.

Parameters:

animation_curve (AnimationCurve | None, default: None ) – The curve of the animation. If None (the default), Map.animation_curve will be used.
animation_duration (DurationValue | None, default: None ) – The duration of the animation. If None (the default), Map.animation_duration will be used.
cancel_ongoing_animations (bool, default: False ) – Whether to cancel/stop all ongoing map-animations before starting this new one.
 zoom_out async #

zoom_out(
    animation_curve: AnimationCurve | None = None,
    animation_duration: DurationValue | None = None,
    cancel_ongoing_animations: bool = False,
) -> None
Zooms out by one zoom-level from the current one.

Parameters:

animation_curve (AnimationCurve | None, default: None ) – The curve of the animation. If None (the default), Map.animation_curve will be used.
animation_duration (DurationValue | None, default: None ) – The duration of the animation. If None (the default), Map.animation_duration will be used.
cancel_ongoing_animations (bool, default: False ) – Whether to cancel/stop all ongoing map-animations before starting this new one.
 zoom_to async #

zoom_to(
    zoom: Number,
    animation_curve: AnimationCurve | None = None,
    animation_duration: DurationValue | None = None,
    cancel_ongoing_animations: bool = False,
) -> None
Zoom the map to a specific zoom level.

Parameters:

zoom (Number) – The zoom level to zoom to.
animation_curve (AnimationCurve | None, default: None ) – The curve of the animation. If None (the default), Map.animation_curve will be used.
animation_duration (DurationValue | None, default: None ) – The duration of the animation. If None (the default), Map.animation_duration will be used.
cancel_ongoing_animations (bool, default: False ) – Whether to cancel/stop all ongoing map-animations before starting this new one.
MapLayer
Inherits: Control

Abstract class for all map layers.

The following layers are available:

CircleLayer
MarkerLayer
PolygonLayer
PolylineLayer
RichAttribution
SimpleAttribution
TileLayer