TileLayer
Inherits: MapLayer

Displays square raster images in a continuous grid, sourced from the provided url_template and fallback_url.

Typically, the first layer to be added to a Map, as it provides the tiles on which other layers are displayed.

Caching
This control supports basic map tile caching (for compatible tile providers). On non-web platforms, built-in caching is automatically enabled with a default soft limit of 1 GB. On web platforms, caching is typically handled by the browser.

No guarantees are provided regarding the persistence or reliability of cached tiles. Cached data may become unavailable or be cleared at any time. For example, do not rely on this caching mechanism in scenarios where missing tiles could create risk or unsafe conditions (for example, offline or safety-critical mapping applications).

It aims to:

Improve developer experience by:
Reducing the costs of using tile servers by reducing duplicate tile requests
Keep your app lightweight - the built-in cache doesn't ship any binaries or databases, just a couple extra libraries you probably already use
Improve user experience by:
Reducing tile loading durations, as fetching from the cache is very quick
Reducing network/Internet usage, which may be limited or metered/expensive (eg. mobile broadband)
Improve compliance with tile server requirements, by reducing the strain on them
Be extensible, customizable, and integrate with multiple tile providers
But it comes at the expense of usage of on-device storage capacity.

Supported sources
flet-map doesn't provide tiles, so you'll need to bring your own raster tiles. There are multiple different supported sources.

Slippy Map/CARTO (XYZ): This is the most common format for raster tiles, although many satellite tiles will instead use WMS. Typically, a URL with placeholders for X, Y, and Z values. Set the url_template to the template provided by the tile server - usually it can be copied directly from an account portal or documentation. Additional information, like API/access keys, can be passed in using the additional_options property. It's also possible to specify a fallback_url template, used if fetching a tile from the primary url_template fails.
Tile Map Service (TMS): This is also supported. Follow the instructions for the XYZ source above, then set the enable_tms property to True. Read more on WMS here.
Web Map Services (WMS): This is also supported. Use wms_configuration to specify the necessary configuration for WMS tile servers. Read more on WMS here.
Example:


ftm.TileLayer(
    url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
    user_agent_package_name="MyTownMaps/1.4 (+https://example.org; contact: maps@example.org)",
)
Properties

additional_options(dict[str, str]) – Static information that should replace placeholders in the url_template.
display_mode(TileDisplay) – Defines how tiles are displayed on the map.
enable_retina_mode(bool) – Whether to enable retina mode.
enable_tms(bool) – Whether to inverse Y-axis numbering for tiles.
error_image_src(str | None) – The source of the tile image to show in place of the tile that failed to load.
evict_error_tile_strategy(TileLayerEvictErrorTileStrategy | None) – If a tile was loaded with error,
fallback_url(str | None) – Fallback URL template used if fetching tiles from url_template fails.
keep_buffer(int) – When panning the map, keep this many rows and columns of
max_native_zoom(int) – Maximum zoom number supported by the tile source has available.
max_zoom(Number) – The maximum zoom level up to which this layer will be displayed (inclusive).
min_native_zoom(int) – Minimum zoom level supported by the tile source.
min_zoom(Number) – The minimum zoom level at which this layer is displayed (inclusive).
pan_buffer(int) – When loading tiles only visible tiles are loaded by default.
subdomains(list[str]) – List of subdomains used in the URL template.
tile_bounds(MapLatitudeLongitudeBounds | None) – Defines the bounds of the map.
tile_size(int) – The size in pixels of each tile image.
url_template(str) – The URL template is a string that contains placeholders,
user_agent_package_name(str) – The package name of the user agent to use when fetching tiles from the tile server.
wms_configuration(WMSTileLayerConfiguration | None) – The configuration for WMS
zoom_offset(Number) – The zoom number used in tile URLs will be offset with this value.
zoom_reverse(bool) – Whether the zoom number used in tile URLs will be reversed
Events

on_image_error(ControlEventHandler[TileLayer] | None) – Fires if an error occurs when fetching the tiles.
Properties#
 additional_options class-attribute instance-attribute #

additional_options: dict[str, str] = field(
    default_factory=dict
)
Static information that should replace placeholders in the url_template. Applying API keys, for example, is a good usecase of this parameter.

Example

