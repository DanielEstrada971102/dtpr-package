from dtpr.geometry.dt_geometry import DTGEOMETRY
from dtpr.geometry.super_layer import SuperLayer

class Station(object):
    """
    Class representing a Drift Station.

    Attributes
    ----------
    id : int
        Identifier of the DT station.
    wheel : int
        Geometrical position within CMS.
    sector : int
        Geometrical position within CMS.
    station : int
        Geometrical position within CMS.
    bounds : tuple
        Space dimensions of the station.
    center : tuple
        Global center coordinates of the station.
    direction : tuple
        Normal vector that determines the direcciont of station refer to CMS.
    super_layers : list
        List of super layers in the station.
    """

    def __init__(self, wheel, sector, station):
        """
        Constructor

        :param wheel: Geometrical position within CMS.
        :type wheel: int
        :param sector: Geometrical position within CMS.
        :type sector: int
        :param station: Geometrical position within CMS.
        :type station: int
        """
        self._super_layers = []

        # == Chamber related parameters
        self.wheel = wheel
        self.sector = sector
        self.station = station
        self.id = DTGEOMETRY.get("rawId", wh=wheel, sec=sector, st=station)
        self.bounds = DTGEOMETRY.get("Bounds", rawId=self.id)
        self.local_center = DTGEOMETRY.get("LocalPosition", rawId=self.id)
        self.global_center = DTGEOMETRY.get("GlobalPosition", rawId=self.id)
        self.direction = DTGEOMETRY.get("NormalVector", rawId=self.id)

        # == Build the station
        self._build_station()

    # == Getters

    @property
    def id(self):
        """
        Identifier of the station.

        :return: Identifier of the station.
        :rtype: int
        """
        return self._id

    @property
    def wheel(self):
        """
        Geometrical position within CMS.

        :return: Wheel position.
        :rtype: int
        """
        return self._wheel

    @property
    def sector(self):
        """
        Geometrical position within CMS.

        :return: Sector position.
        :rtype: int
        """
        return self._sector

    @property
    def station(self):
        """
        Geometrical position within CMS.

        :return: Station position.
        :rtype: int
        """
        return self._station

    @property
    def name(self):
        """
        Name of the station.

        :return: Name of the station.
        :rtype: str
        """
        return f"Wheel {self.wheel}, Sector {self.sector}, Station {self.station}"

    @property
    def super_layers(self):
        """
        Get all the super layers in the station.

        :return: List of super layers in the station.
        :rtype: list
        """
        return self._super_layers

    def super_layer(self, super_layer_number):
        """
        Get a super layer by its number.

        :param super_layer_number: Number of the super layer.
        :type super_layer_number: int
        :return: Super layer with the specified number.
        :rtype: SuperLayer
        """
        return next((sl for sl in self.super_layers if sl.number == super_layer_number), None)

    @property
    def local_center(self):
        """
        Local center coordinates of the station.

        :return: Local center coordinates (x, y, z).
        :rtype: tuple
        """
        return self._x_local, self._y_local, self._z_local

    @property
    def global_center(self):
        """
        Global center coordinates of the station.

        :return: Global center coordinates (x, y, z).
        :rtype: tuple
        """
        return self._x_global, self._y_global, self._z_global

    @property
    def bounds(self):
        """
        Space dimensions of the station.

        :return: Dimensions of the station (width, height, depth).
        :rtype: tuple
        """
        return self._width, self._height, self._depth

    # == Setters

    @id.setter
    def id(self, value):
        """
        Set the identifier of the station.

        :param value: Identifier of the station.
        :type value: int
        """
        self._id = value

    @wheel.setter
    def wheel(self, value):
        """
        Set the wheel position.

        :param value: Wheel position.
        :type value: int
        :raises ValueError: If the value is not between -2 and 2.
        """
        if value < -2 or value > 2:
            raise ValueError("Wheel value must be between -2 and 2")
        self._wheel = value

    @sector.setter
    def sector(self, value):
        """
        Set the sector position.

        :param value: Sector position.
        :type value: int
        :raises ValueError: If the value is not between 1 and 14.
        """
        if value < 1 or value > 14:
            raise ValueError("Sector value must be between 1 and 14")
        if value == 13:
            self._sector = 4
        elif value == 14:
            self._sector = 10
        else:
            self._sector = value

    @station.setter
    def station(self, value):
        """
        Set the station position.

        :param value: Station position.
        :type value: int
        :raises ValueError: If the value is not between 1 and 4.
        """
        if value < 1 or value > 4:
            raise ValueError("Station value must be between 1 and 4")
        self._station = value

    @local_center.setter
    def local_center(self, position):
        """
        Set the local center coordinates of the station.

        :param position: Local center coordinates (x, y, z).
        :type position: tuple
        """
        self._x_local, self._y_local, self._z_local = self._correct_cords(*position)

    @global_center.setter
    def global_center(self, position):
        """
        Set the global center coordinates of the station.

        :param position: Global center coordinates
        :type position: tuple
        """
        self._x_global, self._y_global, self._z_global = self._correct_cords(*position)

    @bounds.setter
    def bounds(self, bounds):
        """
        Set the space dimensions of the station.

        :param bounds: Dimensions of the station (width, height, depth).
        :type bounds: tuple
        """
        self._width, self._height, self._depth = bounds

    def add_super_layer(self, super_layer):
        """
        Add a new super layer to the station.

        :param super_layer: Super layer to be added.
        :type super_layer: SuperLayer
        """
        self.super_layers.append(super_layer)

    def _correct_cords(self, x, y, z):
        """
        Correct the coordinates of the station. Bear in mind that the station reference 
        frame is rotated pi/2 with respect to the CMS frame along x direction:
        
        CMS -> x: right, y: up, z: forward, Station -> x: right, y: forward, z: down

        :param x: x coordinate.
        :type x: float
        :param y: y coordinate.
        :type y: float
        :param z: z coordinate.
        :type z: float
        :return: Corrected coordinates.
        :rtype: tuple
        """
        return x, -1 * z, y

    def _build_station(self):
        """
        Build up the station.
        """
        for SL in DTGEOMETRY.get(rawId=self.id).iter("SuperLayer"):
            new_super_layer = SuperLayer(rawId=SL.get("rawId"), parent=self)
            self.add_super_layer(new_super_layer)


if __name__ == "__main__":
    local=False
    st = Station(wheel=-2, sector=1, station=4)
    print("Local: ", local)
    print("Station center:", st.local_center if local else st.global_center)
    print("Station direction:", st.direction)
    for sl in st.super_layers:
        print(f">Super Layer {sl.number} center:", sl.local_center if local else sl.global_center)
        for l in sl.layers:
            print(f"->Layer {l.number} center:", l.local_center if local else l.global_center)
            print(f"---First Cell center:", l.cells[0].local_center if local else l.cells[0].global_center)
            print(f"---Last Cell center:", l.cells[-1].local_center if local else l.cells[-1].global_center)


    # print(st.center)
    # print(st.super_layers)
    # sl_1 = st.super_layer(1)
    # print(sl_1.id, sl_1.number)
    # sl_2 = st.super_layer(2)
    # # print(sl_2.id, sl_2.number)
    # sl_3 = st.super_layer(3)
    # print(sl_3.id,  sl_3.number)