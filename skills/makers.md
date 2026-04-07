Marker
Inherits: Control

A marker displayed on the Map at the specified location through the MarkerLayer.

Properties

alignment(Alignment | None) – Alignment of the marker relative to the normal center at coordinates.
content(Control) – The content to be displayed at coordinates.
coordinates(MapLatitudeLongitude) – The coordinates of the marker.
height(Number) – The height of the content Control.
rotate(bool | None) – Whether to counter rotate this marker to the map's rotation,
width(Number) – The width of the content Control.
Properties#
 alignment class-attribute instance-attribute #

alignment: Alignment | None = None
Alignment of the marker relative to the normal center at coordinates.

Defaults to the value of the parent MarkerLayer.alignment.

 content instance-attribute #

content: Control
The content to be displayed at coordinates.

Raises:

ValueError – If it is not visible.
 coordinates instance-attribute #

coordinates: MapLatitudeLongitude
The coordinates of the marker.

This will be the center of the marker, if alignment is Alignment.CENTER.

 height class-attribute instance-attribute #

height: Number = 30.0
The height of the content Control.

Raises:

ValueError – If it is less than 0.0.
 rotate class-attribute instance-attribute #

rotate: bool | None = None
Whether to counter rotate this marker to the map's rotation, to keep a fixed orientation. So, when True, this marker will always appear upright and vertical from the user's perspective.

If None, defaults to the value of the parent MarkerLayer.rotate.

Note
This is not used to apply a custom rotation in degrees to this marker.

 width class-attribute instance-attribute #

width: Number = 30.0
The width of the content Control.

Raises:

ValueError – If it is less than 0.0.






CircleMarker
Inherits: Control

A circular marker displayed on the Map at the specified location through the CircleLayer.

Properties

border_color(ColorValue | None) – The color of the circle border line.
border_stroke_width(Number) – The stroke width for the circle border.
color(ColorValue | None) – The color of the circle area.
coordinates(MapLatitudeLongitude) – The center coordinates of the circle
radius(Number) – The radius of the circle
use_radius_in_meter(bool) – Whether the radius should use the unit meters.
Properties#
 border_color class-attribute instance-attribute #

border_color: ColorValue | None = None
The color of the circle border line.

Tip
border_stroke_width must be greater than 0.0 in order for this color to be visible.

 border_stroke_width class-attribute instance-attribute #

border_stroke_width: Number = 0.0
The stroke width for the circle border.

Raises:

ValueError – If it is less than 0.0.
 color class-attribute instance-attribute #

color: ColorValue | None = None
The color of the circle area.

 coordinates instance-attribute #

coordinates: MapLatitudeLongitude
The center coordinates of the circle

 radius instance-attribute #

radius: Number
The radius of the circle

 use_radius_in_meter class-attribute instance-attribute #

use_radius_in_meter: bool = False
Whether the radius should use the unit meters.



PolygonMarker
Inherits: Control

A marker for the PolygonLayer.

Properties

border_color(ColorValue) – The color of the border outline.
border_stroke_width(Number) – The width of the border outline.
color(ColorValue) – The color of the polygon.
coordinates(list[MapLatitudeLongitude]) – The points for the outline of this polygon.
disable_holes_border(bool) – Whether holes should have borders.
label(str | None) – An optional label for this polygon.
label_text_style(TextStyle | None) – The text style for the label.
rotate_label(bool) – Whether to rotate the label counter to the camera's rotation,
stroke_cap(StrokeCap) – Style to use for line endings.
stroke_join(StrokeJoin) – Style to use for line segment joins.
Properties#
 border_color class-attribute instance-attribute #

border_color: ColorValue = GREEN
The color of the border outline.

 border_stroke_width class-attribute instance-attribute #

border_stroke_width: Number = 0.0
The width of the border outline.

Raises:

ValueError – If it is less than 0.0.
 color class-attribute instance-attribute #

color: ColorValue = GREEN
The color of the polygon.

 coordinates instance-attribute #

coordinates: list[MapLatitudeLongitude]
The points for the outline of this polygon.

 disable_holes_border class-attribute instance-attribute #

disable_holes_border: bool = False
Whether holes should have borders.

 label class-attribute instance-attribute #

label: str | None = None
An optional label for this polygon.

Note
Specifying a label will reduce performance, as the internal canvas must be drawn to and 'saved' more frequently to ensure the proper stacking order is maintained. This can be avoided, potentially at the expense of appearance, by setting PolygonLayer.draw_labels_last.

 label_text_style class-attribute instance-attribute #

label_text_style: TextStyle | None = None
The text style for the label.

 rotate_label class-attribute instance-attribute #

rotate_label: bool = False
Whether to rotate the label counter to the camera's rotation, to ensure it remains upright.

 stroke_cap class-attribute instance-attribute #

stroke_cap: StrokeCap = ROUND
Style to use for line endings.

 stroke_join class-attribute instance-attribute #

stroke_join: StrokeJoin = ROUND
Style to use for line segment joins.




PolylineMarker
Inherits: Control

A marker for the PolylineLayer.

Properties

border_color(ColorValue) – The border's color.
border_stroke_width(Number) – The width of the stroke with of the line border.
color(ColorValue) – The color of the line stroke.
colors_stop(list[Number] | None) – The stops for the gradient_colors.
coordinates(list[MapLatitudeLongitude]) – The list of coordinates for the polyline.
gradient_colors(list[ColorValue] | None) – The List of colors in case a gradient should get used.
stroke_cap(StrokeCap) – Style to use for line endings.
stroke_join(StrokeJoin) – Style to use for line segment joins.
stroke_pattern(StrokePattern) – Determines whether the line should be solid, dotted, or dashed, and the
stroke_width(Number) – The width of the stroke.
use_stroke_width_in_meter(bool) – Whether the stroke's width should have meters as unit.
Properties#
 border_color class-attribute instance-attribute #

border_color: ColorValue = YELLOW
The border's color.

 border_stroke_width class-attribute instance-attribute #

border_stroke_width: Number = 0.0
The width of the stroke with of the line border.

Raises:

ValueError – If it is less than 0.0.
 color class-attribute instance-attribute #

color: ColorValue = YELLOW
The color of the line stroke.

 colors_stop class-attribute instance-attribute #

colors_stop: list[Number] | None = None
The stops for the gradient_colors.

 coordinates instance-attribute #

coordinates: list[MapLatitudeLongitude]
The list of coordinates for the polyline.

 gradient_colors class-attribute instance-attribute #

gradient_colors: list[ColorValue] | None = None
The List of colors in case a gradient should get used.

 stroke_cap class-attribute instance-attribute #

stroke_cap: StrokeCap = ROUND
Style to use for line endings.

 stroke_join class-attribute instance-attribute #

stroke_join: StrokeJoin = ROUND
Style to use for line segment joins.

 stroke_pattern class-attribute instance-attribute #

stroke_pattern: StrokePattern = field(
    default_factory=lambda: SolidStrokePattern()
)
Determines whether the line should be solid, dotted, or dashed, and the exact characteristics of each.

 stroke_width class-attribute instance-attribute #

stroke_width: Number = 1.0
The width of the stroke.

Raises:

ValueError – If it is less than 0.0.
 use_stroke_width_in_meter class-attribute instance-attribute #

use_stroke_width_in_meter: bool = False
Whether the stroke's width should have meters as unit.
