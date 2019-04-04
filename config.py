
INPUT_FILE = 'data/pcaCover.csv'

OUTPUT_FOLDER = 'output/pcaCover'

# pial or inflated
BRAIN_TYPE = 'pial'

# can be either cortical or subcortical
IMG_TYPE = 'cortical'

# white -> yellow -> orange -> red
COLORS_RGB = [(1,1,1), (1,1,0), (1,0.4,0), (1,0,0)]
# COLORS_RGB = [(1,1,1), (1,0,0), (1,0,0), (1,0,0)]

# output image resolution for X,Y in pixels
RESOLUTION = (2400, 1800)

# default is white
BACKGROUND_COLOR = (1,1,1)

# to change camera viewing angle and other advanced settings, look into blendHelper.py:setCamera()
# for luminosity settings, look into blendHelper.py:setLamp()

# map the names of each 3D cortical structure to be coloured to the name of the structure you have in your atlas.
cortAreasIndexMap = {
  'bankssts':-1,
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

# do the same map for subcortical structures
subcortAreasIndexMap = {
  'Left-Accumbens-area':-1,
  'Left-Caudate':-1,
  'Left-Cerebellum-White-Matter':-1,
  'Left-Inf-Lat-Vent':-1,
  'Left-Pallidum':-1,
  'Left-Thalamus-Proper':-1,
  'Left-Amygdala':'amygdala',
  'Left-Cerebellum-Cortex':-1,
  'Left-Hippocampus':'hippocampus',
  'Left-Lateral-Ventricle':-1,
  'Left-Putamen':-1,
  'Left-VentralDC':'ventral dc'}