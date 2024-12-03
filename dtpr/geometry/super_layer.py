from dtpr.geometry.layer import Layer
from dtpr.geometry.dt_geometry import DTGeometry
from dtpr.geometry.dt_geometry import DTGEOMETRY


class SuperLayer(object):
    """
    Class representing a SuperLayer.

    Attributes
    ----------
    id : int
        Identifier of the super layer.
    number : int
        Number of the super layer.
    local_center : tuple
        Local center coordinates of the super layer.
    global_center : tuple
        Global center coordinates of the super layer.
    layers : list
        List of layers in the super layer.
    """

    def __init__(self, rawId, parent=None):
        """
        Constructor

        :param rawId: Raw identifier of the super layer.
        :type rawId: int
        """
        self.parent = parent
        self._layers = []
        self.id = rawId
        self.number = int(DTGEOMETRY.get("superLayerNumber", rawId=rawId))
        self.global_center = DTGEOMETRY.get("GlobalPosition", rawId=rawId)
        self.local_center = DTGEOMETRY.get("LocalPosition", rawId=rawId)

        self._build_super_layer()

    @property
    def id(self):
        """
        Identifier of the super layer.

        :return: Identifier of the super layer.
        :rtype: int
        """
        return self._id

    @property
    def number(self):
        """
        Number of the super layer.

        :return: Number of the super layer.
        :rtype: int
        """
        return self._number

    @property
    def local_center(self):
        """
        Local center coordinates of the super layer.

        :return: Local center coordinates (x, y, z).
        :rtype: tuple
        """
        return self._x_local, self._y_local, self._z_local

    @property
    def global_center(self):
        """
        Global center coordinates of the super layer.

        :return: Global center coordinates (x, y, z).
        :rtype: tuple
        """
        return self._x_global, self._y_global, self._z_global

    @property
    def layers(self):
        """
        Get all the layers in the super layer.

        :return: List of layers in the super layer.
        :rtype: list
        """
        return self._layers

    def layer(self, layer_number):
        """
        Get a layer by its number.

        :param layer_number: Number of the layer.
        :type layer_number: int
        :return: Layer with the specified number.
        :rtype: Layer
        """
        return next((l for l in self.layers if l.number == layer_number), None)

    @id.setter
    def id(self, id):
        """
        Set the identifier of the super layer.

        :param id: Identifier of the super layer.
        :type id: int
        """
        self._id = id

    @number.setter
    def number(self, number):
        """
        Set the number of the super layer.

        :param number: Number of the super layer.
        :type number: int
        :raises ValueError: If the number is not between 1 and 3.
        """
        if number < 1 or number > 3:
            raise ValueError("SuperLayer number must be between 1 and 3")
        self._number = number

    @local_center.setter
    def local_center(self, position):
        """
        Set the local center coordinates of the super layer.

        :param position: Local center coordinates (x, y, z).
        :type position: tuple
        """
        self._x_local, self._y_local, self._z_local = self.__correct_cords(*position)

    @global_center.setter
    def global_center(self, position):
        """
        Set the global center coordinates of the super layer.

        :param position: Global center coordinates (x, y, z).
        :type position: tuple
        """
        self._x_global, self._y_global, self._z_global = self.__correct_cords(*position)

    def add_layer(self, layer):
        """
        Add a new layer to the super layer.

        :param layer: Layer to be added.
        :type layer: Layer
        """
        self.layers.append(layer)

    def __correct_cords(self, x, y, z):
        """
        Correct the coordinates of the super layer. Bear in mind that the station reference
        frame is rotated pi/2 with respect to the CMS frame depending on the super layer number:

        if SL == 1 or 3:
            CMS -> x: right, y: up, z: forward, SuperLayer -> x: right, y: forward, z: down

        if SL == 2:
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
        if self.number == 1 or self.number == 3:
            return x, -1 * z, y
        else:
            return -1 * x, y, -1 * z

    def _build_super_layer(self):
        """
        Ensemble a DT super layer.
        """
        for layer in DTGEOMETRY.get(rawId=self.id).iter("Layer"):
            self.add_layer(Layer(layer.get("rawId"), parent=self))


# Example usage
if __name__ == "__main__":
    super_layer = SuperLayer(rawId=589357056)
