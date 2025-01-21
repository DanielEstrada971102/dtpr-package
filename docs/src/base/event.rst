Event
=====

The ``Event`` class is designed to represent an event entry from a root Ntuple, facilitating access
to information by abstracting info into instances of Python objects (**particles**). There are a set 
of already defined particles in the ``dtpr.particles`` module. Each instance of the ``Event`` 
class provides specific methods to comfortably access those objects such as offline segments, 
generation-level muons, simulation digis, showers, and more.

The ``Event`` class can dynamically build particle instances based on the root event's entry information if 
specified through a run configuration file. This configuration file contains information about the types
of particles and how to build them, allowing for flexible and customizable event processing.

To illustrate the dynamic particle building feature, consider the ``GenMuon`` class from the 
``dtpr.particles.gen_muon`` module. Suppose we want to create instances of ``GenMuon`` based
on the root event's entry when an event is instantiated. This requires specifying the following in a `YAML`
configuration file under the ``particle_types`` section:

.. rubric:: config.yaml

.. code-block:: yaml

    particle_types:
        genmuons:
            class: 'dtpr.particles.gen_muon.GenMuon'
            n_branch_name: 'gen_nGenParts'
            conditioner: # optional
                property: 'gen_pdgId'
                condition: "==13"
            sorter: # optional
                by: 'pt'
                reverse: True

The ``Event`` class will create **n** (determined for the value of the ``gen_nGenParts`` branch) instances of the ``GenMuon`` class.
The ``conditioner`` and ``sorter`` are optional. The ``conditioner`` filters the root event's 
entry based on specified conditions, and the ``sorter`` orders the created particles. Ensure 
that the information required to build the particles is present in the root event's entry. The way to 
create an event instance should be like this:

.. code-block:: python

    from ROOT import TFile
    from dtpr.base import Event
    from dtpr.utils.config import EVENT_CONFIG

    # First, you need to change the configuration file path. If not, 
    # it will work with the default one dtpr/utils/templates/config_run_template.yaml.
    # You can also use the latter to define your own configuration file.
    EVENT_CONFIG.change_config(config_path="path/to/config.yaml")

    with TFile("DTDPGNtuple_12_4_2_Phase2Concentrator_Simulation_99.root", "read") as ntuple:
        tree = ntuple["dtNtupleProducer/DTTREE;1"]

        for iev, ev in enumerate(tree):
            event = Event(ev, iev=iev)
            # Print the event summary
            print(event)
            if iev == 1: break # Just to show the first two events

.. rubric:: Output

.. code-block:: text

    >> ------ Event 0 info ------ 
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
    >> ------ Event 1 info ------ 
    + Genmuons 
        * Number of genmuons: 1 
        * Muon 0 
        --> GenPart Idx: 0 
        --> pT: 1797.72 GeV 
        --> Eta: -0.54 
        --> Phi: -0.28 
        --> Matched segments indices: [] 
        --> Matched segments location: [] 
        --> Stations traversed: [] 
        --> Not showered 

The ``Event`` class is not limited to using Ntuple information. It can be used just like a container
by manually adding any type of attribute that you consider necessary. A simple example of this is, 
for instance, adding customized showers to the event. For practice, let us take
the class ``Shower`` from the ``dtpr.particles.shower`` module just to illustrate how to add
objects to the event:

.. code-block:: python

    from dtpr.base import Event
    from dtpr.particles.shower import Shower

    event = Event(iev=0)
    showers = [Shower(iShower=i) for i in range(5)]
    event.showers = showers

    print(event)
    print(event.showers[-1])

.. rubric:: Output

.. code-block:: text

    >> ------ Event 0 info ------ 
    + Showers 
        * Number of showers: 5 
    >> ------ Shower 4 info ------ 
    + Wh: None, Sc: None, St: None, Bx: None, Ndigis: 0, Avg_pos: None, Avg_time: None, Eq2emulator: False 

.. autoclass:: dtpr.base.Event
    :members:
    :private-members: _build_particles
    :special-members: __init__, __str__, __getter__,__setter__