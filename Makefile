cortical:
	cortical=1 blender --background --python blendCreateSnapshot.py
subcortical:
	cortical=0 blender --background --python blendCreateSnapshot.py

cortical_pcaPaper:
	cortical=1 blender --background --python blendCreateSnapshot_BrainPaperCover.py
