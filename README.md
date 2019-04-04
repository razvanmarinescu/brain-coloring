
Cortical surface           |  Subcortical structures
:-------------------------:|:-------------------------:
![Cortical surface](output/pcaCover/cortical_1.png)  |  ![Subcortical structures](output/pcaCover/subcortical_1.png) 

# Brain colouring software 
Author: Razvan V. Marinescu - razvan@csail.mit.edu


INPUT: list of numbers representing pathology at each region in the brain

OUTPUT: brain image coloured according to levels of pathology in those regions

Instructions:

1. simply generate the list of pathology numbers according to the format in data/pcaCover.csv  

2. change configuration file config.py
	- input file: set to your input file
	- brain type: pial or cortical
	- colours to show pathology
	- the mapping between your atlas the 3D brain regions that will be coloured
	- image resolution, etc ...
	
3. run using the Makefile command
	
	``` make ```

