
INPUT_FILE = 'data/pcaCover.csv'

OUTPUT_FOLDER = 'output/pcaCover'

# either pial (with gyri/sulci) or inflated (smooth)
BRAIN_TYPE = 'pial'

# either cortical-outer, cortical-inner or subcortical
IMG_TYPE = 'cortical-inner'

# what colours to use for showing brain pathology
# e.g. if the range of pathology is [0,3],
# then you need four colors (the first one is for pathology 0, i.e. no pathology)
# a pathology at 1.3 will interpolate between the second and third color
COLORS_RGB = [(1,1,1), (1,1,0), (1,0.4,0), (1,0,0)] # white -> yellow -> orange -> red
# COLORS_RGB = [(1,1,1), (1,0,0), (1,0,0), (1,0,0)] # white -> red -> red -> red

# output image resolution for X,Y in pixels
RESOLUTION = (1200, 900)

# default is white
BACKGROUND_COLOR = (1,1,1)

# to change camera viewing angle and other advanced settings, look into blendHelper.py:setCamera()
# for luminosity settings, look into blendHelper.py:setLamp()

# map the names of each 3D cortical structure to be coloured to the name of the structure you have in your atlas.
# only change the right-hand side values, as the left-hand side are used by blender.
cortAreasIndexMap = {
  'bankssts':-1, # -1 means do not colour this region
  'caudalanteriorcingulate':'anterior cingulate',
  'caudalmiddlefrontal':'medial frontal',
  'cuneus':'cuneus',
  'entorhinal':'entorhinal',
  'frontalpole':'frontal pole',
  'fusiform':'fusiform',
  'inferiorparietal':'angular',
  'inferiortemporal':'inferior temporal',
  'insula':'anterior insula', # should be avg of anterior and posterior insula
  'isthmuscingulate':'posterior cingulate',
  'lateraloccipital':'inferior occipital',
  'lateralorbitofrontal':'medial frontal',
  'lingual':'lingual',
  'medialorbitofrontal':'medial frontal',
  'middletemporal':'middle temporal',
  'paracentral':'precentral', # should be avg of pre-central and post-central though
  'parahippocampal':'parahippocampal',
  'parsopercularis':'central operculum',
  'parsorbitalis':'anterior orbital',
  'parstriangularis':'angular',
  'pericalcarine':'calcarine',
  'postcentral':'postcentral',
  'posteriorcingulate':'posterior cingulate',
  'precentral':'precentral',
  'precuneus':'precuneus',
  'rostralanteriorcingulate':'anterior cingulate',
  'rostralmiddlefrontal':'middle frontal',
  'superiorfrontal':'superior frontal',
  'superiorparietal':'superior parietal',
  'superiortemporal':'superior temporal',
  'supramarginal':'supramarginal',
  'temporalpole':'temporal pole',
  'transversetemporal':'planum temporale',
  'unknown':-1}

# do the same map for subcortical
# only change the right-hand side values
subcortAreasIndexMap = {
  'Left-Accumbens-area':'accumbens', # -1 means do not colour this region
  'Left-Caudate':'caudate',
  'Left-Cerebellum-White-Matter':-1,
  'Left-Inf-Lat-Vent':-1,
  'Left-Pallidum':'pallidum',
  'Left-Thalamus-Proper':'thalamus',
  'Left-Amygdala':'amygdala',
  'Left-Cerebellum-Cortex':-1,
  'Left-Hippocampus':'hippocampus',
  'Left-Lateral-Ventricle':-1,
  'Left-Putamen':'putamen',
  'Left-VentralDC':'ventral dc'}
