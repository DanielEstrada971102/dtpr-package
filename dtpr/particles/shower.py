from dtpr.utils.functions import color_msg


class Shower(object):
    __slots__ = [
        "index",
        "wh",
        "sc",
        "st",
        "BX",
        "nDigis",
        "avg_pos",
        "avg_time",
        "_others",
    ]

    def __init__(
        self,
        iShower,
        ev=None,
        wh=-2,
        sc=1,
        st=1,
        BX=0,
        nDigis=0,
        avg_pos=0,
        avg_time=0,
    ):
        """
        Initialize a Shower instance.

        A Shower can be initialized either by providing the root event entry (`ev`) or by passing each parameter individually.

        :param iShower: The index of the shower.
        :type iShower: int
        :param ev: The root event object containing event data.
        :param wh: The wheel number.
        :type wh: int, optional
        :param sc: The sector number.
        :type sc: int, optional
        :param st: The station number.
        :type st: int, optional
        :param BX: The bunch crossing number.
        :type BX: int, optional
        :param nDigis: The number of digis.
        :type nDigis: int, optional
        :param avg_pos: The average position.
        :type avg_pos: float, optional
        :param avg_time: The average time.
        :type avg_time: float, optional
        """
        self.index = iShower
        self._others = {}
        if ev is not None:  # constructor with root_event info
            self.wh = ev.ph2Shower_wheel[iShower]
            self.sc = ev.ph2Shower_sector[iShower]
            self.st = ev.ph2Shower_station[iShower]
            self.BX = ev.ph2Shower_BX[iShower]
            self.nDigis = ev.ph2Shower_ndigis[iShower]
            self.avg_pos = ev.ph2Shower_avg_pos[iShower]
            self.avg_time = ev.ph2Shower_avg_time[iShower]

        else:  # constructor with explicit info
            self.wh = wh
            self.sc = sc
            self.st = st
            self.BX = BX
            self.nDigis = nDigis
            self.avg_pos = avg_pos
            self.avg_time = avg_time


    def to_dict(self):
        """
        Convert the Shower instance to a dictionary.

        :return: A dictionary representation of the Shower instance.
        :rtype: dict
        """
        _dict = {attr: getattr(self, attr) for attr in self.__slots__} 
        return {**_dict, **self._others}

    def __str__(self, indentLevel=0):
        """
        Generate a string representation of the Shower instance.

        :param indentLevel: The indentation level for the summary.
        :type indentLevel: int
        :return: The shower summary.
        :rtype: str
        """
        summary = [
            color_msg(
                f"------ Shower {self.index} info ------",
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
    
    def __getattr__(self, name):
        """
        Override __getattr__ to return attributes from the _others dictionary.

        :param name: The name of the attribute.
        :return: The attribute value.
        :raises AttributeError: If the attribute is not found.
        """
        if name in self.__slots__:
            return object.__getattribute__(self, name)
        if name in self._others:
            return self._others[name]
        raise AttributeError(f"'Shower' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        """
        Override __setattr__ to store aditional attributes in the _others dictionary.

        :param name: The name of the attribute.
        :param value: The value to set.
        """
        if name in self.__slots__:
            object.__setattr__(self, name, value)
        else:
            self._others[name] = value
