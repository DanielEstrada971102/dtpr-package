import math
from dtpr.utils.functions import color_msg, phiConv

class GenMuon(object):
    __slots__ = ["index", "pt", "eta", "phi", "charge", "matches", "matched_segments_stations", "showered"]

    def __init__(self, igm, ev=None, pt=None, eta=None, phi=None, charge=None):
        """
        Initialize a Generator Level Muon instance.

        :param igm: The index of the generator muon.
        :type igm: int
        :param ev: The root event object containing event data.
        :type ev: optional
        :param pt: The transverse momentum.
        :type pt: float, optional
        :param eta: The pseudorapidity.
        :type eta: float, optional
        :param phi: The azimuthal angle.
        :type phi: float, optional
        :param charge: The charge of the muon.
        :type charge: int, optional
        """
        self.index = igm
        if ev is not None: # constructor with root_event info
            self.pt = ev.gen_pt[igm]
            self.eta = ev.gen_eta[igm]
            self.phi = ev.gen_phi[igm]
            self.charge = ev.gen_charge[igm]
        else: # constructor with explicit info
            self.pt = pt
            self.eta = eta
            self.phi = phi
            self.charge = charge 
        
        # Attributes
        self.matches = []
        self.matched_segments_stations = []
        self.showered = False
        return

    def to_dict(self):
        """
        Convert the Generator Level Muon instance to a dictionary.

        :return: A dictionary representation of the Generator Level Muon instance.
        :rtype: dict
        """
        return {attr: getattr(self, attr) for attr in self.__slots__}

    def add_match(self, seg):
        """
        Add a matched segment to the muon.

        :param seg: The segment to add.
        :type seg: Segment
        """
        if seg not in self.matches: self.matches.append(seg)
        location = (seg.st, seg.sc, seg.wh) 
        self.matched_segments_stations.append(location)

    def match_segment(self, seg, max_dPhi, max_dEta):
        """
        Check which matching criteria the muon satisfies with a given segment.

        :param seg: The segment to match.
        :type seg: Segment
        :param max_dPhi: The maximum dPhi for matching.
        :type max_dPhi: float
        :param max_dEta: The maximum dEta for matching.
        :type max_dEta: float
        """
        st = seg.st
        isMB4 = (st == 4)            
        dphi = abs(math.acos(math.cos(self.phi - seg.phi)))
        deta = abs(self.eta - seg.eta)            
        matches = (dphi < max_dPhi) and (deta < max_dEta) and seg.nHits_phi >= 4 and (seg.nHits_z >= 4 or isMB4)
        if matches: 
            self.add_match(seg)
    
    def get_max_dphi(self):
        """
        Compute the maximum dPhi of the segments that match to the generator muon.

        :return: The maximum dPhi.
        :rtype: float
        """
        if self.matches == []: 
            return -99
        return max([abs(math.acos(math.cos(self.phi - seg.phi))) for seg in self.matches])
    
    def get_dphimax_segments(self):
        """
        Compute the maximum dPhi of the segments of two adjacent stations that match to the generator muon.

        :return: The maximum dPhi.
        :rtype: float
        """
        if self.matches == []: 
            return -99
        
        dphi = []
        for seg1 in self.matches:
            for seg2 in self.matches: 
                # ignore the same segment or any segment on the same chamber
                if seg1.st == seg2.st: continue 
                dphi.append(abs(math.acos(math.cos(seg1.phi - seg2.phi))))
        if dphi == []: 
            return -99
        else:               
            return max(dphi) 
        
    def get_dphimax_tp(self):
        """
        Compute the maximum dPhi of the TPs of two adjacent stations that match to the generator muon.

        :return: The maximum dPhi.
        :rtype: float
        """
        if self.matches == []: 
            return -99
        
        dphi = []
        for seg1 in self.matches:
            phi_tp1 = [tp.phi for tp in seg1.matches]
            for seg2 in self.matches: 
                # ignore the same segment or any segment on the same chamber
                if seg1.st == seg2.st: continue
                if seg1.sc != seg2.sc: continue
                phi_tp2 = [tp.phi for tp in seg2.matches]
                if phi_tp1 == [] or phi_tp2 == []: continue
                dphi.append(max([abs(math.acos(math.cos(phiConv(phi1) - phiConv(phi2)))) for phi1 in phi_tp1 for phi2 in phi_tp2]))

        if dphi == []: 
            return -99
        else:               
            return dphi
    
    def get_dphi_segments(self):
        """
        Compute the dPhi of the segments of two adjacent stations that match to the generator muon.

        :return: A list of dPhi values.
        :rtype: list
        """
        if self.matches == []: 
            return -99
        
        dphi = []
        for seg1 in self.matches:
            for seg2 in self.matches: 
                # ignore the same segment or any segment on the same chamber
                if seg1.st == seg2.st: continue 
                dphi.append(abs(math.acos(math.cos(seg1.phi - seg2.phi))))
        
        if dphi == []: 
            return -99
        else:               
            return dphi
        
    def get_dphi_tp(self):
        """
        Compute the dPhi of the TPs of two adjacent stations that match to the generator muon.

        :return: A list of dPhi values.
        :rtype: list
        """
        if self.matches == []: 
            return -99
        
        dphi = []
        for seg1 in self.matches:
            phi_tp1 = [tp.phi for tp in seg1.matches]
            for seg2 in self.matches: 
                # ignore the same segment or any segment on the same chamber
                if seg1.st == seg2.st: continue
                if seg1.sc != seg2.sc: continue
                phi_tp2 = [tp.phi for tp in seg2.matches]
                if phi_tp1 == [] or phi_tp2 == []: continue
                dphi.append([abs(math.acos(math.cos(phiConv(phi1) - phiConv(phi2)))) for phi1 in phi_tp1 for phi2 in phi_tp2])

        if dphi == []: 
            return -99
        else:               
            return dphi

    def get_max_deta(self):
        """
        Compute the maximum dEta of the segments that match to the generator muon.

        :return: The maximum dEta.
        :rtype: float
        """
        if self.matches == []: 
            return -99
        return max([abs(self.eta - seg.eta) for seg in self.matches])
    
    def did_shower(self):
        """
        Check if the muon showered.

        :return: True if the muon showered, False otherwise.
        :rtype: bool
        """
        return self.showered
        
    def __str__(self, indentLevel=0):
        """
        Generate a string representation of the Generator Level Muon instance.

        :param indentLevel: The indentation level for the summary.
        :type indentLevel: int
        :return: The generator muon summary.
        :rtype: str
        """
        summary = []
        summary.append(color_msg(f"GenPart Idx: {self.index}", indentLevel=indentLevel, return_str=True))
        summary.append(color_msg(f"pT: {self.pt:.2f} GeV", indentLevel=indentLevel, return_str=True))
        summary.append(color_msg(f"Eta: {self.eta:.2f}", indentLevel=indentLevel, return_str=True))
        summary.append(color_msg(f"Phi: {self.phi:.2f}", indentLevel=indentLevel, return_str=True))
        summary.append(color_msg(f"Matched segments indices: {[seg.index for seg in self.matches]}", indentLevel=indentLevel, return_str=True))
        summary.append(color_msg(f"Matched segments location: {[(seg.st, seg.sc, seg.wh) for seg in self.matches]}", indentLevel=indentLevel, return_str=True))
        summary.append(color_msg(f"Stations traversed: {self.matched_segments_stations}", indentLevel=indentLevel, return_str=True))
        if self.showered:
            summary.append(color_msg(f"Showered", color="red", indentLevel=indentLevel, return_str=True,))
        else:
            summary.append(color_msg(f"Not showered", indentLevel=indentLevel, return_str=True,))
        return "\n".join(summary)