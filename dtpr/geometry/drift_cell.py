# Class definition of a Drift Cell.
#
# parent: layer in which the cell is ensembled
#
# idx: identifier along the X axis -- from 1 to nDriftCells
#          _________________________
#         |                         |
#         |                         |
#  1.3 cm |                         |
#         |                         |
#         |_________________________|
#         <------- 4.2 cm --------->


import numpy as np
from dtpr.geometry.dt_geometry import DTGEOMETRY


class DriftCell(object):
    """
    Class representing a Drift Cell.

    Attributes
    ----------
    id : int
        Identifier of the drift cell.
    local_center : tuple
        Local center coordinates of the drift cell.
    global_center : tuple
        Global center coordinates of the drift cell.
    driftTime : float
        Drift time of the drift cell.
    """

    # class variables
    _height = float(DTGEOMETRY.root.find(".//Topology//cellHeight").text)
    _width = float(DTGEOMETRY.root.find(".//Topology//cellWidth").text)
    _length = float(DTGEOMETRY.root.find(".//Topology//cellLength").text)

    def __init__(self, id=-1, parent=None):
        """
        Constructor for DriftCell.

        :param id: Identifier of the drift cell (default is -1).
        :type id: int, optional
        """
        self.parent = parent
        self.id = id
        self.local_center = (0, 0, 0)
        self.global_center = (0, 0, 0)
        self._driftTime = 0

    # == Getters ==
    @property
    def id(self):
        """
        Identifier of the drift cell.

        :return: Identifier of the drift cell.
        :rtype: int
        """
        return self._id

    @property
    def width(self):
        """
        Width of the drift cell.

        :return: Width of the drift cell.
        :rtype: float
        """
        return self._width

    @property
    def height(self):
        """
        Height of the drift cell.

        :return: Height of the drift cell.
        :rtype: float
        """
        return self._height

    @property
    def length(self):
        """
        Length of the drift cell.

        :return: Length of the drift cell.
        :rtype: float
        """
        return self._length

    @property
    def local_center(self):
        """
        Local center coordinates of the drift cell.

        :return: Local center coordinates (x, y, z).
        :rtype: tuple
        """
        return self._x_local, self._y_local, self._z_local

    @property
    def global_center(self):
        """
        Global center coordinates of the drift cell.

        :return: Global center coordinates (x, y, z).
        :rtype: tuple
        """
        return self._x_global, self._y_global, self._z_global

    @property
    def local_position_at_min(self):
        """
        Local position at the minimum coordinates of the drift cell.

        :return: Local position at minimum coordinates (x, y, z).
        :rtype: tuple
        """
        x = self._x_local - self._width / 2
        y = self._y_local - self._height / 2
        z = self._z_local - self._length / 2
        return x, y, z

    @property
    def global_position_at_min(self):
        """
        Global position at the minimum coordinates of the drift cell.

        :return: Global position at minimum coordinates (x, y, z).
        :rtype: tuple
        """
        x = self._x_global - self._width / 2
        y = self._y_global - self._height / 2
        z = self._z_global - self._length / 2
        return x, y, z

    @property
    def driftTime(self):
        """
        Drift time of the drift cell.

        :return: Drift time.
        :rtype: float
        """
        return self._driftTime

    # == Setters ==
    @id.setter
    def id(self, value):
        """
        Set the identifier of the drift cell.

        :param value: Identifier of the drift cell.
        :type value: int
        """
        self._id = value

    @width.setter
    def width(cls, value):
        """
        Set the width of the drift cell.

        :param value: Width of the drift cell.
        :type value: float
        """
        cls._width = value

    @height.setter
    def height(cls, value):
        """
        Set the height of the drift cell.

        :param value: Height of the drift cell.
        :type value: float
        """
        cls.height = value

    @length.setter
    def length(cls, value):
        """
        Set the length of the drift cell.

        :param value: Length of the drift cell.
        :type value: float
        """
        cls._length = value

    @local_center.setter
    def local_center(self, position):
        """
        Set the local center coordinates of the drift cell.

        :param position: Local center coordinates (x, y, z).
        :type position: tuple
        """
        self._x_local, self._y_local, self._z_local = position

    @global_center.setter
    def global_center(self, position):
        """
        Set the global center coordinates of the drift cell.

        :param position: Global center coordinates (x, y, z).
        :type position: tuple
        """
        self._x_global, self._y_global, self._z_global = position

    @driftTime.setter
    def driftTime(self, time):
        """
        Set the drift time of the drift cell.

        :param time: Drift time.
        :type time: float
        """
        self._driftTime = time