# -*- coding: utf-8 -*-
"""
Device Collection

"""

import samplemaker.makers as sm  # used for drawing
from samplemaker.devices import (
    Device,
    registerDevicesInModule,
)
import numpy as np


class CBG(Device):
    """Defines Circular Bragg Gratings with a gap between the center rings and the outer ones
    The mask corresponds to the material to be etched
    A sketch of the parameters can be found in "Sketch_Definitions.png"

    Parameters:
        -   Rc      :   Radius of center Disk in um
        -   w_Air   :   width of Air Gaps in um
        -   w_GaAs  :   width of GaAs rings in um
        -   n_rings :   No of rings (GaAs rings, not etched rings)
        -   x0      :   center position x in um
        -   y0      :   center position y in um
        
        -   elC_n           :   No of el. contacts
        -   elC_w           :   width of el. contacts in um
        -   elC_relAngle    :   relative angle between el. contacts

        -   gap_index       :   after which ring the gap is supposed to be (0: no gap)
        -   gap_width       :   width of the gap in um

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


registerDevicesInModule(__name__)


## Keep for now, old definition

# class CBG_oldDef(Device):
#     """Defines Circular Bragg Gratings with a gap between the center rings and the outer ones

#     Args:
#         Device (_type_): _description_
#     """

#     def initialize(self):
#         # This function setups some variable, like the unique identifier name
#         self.set_name("CUSTOM_CBG")
#         self.set_description("Circular Bragg Grating")

#     def parameters(self):
#         # define all the paramters of the device and their default values.
#         # You can specify what type the parameter has and what it the minimum-maximum allowed values
#         # Default is float and range (0,infinity) for all parameters.
#         self.addparameter(
#             "p", 0.360, "Periodicity", param_type=float, param_range=(0, 2)
#         )
#         self.addparameter(
#             "Rc",
#             0.360,
#             "Radius of the Center Disk",
#             param_type=float,
#             param_range=(0, 2),
#         )
#         self.addparameter(
#             "dc", 0.67, "Duty Cycle", param_type=float, param_range=(0, 1)
#         )
#         self.addparameter(
#             "n_rings", 4, "Number of Rings", param_type=int, param_range=(0, 20)
#         )
#         self.addparameter(
#             "x0", 0, "Center Position", param_type=float, param_range=(0, 2)
#         )
#         self.addparameter(
#             "y0", 0, "Center Position", param_type=float, param_range=(0, 2)
#         )

#         # Arc Parameters
#         self.addparameter(
#             "elC_n",
#             4,
#             "Number of electrical contacts",
#             param_type=int,
#             param_range=(0, 20),
#         )
#         self.addparameter(
#             "elC_w",
#             0.1,
#             "Width of the electrical contacts ",
#             param_type=float,
#             param_range=(0, 2),
#         )
#         self.addparameter(
#             "elC_relAngle",
#             90,
#             "relative angle of the el. contacts to the next ring",
#             param_type=float,
#             param_range=(0, 90),
#         )

#         self.addparameter(
#             "gap_index",
#             0,
#             "Index at which the gap starts. 0: no gap",
#             param_type=int,
#             param_range=(0, 20),
#         )
#         self.addparameter(
#             "gap_width",
#             1,
#             "width of the gap",
#             param_type=int,
#             param_range=(0, 10),
#         )

#     def geom(self):
#         params = self.get_params(cast_types=True, clip_in_range=True)

#         # Calculate Values
#         w = (1 - params["dc"]) * params["p"]

#         # Angles
#         alpha = 0  # Central Angle of Ring n
#         angle_diff = 360 / params["elC_n"]  # Angle between el. contacts in Ring n
#         CBG = sm.GeomGroup()

#         # Loop over all rings
#         for n in range(0, int(params["n_rings"] + 1)):
#             # Define Ring Radius
#             r_center = params["Rc"] + w / 2 + n * params["p"]
#             if params["gap_index"] > 0 and n > params["gap_index"]:
#                 r_center += params["gap_width"]
#             beta = np.degrees(np.arcsin(params["elC_w"] / (2 * (r_center - w / 2))))

#             print(
#                 f"Ring {n}: center radius = {r_center}, width = {w} opening half angle beta = {beta}"
#             )
#             for i in range(0, int(params["elC_n"])):
#                 # Draw Arcs
#                 angle_min = alpha + i * angle_diff + beta
#                 angle_max = alpha + (i + 1) * angle_diff - beta

#                 CBG += sm.make_arc(
#                     params["x0"],
#                     params["y0"],
#                     r_center,
#                     r_center,
#                     0,
#                     w,
#                     angle_min,
#                     angle_max,
#                     to_poly=True,
#                 )
#             alpha += params["elC_relAngle"]
#         return CBG
