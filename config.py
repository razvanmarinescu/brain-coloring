
INPUT_FILE = 'input/DK_template.csv' # input template should match ATLAS below

OUTPUT_FOLDER = 'output/DK_Output'

# either 'DK', 'Destrieux', 'Tourville' or 'Custom'
ATLAS = 'DK'

# either 'pial' (with gyri/sulci), 'inflated' (smooth) or 'white' (white-matter surface)
BRAIN_TYPE = 'pial'

# either cortical-outer, cortical-inner, subcortical 
# add -right-hemisphere or -left-hemisphere to end of image type to specify view
# image types "top" and "bottom" are available to show asymmetry
IMG_TYPE = 'cortical-outer-right-hemisphere'

# what colours to use for showing brain pathology
# e.g. if the range of pathology is [0,3],
# then you need four colors (the first one is for pathology 0, i.e. no pathology)
# a pathology at 1.3 will interpolate between the second and third color

# NOTE: you can add more than 4 colours (as many as you want), in which case you should increase the range of the input biomarkers.
COLORS_RGB = [(1,1,1), (1,1,0), (1,0.4,0), (1,0,0)] # white -> yellow -> orange -> red
# COLORS_RGB = [(1,1,1), (1,0,0), (1,0,0), (1,0,0)] # white -> red -> red -> red

# output image resolution for X,Y in pixels
RESOLUTION = (1200, 900)

# default is white
BACKGROUND_COLOR = (1,1,1)

# to change camera viewing angle and other advanced settings, look into blendHelper.py:setCamera()
# for luminosity settings, look into blendHelper.py:setLamp()





### Advanced settings, only change if you want to use custom atlas or if you'd like to not color at all some regions #####

# map the names of each 3D cortical structure to be coloured to the name of the structure you have in your atlas.
# only change the right-hand side values, as the left-hand side are used by blender.

# Common customisations:
# 1. to completely remove a region from being displayed, remove both the (key,value) pair.
# 2. to deactivate a region (always color it in default dark gray color), map its value to -1

# NOTE: Always make sure the RHS regions (dict values) below are present in your input .csv file.

### DK atlas ###

# Left-Hand-Side = Blender Regions   Right-Hand-Side = Regions in custom input atlas (.csv INPUT_FILE)
# disable any regions by setting its RHS to -1
cortAreasIndexMapDK = {
  'bankssts':'bankssts',
  'caudalanteriorcingulate':'caudalanteriorcingulate',
  'caudalmiddlefrontal':'caudalmiddlefrontal',
  'cuneus':'cuneus',
  'entorhinal':'entorhinal',
  'frontalpole': 'frontalpole',
  'fusiform':'fusiform',
  'inferiorparietal':'inferiorparietal',
  'inferiortemporal':'inferiortemporal',
  'insula':'insula',
  'isthmuscingulate':'isthmuscingulate',
  'lateraloccipital':'lateraloccipital',
  'lateralorbitofrontal':'lateralorbitofrontal',
  'lingual':'lingual',
  'medialorbitofrontal':'medialorbitofrontal',
  'middletemporal':'middletemporal',
  'paracentral':'paracentral',
  'parahippocampal':'parahippocampal',
  'parsopercularis':'parsopercularis',
  'parsorbitalis':'parsorbitalis',
  'parstriangularis':'parstriangularis',
  'pericalcarine':'pericalcarine',
  'postcentral':'postcentral',
  'posteriorcingulate':'posteriorcingulate',
  'precentral':'precentral',
  'precuneus':'precuneus',
  'rostralanteriorcingulate':'rostralanteriorcingulate',
  'rostralmiddlefrontal':'rostralmiddlefrontal',
  'superiorfrontal':'superiorfrontal',
  'superiorparietal':'superiorparietal',
  'superiortemporal':'superiortemporal',
  'supramarginal':'supramarginal',
  'temporalpole':'temporalpole',
  'transversetemporal':'transversetemporal',
  'unknown':-1 # this is actually the middle region inside the cortical surface. color it as gray
}


### Destrieux atlas ###

