NTuple
========

The ``NTuple`` class serves as a simple gateway to access information from single or multiple `.root` 
Ntuples (flat) located in the specified input path. It represents an interface to build ``Event`` instances
directly from the root event entries. This class is capable of filtering and building ``Event`` 
instances according to the **selectors** passed.

A selector should be a function that returns a boolean based on the information of an ``Event`` instance.
For instance, follow function will be pass all events:

.. code-block:: python

    def example_selector(event):
        # Example selector function that always returns True
        return True

The ``NTuple`` class is designed to be generic and handle any type of root flat NTuple. It is intended to
be used as a parent class. In practice, you should create a child class that inherits from ``NTuple``
and implement the ``event_preprocessor`` method to perform any necessary preprocessing steps before creating and 
selecting ``Event`` instances. This was implemented in that way to allow create selector based on properties that by default
does not come direclty from the root input, but cab be computed with extra funcions steps before apply the selection.

You can generate a skeleton of a child class using the dtpr command as follows:

.. code-block:: bash

    dtpr create ntuple --name DtNtuple -o [output_folder]

This will create a new file called ``dt_ntuple.py`` in the specified output folder with the following content:

.. code-block:: python

    from dtpr.base import Event, NTuple

    class DtNtuple(NTuple):
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
            super().__init__(inputFolder, selectors, maxfiles) # add tree_name argument if needed, default is "/TTREE"

        def event_preprocessor(self, ev: Event):
            """
            Preprocess the event. Specific to DtNtuple.

            :param ev: The event to preprocess.
            :type ev: Event
            :returns: The preprocessed event if it passes the selection criteria, otherwise None.
            :rtype: Event
            """
            # Implement specific analysis here before apply global selection
            # ...

            # Apply global selection
            if not self.select_event(ev):
                pass
            else:
                return ev

and then, you can implement the specific analysis for your NTuple as follow.

.. important::
    In the exemple below, the tree_name argument in the ``super.__init__`` call was set to ``/dtNtupleProducer/DTTREE`` to agree with the inputs used

.. code-block:: python

    from dt_ntuple import DtNtuple

    """
    Example of how to use the DtNtuple class to read DT Ntuples and analyze events.
    """
    def example_selector(event):
        # Example selector function that always returns True
        return True

    input_folder = "./DTDPGNtuple_12_4_2_Phase2Concentrator_Simulation_99.root"
    selectors = [example_selector]

    dt_ntuple = DtNtuple(input_folder, selectors)
    # you can access events by index or slice such as a list
    print(dt_ntuple.events[10])
    print(dt_ntuple.events[3:5])

    # or loop over the events
    for iev, ev in enumerate(dt_ntuple.events):
        print(ev)
        if iev == 2: break

    # or simply use the root tree, which is a ROOT.TChain
    for i, ev in enumerate(dt_ntuple.tree):
        print(ev.event_orbitNumber)
        if i == 0: break

.. rubric:: Output

.. code-block:: text

    + Opening input file /mnt_pool/c3_users/user/destrada/Public/DTPatternRecognition/src/ntuples/DTDPGNtuple_12_4_2_Phase2Concentrator_Simulation_99.root 
    >> ------ Event 10 info ------ 
    + Digis 
        * Number of digis: 127 
    + Segments 
        * Number of segments: 11 
        * (iSeg, Phi, eta): ['(0.00, 1.70, -1.14)', '(1.00, 2.39, -1.01)', '(2.00, 2.39, -1.00)', '(3.00, -2.00, -0.35)', '(4.00, -1.08, 0.92)'] 
    + Tps 
        * Number of tps: 27 
    + Genmuons 
        * Number of genmuons: 1 
        * Muon 0 
        --> GenPart Idx: 0 
        --> pT: 656.94 GeV 
        --> Eta: -0.97 
        --> Phi: -1.23 
        --> Matched segments indices: [8] 
        --> Matched segments location: [(2, 11, -2)] 
        --> Stations traversed: [(2, 11, -2)] 
        --> Showered 
    + Emushowers 
        * Number of emushowers: 1 
    + Simhits 
        * Number of simhits: 140 
    [<dtpr.base.event.Event object at 0x7fc6f4ecfb20>, <dtpr.base.event.Event object at 0x7fc6f4ce4b80>]
    >> ------ Event 0 info ------ 
    + Digis 
        * Number of digis: 340 
    + Segments 
        * Number of segments: 28 
        * (iSeg, Phi, eta): ['(0.00, 0.09, -1.15)', '(1.00, 0.31, 0.99)', '(2.00, 0.31, 0.99)', '(3.00, 0.77, -1.02)', '(4.00, 1.30, 0.57)'] 
    + Tps 
        * Number of tps: 71 
    + Genmuons 
        * Number of genmuons: 1 
        * Muon 0 
        --> GenPart Idx: 0 
        --> pT: 1601.72 GeV 
        --> Eta: 1.00 
        --> Phi: 0.31 
        --> Matched segments indices: [1, 2, 21, 22] 
        --> Matched segments location: [(1, 1, 2), (1, 1, 2), (2, 2, 2), (2, 2, 2)] 
        --> Stations traversed: [(1, 1, 2), (1, 1, 2), (2, 2, 2), (2, 2, 2)] 
        --> Showered 
    + Emushowers 
        * Number of emushowers: 2 
    + Simhits 
        * Number of simhits: 1031 
    event orbit number:  -1

.. important::
    
    The ``NTuple.events`` attribute is not a simple list, but an instance of the :doc:`event_list` class.
    This design prevents loading all events into memory simultaneously. Instead, it allows iteration and access by index and slice,
    while internally iterating over the root tree entries to create the required event on the fly.


.. autoclass:: dtpr.base.NTuple
    :members:
    :exclude-members: __weakref__, __dict__, __module__