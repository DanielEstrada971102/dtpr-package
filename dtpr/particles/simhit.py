from dtpr.utils.functions import color_msg

class SimHit(object):
    __slots__ = ["index", "wh", "sc", "st", "sl", "l", "w", "process_type", "particle_type"] # add more attributes here

    def __init__(
        self,
        isimhit,
        ev=None,
        wh=None,
        sc=None,
        st=None,
        sl=None,
        l=None,
        w=None,
        process_type=None,
        particle_type=None,
    ):
        """
        Initialize a SimHit instance.

        You can either pass a root event entry from the ntuple or provide each attribute individually.

        :param isimhit: The index of the simhit.
        :type isimhit: int
        :param ev: The root event object containing event data. If provided, other attributes are ignored.
        :param wh: The wheel number.
        :type wh: int, optional
        :param sc: The sector number.
        :type sc: int, optional
        :param st: The station number.
        :type st: int, optional
        :param sl: The superlayer number.
        :type sl: int, optional
        :param l: The layer number.
        :type l: int, optional
        :param w: The wire number.
        :type w: int, optional
        :param process_type: The process type of the simhit.
        :type process_type: int, optional
        :param particle_type: The particle type of the simhit.
        :type particle_type: int, optional
        """
        self.index = isimhit
        if ev is not None: # constructor with root event entry info
            self.wh = int(ev.simHit_wheel[isimhit])
            self.sc = int(ev.simHit_sector[isimhit])
            self.st = int(ev.simHit_station[isimhit])
            self.sl = int(ev.simHit_superLayer[isimhit])
            self.l = int(ev.simHit_layer[isimhit])
            self.w = int(ev.simHit_wire[isimhit])
            self.process_type = int(ev.simHit_processType[isimhit])
            self.particle_type = int(ev.simHit_particleType[isimhit])
        else: # constructor with explicit info
            self.wh = wh
            self.sc = sc
            self.st = st
            self.sl = sl
            self.l = l
            self.w = w
            self.process_type = process_type
            self.particle_type = particle_type

    def to_dict(self):
        """
        Convert the SimHit instance to a dictionary.

        :return: A dictionary representation of the SimHit instance.
        :rtype: dict
        """
        return {attr: getattr(self, attr) for attr in self.__slots__}

    def __str__(self, indentLevel=0):
        """
        Generate a string representation of the SimHit instance.

        :param indentLevel: The indentation level for the summary.
        :type indentLevel: int
        :return: The simhit summary.
        :rtype: str
        """
        summary = [
            color_msg(
                f"------ SimHit {self.index} info ------",
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


if __name__ == '__main__':
    # Test the class here
    particle_instance = SimHit(1)

    print(particle_instance)