# Left-Hand-Side = Blender Regions   Right-Hand-Side = Regions in custom input atlas (.csv INPUT_FILE)
cortAreasIndexMapDestrieux = {'G_Ins_lg_and_S_cent_ins': 'G_Ins_lg_and_S_cent_ins',
  'G_and_S_cingul-Ant': 'G_and_S_cingul-Ant',
  'G_and_S_cingul-Mid-Ant': 'G_and_S_cingul-Mid-Ant',
  'G_and_S_cingul-Mid-Post': 'G_and_S_cingul-Mid-Post',
  'G_and_S_frontomargin': 'G_and_S_frontomargin',
  'G_and_S_occipital_inf': 'G_and_S_occipital_inf',
  'G_and_S_paracentral': 'G_and_S_paracentral',
  'G_and_S_subcentral': 'G_and_S_subcentral',
  'G_and_S_transv_frontopol': 'G_and_S_transv_frontopol',
  'G_cingul-Post-dorsal': 'G_cingul-Post-dorsal',
  'G_cingul-Post-ventral': 'G_cingul-Post-ventral',
  'G_cuneus': 'G_cuneus',
  'G_front_inf-Opercular': 'G_front_inf-Opercular',
  'G_front_inf-Orbital': 'G_front_inf-Orbital',
  'G_front_inf-Triangul': 'G_front_inf-Triangul',
  'G_front_middle': 'G_front_middle',
  'G_front_sup': 'G_front_sup',
  'G_insular_short': 'G_insular_short',
  'G_oc-temp_lat-fusifor': 'G_oc-temp_lat-fusifor',
  'G_oc-temp_med-Lingual': 'G_oc-temp_med-Lingual',
  'G_oc-temp_med-Parahip': 'G_oc-temp_med-Parahip',
  'G_occipital_middle': 'G_occipital_middle',
  'G_occipital_sup': 'G_occipital_sup',
  'G_orbital': 'G_orbital',
  'G_pariet_inf-Angular': 'G_pariet_inf-Angular',
  'G_pariet_inf-Supramar': 'G_pariet_inf-Supramar',
  'G_parietal_sup': 'G_parietal_sup',
  'G_postcentral': 'G_postcentral',
  'G_precentral': 'G_precentral',
  'G_precuneus': 'G_precuneus',
  'G_rectus': 'G_rectus',
  'G_subcallosal': 'G_subcallosal',
  'G_temp_sup-G_T_transv': 'G_temp_sup-G_T_transv',
  'G_temp_sup-Lateral': 'G_temp_sup-Lateral',
  'G_temp_sup-Plan_polar': 'G_temp_sup-Plan_polar',
  'G_temp_sup-Plan_tempo': 'G_temp_sup-Plan_tempo',
  'G_temporal_inf': 'G_temporal_inf',
  'G_temporal_middle': 'G_temporal_middle',
  'Lat_Fis-ant-Horizont': 'Lat_Fis-ant-Horizont',
  'Lat_Fis-ant-Vertical': 'Lat_Fis-ant-Vertical',
  'Lat_Fis-post': 'Lat_Fis-post',
  'Pole_occipital': 'Pole_occipital',
  'Pole_temporal': 'Pole_temporal',
  'S_calcarine': 'S_calcarine',
  'S_central': 'S_central',
  'S_cingul-Marginalis': 'S_cingul-Marginalis',
  'S_circular_insula_ant': 'S_circular_insula_ant',
  'S_circular_insula_inf': 'S_circular_insula_inf',
  'S_circular_insula_sup': 'S_circular_insula_sup',
  'S_collat_transv_ant': 'S_collat_transv_ant',
  'S_collat_transv_post': 'S_collat_transv_post',
  'S_front_inf': 'S_front_inf',
  'S_front_middle': 'S_front_middle',
  'S_front_sup': 'S_front_sup',
  'S_interm_prim-Jensen': 'S_interm_prim-Jensen',
  'S_intrapariet_and_P_trans': 'S_intrapariet_and_P_trans',
  'S_oc-temp_lat': 'S_oc-temp_lat',
  'S_oc-temp_med_and_Lingual': 'S_oc-temp_med_and_Lingual',
  'S_oc_middle_and_Lunatus': 'S_oc_middle_and_Lunatus',
  'S_oc_sup_and_transversal': 'S_oc_sup_and_transversal',
  'S_occipital_ant': 'S_occipital_ant',
  'S_orbital-H_Shaped': 'S_orbital-H_Shaped',
  'S_orbital_lateral': 'S_orbital_lateral',
  'S_orbital_med-olfact': 'S_orbital_med-olfact',
  'S_parieto_occipital': 'S_parieto_occipital',
  'S_pericallosal': 'S_pericallosal',
  'S_postcentral': 'S_postcentral',
  'S_precentral-inf-part': 'S_precentral-inf-part',
  'S_precentral-sup-part': 'S_precentral-sup-part',
  'S_suborbital': 'S_suborbital',
  'S_subparietal': 'S_subparietal',
  'S_temporal_inf': 'S_temporal_inf',
  'S_temporal_sup': 'S_temporal_sup',
  'S_temporal_transverse': 'S_temporal_transverse',
  'Unknown':-1 # this is actually the middle region inside the cortical surface. color it as gray
}


