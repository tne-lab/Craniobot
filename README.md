# "Craniobot", a craniotomy robot for small rodents.
This is a simple 3-axis high-prcision robot designed to perform craniotomies on small rodents. 
These small craniotomies are often needed for electrode implantation and neuroscience research.

## General Description
This small 3-axis craniotomy robot consists of three ThorLabs 2.5 cm linear actuators, 
a 3D printed streotaxi alignment tool, a 3D printed drill holder, some mounting hardware, 
and a python GUI interface developed by Flavio JK da Silva and Mark Scatza.  The 3D printed parts were designed using FreeCAD.  
The *.stl files as well as the FreeCAD files are available here in the PARTS folder.

## GUI interface
Control of the robot is done using setupGUI2.0.py. Drill_holes2.py and drill_craniotomy.py are called by the GUI. 
Some ThorLabs control functions are included in the throlabs_apt_master folder. The RESOURCES folder contains GUI elements, logos, 
graphics and a function to calculates the best-fit plane through 5 points marked on the surface of the skull.  
After the skull is surgically exposed,  The robot is pushed against the stereotaxic equipment to align the XY plane of the robot with the XY plane of the sterotaxic equipment.
Then use the XYZ motion control buttons to move the drill to the rodent (0,0,0) point (the Bregma location) to establish a point ofrdina correspondance between the robot and rodent coordinates.  
This best-fit plane can be used if the rodent skull surface is not completely horizontal. However it is not generally required as the 
surface of the skull is easily oriented along a horizontal plane using stereotaxic equipment.  
The GUI displays the drill current position, as well a record of where cuts have been made.  Each pass of the craniotomy is only 0.1 mm deep.  
After each pass the user has the option of doing another pass, each 0.1 mm deeper.  Screw holes are set to be 1.0 mm deep, but the user has 
the option of going deeper in 0.1 mm increments.  The position of the drill along any axis can be manipulated by the control buttons on the GUI.
![][GUI]




[GUI]: https://github.com/tne-lab/Craniobot/blob/master/RESOURCES/GUI.PNG "GUI" 
