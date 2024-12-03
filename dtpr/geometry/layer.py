from dtpr.geometry.drift_cell import DriftCell
from dtpr.geometry.dt_geometry import DTGeometry, DTGEOMETRY


class Layer(object):
    """
    Class representing a Layer.

    Attributes
    ----------
    id : int
        Identifier of the layer.
    number : int
        Number of the layer.
    local_center : tuple
        Local center coordinates of the layer.
    global_center : tuple
        Global center coordinates of the layer.
    cells : list
        List of drift cells in the layer.
    """

    def __init__(self, rawId, parent=None):
        """
        Constructor

        :param rawId: Raw identifier of the layer.
        :type rawId: int
        """
        self.parent = parent
        self.id = rawId
        self._xml_info = DTGEOMETRY.get(rawId=rawId)

        self.number = int(DTGEOMETRY.get("layerNumber", rawId=rawId))
        self._DriftCells = []

        self._first_cell_id = int(DTGEOMETRY.get(".//Channels//first", rawId=rawId))
        self._last_cell_id = int(DTGEOMETRY.get(".//Channels//last", rawId=rawId))

        self.local_center = DTGEOMETRY.get("LocalPosition", rawId=rawId)
        self.global_center = DTGEOMETRY.get("GlobalPosition", rawId=rawId)

        self._build_layer()

    @property
    def id(self):
        """
        Identifier of the layer.

        :return: Identifier of the layer.
        :rtype: int
        """
        return self._id

    @property
    def number(self):
        """
        Number of the layer.

        :return: Number of the layer.
        :rtype: int
        """
        return self._number

    @property
    def local_center(self):
        """
        Local center coordinates of the layer.

        :return: Local center coordinates (x, y, z).
        :rtype: tuple
        """
        return self._x_local, self._y_local, self._z_local

    @property
    def global_center(self):
        """
        Global center coordinates of the layer.

        :return: Global center coordinates (x, y, z).
        :rtype: tuple
        """
        return self._x_global, self._y_global, self._z_global

    @property
    def cells(self):
        """
        Get all the layer's cells.

        :return: List of drift cells in the layer.
        :rtype: list
        """
        return self._DriftCells

    def cell(self, cell_id):
        """
        Get a layer cell by its id.

        :param cell_id: Identifier of the cell.
        :type cell_id: int
        :return: Drift cell with the specified id.
        :rtype: DriftCell
        :raises ValueError: If the cell_id is invalid.
        """
        if cell_id < self._first_cell_id or cell_id > self._last_cell_id:
            raise ValueError(f"Invalid cell id: {cell_id}")
        return self.cells[
            cell_id - self._first_cell_id
        ]  # to match the cell id with the list index

    @id.setter
    def id(self, id):
        """
        Set the identifier of the layer.

        :param id: Identifier of the layer.
        :type id: int
        """
        self._id = id

    @number.setter
    def number(self, number):
        """
        Set the number of the layer.

        :param number: Number of the layer.
        :type number: int
        :raises ValueError: If the number is not between 1 and 4.
        """
        if number < 1 or number > 4:
            raise ValueError("Layer number must be between 1 and 4")
        self._number = number

    @local_center.setter
    def local_center(self, position):
        """
        Set the local center coordinates of the layer.

        :param position: Local center coordinates (x, y, z).
        :type position: tuple
        """
        self._x_local, self._y_local, self._z_local = self.__correct_cords(*position)

    @global_center.setter
    def global_center(self, position):
        """
        Set the global center coordinates of the layer.

        :param position: Global center coordinates (x, y, z).
        :type position: tuple
        """
        self._x_global, self._y_global, self._z_global = self.__correct_cords(*position)

    def add_cell(self, cell):
        """
        Add a new cell to the layer.

        :param cell: Drift cell to be added.
        :type cell: DriftCell
        """
        self.cells.append(cell)

    def __correct_cords(self, x, y, z):
        """
        Correct the coordinates of the layer. Bear in mind that the station reference
        frame is rotated pi/2 with respect to the CMS frame depending on the super layer number:

        if L lives in SL == 1 or 3:
            CMS -> x: right, y: up, z: forward, SuperLayer -> x: right, y: forward, z: down

        if L lives in SL == 2:
            CMS -> x: right, y: up, z: forward, SuperLayer -> x: backward, y: right, z: down

        :param x: x-coordinate.
        :type x: float
        :param y: y-coordinate.
        :type y: float
        :param z: z-coordinate.
        :type z: float
        :return: Corrected coordinates (x, y, z).
        :rtype: tuple
        """
        if self.parent is not None:
            if self.parent.number == 1 or self.parent.number == 3:
                return x, -1 * z, y
            else:
                return -1 * x, y, -1 * z
        else:
            return x, y, z

    def _build_layer(self):
        """
        Ensemble a DT layer.
        """

        # _firs_wire_local = float(DTGEOMETRY.get( ".//WirePositions//FirstWire" , rawId=self.id))
        _firs_wire_local = float(
            DTGEOMETRY.get(".//WirePositions//FirstWire_ref_to_chamber", rawId=self.id)
        )

        _, y_local, z_local = self.local_center
        x_global, y_global, z_global = self.global_center  # station global center

        for i, n_cell in enumerate(range(self._first_cell_id, self._last_cell_id + 1)):
            cell = DriftCell(id=n_cell, parent=self)
            # positioned correctly
            cell.local_center = (
                _firs_wire_local + (i - 1) * cell.width,
                y_local,
                z_local,
            )
            cell.global_center = (
                (x_global + _firs_wire_local) + (i - 1) * cell.width,
                y_global,
                z_global,
            )

            self.add_cell(cell)


if __name__ == "__main__":
    layer = Layer(589603840)
    print(layer.cells)