### Tourville atlas ###

# Left-Hand-Side = Blender Regions   Right-Hand-Side = Regions in custom input atlas (.csv INPUT_FILE)
cortAreasIndexMapTourville = {
  'caudalanteriorcingulate': 'caudalanteriorcingulate',
  'caudalmiddlefrontal': 'caudalmiddlefrontal',
  'cuneus': 'cuneus',
  'entorhinal': 'entorhinal',
  'fusiform': 'fusiform',
  'inferiorparietal': 'inferiorparietal',
  'inferiortemporal': 'inferiortemporal',
  'insula': 'insula',
  'isthmuscingulate': 'isthmuscingulate',
  'lateraloccipital': 'lateraloccipital',
  'lateralorbitofrontal': 'lateralorbitofrontal',
  'lingual': 'lingual',
  'medialorbitofrontal': 'medialorbitofrontal',
  'middletemporal': 'middletemporal',
  'paracentral': 'paracentral',
  'parahippocampal': 'parahippocampal',
  'parsopercularis': 'parsopercularis',
  'parsorbitalis': 'parsorbitalis',
  'parstriangularis': 'parstriangularis',
  'pericalcarine': 'pericalcarine',
  'postcentral': 'postcentral',
  'posteriorcingulate': 'posteriorcingulate',
  'precentral': 'precentral',
  'precuneus': 'precuneus',
  'rostralanteriorcingulate': 'rostralanteriorcingulate',
  'rostralmiddlefrontal': 'rostralmiddlefrontal',
  'superiorfrontal': 'superiorfrontal',
  'superiorparietal': 'superiorparietal',
  'superiortemporal': 'superiortemporal',
  'supramarginal': 'supramarginal',
  'transversetemporal': 'transversetemporal',
  'unknown':-1 # this is actually the middle region inside the cortical surface. color it as gray
}




### For Custom ATLAS #####

# MAP from custom atlas to DK. Left-Hand-Side = Blender Regions   Right-Hand-Side = Regions in custom input atlas (.csv INPUT_FILE)
cortAreasIndexMapCustom = {
  'bankssts':-1, # -1 means do not colour this region
  'caudalanteriorcingulate':'anterior cingulate',
  'caudalmiddlefrontal':'medial frontal',
  'cuneus':'cuneus',
  'entorhinal':'entorhinal',
  'frontalpole':'frontal pole',
  'fusiform':'fusiform',
  'inferiorparietal':'angular',
  'inferiortemporal':'inferior temporal',
  'insula':'anterior insula',
  'isthmuscingulate':'posterior cingulate',
  'lateraloccipital':'inferior occipital',
  'lateralorbitofrontal':'medial frontal',
  'lingual':'lingual',
  'medialorbitofrontal':'medial frontal',
  'middletemporal':'middle temporal',
  'paracentral':'precentral',
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
  'unknown':-1 # this is actually the middle region inside the cortical surface. color it as gray
}


# Subcortical areas
# this map is used by all atlases (DK, Destrieux, Tourville)
subcortAreasIndexMap = {
  'Left-Accumbens-area':'Accumbens-area', # -1 means do not colour this region
  'Left-Caudate':'Caudate',
  'Left-Cerebellum-White-Matter':'Cerebellum-White-Matter',
  'Left-Inf-Lat-Vent': 'Inf-Lat-Vent',
  'Left-Pallidum':'Pallidum',
  'Left-Thalamus-Proper':'Thalamus-Proper',
  'Left-Amygdala':'Amygdala',
  'Left-Cerebellum-Cortex':'Cerebellum-Cortex',
  'Left-Hippocampus':'Hippocampus',
  'Left-Lateral-Ventricle':'Lateral-Ventricle',
  'Left-Putamen':'Putamen',
  'Left-VentralDC':'VentralDC'}


subcortAreasIndexMapCustom = {
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
