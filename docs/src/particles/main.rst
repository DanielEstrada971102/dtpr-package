particles
=========

In the context of ``dtpr``, a particle is a class that represents any object you would like to
add to an ``Event`` instance. The purpose of defining a particle is to easily access the 
information of root Ntuple and to have the possibility to build them on the fly each time an Event
instance is produced. However, you can also manually add a particle to an event instance if desired.

You can generate a skeleton of a particle class using the dtpr command as follows:

.. code-block:: bash

    dtpr create particle --name TestParticle -o [output_folder]

This will create a new file called `testparticle.py` in the specified output folder with the following
content:

.. code-block:: python

    from dtpr.utils.functions import color_msg

    class TestParticle(object):
        # Define the attributes of the class in the __slots__ list to save memory
        __slots__ = ["index"] # add more attributes here

        def __init__(self, index, ev=None):
            """
            Initialize a TestParticle instance.

            :param index: The index of the particle.
            :type index: int
            :param ev: The root event entry containing event data.
            """
            self.index = index
            if ev is not None: # constructor with root event entry info
                # Extract the needed attributes from the root event entry
                # and assign them to the corresponding attributes of the instance
                pass
            else: # constructor with explicit info
                # Initialize the attributes of the instance with the input arguments
                pass

        def to_dict(self):
            """
            Convert the TestParticle instance to a dictionary.

            :return: A dictionary representation of the TestParticle instance.
            :rtype: dict
            """
            return {attr: getattr(self, attr) for attr in self.__slots__}

        def __str__(self, indentLevel=0):
            """
            Generate a string representation of the TestParticle instance.

            :param indentLevel: The indentation level for the summary.
            :type indentLevel: int
            :return: The particle summary.
            :rtype: str
            """
            summary = [
                color_msg(
                    f"------ Particle {self.index} info ------",
                    color="yellow",
                    indentLevel=indentLevel,
                    return_str=True,
                )
            ]

            summary.append(
                color_msg(
                    ", ".join(
                        [
                            f"{attr.capitalize()}: {getattr(self, attr)}"
                            for attr in self.__slots__
                            if attr != "index"
                        ]
                    ),
                    indentLevel=indentLevel + 1,
                    return_str=True,
                )
            )
            return "\n".join(summary)

To have your particle type generated on the fly when an Event instance is created,
you need to add the necessary information into an event configuration `YAML` file as described in 
the :doc:`../base/event` section. You can also generate a skeleton of an event configuration file using the ``dtpr`` 
bash command as follows:

.. code-block:: bash

    dtpr create event-config -o [output_folder]

This will create a new file called `event_config.yaml` in the specified output folder with the 
following content, where you can include your particle type:

.. code-block:: yaml

    # List of particle types
    # Add or delete the particle types as needed
    particle_types:
    digis:
        class: 'dtpr.particles.digi.Digi'
        n_branch_name: 'digi_nDigis'
        sorter:
        by: 'BX'
    segments:
        class: 'dtpr.particles.segment.Segment'
        n_branch_name: 'seg_nSegments'
    tps:
        class: 'dtpr.particles.ph2tp.Ph2tp'
        n_branch_name: 'ph2TpgPhiEmuAm_nTrigs'
    genmuons:
        class: 'dtpr.particles.gen_muon.GenMuon'
        n_branch_name: 'gen_nGenParts'
        conditioner: 
        property: 'gen_pdgId'
        condition: "==13"
        sorter:
        by: 'pt'
        reverse: True
    emushowers:
        class: 'dtpr.particles.shower.Shower'
        n_branch_name: 'ph2Shower_station'


Then, to use your configuration, ensure that the correct file path is set in `EVENT_CONFIG` by doing:


.. code-block:: python

    from dtpr.utils.config import EVENT_CONFIG

    EVENT_CONFIG.change_config(config_path="path/to/event_config.yaml")
    # your code here...


The following particles are available in the package:

.. toctree::
    :maxdepth: 1
    :caption: Classes:

    digi
    gen_muon
    ph2tp
    segment
    shower
    simhit