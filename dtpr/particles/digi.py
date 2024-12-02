from dtpr.utils.functions import color_msg


class Digi(object):
    __slots__ = ["index", "wh", "sc", "st", "sl", "w", "l", "time", "BX"]

    def __init__(
        self, idigi, ev=None, wh=None, sc=None, st=None, sl=None, w=None, l=None, time=None, bx=None
    ):
        """
        Initialize a Digi instance.

        You can either pass a root event entry from the ntuple or provide each attribute individually.

        :param idigi: The index of the digi.
        :type idigi: int
        :param ev: The root event object containing event data. If provided, other attributes are ignored.
        :param wh: The wheel number.
        :type wh: int, optional
        :param sc: The sector number.
        :type sc: int, optional
        :param st: The station number.
        :type st: int, optional
        :param sl: The superlayer number.
        :type sl: int, optional
        :param w: The wire number.
        :type w: int, optional
        :param l: The layer number.
        :type l: int, optional
        :param time: The time of the digi.
        :type time: int, optional
        :param bx: The bunch crossing number.
        :type bx: int, optional
        """
        self.index = idigi
        if ev is not None:
            self.wh = ev.digi_wheel[idigi]
            self.sc = ev.digi_sector[idigi]
            self.st = ev.digi_station[idigi]
            self.sl = int(ev.digi_superLayer[idigi])
            self.w = int(ev.digi_wire[idigi])
            self.l = int(ev.digi_layer[idigi])
            self.time = int(ev.digi_time[idigi])
            self.BX = self.time // 25  # each BX is at 25ns
        else:
            self.wh = wh
            self.sc = sc
            self.st = st
            self.sl = sl
            self.w = w
            self.l = l
            self.time = time
            self.BX = bx

    def to_dict(self):
        """
        Convert the Digi instance to a dictionary. Useful to use pandas.DataFrame's.

        :returns: A dictionary representation of the Digi instance.
        :rtype: dict
        """
        return {attr: getattr(self, attr) for attr in self.__slots__}

    def __str__(self, indentLevel=0):
        """
        Generate a string representation of the Digi instance.

        :param indentLevel: The indentation level for the summary.
        :type indentLevel: int
        :returns: The digi summary.
        :rtype: str
        """
        summary = [
            color_msg(
                f"------ Digi {self.index} info ------",
                color="yellow",
                indentLevel=indentLevel,
                return_str=True,
            )
        ]

        summary.append(
            color_msg(
                ", ".join(
                    [
                        f"{attr.capitalize()}: {getattr(self, attr)}"
                        for attr in self.__slots__
                        if attr != "index"
                    ]
                ),
                indentLevel=indentLevel + 1,
                return_str=True,
            )
        )
        return "\n".join(summary)


if __name__ == "__main__":
    digi = Digi(0, wh=1, sc=1, st=1, sl=1, w=1, l=1, time=25, bx=1)
    print(digi.to_dict())