TileLayer(
    url_template="https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}{r}.png?access_token={accessToken}",
    additional_options={
        'accessToken': '<ACCESS_TOKEN_HERE>',
        'id': 'mapbox.streets',
    },
)
 display_mode class-attribute instance-attribute #

display_mode: TileDisplay = field(
    default_factory=lambda: FadeInTileDisplay()
)
Defines how tiles are displayed on the map.

 enable_retina_mode class-attribute instance-attribute #

enable_retina_mode: bool = False
Whether to enable retina mode. Retina mode improves the resolution of map tiles, particularly on high density displays.

 enable_tms class-attribute instance-attribute #

enable_tms: bool = False
Whether to inverse Y-axis numbering for tiles. Turn this on for TMS services.

 error_image_src class-attribute instance-attribute #

error_image_src: str | None = None
The source of the tile image to show in place of the tile that failed to load.

See on_image_error property for details on the error.

 evict_error_tile_strategy class-attribute instance-attribute #

evict_error_tile_strategy: (
    TileLayerEvictErrorTileStrategy | None
) = NONE
If a tile was loaded with error, the tile provider will be asked to evict the image based on this strategy.

 fallback_url class-attribute instance-attribute #

fallback_url: str | None = None
Fallback URL template used if fetching tiles from url_template fails.

The template must follow the same format and support the same placeholders as url_template.

Note
When this is specified, tiles will not be cached in memory, to prevent inconsistencies when url_template is unreliable, avoiding situations where tiles from different sources are displayed simultaneously. Disabling caching may negatively impact performance and efficiency, hence the recommendation to only specify a fallback URL when really necessary.

 keep_buffer class-attribute instance-attribute #

keep_buffer: int = 2
When panning the map, keep this many rows and columns of tiles before unloading them.

 max_native_zoom class-attribute instance-attribute #

max_native_zoom: int = 19
Maximum zoom number supported by the tile source has available.

Tiles from above this zoom level will not be displayed, instead tiles at this zoom level will be displayed and scaled.

Most tile servers support up to zoom level 19, which is the default. Otherwise, this should be specified.

You can also set max_zoom, which is an absolute zoom limit for users. It is recommended to set it to a few levels greater than the maximum zoom level covered by any of your tile layers.

Raises:

ValueError – If it is less than 0.0.
 max_zoom class-attribute instance-attribute #

max_zoom: Number = float('inf')
The maximum zoom level up to which this layer will be displayed (inclusive). The main usage for this property is to display a different TileLayer when zoomed far in.

Prefer max_native_zoom for setting the maximum zoom level supported by the tile source.

Typically set to infinity so that there are tiles always displayed.

Raises:

ValueError – If it is less than 0.0.
 min_native_zoom class-attribute instance-attribute #

min_native_zoom: int = 0
Minimum zoom level supported by the tile source.

Tiles from below this zoom level will not be displayed, instead tiles at this zoom level will be displayed and scaled.

This should usually be 0 (as default), as most tile sources will support zoom levels onwards from this.

Raises:

ValueError – If it is less than 0.0.
 min_zoom class-attribute instance-attribute #

min_zoom: Number = 0.0
The minimum zoom level at which this layer is displayed (inclusive).

Typically 0.0.

Raises:

ValueError – If it is less than 0.0.
 pan_buffer class-attribute instance-attribute #

pan_buffer: int = 1
When loading tiles only visible tiles are loaded by default.

This option increases the loaded tiles by the given number on both axis which can help prevent the user from seeing loading tiles whilst panning. Setting the pan buffer too high can impact performance, typically this is set to 0 or 1.

 subdomains class-attribute instance-attribute #

subdomains: list[str] = field(
    default_factory=lambda: ["a", "b", "c"]
)
List of subdomains used in the URL template.

To use subdomains, add the {s} placeholder to the URL template (url_template and fallback_url)

Note
Subdomains are now usually considered redundant due to the usage of HTTP/2 & HTTP/3 which don't have the same restrictions. Usage of subdomains will also hinder the ability to cache tiles, potentially leading to increased tile requests and costs. Hence, if the server supports HTTP/2 or HTTP/3 (how to check), avoid using subdomains.

Example
If subdomains is set to ["a", "b", "c"] and the url_template is "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", the resulting tile URLs will be:

