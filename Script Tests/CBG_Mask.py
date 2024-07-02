# This file contains a first test to design the mask with using CBGs
# Just a playground to test some of the functions from the tutorials

import samplemaker.layout as smlay  # used for layout
import samplemaker.makers as sm  # used for drawing
# from samplemaker.viewers import GeomView  # Used to inspect drawing before viewing

# from samplemaker.devices import Device
import samplemaker.devices as smdev  # used for device function

import numpy as np
import Collection


# Create a simple mask layout
themask = smlay.Mask("Mask_CBG_gap")


geomE = sm.GeomGroup()

dev = smdev.Device.build_registered("CUSTOM_CBG")

# To create a table, we can use the DeviceTable() function in the layout package
tab = smlay.DeviceTable(
    dev, 3, 6, 
    {"Rc": np.linspace(0.35, 0.37, 3), "gap_index": np.linspace(1,3,3)}, 
    {"w_Air": np.linspace(0.35, 0.4, 6)}
)

# Autoalign with with spacing 5 and 5 in x,y direction
tab.auto_align(5, 5, numkey=1)

# set Annotations on the top and left side
tab.set_annotations(
    smlay.DeviceTableAnnotations(
        "Rc=%R0", "W=%C0", 80, 40, ("Rc",), ("w_Air",), right=False, below=False
    )
)


# Add device table to x,y = 150,150
themask.addDeviceTable(tab, 150, 150)

# Export to GDS
themask.exportGDS()
