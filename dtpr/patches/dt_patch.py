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
from pandas import DataFrame
from dtpr.geometry.station import Station
from math import atan2, degrees

plt.style.use(style.CMS)
cmap = plt.get_cmap("viridis").copy()
cmap.set_under("w")
norm = Normalize(vmin=299, vmax=1000, clip=False)


class dtpatch(object):
    def __init__(self, MB: Station, fig, axes, view="phi", dt_info=None, local=True):
        self.current_DT = MB
        self.fig = fig
        self.axes = axes
        self.view = view

        # self.local = True  # local At the moment global is not working
        self.local = local

        self.setup_canvas()

        if dt_info is not None:
            self.set_cells_times(dt_info)

        self.cell_patches, cell_times = self._make_dt_patches()

        collection = PatchCollection(
            self.cell_patches,
            cmap=cmap,
            norm=norm,
            edgecolors="k",
            linewidth=1,
        )
        collection.set_array(cell_times)

        self.axes.add_collection(collection)
        # add circle
        if not self.local:
            axs.add_patch(
                plt.Circle((0, 0), 750, alpha=1, edgecolor="black", facecolor="none")
            )
        # add colorbar
        self.fig.colorbar(collection, label="time [ns]")

    def setup_canvas(self):
        width, height, length = self.current_DT.bounds
        x, y, z = (
            self.current_DT.global_center
            if not self.local
            else self.current_DT.local_center
        )

        # print(f"Setting limits: x = {x}, y = {y}, width = {width}, height = {height}")
        # print("xlims: ", x - (width * 0.5) - 5, x + (width * 0.5) + 5)

        if not self.local or self.view == "phi":
            self.axes.set_xlabel("x[cm]")
            self.axes.set_ylabel("y[cm]")
            self.axes.set_xlim(x - (width * 0.5) - 5, x + (width * 0.5) + 5)
            self.axes.set_ylim(y - (height * 0.5) - 5, y + (height * 0.5) + 5)

        elif self.view == "theta":
            self.axes.set_xlabel("-y[cm]")
            self.axes.set_ylabel("z[cm]")
            self.axes.set_xlim(y - (length * 0.5) - 5, y + (length * 0.5) + 5)
            self.axes.set_ylim(z - (height * 0.5) - 5, z + (height * 0.5) + 5)

        return

    def _make_dt_patches(self):
        MB = self.current_DT
        cell_patches = []
        cell_times = []

        if not self.local:  # if global, compute the angle to rotate the patches
            nx, ny, nz = MB.direction
            angle = degrees(atan2(ny, nx)) + 90  # ang_incline = ang_normal_refx + 90

        for super_layer in MB.super_layers:
            if not self.local or self.view == "phi":
                if super_layer.number == 2:
                    continue  # we are not plotting SL-Theta
            elif self.view == "theta":
                if super_layer.number != 2:
                    continue

            for layer in super_layer.layers:
                for cell in layer.cells:
                    xmin, ymin, _ = (
                        cell.local_position_at_min
                        if self.local
                        else cell.global_position_at_min
                    )  # the global location appears to be wrong, ask pelayo
                    width = cell.width
                    height = cell.height
                    drift_time = cell.driftTime

                    # create cell patch
                    cell_patch = Rectangle(
                        (xmin, ymin),
                        width,
                        height,
                    )

                    if not self.local:  # if global, rotate the patch
                        x, y, _ = layer.global_center  # rotation_point

                        cell_patch.rotation_point = (x, y)
                        cell_patch.set_angle(angle)

                    cell_patches.append(cell_patch)
                    cell_times.append(drift_time)

        return cell_patches, cell_times

    def set_cells_times(self, DT_info):
        info_iter = (
            DataFrame(DT_info) if isinstance(DT_info, (dict, list)) else DT_info
        ).itertuples(index=False)
        for info in info_iter:
            sl, l, w, time = info.sl, info.l, info.w, info.time
            if not self.local or self.view == "phi":
                if sl == 2:
                    continue  # we are not plotting info in SL-Theta
            elif self.view == "theta":
                if sl != 2:
                    continue
            self.current_DT.super_layer(sl).layer(l).cell(w).driftTime = time
        return


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from dtpr.geometry.station import Station

    # local = True
    local = False
    fig, axs = plt.subplots(1, 1, figsize=(60, 50))
    dt_chamber = Station(wheel=-2, sector=12, station=1)
    dt_patch = dtpatch(
        MB=dt_chamber,
        # dt_info=[
        #     {"sl": 1, "l": 1, "w": 1, "time": 300},
        #     {"sl": 1, "l": 1, "w": 2, "time": 400},
        #     {"sl": 1, "l": 2, "w": 1, "time": 500},
        #     {"sl": 1, "l": 2, "w": 2, "time": 600},
        #     {"sl": 2, "l": 1, "w": 1, "time": 700},
        #     {"sl": 2, "l": 1, "w": 2, "time": 800},
        #     {"sl": 2, "l": 2, "w": 1, "time": 900},
        #     {"sl": 3, "l": 1, "w": 1, "time": 700},
        #     {"sl": 3, "l": 1, "w": 2, "time": 800},
        #     {"sl": 3, "l": 2, "w": 1, "time": 900},
        #     {"sl": 3, "l": 2, "w": 2, "time": 1000},
        # ],
        fig=fig,
        axes=axs,
        local=local,
    )

    x, y, _ = dt_chamber.local_center if local else dt_chamber.global_center
    axs.scatter(x, y, color="red", s=10)

    for sl in dt_chamber.super_layers:
        if sl.number == 2:
            continue
        x, y, _ = sl.local_center if local else sl.global_center
        axs.scatter(x, y, color="green", s=10)
        for l in sl.layers:
            x, y, _ = l.local_center if local else l.global_center
            axs.scatter(x, y, color="orange", s=10)
            x_c, y_c, _ = l.cells[0].local_center if local else l.cells[0].global_center
            axs.scatter(x_c, y_c, color="purple", s=10)

    if not local:
        axs.set_xlim(-750, 750)
        axs.set_ylim(-750, 750)

    # fig.savefig("test.svg")
    plt.show()
