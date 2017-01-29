#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
##############################################################################
#
# MODULE:       r.patch.smooth
#
# AUTHOR(S):    Anna Petrasova (kratochanna gmail.com)
#
# PURPOSE:      Patch raster and smooth along edges
#
# COPYRIGHT:    (C) 2015 by the GRASS Development Team
#
#               This program is free software under the GNU General Public
#               License (>=v2). Read the file COPYING that comes with GRASS
#               for details.
#
##############################################################################

#%module
#% description: Module for patching rasters with smoothing along edges
#% keyword: raster
#% keyword: patch
#%end
#%option G_OPT_R_INPUT
#% key: input_a
#% label: Name for input raster map A
#%end
#%option G_OPT_R_INPUT
#% key: input_b
#% label: Name for input raster map B
#%end
#%option G_OPT_R_OUTPUT
#%end
#%option G_OPT_R_OUTPUT
#% key: overlap
#% label: Name for raster map of spatially variable overlap
#% required: no
#%end
#%option
#% type: double
#% key: smooth_dist
#% description: Smoothing distance in map units
#% required: no
#% guisection: Settings
#%end
#%option
#% type: double
#% key: transition_angle
#% label: Angle of transition for spatially variable overlap
#% description: Recommended values between 1 and 5 degrees
#% required: no
#% guisection: Settings
#%end
#%flag
#% key: s
#% description: Use spatially variable overlap
#% guisection: Settings
#%end
#%rules
#% collective: -s,transition_angle
#% exclusive: transition_angle,smooth_dist
#% required: -s,smooth_dist
#% excludes: smooth_dist,overlap
#%end

import os
import sys
import atexit

import grass.script as gscript


TMP = []


def cleanup():
    gscript.run_command('g.remove', flags='f', type=['raster', 'vector'], name=TMP, quiet=True)


def main():
    input_A = options['input_a']
    input_B = options['input_b']
    output = options['output']
    overlap = options['overlap']
    smooth_dist = options['smooth_dist']
    angle = options['transition_angle']
    simple = not flags['s']

    postfix = str(os.getpid())
    tmp_absdiff = "tmp_absdiff_" + postfix
    tmp_absdiff_smooth = "tmp_absdiff_smooth" + postfix
    tmp_grow = "tmp_grow" + postfix
    tmp_diff_overlap_1px = "tmp_diff_overlap_1px" + postfix
    tmp_value = "tmp_value" + postfix
    tmp_value_smooth = "tmp_value_smooth" + postfix
    tmp_stretch_dist = "tmp_stretch_dist" + postfix
    tmp_overlap = "tmp_overlap" + postfix
    TMP.extend([tmp_absdiff, tmp_absdiff_smooth, tmp_grow, tmp_diff_overlap_1px, tmp_value, tmp_value_smooth, tmp_stretch_dist, tmp_overlap])

    gscript.run_command('r.grow.distance', flags='n', input=input_A, distance=tmp_grow)
    if simple:
        gscript.mapcalc("{out} = if({grow} > {smooth}, {A}, if({grow} == 0, {B},"
                        "if (isnull({B}) && ! isnull({A}), {A},"
                        "(1 - {grow}/{smooth}) * {B} + ({grow}/{smooth} * {A}))))".format(out=output, grow=tmp_grow,
                                                                                          smooth=smooth_dist, A=input_A, B=input_B))
        return
    # smooth values of closest difference
    # should this be parameter
    smooth_closest_difference_size = 15

    # difference
    gscript.mapcalc("{new} = abs({A} - {B})".format(new=tmp_absdiff, A=input_A, B=input_B))

    # take maximum difference from near cells
    gscript.run_command('r.neighbors', flags='c', input=tmp_absdiff, output=tmp_absdiff_smooth, method='maximum', size=5)

    # closest value of difference
    gscript.mapcalc("{new} = if ({dist} > 0 && {dist} <= 1.5*nsres(), {diff}, null())".format(new=tmp_diff_overlap_1px,
                                                                                              dist=tmp_grow, diff=tmp_absdiff_smooth))
    # closest value of difference
    gscript.run_command('r.grow.distance', input=tmp_diff_overlap_1px, value=tmp_value)

    # smooth closest value
    gscript.run_command('r.neighbors', flags='c', input=tmp_value, output=tmp_value_smooth, method='average',
                        size=smooth_closest_difference_size)

    # stretch 10cm height difference per 5 meters
    gscript.mapcalc("{stretch} = {value}/tan({alpha})".format(stretch=tmp_stretch_dist, value=tmp_value_smooth, alpha=angle))

    # spatially variable overlap width s
    gscript.mapcalc("{s} = if (isnull({B}) && ! isnull({A}), 1, {dist} / {stretch})".format(s=tmp_overlap, B=input_B,
                                                                                            A=input_A, dist=tmp_grow, stretch=tmp_stretch_dist))
    # fusion
    gscript.mapcalc("{fused} = if({s} >= 1, {A} , if({s} == 0,  {B},  (1 - {s}) * {B} +  {A} * {s}))".format(fused=output, s=tmp_overlap,
                                                                                                             B=input_B, A=input_A))
    # visualize overlap
    if overlap:
        gscript.mapcalc("{s_trim} = if ({s}>=1, null(), if({s}<=0, null(), {s}))".format(s_trim=overlap, s=tmp_overlap))


if __name__ == "__main__":
    options, flags = gscript.parser()
    atexit.register(cleanup)
    sys.exit(main())
