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
#%option G_OPT_R_INPUTS
#%end
#%option G_OPT_R_OUTPUT
#%end
#%option
#% type: double
#% key: smooth_dist
#% description: Smoothing distance
#% required: yes
#%end

import os
import sys
import atexit

import grass.script as gscript


TMP = []


def cleanup():
    gscript.run_command('g.remove', flags='f', type=['raster', 'vector'], name=TMP)


def main():
    rasters = options['input'].split(',')
    output = options['output']
    smooth = options['smooth_dist']
    if len(rasters) <= 1:
        gscript.fatal(_("At least 2 input rasters required"))

    tmp_grow = "tmp_grow_" + str(os.getpid())
    tmp_out = "tmp_grow_out_" + str(os.getpid())
    tmp_mask = "tmp_mask_" + str(os.getpid())
    TMP.append(tmp_grow)
    TMP.append(tmp_out)
    TMP.append(tmp_mask)
    patch = rasters[0]
    for i in range(len(rasters) - 1):
        gscript.mapcalc("{mask} = if(!isnull({r2}) && !isnull({r1}), null(), {r1})".format(mask=tmp_mask, r1=patch, r2=rasters[i + 1]), overwrite=True)
        gscript.run_command('r.grow.distance', input=tmp_mask, distance=tmp_grow, overwrite=True)
        gscript.mapcalc("{out} = if({grow} > {smooth}, {second}, if({grow} == 0, {first},"
                        "(1 - {grow}/{smooth}) * {first} + ({grow}/{smooth} * {second})))".format(out=tmp_out, grow=tmp_grow,
                            smooth=smooth, first=patch, second=rasters[i + 1]))
        gscript.run_command('g.rename', raster=[tmp_out, output], overwrite=True, quiet=True)
        patch = output

if __name__ == "__main__":
    options, flags = gscript.parser()
    atexit.register(cleanup)
    sys.exit(main())
