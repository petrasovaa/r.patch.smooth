# r.patch.smooth
GRASS GIS module r.patch.smooth fuses rasters representing elevation together by patching them and smoothing
values along edges using either fixed or spatially variable overlap width.
Spatially variable overlap width is given by the difference
along the edge between the two rasters. Higher difference results in larger overlap width
to smooth the transition.

r.patch.smooth can be used, for example, for updating older, lower resolution
DEM (<b>input_b</b>) with newer, higher resolution DEM (<b>input_a</b>).
Smoothing uses weighted averaging on the overlap of the rasters.
r.patch.smooth supports 2 types of smoothing. The default one is
simpler and uses fixed overlap width defined in <b>smooth_dist</b>.
Since the differences along the seam line can vary,
the second option uses spatially variable overlap width and can be activated with flag <b>-s</b>.
The width is then computed based on the elevation differences along the edge and
transition angle <b>transition_angle</b> controlling the steepness of the transition.
If option <b>overlap</b> is specified, a map representing the spatially variable overlap
is created and can be used for inspecting the fusion results.

r.patch.smooth must be run from GRASS GIS 7 environment.
