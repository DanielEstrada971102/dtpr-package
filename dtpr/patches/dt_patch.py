""" 
Implementation of the DT plotter class

Used for plotting hits, segments, and generated muons for a given event.
It is not recommended to run this code for multiple events, since it is
very disk consuming (plots are quite full of stuff).

"""

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from matplotlib.collections import PatchCollection
from matplotlib.colors import Normalize
from mplhep import style
from pandas import DataFrame
from dtpr.geometry.station import Station
from math import atan2, degrees

plt.style.use(style.CMS)
cmap = plt.get_cmap("viridis").copy()
cmap.set_under("w")
norm = Normalize(vmin=299, vmax=1000, clip=False)


class dtpatch(object):
    def __init__(self, MB: Station, fig, axes, dt_info=None, local=True):
        self.current_DT = MB
        self.fig = fig
        self.axes = axes

        self.local = local

        if not self.local:  # if global, compute the angle to rotate the patches
            nx, ny, nz = MB.direction
            self.angle = degrees(atan2(ny, nx)) + 90  # ang_incline = ang_normal_refx + 90

        #draw Sl bounds
        frames = self.draw_dt_bounds()
        self.axes.add_collection(PatchCollection(frames, match_original=True))

        if dt_info is not None:
            self.set_cells_times(dt_info)

        self.cell_patches, cell_times = self._make_dt_patches()

        self.collection = PatchCollection(
            self.cell_patches,
            cmap=cmap,
            norm=norm,
            edgecolors="k",
            linewidth=.5,
        )
        self.collection.set_array(cell_times)

        self.axes.add_collection(self.collection)

        # add colorbar
        # self.fig.colorbar(self.collection, label="time [ns]")

    def draw_dt_bounds(self):
        colors = {1 : "lightblue", 2 : "orange", 3 : "green"}
        frames = []
        for super_layer in self.current_DT.super_layers:
            width, height, length = super_layer.bounds
            x, y, z = (
                super_layer.local_center
                if self.local
                else super_layer.global_center
            )

            x_min, y_min = x - (width * 0.5), y - (height * 0.5)
            frame = Rectangle(
                (x_min-.25, y_min),
                width + 0.5,
                height,
                edgecolor="black",
                linewidth=1,
                facecolor=colors[super_layer.number],
                alpha=0.3,
            )
            if not self.local:  # if global, rotate the frame
                x, y, z = super_layer.global_center  # rotation_point

                frame.rotation_point = (x, y)
                frame.set_angle(self.angle)
            frames.append(frame)
        return frames

    def _make_dt_patches(self):
        MB = self.current_DT
        cell_patches = []
        cell_times = []

        for super_layer in MB.super_layers:
            for layer in super_layer.layers:
                for cell in layer.cells:
                    xmin, ymin, zmin = (
                        cell.local_position_at_min
                        if self.local
                        else cell.global_position_at_min
                    )
                    width = cell.width
                    height = cell.height
                    length = cell.length
                    drift_time = cell.driftTime

                    # create cell patch
                    cell_patch = Rectangle(
                        (xmin, ymin),
                        width, # length if super_layer.number != 2 else width,
                        height,
                    )

                    if not self.local:  # if global, rotate the patch
                        x, y, z = layer.global_center  # rotation_point

                        cell_patch.rotation_point = (x, y)
                        cell_patch.set_angle(self.angle)

                    cell_patches.append(cell_patch)
                    cell_times.append(drift_time) # if super_layer.number == 2 else 0)

        return cell_patches, cell_times

    def set_cells_times(self, DT_info):
        info_iter = (
            DataFrame(DT_info) if isinstance(DT_info, (dict, list)) else DT_info
        ).itertuples(index=False)
        for info in info_iter:
            sl, l, w, time = info.sl, info.l, info.w, info.time
            try:
                self.current_DT.super_layer(sl).layer(l).cell(w).driftTime = time
            except:
                pass
        return
