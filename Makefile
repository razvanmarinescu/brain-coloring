all:
	configFile=config.py blender --background --python blendCreateSnapshot.py
	# remove --background to run blender interactively