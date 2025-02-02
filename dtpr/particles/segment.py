import math
from dtpr.utils.functions import color_msg


class Segment(object):
    __slots__ = [
        "index",
        "wh",
        "sc",
        "st",
        "phi",
        "eta",
        "nHits_phi",
        "nHits_z",
        "t0_phi",
        "matches",
        "pos_locx_sl1",
        "pos_locx_sl3",
    ]

    def __init__(
        self,
        iseg,
        ev=None,
        wh=None,
        sc=None,
        st=None,
        phi=None,
        eta=None,
        nHits_phi=None,
        nHits_z=None,
        t0_phi=None,
        pos_locx_sl1=0,
        pos_locx_sl3=0,
    ):
        """
        Initialize a Segment instance.

        A Segment can be initialized either by providing the root event entry (`ev`) or by passing each parameter individually.

        :param iseg: The index of the segment.
        :type iseg: int
        :param ev: The root event object containing event data.
        :param wh: The wheel number.
        :type wh: int, optional
        :param sc: The sector number.
        :type sc: int, optional
        :param st: The station number.
        :type st: int, optional
        :param phi: The global phi position.
        :type phi: float, optional
        :param eta: The global eta position.
        :type eta: float, optional
        :param nHits_phi: The number of phi hits.
        :type nHits_phi: int, optional
        :param nHits_z: The number of z hits.
        :type nHits_z: int, optional
        :param t0_phi: The phi time offset.
        :type t0_phi: float, optional
        """
        self.index = iseg
        if ev is not None:
            self.wh = ev.seg_wheel[iseg]
            self.sc = ev.seg_sector[iseg]
            self.st = ev.seg_station[iseg]
            self.phi = ev.seg_posGlb_phi[iseg]
            self.eta = ev.seg_posGlb_eta[iseg]
            self.nHits_phi = ev.seg_phi_nHits[iseg]
            self.nHits_z = ev.seg_z_nHits[iseg]
            self.t0_phi = ev.seg_phi_t0[iseg]
            self.pos_locx_sl1 = ev.seg_posLoc_x_SL1[iseg]
            self.pos_locx_sl3 = ev.seg_posLoc_x_SL3[iseg]
        else:
            self.wh = wh
            self.sc = sc
            self.st = st
            self.phi = phi
            self.eta = eta
            self.nHits_phi = nHits_phi
            self.nHits_z = nHits_z
            self.t0_phi = t0_phi
            self.pos_locx_sl1 = pos_locx_sl1
            self.pos_locx_sl3 = pos_locx_sl3

        self.matches = []

    def to_dict(self):
        """
        Convert the Segment instance to a dictionary.

        :return: A dictionary representation of the Segment instance.
        :rtype: dict
        """
        return {attr: getattr(self, attr) for attr in self.__slots__}

    def __str__(self, indentLevel=0):
        """
        Generate a string representation of the Segment instance.

        :param indentLevel: The indentation level for the summary.
        :type indentLevel: int
        :return: The segment summary.
        :rtype: str
        """
        summary = [
            color_msg(
                f"------ Segment {self.index} info ------",
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

    def _add_match(self, tp):
        """
        Add a match to the segment.

        :param tp: The trigger primitive to match.
        """
        if tp not in self.matches:
            self.matches.append(tp)

    def match_offline_to_AM(self, tp, max_dPhi=0.1):
        """
        Match the segment to a trigger primitive based on dPhi.

        :param tp: The trigger primitive to match.
        :param max_dPhi: The maximum dPhi for matching.
        :type max_dPhi: float
        """
        # Fix issue with sector numbering
        seg_sc = self.sc
        if seg_sc == 13:
            seg_sc = 4
        elif seg_sc == 14:
            seg_sc = 10

        # Match only if TP and segment are in the same chamber
        if tp.wh == self.wh and tp.sc == seg_sc and tp.st == self.st:
            # In this case, they are in the same chamber: match dPhi
            # -- Use a conversion factor to express phi in radians
            trigGlbPhi = tp.phi / tp.phires_conv + math.pi / 6 * (tp.sc - 1)
            dphi = abs(math.acos(math.cos(self.phi - trigGlbPhi)))
            matches = dphi < max_dPhi and tp.BX == 0
            if matches:
                self._add_match(tp)


if __name__ == "__main__":
    seg = Segment(
        0, wh=1, sc=1, st=1, phi=0.1, eta=0.2, nHits_phi=3, nHits_z=2, t0_phi=0.3
    )
    print(seg)
