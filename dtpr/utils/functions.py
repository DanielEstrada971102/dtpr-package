""" Miscelaneous """
import math
import ROOT as r
r.gStyle.SetOptStat(0)
import os
from copy import deepcopy
import numpy as np

# Make Iterators for when we want to iterate over different subdetectors
wheels   = range(-2, 3)
sectors  = range(1, 15)
stations = range(1, 5)
superlayers = range(1, 4)

_noDelete = { "lines" : []}

def color_msg(msg, color="none", indentLevel=-1, return_str=False):
    """
    Prints a message with ANSI coding so it can be printed with colors.

    Args:
        msg (str): The message to print.
        color (str): The color to use for the message. Default is "none".
        indentLevel (int): The level of indentation. Default is -1.
        return_str (bool): If True, returns the formatted message as a string. Default is False.

    Returns:
        str: The formatted message if return_str is True.
    """
    codes = {
        "none": "0m",
        "green": "1;32m",
        "red": "1;31m",
        "blue": "1;34m",
        "yellow": "1;33m",
        "purple": "1;35m",
    }

    indentStr = ""
    if indentLevel == 0: indentStr = ">>"
    if indentLevel == 1: indentStr = "+"
    if indentLevel == 2: indentStr = "*"
    if indentLevel == 3: indentStr = "-->"
    if indentLevel >= 4: indentStr = "-"

    try:
        formatted_msg = "\033[%s%s %s \033[0m" % (codes[color], "  " * indentLevel + indentStr, msg)
    except KeyError:
        formatted_msg = "\033[%s%s %s \033[0m" % (codes["none"], "  " * indentLevel + indentStr, msg)
    
    if return_str:
        return formatted_msg
    else:
        print(formatted_msg)

def warning_handler(message, category, filename, lineno, file=None, line=None):
    """
    Handles warnings by printing them with color formatting.

    Args:
        message (str): The warning message.
        category (Warning): The category of the warning.
        filename (str): The name of the file where the warning occurred.
        lineno (int): The line number where the warning occurred.
        file (file object, optional): The file object. Default is None.
        line (str, optional): The line of code where the warning occurred. Default is None.
    """
    print(
        "".join([
            color_msg(f"{category.__name__} in:", color="yellow", return_str=True, indentLevel=-1),
            color_msg(f"{filename}-{lineno} :", color="purple", return_str=True, indentLevel=-1),
            color_msg(f"{message}", return_str=True, indentLevel=-1),
        ])
    )

def error_handler(exc_type, exc_value, exc_traceback):
    """
    Handles errors by printing them with color formatting.

    Args:
        exc_type (type): The type of the exception.
        exc_value (Exception): The exception instance.
        exc_traceback (traceback): The traceback object.
    """
    import traceback
    print(
        "".join([
            color_msg(f"{exc_type.__name__}:", color="red", return_str=True, indentLevel=-1),
            color_msg(f"{exc_value}", color="yellow", return_str=True, indentLevel=-1),
            color_msg("Traceback (most recent call last):" + "".join(traceback.format_tb(exc_traceback)) if exc_traceback else "", return_str=True, indentLevel=-1),#[-2:]
        ])
    )

def flatten(lst):
    """
    Flattens a nested list.

    Args:
        lst (list): The nested list to flatten.

    Returns:
        list: The flattened list.
    """
    result = []
    for i in lst:
        if isinstance(i, list):
            result.extend(flatten(i))
        else:
            result.append(i)
    return result

def create_outfolder(outname):
    """
    Creates an output directory if it does not exist.

    Args:
        outname (str): The path of the output directory.
    """
    if not(os.path.exists(outname)): 
        os.system("mkdir -p %s"%outname)

