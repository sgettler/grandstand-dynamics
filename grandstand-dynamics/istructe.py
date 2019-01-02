# istructe.py
"""IStructE analysis module.

This module implements grandstand dynamics calculations in accordance with the
IStructE performance requirements.
"""

import argparse

import grandstand



class IStructE:
    """IStructE analysis object.

    Attributes:
        options: analsis options
    """

    TITLE = "SPS Terraces IStructE Dynamics Analysis"
    VERSION = "0.0"

    def __init__(self, options):
        """Set analysis options."""
        print(IStructE.TITLE, IStructE.VERSION)
        self.options = options

    def load(self):
        """Load the model results from file."""
        with open(self.options.inputfile, "rb") as xmlfile:
            self.model = grandstand.load_sap2000_xml(xmlfile,
                self.options.verbose)



if __name__ == '__main__':
    """Run analysis."""
    parser = argparse.ArgumentParser()
    parser.add_argument("inputfile", help="FEA model source")
    parser.add_argument("--scenario", help="IStructE event scenarios to "
        "check (default is all)", type=int, choices=[2, 3, 4], nargs="*",
        default=[2, 3, 4])
    parser.add_argument("--verbose", help="verbose mode", action="store_true")

    istructe = IStructE(parser.parse_args())
    istructe.load()
    for scenario in istructe.options.scenario:
        pass