"https://a.tile.openstreetmap.org/{z}/{x}/{y}.png"
"https://b.tile.openstreetmap.org/{z}/{x}/{y}.png"
"https://c.tile.openstreetmap.org/{z}/{x}/{y}.png"
 tile_bounds class-attribute instance-attribute #

tile_bounds: MapLatitudeLongitudeBounds | None = None
Defines the bounds of the map. Only tiles that fall within these bounds will be loaded.

 tile_size class-attribute instance-attribute #

tile_size: int = 256
The size in pixels of each tile image. Should be a positive power of 2.

Note
Some tile servers will use 512x512px tiles instead of 256x256px, such as Mapbox. Using these larger tiles can help reduce tile requests, and when ombined with Retina Mode, it can give the same resolution.

To use these tiles, set tile_size to the actual dimensions of the tiles (otherwise they will appear to small), such as 512. Also set zoom_offset to the result of -((d/256) - 1) - ie. -1 for x512px tiles (otherwise they will appear at the wrong geographical locations).

The {d} placeholder may also be used in the URL template (url_template and fallback_url) to pass through the value of tile_size.

Raises:

ValueError – If it is less than 0.0.
 url_template instance-attribute #

url_template: str
The URL template is a string that contains placeholders, which, when filled in, create a URL/URI to a specific tile.

Provider Examples: https://wiki.openstreetmap.org/wiki/Raster_tile_providers

Placeholders
As well as the standard XYZ placeholders in the template, the following placeholders may also be used:

{s}: see subdomains property
{r}: retina scaling factor (2 or 1)
{d}: reflects the tile_size property
Additional placeholders can also be added freely to the template, and are filled in with the specified values in additional_options. This can be used to easier add switchable styles or access tokens.

Compliance with tile server requirements
It is your own responsibility to comply with any appropriate restrictions and requirements set by your chosen tile server/provider. Always read their terms of service. Failure to do so may lead to any punishment, at the tile server's discretion.

Production apps should be extremely cautious about using this tile server; other projects, libraries, and packages suggesting that OpenStreetMap provides free-to-use map tiles are incorrect.

Case Example: OpenStreetMap (direct)

OpenStreetMap (OSM) is one of the most popular sources for map tiles and data. Their data is free for everyone to use (under ODbL), but their public tile server is not free for everyone to use. It is without cost (for users), but, "without cost" ≠ "without restriction" ≠ "open". Due to excessive usage, the OSM Foundation (running OSM as a not-for-profit) has implemented some measures to prevent abuse and ensure the sustainability of their service.

For example: on non-web platforms (ex: desktop), they require a proper User-Agent header to be set. See the user_agent_package_name property for details and recommended best practices. This does not apply to the web platform, because you cannot set a User-Agent header different to what is provided by the browser.

Read more on their tile usage policy here.

 user_agent_package_name class-attribute instance-attribute #

user_agent_package_name: str = 'unknown'
The package name of the user agent to use when fetching tiles from the tile server.

This is used to identify your app to the tile server, and is important for compliance with tile server usage policies.

OSM best practice recommendations
OpenStreetMap (OSM) recommends the following:

