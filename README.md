## Note
Please use version from GRASS GIS Addons repository, you can install it with:
    
    g.extension r.patch.smooth

This repository will become eventually obsolete.

# r.patch.smooth
GRASS GIS module r.patch.smooth fuses rasters representing elevation together by patching them and smoothing
values along edges using either fixed or spatially variable overlap width.
Spatially variable overlap width is given by the difference
along the edge between the two rasters. Higher difference results in larger overlap width
to smooth the transition.

r.patch.smooth can be used, for example, for updating older, lower resolution
DEM (<b>input_b</b>) with newer, higher resolution DEM (<b>input_a</b>).
Note that both DEMs must be aligned and have the same resolution.
Smoothing uses weighted averaging on the overlap of the rasters.
r.patch.smooth supports 2 types of smoothing. The default one is
simpler and uses fixed overlap width defined in <b>smooth_dist</b>.
Since the differences along the seam line can vary,
the second option uses spatially variable overlap width and can be activated with flag <b>-s</b>.
The width is then computed based on the elevation differences along the edge and
transition angle <b>transition_angle</b> controlling the steepness of the transition.
If option <b>overlap</b> is specified, a map representing the spatially variable overlap
is created and can be used for inspecting the fusion results.



<img src="r_patch_smooth_overview.png" width=600 border=0><br>
Difference between fixed overlap width and spatially variable overlap.

<p>
For spatially variable overlap, options <b>parallel_smoothing</b>
and <b>difference_reach</b> can be specified.
Option <b>parallel_smoothing</b> smoothes the overlap zone in direction
parallel to the edge.
Option <b>difference_reach</b> enables to increase the sensitivity to higher
differences on the edges by taking maximum difference values in the cells
close to edges.

<img src="r_patch_smooth_parallel_smoothing.png" border=0><br>
Effect of <b>parallel_smoothing</b> option shown on overlap zone (created by specifying <b>overlap</b> option).
Image A shows result with value 3 and B with value 9.


Option <b>blend_mask</b> (experimental) can be used to specify which edges of
the input_a DEM should be excluded from the blending. This is useful when
DEMs A and B have identical edges (on the coast, for example) and we want
to preserve only A (not blend it with B along the coast).
The <b>blend_mask</b> raster can be created by digitizing area approximately around the excluded edges,
so that the edge of DEM A is inside the areas and the rest are NULLs.
This option requires more testing.

## Installation
Module r.patch.smooth must be run from GRASS GIS 7 environment. Within GRASS session, run in command line:

    g.extension r.patch.smooth url=https://github.com/petrasovaa/r.patch.smooth
