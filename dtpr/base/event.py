# This module contains the Event class, which is used to build particles from the Ntuple root entry.

# -- Import modules -- #
import os
import warnings
from importlib import import_module
from dtpr.utils.config import RUN_CONFIG
from dtpr.utils.functions import color_msg

class Event:
    __slots__ = ["iev", "particles"]

    def __init__(self, root_ev=None, iev=-1):
        """
        Initialize an Event instance.

        :param root_ev: The Ntuple root entry containing event data.
        :param iev: The event index.
        """

        self.iev = iev
        self.particles = {}  # Initialize an empty dictionary for particles

        if root_ev is not None:
            if RUN_CONFIG.particle_types:
                for ptype, pinfo in RUN_CONFIG.particle_types.items():
                    self.build_particles(root_ev, ptype, pinfo)
            else:
                warnings.warn("No particle types defined in the configuration file. Initializing an empty Event instance.")

    def __getattr__(self, name):
        """
        Override __getattr__ to return particles from the particles dictionary.

        :param name: The name of the attribute.
        :return: The list of particles if the name matches a particle type, or the attribute value.
        :raises AttributeError: If the attribute is not found and not a particle type.
        """
        if name in self.__slots__:
            return super().__getattr__(name)
        if name in self.particles:
            return self.particles[name]
        raise AttributeError(f"'Event' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        """
        Override __setattr__ to store particles in the particles dictionary if the name matches a particle type.

        :param name: The name of the attribute.
        :param value: The value to set.
        """
        if name in self.__slots__ or name == "particles":
            super().__setattr__(name, value)
        else:
            self.particles[name] = value

    def __str__(self, indentLevel=0):
        """
        Generate a string representation of the event summary.

        :param indentLevel: The indentation level for the summary.
        :return: The event summary.
        """
        summary = [color_msg(f"------ Event {self.iev} info ------", color="yellow", indentLevel=indentLevel, return_str=True)]
        for ptype, particles in self.particles.items():
            summary.append(color_msg(f"{ptype.capitalize()}", color="green", indentLevel=indentLevel+1, return_str=True))
            summary.append(color_msg(f"Number of {ptype}: {len(particles)}", color="purple", indentLevel=indentLevel+2, return_str=True))
            if ptype == "genmuons":
                for igm, gm in enumerate(particles):
                    summary.append(color_msg(f"Muon {igm}", indentLevel=indentLevel+2, return_str=True))
                    summary.append(gm.__str__(indentLevel=indentLevel+3))
            elif ptype == "segments":
                phiseg = [f"({seg.index:.2f}, {seg.phi:.2f}, {seg.eta:.2f})" for seg in particles]
                summary.append(color_msg(f"(iSeg, Phi, eta): {phiseg[:5]}", indentLevel=indentLevel+2, return_str=True))
            # Add summaries for other particle types as needed
        return "\n".join(summary)

    def build_particles(self, root_ev, ptype, pinfo):
        """
        Build particles of a specific type based on the information provided in the root event entry.

        :param root_ev: The Ntuple root entry containing event data.
        :param ptype: The type of particles to build. It will be the name of the attribute in the Event instance.
        :param pinfo: The information dictionary for the particle type builder. It should contain the class builder path, the name of the branch to infer the number of particles, and optional conditions and sorting parameters.
        """
        module_name, class_name = pinfo["class"].rsplit('.', 1)
        module = import_module(module_name)
        ParticleClass = getattr(module, class_name)

        num_particles = n if isinstance(n := eval(f"root_ev.{pinfo['n_branch_name']}") , int) else len(n)
        if "conditioner" in pinfo:
            conditioner = pinfo["conditioner"]
            particles = [
            ParticleClass(i, root_ev)
            for i in range(num_particles)
            if abs(eval(f"root_ev.{conditioner['property']}[{i}]{conditioner['condition']}")) #abs should not be hardcoded
            ]
        else:
            particles = [ParticleClass(i, root_ev) for i in range(num_particles)]

        if "sorter" in pinfo:
            sorter = pinfo["sorter"]
            particles = sorted(particles, key=lambda p: getattr(p, sorter["by"]), reverse=sorter["reverse"] if "reverse" in sorter else False)

        setattr(self, ptype, particles)  # Add the particles to the Event instance

    def filter_particles(self, particle_type, **kwargs):
        """
        Filter all particles of a specific type that satisfy given attributes.

        :param particle_type: The type of particles to filter (e.g., 'digis', 'segments', 'tps').
        :param kwargs: Key-value pairs of attributes to filter by (e.g., wh=1, sc=2, st=3).
        :return: A list of filtered particles. If no particles are found, an empty list is returned.
        :raises ValueError: If invalid keys are provided for filtering.
        """
        if particle_type not in self.particles:
            warnings.warn(f"Invalid particle type {particle_type} to apply filter. Valid types are: {list(self.particles.keys())}")
            return []

        particles = self.particles.get(particle_type, [])

        if not particles:
            return []  # Return an empty list if there are no particles

        valid_keys = set()
        for particle in particles:
            valid_keys.update(list(particle.to_dict().keys()))

        if not all(key in valid_keys for key in kwargs):
            raise ValueError(f"Invalid keys to filter. Valid keys are: {valid_keys}")

        def match(particle, kwargs):
            return all(getattr(particle, key) == value for key, value in kwargs.items())

        return [particle for particle in particles if match(particle, kwargs)]

if __name__ == "__main__":
    """
    Example of how to use the Event class to build particles and analyze them.
    """
    from ROOT import TFile
    from dtpr.particles.shower import Shower
    _maxevents = 1
    with TFile(os.path.abspath(os.path.join(os.path.dirname(__file__), "../utils/templates/DTDPGNtuple_12_4_2_Phase2Concentrator_Simulation_101.root")), "read") as ntuple:
        tree = ntuple["dtNtupleProducer/DTTREE;1"]

        for iev, ev in enumerate(tree):
            event = Event(ev, iev=iev)
            # Print the event summary
            print(event)
            shower = Shower(iShower=0, wh=1, sc=1, st=1, BX=0, nDigis=2, avg_pos=12.3, avg_time=0.5)
            event.test_showers = [shower]
            print(event)
            if iev + 1 == _maxevents: break
