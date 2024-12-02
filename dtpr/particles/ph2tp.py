import math
from dtpr.utils.functions import color_msg

class Ph2tp(object):
    __slots__ = ["index", "wh", "sc", "st", "phi", "phiB", "BX", "quality", "rpcFlag", "phires_conv", "matches", "matches_with_segment"]

    def __init__(self, itp, ev=None, wh=None, sc=None, st=None, phi=None, phiB=None, BX=None, quality=None, rpcFlag=None):
        """
        Initialize a Phase2 Trigger Primitive (Ph2tp) instance.

        A Phase2 Trigger Primitive can be initialized either by providing the root event entry (`ev`) or by passing each parameter individually.

        :param itp: The index of the trigger primitive.
        :type itp: int
        :param ev: The root event object containing event data.
        :param wh: The wheel number.
        :type wh: int, optional
        :param sc: The sector number.
        :type sc: int, optional
        :param st: The station number.
        :type st: int, optional
        :param phi: The phi position.
        :type phi: float, optional
        :param phiB: The phi bending angle.
        :type phiB: float, optional
        :param BX: The bunch crossing number.
        :type BX: int, optional
        :param quality: The quality of the trigger primitive.
        :type quality: int, optional
        :param rpcFlag: The RPC flag.
        :type rpcFlag: int, optional
        """
        self.index = itp
        if ev is not None:
            self.wh = ev.ph2TpgPhiEmuAm_wheel[itp]
            self.sc = ev.ph2TpgPhiEmuAm_sector[itp]
            self.st = ev.ph2TpgPhiEmuAm_station[itp]
            self.phi = ev.ph2TpgPhiEmuAm_phi[itp]
            self.phiB = ev.ph2TpgPhiEmuAm_phiB[itp]
            self.BX = ev.ph2TpgPhiEmuAm_BX[itp] - 20  # Correct to center BX at 0
            self.quality = ev.ph2TpgPhiEmuAm_quality[itp]
            self.rpcFlag = ev.ph2TpgPhiEmuAm_rpcFlag[itp]
        else:
            self.wh = wh
            self.sc = sc
            self.st = st
            self.phi = phi
            self.phiB = phiB
            self.BX = BX
            self.quality = quality
            self.rpcFlag = rpcFlag

        # Constants
        self.phires_conv = 65536. / 0.5
        self.matches = []
        self.matches_with_segment = False
        return
    
    def to_dict(self):
        """
        Convert the Phase2 Trigger Primitive (Ph2tp) instance to a dictionary.

        :return: A dictionary representation of the Ph2tp instance.
        :rtype: dict
        """
        return {attr: getattr(self, attr) for attr in self.__slots__}

    def __str__(self, indentLevel=0):
        """
        Generate a string representation of the Phase2 Trigger Primitive (Ph2tp) instance.

        :param indentLevel: The indentation level for the summary.
        :type indentLevel: int
        :return: The trigger primitive summary.
        :rtype: str
        """
        summary = [
            color_msg(
                f"------ ph2tpg {self.index} info ------",
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
    ph2tpg = Ph2tp(wh=1, sc=1, st=1, phi=1, phiB=1, BX=1, quality=1, rpcFlag=1)
    print(ph2tpg)
