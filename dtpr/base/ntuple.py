import ROOT as r
import os
from dtpr.base import Event, EventList
from dtpr.utils.functions import color_msg


class NTuple(object):
    """
    A class to handle the loading and processing of ROOT TTrees.

    Attributes
    ----------
    tree : ROOT.TChain
        The TChain containing the loaded TTrees.
    events : EventList
        The list of events from the TTree.
    """

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
        self._selectors = selectors
        self._maxfiles = maxfiles
        self._tree_name = tree_name
        self.tree = r.TChain()

        # Prepare input
        self.load_tree(inputFolder)
        self.events = EventList(self.tree, self.event_preprocessor)

    def event_preprocessor(self, ev: Event):
        """
        Preprocess the event.

        :param ev: The event to preprocess.
        :type ev: Event
        :returns: The preprocessed event if it passes the selection criteria, otherwise None.
        :rtype: Event
        """
        raise NotImplementedError("Subclasses should implement this method")

    def select_event(self, ev: Event):
        """
        Apply global cuts on the events using the selectors.

        :param ev: The event to check.
        :type ev: Event
        :returns: True if the event passes all selectors, False otherwise.
        :rtype: bool
        """
        return all(selector(ev) for selector in self._selectors)

    def load_tree(self, inpath):
        """
        Retrieve a chain with all the trees to be analyzed.

        :param inpath: The path to the input files.
        :type inpath: str
        """

        if "root" in inpath:
            color_msg(f"Opening input file {inpath}", "blue", 1)
            self.tree.Add(inpath + self._tree_name)
            self._maxfiles = 1
        else:
            color_msg(f"Opening input files from {inpath}", "blue", 1)
            allFiles = os.listdir(inpath)
            nFiles = (
                len(allFiles)
                if self._maxfiles == -1
                else min(len(allFiles), self._maxfiles)
            )
            self._maxfiles = nFiles

            for iF in range(nFiles):
                if "root" not in allFiles[iF]:
                    continue
                color_msg(f"File {allFiles[iF]} added", indentLevel=2)
                self.tree.Add(os.path.join(inpath, allFiles[iF]) + self._tree_name)
