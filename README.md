
Cortical surface           |  Subcortical structures
:-------------------------:|:-------------------------:
![Cortical surface](output/pcaCover/cortical_1.png)  |  ![Subcortical structures](output/pcaCover/subcortical_1.png) 

# Brain colouring software 
Author: Razvan V. Marinescu - razvan@csail.mit.edu


INPUT: list of numbers representing pathology at each region in the brain

OUTPUT: brain image coloured according to levels of pathology in those regions


# Installation

## Using the Docker container

In order to remove the need to install blender and the python libraries, we made a container which has blender and this repository already pre-installed and ready to run.

First pull the docker container locally:

```  ```


Copy the image out of the docker container to the home directory ~/ :

``` sudo docker cp 9f52258c25f6:/home/brain-coloring/output/pcaCover/cortical_0.png ~/ ```

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

