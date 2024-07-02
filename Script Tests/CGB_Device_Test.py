# This file is just for testing the class for CBGs
# The actual implementation of is to be found in 'Collection.py'

# Import libraries for layout, geometry objects, devices and viewers
import samplemaker.layout as smlay  
import samplemaker.makers as sm  
from samplemaker.devices import Device
from samplemaker.viewers import DeviceInspect

import numpy as np


class CBG(Device):
    """Defines Circular Bragg Gratings with a gap between the center rings and the outer ones
    The mask corresponds to the material to be etched
    Args:
        Device (_type_): _description_
    """

    def initialize(self):
        # This function setups some variable, like the unique identifier name
        self.set_name("CUSTOM_CBG")
        self.set_description("Circular Bragg Grating")

    def parameters(self):
        self.addparameter(
            "w_GaAs",
            0.360,
            "width of GaAs ring in um,",
            param_type=float,
            param_range=(0, 2),
        )
        self.addparameter(
            "Rc",
            0.360,
            "Radius of the Center Disk in um",
            param_type=float,
            param_range=(0, 2),
        )
        self.addparameter(
            "w_Air",
            0.300,
            "width of Air Gap in um",
            param_type=float,
            param_range=(0, 2),
        )
        self.addparameter(
            "n_rings", 4, "Number of Rings", param_type=int, param_range=(0, 20)
        )
        self.addparameter(
            "x0", 0, "Center Position", param_type=float, param_range=(0, 2)
        )
        self.addparameter(
            "y0", 0, "Center Position", param_type=float, param_range=(0, 2)
        )

        # Arc Parameters
        self.addparameter(
            "elC_n",
            4,
            "Number of electrical contacts",
            param_type=int,
            param_range=(0, 20),
        )
        self.addparameter(
            "elC_w",
            0.1,
            "Width of the electrical contacts ",
            param_type=float,
            param_range=(0, 2),
        )
        self.addparameter(
            "elC_relAngle",
            90,
            "relative angle of the el. contacts to the next ring",
            param_type=float,
            param_range=(0, 90),
        )

        self.addparameter(
            "gap_index",
            0,
            "Index at which the gap starts. 0: no gap",
            param_type=int,
            param_range=(0, 20),
        )
        self.addparameter(
            "gap_width",
            1,
            "width of the gap",
            param_type=int,
            param_range=(0, 10),
        )

    def geom(self):
        """Defines the geometry of the material to be etched away

        Returns:
            geometry: The pattern of the CBG as a geomety element
        """
        # Load the parameters set in init
        params = self.get_params(cast_types=True, clip_in_range=True)

        # Calculate the Angles for electrical contacts
        alpha = 0  # Central Angle of Ring n
        angle_diff = 360 / params["elC_n"]  # Angle between el. contacts in Ring n

        # Define empty CBG geometry
        CBG = sm.GeomGroup()

        # Loop over all rings
        for n in range(0, int(params["n_rings"] + 1)):
            # Define Ring Radius
            r_center = (
                params["Rc"]
                + params["w_Air"] / 2
                + n * (params["w_Air"] + params["w_GaAs"])
            )

            # In case a gap is defined add it between the ring
            if params["gap_index"] > 0 and n > params["gap_index"]:
                r_center += params["gap_width"]

            # Calculate the opening angle for ring n, that corresponds to a width elC_w of the el contacts
            beta = np.degrees(
                np.arcsin(params["elC_w"] / (2 * (r_center - params["w_Air"] / 2)))
            )

            # Draw the individual rings composed of elC_n arcs
            for i in range(0, int(params["elC_n"])):

                # Calculate start and stop angle for the arc
                angle_min = alpha + i * angle_diff + beta
                angle_max = alpha + (i + 1) * angle_diff - beta

                # Draw the acts with the set parameters
                CBG += sm.make_arc(
                    params["x0"],
                    params["y0"],
                    r_center,
                    r_center,
                    0,
                    params["w_Air"],
                    angle_min,
                    angle_max,
                    to_poly=True,
                )
            # Update the center angle for the next ring
            alpha += params["elC_relAngle"]
        return CBG

# Create an empty mask layout
themask = smlay.Mask("Mask_CBG")

# Create an empty geometry group
geomE = sm.GeomGroup()

# Add the CBG with standard parameters
CBG_dev = CBG.build()

# View the structure in the device imspector
DeviceInspect(CBG_dev)

# CBG_dev.set_param("n_rings", 2)
# geomE += CBG_dev.run()


# # Create a Cell with a single CBG
# themask.addCell("BASIS_CELL",geomE)

# geomMask = sm.make_aref(0,50,"BASIS_CELL",geomE,3, 4, 25.0, 0.0, 0.0, 20.0)

# # Let's add all to main cell
# themask.addToMainCell(geomMask)

# themask.exportGDS()
