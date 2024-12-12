""" 
Implementation of the DT plotter class

Used for plotting hits, segments, and generated muons for a given event.
It is not recommended to run this code for multiple events, since it is
very disk consuming (plots are quite full of stuff).

"""

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
from matplotlib.colors import Normalize
from mplhep import style
from dtpr.geometry.station import Station
from math import atan2, degrees

plt.style.use(style.CMS)
cmap = plt.get_cmap("viridis").copy()
cmap.set_under("none")
norm = Normalize(vmin=299, vmax=1000, clip=False)


class DTPatch():
    def __init__(self, station: Station, fig, axes, local=True, faceview="phi"):
        self.current_DT = station
        self.axes = axes
        self.view = faceview
        self.bounds_collections = PatchCollection([])
        self.cells_collection = PatchCollection([])

        self.local = local

        if not self.local:  # if global, compute the angle to rotate the patches
            nx, ny, _ = station.direction
            self.angle = degrees(atan2(ny, nx)) + 90  # ang_incline = ang_normal_refx + 90

        #draw Sl bounds
        self._draw_bounds()

        # self.axes.add_collection(PatchCollection(frames, match_original=True))

        self._draw_cells()

        # add collections to axes
        axes.add_collection(self.bounds_collections)
        axes.add_collection(self.cells_collection)

        # # add colorbar
        # if not any(hasattr(ax, 'colorbar') for ax in plt.gcf().get_axes()):
        #     fig.colorbar(self.cells_collection, label="time [ns]")

    def _draw_bounds(self):
        frames = []
        # first draw the DT frame
        frames.append(self._create_frame(self.current_DT))

        # then draw the superlayer frames
        for super_layer in self.current_DT.super_layers:
            frames.append(self._create_frame(super_layer))

        self.bounds_collections.set_paths(frames)
        self.bounds_collections.set_facecolor(["lightgray", "lightyellow", "lightpink", "lightblue"])
        self.bounds_collections.set_edgecolor("k")
        self.bounds_collections.set_linewidth(1)
        self.bounds_collections.set_alpha(0.3)


    def _create_frame(self, obj):
        width, height, length = obj.bounds
        x_min, y_min, z_min = (
            obj.local_position_at_min if self.local
            else obj.global_position_at_min
        )
        x, y, z = (
            obj.local_center
            if self.local
            else obj.global_center
        )

        if self.view == "eta":
            if getattr(obj, "number", None) != 2:
                width = length
                x = z
                x_min = z_min

        elif self.view == "phi":
            if hasattr(obj, "number") and obj.number == 2:
                width = length
                if self.local:
                    x = z
                    x_min = z_min
                else:
                    x_min = x - (length / 2)

        frame = Rectangle(
            (x_min, y_min),
            width,
            height,
        )

        if not self.local:  # if global, rotate the frame
            frame.rotation_point = (x, y)
            frame.set_angle(self.angle)

        return frame

    def _draw_cells(self):
        cells = []
        times = []
        for super_layer in self.current_DT.super_layers:
            if self.view=="phi" and super_layer.number == 2: continue # skip superlayer 2
            elif self.view=="eta" and super_layer.number != 2: continue # skip superlayer 1 and 3
            for layer in super_layer.layers:
                for cell in layer.cells:
                    xmin, ymin, _ = (
                        cell.local_position_at_min if self.local
                        else cell.global_position_at_min
                    )
                    width = cell.width
                    height = cell.height
                    time = cell.driftTime

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

                    cells.append(cell_patch),
                    times.append(time)

        self.cells_collection.set_paths(cells)
        self.cells_collection.set_array(times)
        self.cells_collection.set_cmap(cmap)
        self.cells_collection.set_norm(norm)
        self.cells_collection.set_edgecolor("k")
        self.cells_collection.set_linewidth(.1)

# extender create_frame to cells...