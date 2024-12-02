DtNtuple
========

The ``DtNtuple`` class serves as a simple gateway to access information from single or multiple DT 
Ntuples located in the specified input path. It provides an interface to build ``Event`` instances
directly from the Ntuple event entries. This class is capable of filtering and building ``Event`` 
instances according to the selectors passed.

A selector should be a function that returns a boolean based on the information of an ``Event`` instance.
For instance, follow function will be pass all events:

.. rubric:: Example

.. code-block:: python

    from dtpr.base.dtntuple import DtNtuple
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

.. autoclass:: dtpr.base.dtntuple.DtNtuple
    :members:
    :undoc-members:
    :special-members: __init__