import ROOT as r
import os
from dtpr.base.event import Event
from dtpr.utils.functions import color_msg


class NTuple(object):
    def __init__(self, inputFolder, selectors, maxfiles=-1, tree_name="/TTREE"):
        """
        Initialize an NTuple instance.

        :param inputFolder: The folder containing the input files.
        :type inputFolder: str
        :param selectors: A list of selector functions to apply to the events. See dtpr.utils.filters
        :type selectors: list
        :param maxfiles: The maximum number of files to process. Defaults to -1 (process all files).
        :type maxfiles: int, optional
        :param tree_name: The name of the TTree to load. Defaults to "/TTREE".
        :type tree_name: str, optional
        """
        # Save in attributes
        self.inputFolder = inputFolder
        self.selectors = selectors
        self.maxfiles = maxfiles
        self.tree_name = tree_name

        # Prepare input
        self.load_tree(inputFolder)
        self.events = (
            ev
            for iev, root_ev in enumerate(self.tree)
            if (ev := self.run(Event(root_ev, iev)))
        )

    def run(self, ev: Event):
        """
        Run the event analysis.

        :param ev: The event to analyze.
        :type ev: Event
        :returns: The analyzed event if it passes the selection criteria, otherwise None.
        :rtype: Event
        """
        raise NotImplementedError("Subclasses should implement this method")

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
            self.tree.Add(inpath + self.tree_name)
            self.maxfiles = 1
        else:
            color_msg(f"Opening input files from {inpath}", "blue", 1)
            allFiles = os.listdir(inpath)
            nFiles = (
                len(allFiles)
                if self.maxfiles == -1
                else min(len(allFiles), self.maxfiles)
            )
            self.maxfiles = nFiles

            for iF in range(nFiles):
                if "root" not in allFiles[iF]:
                    continue
                color_msg(f"File {allFiles[iF]} added", indentLevel=2)
                self.tree.Add(os.path.join(inpath, allFiles[iF]) + self.tree_name)