def get_best_matches( reader, station = 1, _4showereds=None):
    """
    Returns the best matching segments for each generator muon.

    Args:
        reader (object): The reader object containing generator muons.
        station (int): The station number. Default is 1.
        _4showereds (bool, optional): If specified, filters generator muons based on showered status. Default is None.

    Returns:
        list: The best matching segments.
    """
    # Fill with dummy segments
    if _4showereds is not None:
        genmuons = [genmuon for genmuon in reader.genmuons if (genmuon.showered == _4showereds)]
    else:
        genmuons = reader.genmuons

    bestMatches = [ None for igm in range(len(genmuons)) ]

    # This is what's done in Jaime's code: https://github.com/jaimeleonh/DTNtuples/blob/unifiedPerf/test/DTNtupleTPGSimAnalyzer_Efficiency.C#L181-L208
    # Basically: get the best matching segment to a generator muon per MB chamber

    #color_msg(f"[FUNCTIONS::GET_BEST_MATCHES] Debugging with station {station}", color = "red", indentLevel = 0)
    for igm, gm in enumerate(genmuons):
        #color_msg(f"[FUNCTIONS::GET_BEST_MATCHES] igm {igm}", indentLevel = 1)
        #gm.summarize(indentLevel = 2)
        for bestMatch in gm.matches:
            if bestMatch.st == station:
                bestMatches[ igm ] =  bestMatch
            
    # Remove those that are None which are simply dummy values
    bestMatches = filter( lambda key: key is not None, bestMatches )
    return bestMatches

def get_digis_distribution(reader, station=1, _4showereds=False, distribution_type="mean", group_by_sl=False):
    """
    Calculates the distribution of digis for a given station and showered status.

    Args:
        reader (object): The reader object containing digis.
        station (int): The station number. Default is 1.
        _4showereds (bool): The showered status. Default is False.
        distribution_type (str): The type of distribution to calculate ("mean" or "length"). Default is "mean".
        group_by_sl (bool): If True, groups digis by superlayer. Default is False.

    Returns:
        list: The calculated distribution data.
    """
    hasShowereds = any(genmuon.showered for genmuon in reader.genmuons)
    data = []

    if hasShowereds == _4showereds:
        # Iterate over all wheels
        for wh in wheels:
            # Iterate over all sectors
            for sc in sectors:
                # Iterate over all superlayers if needed
                sl_range = [1, 2, 3] if group_by_sl else [None]

                for sl in sl_range:
                    # Filter digis for the current wheel, sector, and station (and superlayer if it's the case) 
                    if sl:
                        digis = reader.filter_particles("digis", wh=wh, sc=sc, st=station, sl=sl)
                    else:
                        digis = reader.filter_particles("digis", wh=wh, sc=sc, st=station)

                    if not digis:
                        continue
                    wires = [digi.w for digi in digis]
                    if distribution_type == "mean":
                        w_mean = np.mean(wires)
                        data += [(wh, sl, w - w_mean) for w in wires] if group_by_sl else [(wh, w - w_mean) for w in wires]
                    elif distribution_type == "length":
                        w_min, w_max = min(wires), max(wires)
                        data.append((wh, sl, w_max - w_min) if group_by_sl else (wh, w_max - w_min))

    return data

def deltaPhi(phi1, phi2):
    """
    Calculates the difference in phi between two angles.

    Args:
        phi1 (float): The first angle in radians.
        phi2 (float): The second angle in radians.

    Returns:
        float: The difference in phi.
    """
    res = phi1 - phi2
    while res > math.pi: res -= 2*math.pi
    while res <= -math.pi: res += 2*math.pi
    return res

def deltaR(p1, p2):
    """
    Calculates the delta R between two particles.

    Args:
        p1 (object): The first particle with attributes eta and phi.
        p2 (object): The second particle with attributes eta and phi.

    Returns:
        float: The delta R value.
    """
    dEta = abs(p1.eta-p2.eta)
    dPhi = deltaPhi(p1.phi, p2.phi)
    return math.sqrt(dEta*dEta + dPhi*dPhi)

def phiConv(phi):
    """
    Converts a phi value.

    Args:
        phi (float): The phi value to convert.

    Returns:
        float: The converted phi value.
    """
    return 0.5*phi/65536.

