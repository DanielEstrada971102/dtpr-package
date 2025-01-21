# functions to analyze generator level muons

from dtpr.base import Event


def analyze_genmuon_matches(ev: Event):
    """
    Match generator muons to segments and TPs in a broad dPhi/dEta window.
    """
    if not hasattr(ev, "segments"):
        raise ValueError(
            "Event does not have 'segments' they are required to analyze matches."
        )
    if not hasattr(ev, "genmuons"):
        raise ValueError(
            "Event does not have 'genmuons' they are required to analyze matches."
        )
    if not hasattr(ev, "tps"):
        raise ValueError(
            "Event does not have 'tps' they are required to analyze matches."
        )

    for gm in ev.genmuons:
        # Match segments to generator muons
        for seg in ev.segments:
            # gm.match_segment(seg, math.pi / 6., 0.8)
            gm.match_segment(seg, 0.1, 0.3)
        # Now re-match with TPs
        matched_segments = gm.matches
        for seg in matched_segments:
            for tp in ev.tps:
                seg.match_offline_to_AM(tp, max_dPhi=0.1)


def analyze_genmuon_showers(ev: Event):
    """
    Analyze if the generator muon showered based on matched segments.
    """
    if not hasattr(ev, "genmuons"):
        raise ValueError("Event does not have 'genmuons' they are required")

    for gm in ev.genmuons:
        locs = gm.matched_segments_stations
        if len(locs) != len(set(locs)):
            # There's at least two matching segments in the same station for this muon
            gm.showered = True
