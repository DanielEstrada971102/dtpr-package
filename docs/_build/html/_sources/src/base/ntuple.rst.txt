NTuple
========

The ``NTuple`` class serves as a simple gateway to access information from single or multiple root 
Ntuples located in the specified input path. It provides an interface to build ``Event`` instances
directly from the root event entries. This class is capable of filtering and building ``Event`` 
instances according to the **selectors** passed.

A selector should be a function that returns a boolean based on the information of an ``Event`` instance.
For instance, follow function will be pass all events:

The ``NTuple`` class is designed to be generic and handle any type of root NTuple. It is intended to
be used as a parent class. In practice, you should create a child class that inherits from ``NTuple``
and implement the ``run`` method to perform any necessary preprocessing steps before creating and 
selecting ``Event`` instances.

You can generate a skeleton of a child class using the dtpr command as follows:

.. code-block:: bash

    dtpr create ntuple --name DtNtuple -o [output_folder]

This will create a new file called ``dt_ntuple.py`` in the specified output folder with the following content:

.. code-block:: python

    from dtpr.base.event import Event
    from dtpr.base.ntuple import NTuple

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

        def run(self, ev: Event):
            """
            Run the event analysis specific to DtNtuple.

            :param ev: The event to analyze.
            :type ev: Event
            :returns: The analyzed event if it passes the selection criteria, otherwise None.
            :rtype: Event
            """
            # Implement specific analysis here before applying global selection
            # ...

            # Apply global selection
            if not self.passes_event(ev):
                pass
            else:
                return ev

and then, you can implement the specific analysis for your NTuple (from the previous skeleton,
the tree_name argument was set to `/dtNtupleProducer/DTTREE`` to agree with the inputs).

.. code-block:: python

    from dtpr.base.event import Event

    def example_selector(event: Event) -> bool:
        # Example selector function that always returns True
        return True

    input_folder = "DTDPGNtuple_12_4_2_Phase2Concentrator_Simulation_101.root"
    selectors = [example_selector]

    dt_ntuple = DtNtuple(input_folder, selectors)
    # you can iterate over the events built as Event instances
    event = iter(dt_ntuple.events)
    print(next(event))

    # or simply use the root tree which is a ROOT.TChain
    for ev in dt_ntuple.tree:
        print("Driectly from ROOT.TChain")
        print(ev.gen_pt)
        break

.. rubric:: Output

.. code-block:: text

    + Opening input file DTDPGNtuple_12_4_2_Phase2Concentrator_Simulation_101.root 
    >> ------ Event 0 info ------ 
    + Digis 
        * Number of digis: 95 
    + Segments 
        * Number of segments: 8 
        * (iSeg, Phi, eta): ['(0.00, 0.65, -1.03)', '(1.00, -0.82, -1.02)', '(2.00, 0.93, 0.67)', '(3.00, -3.07, -0.00)', '(4.00, -2.78, -0.40)'] 
    + Tps 
        * Number of tps: 15 
    + Genmuons 
        * Number of genmuons: 1 
        * Muon 0 
        --> GenPart Idx: 0 
        --> pT: 1953.97 GeV 
        --> Eta: 1.39 
        --> Phi: 0.35 
        --> Matched segments indices: [] 
        --> Matched segments location: [] 
        --> Stations traversed: [] 
        --> Not showered 
    + Emushowers 
        * Number of emushowers: 0 
    { 1953.97f, 1947.34f }

.. important::
    
    NTuple.events is a generator that yields Event instances. You can iterate over it to access the
    events but you can't access the events by index. If you need to access the events by index, you
    can convert the generator to a list but be aware that this will load all the events into memory.


.. autoclass:: dtpr.base.ntuple.NTuple
    :members:
    :undoc-members:
    :special-members: __init__