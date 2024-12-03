"""Main CLI interface"""

import sys
import argparse
import warnings

from dtpr.utils.functions import warning_handler, error_handler
from dtpr.utils.create_templates import create_ntuple_class_template, create_particle_class_template, create_event_config_template

warnings.filterwarnings(action="once", category=UserWarning)
# Set the custom warning handler
warnings.showwarning = warning_handler
# Set the custom error handler
sys.excepthook = error_handler


def main():
    parser = argparse.ArgumentParser(
        description="Command Line Interface for the dtpr-package, providing tools for produce useful class from templates."
    )
    subparsers = parser.add_subparsers(required=True, dest="command")

    # -------------------------------------- "create" command --------------------------------------
    create_subparser = subparsers.add_parser("create", help="Command for create from any of the available templates.")
    create_subparsers = create_subparser.add_subparsers(required=True, dest="subcommand")

    # -----------> "particle" subcommand
    create_particle_parser = create_subparsers.add_parser(
        "particle",
        help="Create a new particle class from the template.",
    )
    create_particle_parser.add_argument(
        "-n", "--name",
        dest="name",
        type=str,
        default="MyParticle",
        help=(
            "Name of the new particle class. "
            "By default, the class will be named 'MyParticle'."
        ),
    )
    create_particle_parser.add_argument(
        "-o", "--output",
        dest="output",
        type=str,
        default="./",
        help="Output folder where put the new class.",
    )
    create_particle_parser.set_defaults(
        func=lambda args: create_particle_class_template(args.name, args.output),
    )

    # -----------> "ntuple" subcommand
    create_ntuple_parser = create_subparsers.add_parser(
        "ntuple",
        help="Create a new ntuple class from the template.",
    )
    create_ntuple_parser.add_argument(
        "-n", "--name",
        dest="name",
        type=str,
        default="MyNtuple",
        help=(
            "Name of the new ntuple class. "
            "By default, the class will be named 'MyNtuple'."
        ),
    )
    create_ntuple_parser.add_argument(
        "-o", "--output",
        dest="output",
        type=str,
        default="./",
        help="Output folder where put the new class.",
    )
    create_ntuple_parser.set_defaults(
        func=lambda args: create_ntuple_class_template(args.name, args.output),
    )

    # -----------> "event-config" subcommand
    create_event_config_parser = create_subparsers.add_parser(
        "event-config",
        help="Create a new event configuration file from the template.",
    )
    create_event_config_parser.add_argument(
        "-o", "--output",
        dest="output",
        type=str,
        default="./",
        help="Output folder where to put the new event configuration file.",
    )
    create_event_config_parser.set_defaults(
        func=lambda args: create_event_config_template(args.output),
    )

    # Parse the command line
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