Use a clear, unique User-Agent string that names your app and optionally includes a contact URL or email.
Good Example: MyTownMaps/1.4 (+https://example.org; contact: maps@example.org)
Bad Example: com.example.app
For web apps, the browsers will use the browser’s default User-Agent header.
Do not use a library default User-Agent, and never impersonate another app or a browser.
If your platform automatically sets an X-Requested-With header with an app ID, that is acceptable, but a proper User-Agent is still recommended.
Referer (web only): Browsers are expected to send a valid Referer header. Native apps usually do not have a referer, this is ok.
 wms_configuration class-attribute instance-attribute #

wms_configuration: WMSTileLayerConfiguration | None = None
The configuration for WMS tile servers.

 zoom_offset class-attribute instance-attribute #

zoom_offset: Number = 0.0
The zoom number used in tile URLs will be offset with this value.

Raises:

ValueError – If it is less than 0.0.
 zoom_reverse class-attribute instance-attribute #

zoom_reverse: bool = False
Whether the zoom number used in tile URLs will be reversed (max_zoom - zoom instead of zoom).

Events#
 on_image_error class-attribute instance-attribute #

on_image_error: ControlEventHandler[TileLayer] | None = None
Fires if an error occurs when fetching the tiles.

Event handler argument data property contains information about the error.





MarkerLayer
Inherits: MapLayer

A layer to display Markers.

Properties

alignment(Alignment | None) – The alignment of each marker relative to its normal center at
markers(list[Marker]) – A list of Markers to display.
rotate(bool) – Whether to counter-rotate markers to the map's rotation,
Properties#
 alignment class-attribute instance-attribute #

alignment: Alignment | None = field(
    default_factory=lambda: CENTER
)
The alignment of each marker relative to its normal center at Marker.coordinates.

 markers instance-attribute #

markers: list[Marker]
A list of Markers to display.

 rotate class-attribute instance-attribute #

rotate: bool = False
Whether to counter-rotate markers to the map's rotation, to keep a fixed orientation.





CircleLayer
Inherits: MapLayer

A layer to display CircleMarkers.

Properties

circles(list[CircleMarker]) – A list of CircleMarkers to display.
Properties#
 circles instance-attribute #

circles: list[CircleMarker]
A list of CircleMarkers to display.




PolygonLayer
Inherits: MapLayer

A layer to display PolygonMarkers.

Properties

draw_labels_last(bool) – Whether to draw labels last and thus over all the polygons.
polygon_culling(bool) – Whether to cull polygons and polygon sections that are outside of the viewport.
polygon_labels(bool) – Whether to draw per-polygon labels.
polygons(list[PolygonMarker]) – A list of PolygonMarkers to display.
simplification_tolerance(Number) – The tolerance value used to simplify polygon outlines before rendering.
use_alternative_rendering(bool) – Whether to use an alternative rendering pathway to draw polygons onto the
Properties#
 draw_labels_last class-attribute instance-attribute #

draw_labels_last: bool = False
Whether to draw labels last and thus over all the polygons.

 polygon_culling class-attribute instance-attribute #

polygon_culling: bool = True
Whether to cull polygons and polygon sections that are outside of the viewport.

 polygon_labels class-attribute instance-attribute #

polygon_labels: bool = True
Whether to draw per-polygon labels.

 polygons instance-attribute #

polygons: list[PolygonMarker]
A list of PolygonMarkers to display.

 simplification_tolerance class-attribute instance-attribute #

simplification_tolerance: Number = 0.3
The tolerance value used to simplify polygon outlines before rendering.

Higher values will result in polygons with fewer points, which can improve rendering performance at the cost of reduced geometric accuracy. Lower values preserve more detail but may decrease performance, especially with complex polygons.

Set to 0 to disable simplification.

 use_alternative_rendering class-attribute instance-attribute #

use_alternative_rendering: bool = False
Whether to use an alternative rendering pathway to draw polygons onto the underlying Canvas, which can be more performant in 'some' circumstances.

This will not always improve performance, and there are other important considerations before enabling it. It is intended for use when prior profiling indicates more performance is required after other methods are already in use. For example, it may worsen performance when there are a huge number of polygons to triangulate - and so this is best used in conjunction with simplification, not as a replacement.




PolylineLayer
Inherits: MapLayer

A layer to display PolylineMarkers.

Properties

culling_margin(Number) – Acceptable extent outside of viewport before culling polyline segments.
min_hittable_radius(Number) – The minimum radius of the hittable area around each polyline in logical pixels.
polylines(list[PolylineMarker]) – List of PolylineMarkers to be drawn.
simplification_tolerance(Number) – The tolerance (in map units) used to simplify polylines for rendering.
Properties#
 culling_margin class-attribute instance-attribute #

culling_margin: Number = 10.0
Acceptable extent outside of viewport before culling polyline segments.

 min_hittable_radius class-attribute instance-attribute #

min_hittable_radius: Number = 10.0
The minimum radius of the hittable area around each polyline in logical pixels.

The entire visible area is always hittable, but if the visible area is smaller than this, then this will be the hittable area.

 polylines instance-attribute #

polylines: list[PolylineMarker]
List of PolylineMarkers to be drawn.

 simplification_tolerance class-attribute instance-attribute #

simplification_tolerance: Number = 0.3
The tolerance (in map units) used to simplify polylines for rendering.

Higher values result in more aggressive simplification, which can improve performance but may reduce the accuracy of the displayed polyline.