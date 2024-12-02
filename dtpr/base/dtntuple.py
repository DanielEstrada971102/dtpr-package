# Module to read DT Ntuples and create Event instances from root entries

# -- Import libraries -- #
import ROOT as r
import os
from dtpr.base.event import Event
from dtpr.utils.functions import color_msg
from dtpr.utils.genmuon_functions import analyze_genmuon_matches, analyze_genmuon_showers

class DtNtuple(object):
    def __init__(self, inputFolder, selectors, maxfiles=-1):
        """
        Initialize a DtNtuple instance.

        :param inputFolder: The folder containing the input files.
        :type inputFolder: str
        :param selectors: A list of selector functions to apply to the events. See dtpr.utils.filters
        :type selectors: list
        :param maxfiles: The maximum number of files to process. Defaults to -1 (process all files).
        :type maxfiles: int, optional
        """
        # Save in attributes
        self.inputFolder = inputFolder
        self.selectors = selectors
        self.maxfiles = maxfiles

        # Prepare input
        self.load_tree(inputFolder)
        self.events = (ev for iev, root_ev in enumerate(self.tree) if (ev := self.run(Event(root_ev, iev))))

    def run(self, ev: Event):
        """
        Run the event analysis.

        :param ev: The event to analyze.
        :type ev: Event
        :returns: The analyzed event if it passes the selection criteria, otherwise None.
        :rtype: Event
        """
        analyze_genmuon_matches(ev)
        analyze_genmuon_showers(ev)
        # Apply global selection
        if not self.passes_event(ev):
            pass
        else:
            return ev

    def passes_event(self, ev: Event):
        """
        Apply global cuts on the events using the selectors.

        :param ev: The event to check.
        :type ev: Event
        :returns: True if the event passes all selectors, False otherwise.
        :rtype: bool
        """
        return all(selector(ev) for selector in self.selectors)

    def load_tree(self, inpath):
        """
        Retrieve a chain with all the trees to be analyzed.

        :param inpath: The path to the input files.
        :type inpath: str
        """
        self.tree = r.TChain()

        if "root" in inpath:
            color_msg(f"Opening input file {inpath}", "blue", 1)
            self.tree.Add(inpath + "/dtNtupleProducer/DTTREE")
            self.maxfiles = 1
        else:
            color_msg(f"Opening input files from {inpath}", "blue", 1)
            allFiles = os.listdir(inpath)
            nFiles = len(allFiles) if self.maxfiles == -1 else min(len(allFiles), self.maxfiles)
            self.maxfiles = nFiles

            for iF in range(nFiles):
                if "root" not in allFiles[iF]:
                    continue
                color_msg(f"File {allFiles[iF]} added", indentLevel=2)
                self.tree.Add(os.path.join(inpath, allFiles[iF]) + "/dtNtupleProducer/DTTREE")

if __name__ == "__main__":
    """
    Example of how to use the DtNtuple class to read DT Ntuples and analyze events.
    """
    def example_selector(event):
        # Example selector function that always returns True
        return True

    input_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../utils/templates/DTDPGNtuple_12_4_2_Phase2Concentrator_Simulation_101.root"))
    selectors = [example_selector]
    max_files = 5

    dt_ntuple = DtNtuple(input_folder, selectors, maxfiles=max_files)
    # you can iterate over the events built as Event instances
    ev_iter = iter(dt_ntuple.events)
    print(next(ev_iter))

    # or simply use the root tree which is a ROOT.TChain
    for ev in dt_ntuple.tree:
        print(ev.gen_pt)
        break
