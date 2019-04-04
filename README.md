![Alt text](output/pcaCover/cortical_1.png?raw=true "Generated brain image")


# Brain colouring software

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
	
3. run make

