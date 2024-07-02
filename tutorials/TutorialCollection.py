# -*- coding: utf-8 -*-
"""
Tutorial device collection

"""

# This is how you create a collection of devices, just add all the classes in this file
# Check the end of this file, we run a command to make samplemaker aware of our devices

import samplemaker.makers as sm # used for drawing
from samplemaker.devices import Device, registerDevicesInModule # We need the registerDevicesInModule function
import numpy as np


# class definition
class FreeFreeMembrane(Device):
    # We need to implement a few mandatory functions here:
    def initialize(self):
        # This function setups some variable, like the unique identifier name
        self.set_name("CUSTOM_FFM")
        # Also add a description, useful for documenting later
        self.set_description("Free free membrane as in 10.1103/PhysRevB.98.155316, etc etc")
                
    def parameters(self):
        # define all the paramters of the device and their default values.
        # You can specify what type the parameter has and what it the minimum-maximum allowed values
        # Default is float and range (0,infinity) for all parameters.
        self.addparameter("L", 40, "Length of the membrane", param_type=float, param_range=(0.5,150))
        self.addparameter("W", 12.5, "Width of the membrane")
        self.addparameter("tetW", 2, "Tether width")
        self.addparameter("tetOff", 11, "Tether offset from the center")
        self.addparameter("R", 30, "Support ring radius")
        
    def geom(self):
        # This is where we place the commands for drawing!
        # This function should return a GeomGroup
        
        # we can fetch the parameters first to shorten the notation
        # note that you can choose whetner a type cast should be made (i.e. forcing the parameter to be
        # of the type specified in the addparameter command) and if it should be clipped in the allowed range. 
        p = self.get_params(cast_types=True,clip_in_range=True)
        # Draw the membrane
        mem = sm.make_rect(0,0,p["W"],p["L"])
        # Draw tether
        tet = sm.make_rect(0,p["tetOff"],p["R"]*2,p["tetW"])
        # Mirror to get the second one
        tet2 = tet.copy()
        tet2.mirrorY(0)
        mem+=tet+tet2
        # Support ring
        ring = sm.make_circle(0, 0, p["R"],to_poly=True,vertices=64)
        # boolean
        ring.boolean_difference(mem, 1, 1)
        return ring

class CBG(Device):
    """Defines Circular Bragg Gratings with optional electrial contacts

    Args:
        Device (_type_): _description_
    """
    def initialize(self):
        # This function setups some variable, like the unique identifier name
        self.set_name("CUSTOM_CBG")
        self.set_description("Circular Bragg Grating")

    def parameters(self):
        # define all the paramters of the device and their default values.
        # You can specify what type the parameter has and what it the minimum-maximum allowed values
        # Default is float and range (0,infinity) for all parameters.
        self.addparameter(
            "p", 0.360, "Periodicity", param_type=float, param_range=(0, 2)
        )
        self.addparameter(
            "Rc",
            0.360,
            "Radius of the Center Disk",
            param_type=float,
            param_range=(0, 2),
        )
        self.addparameter(
            "dc", 0.67, "Duty Cycle", param_type=float, param_range=(0, 1)
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

    def geom(self):
        params = self.get_params(cast_types=True, clip_in_range=True)

        # Calculate Values
        w = (1 - params["dc"]) * params["p"]

        # Angles
        alpha = 0  # Central Angle of Ring n
        angle_diff = 360 / params["elC_n"]  # Angle between el. contacts in Ring n

        for n in range(0, int(params["n_rings"] + 1)):
            # Get ring diameter
            r_center = params["Rc"] + w / 2 + n * params["p"]
            beta = np.degrees(np.arcsin(params["elC_w"] / (2 * (r_center - w / 2))))

            print(
                f"Ring {n}: center radius = {r_center}, width = {w} opening half angle beta = {beta}"
            )
            for i in range(0, int(params["elC_n"])):
                # Draw Arcs
                angle_min = alpha + i * angle_diff + beta
                angle_max = alpha + (i + 1) * angle_diff - beta
                try:
                    CBG += sm.make_arc(
                        params["x0"],
                        params["y0"],
                        r_center,
                        r_center,
                        0,
                        w,
                        angle_min,
                        angle_max,
                        to_poly=True,
                    )
                except:
                    CBG = sm.make_arc(
                        params["x0"],
                        params["y0"],
                        r_center,
                        r_center,
                        0,
                        w,
                        angle_min,
                        angle_max,
                        to_poly=True,
                    )
            alpha += params["elC_relAngle"]
        return CBG
    
### Important: register all devices in this module
registerDevicesInModule(__name__)