def plot_graphs(graphs, name, nBins, firstBin, lastBin, 
                xMin = None, xMax = None, maxY = None, titleX = None, titleY = None, 
                labels = [], notes = [], lines = [],
                legend_pos = (0.62, 0.37, 0.70, 0.45),
                outfolder = "results/plots"):
    """
    Plots a set of graphs.

    Args:
        graphs (list): The list of graphs to plot.
        name (str): The name of the plot.
        nBins (int): The number of bins.
        firstBin (float): The first bin value.
        lastBin (float): The last bin value.
        xMin (float, optional): The minimum x-axis value. Default is None.
        xMax (float, optional): The maximum x-axis value. Default is None.
        maxY (float, optional): The maximum y-axis value. Default is None.
        titleX (str, optional): The x-axis title. Default is None.
        titleY (str, optional): The y-axis title. Default is None.
        labels (list, optional): The list of labels for the x-axis. Default is [].
        notes (list, optional): The list of notes to add to the plot. Default is [].
        lines (list, optional): The list of lines to add to the plot. Default is [].
        legend_pos (tuple, optional): The position of the legend. Default is (0.62, 0.37, 0.70, 0.45).
        outfolder (str, optional): The output folder to save the plot. Default is "results/plots".
    """
    # --- Create canvas --- #
    c = r.TCanvas("c_%s"%(name), "", 800, 800)
    
    # --- Create legend --- #
    x0leg, y0leg, x1leg, y1leg = legend_pos
    legend = r.TLegend(x0leg, y0leg, x1leg, y1leg)
    legend.SetName("l_%s"%(name))
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.028)
    legend.SetNColumns(1)
    
    # --- Create a frame metadata --- #
    frame = r.TH1D(name, "", nBins, firstBin, lastBin)
    frame.GetXaxis().SetTitleFont(42)
    frame.GetXaxis().SetTitleSize(0.03)
    frame.GetXaxis().SetLabelFont(42)
    frame.GetXaxis().SetLabelSize(0.04)
    frame.GetYaxis().SetTitleFont(42)
    frame.GetYaxis().SetTitleSize(0.03)
    frame.GetYaxis().SetLabelFont(42)
    frame.GetYaxis().SetLabelSize(0.04)
    
    if xMin and xMax:
        frame.GetXaxis().SetRangeUser(xMin, xMax)
    if maxY:
        frame.GetYaxis().SetRangeUser(0, maxY)
    if titleX: 
        frame.GetYaxis().SetTitle(titleX)
    if titleY:
        frame.GetXaxis().SetTitle(titleY)
    
    if labels != []:
        for iBin in range(frame.GetNbinsX()):
            frame.GetXaxis().SetBinLabel(iBin + 1, labels[iBin])
    frame.Draw("axis")
    
    # open the root files
    color = 1
    for igr, grInfo in enumerate( graphs ):
        effgr, legendName = grInfo
        effgr.SetMarkerColor( color )
        effgr.SetLineColor( color )
        effgr.SetMarkerSize( 1 )
        effgr.SetMarkerStyle( 20 )
        legend.AddEntry( effgr, legendName, "p")

        if color == [10, 18]: color += 1 # skip white colors
        effgr.Draw("pe1 same")
        color += 1

    
    # Now add texts and lines
    for note in notes:
        text = note[0]
        x1, y1, x2, y2 = note[1]
        textSize = note[2]
        align=12 
        texnote = deepcopy(r.TPaveText(x1, y1, x2, y2,"NDC"))
        texnote.SetTextSize(textSize)
        texnote.SetFillColor(0)
        texnote.SetFillStyle(0)
        texnote.SetLineWidth(0)
        texnote.SetLineColor(0)
        texnote.SetTextAlign(align)
        texnote.SetTextFont(42)
        texnote.AddText(text)
        texnote.Draw("same")
        _noDelete[texnote] = texnote # So it does not get deleted by ROOT

        
    for line in lines:
        xpos0, ypos0, xpos1, ypos1 = line
        texline = deepcopy(r.TLine(xpos0, ypos0, xpos1, ypos1))
        texline.SetLineWidth(3)
        texline.Draw("same") 
        _noDelete[texline] = texline # So it does not get deleted by ROOT


    legend.Draw("same")
    
    outpath = os.path.join( outfolder, name)
    if not os.path.exists(outpath):    
        os.system("mkdir -p %s"%outpath)
    c.SaveAs(outpath+"/%s.png"%name)
    c.SaveAs(outpath+"/%s.pdf"%name)
