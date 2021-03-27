
INPUT_FILE = 'input/mouse_template.csv' # input template should match ATLAS below

OUTPUT_FOLDER = 'output/mice_output'

# either 'DK', 'Destrieux', 'Tourville', 'Mice' or 'Custom'
ATLAS = 'Mice'

# either 'pial' (with gyri/sulci), 'inflated' (smooth) or 'white' (white-matter surface)
BRAIN_TYPE = 'pial'

# either cortical-outer, cortical-inner, subcortical 
# add -right-hemisphere or -left-hemisphere to end of image type to specify view
# image types "top" and "bottom" are available to show asymmetry
IMG_TYPE = 'top'

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

if ATLAS == 'Mice': 
    # we do not have white/inflated for mice yet
    BRAIN_TYPE = 'pial'



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
  'Right-bankssts':'Right-bankssts',
  'Right-caudalanteriorcingulate':'Right-caudalanteriorcingulate',
  'Right-caudalmiddlefrontal':'Right-caudalmiddlefrontal',
  'Right-cuneus':'Right-cuneus',
  'Right-entorhinal':'Right-entorhinal',
  'Right-frontalpole': 'Right-frontalpole',
  'Right-fusiform':'Right-fusiform',
  'Right-inferiorparietal':'Right-inferiorparietal',
  'Right-inferiortemporal':'Right-inferiortemporal',
  'Right-insula':'Right-insula',
  'Right-isthmuscingulate':'Right-isthmuscingulate',
  'Right-lateraloccipital':'Right-lateraloccipital',
  'Right-lateralorbitofrontal':'Right-lateralorbitofrontal',
  'Right-lingual':'Right-lingual',
  'Right-medialorbitofrontal':'Right-medialorbitofrontal',
  'Right-middletemporal':'Right-middletemporal',
  'Right-paracentral':'Right-paracentral',
  'Right-parahippocampal':'Right-parahippocampal',
  'Right-parsopercularis':'Right-parsopercularis',
  'Right-parsorbitalis':'Right-parsorbitalis',
  'Right-parstriangularis':'Right-parstriangularis',
  'Right-pericalcarine':'Right-pericalcarine',
  'Right-postcentral':'Right-postcentral',
  'Right-posteriorcingulate':'Right-posteriorcingulate',
  'Right-precentral':'Right-precentral',
  'Right-precuneus':'Right-precuneus',
  'Right-rostralanteriorcingulate':'Right-rostralanteriorcingulate',
  'Right-rostralmiddlefrontal':'Right-rostralmiddlefrontal',
  'Right-superiorfrontal':'Right-superiorfrontal',
  'Right-superiorparietal':'Right-superiorparietal',
  'Right-superiortemporal':'Right-superiortemporal',
  'Right-supramarginal':'Right-supramarginal',
  'Right-temporalpole':'Right-temporalpole',
  'Right-transversetemporal':'Right-transversetemporal',
  'Right-unknown':-1, # this is actually the middle region inside the cortical surface. color it as gray
  
  'Left-bankssts':'Left-bankssts',
  'Left-caudalanteriorcingulate':'Left-caudalanteriorcingulate',
  'Left-caudalmiddlefrontal':'Left-caudalmiddlefrontal',
  'Left-cuneus':'Left-cuneus',
  'Left-entorhinal':'Left-entorhinal',
  'Left-frontalpole': 'Left-frontalpole',
  'Left-fusiform':'Left-fusiform',
  'Left-inferiorparietal':'Left-inferiorparietal',
  'Left-inferiortemporal':'Left-inferiortemporal',
  'Left-insula':'Left-insula',
  'Left-isthmuscingulate':'Left-isthmuscingulate',
  'Left-lateraloccipital':'Left-lateraloccipital',
  'Left-lateralorbitofrontal':'Left-lateralorbitofrontal',
  'Left-lingual':'Left-lingual',
  'Left-medialorbitofrontal':'Left-medialorbitofrontal',
  'Left-middletemporal':'Left-middletemporal',
  'Left-paracentral':'Left-paracentral',
  'Left-parahippocampal':'Left-parahippocampal',
  'Left-parsopercularis':'Left-parsopercularis',
  'Left-parsorbitalis':'Left-parsorbitalis',
  'Left-parstriangularis':'Left-parstriangularis',
  'Left-pericalcarine':'Left-pericalcarine',
  'Left-postcentral':'Left-postcentral',
  'Left-posteriorcingulate':'Left-posteriorcingulate',
  'Left-precentral':'Left-precentral',
  'Left-precuneus':'Left-precuneus',
  'Left-rostralanteriorcingulate':'Left-rostralanteriorcingulate',
  'Left-rostralmiddlefrontal':'Left-rostralmiddlefrontal',
  'Left-superiorfrontal':'Left-superiorfrontal',
  'Left-superiorparietal':'Left-superiorparietal',
  'Left-superiortemporal':'Left-superiortemporal',
  'Left-supramarginal':'Left-supramarginal',
  'Left-temporalpole':'Left-temporalpole',
  'Left-transversetemporal':'Left-transversetemporal',
  'Left-unknown':-1 # this is actually the middle region inside the cortical surface. color it as gray
}


### Destrieux atlas ###

# Left-Hand-Side = Blender Regions   Right-Hand-Side = Regions in custom input atlas (.csv INPUT_FILE)
cortAreasIndexMapDestrieux = {
    'Right-G_and_S_frontomargin': 'Right-G_and_S_frontomargin',
    'Right-G_and_S_occipital_inf': 'Right-G_and_S_occipital_inf',
    'Right-G_and_S_paracentral': 'Right-G_and_S_paracentral',
    'Right-G_and_S_subcentral': 'Right-G_and_S_subcentral',
    'Right-G_and_S_transv_frontopol': 'Right-G_and_S_transv_frontopol' ,
    'Right-G_and_S_cingul-Ant': 'Right-G_and_S_cingul-Ant',
    'Right-G_and_S_cingul-Mid-Ant': 'Right-G_and_S_cingul-Mid-Ant',
    'Right-G_and_S_cingul-Mid-Post': 'Right-G_and_S_cingul-Mid-Post',
    'Right-G_cingul-Post-dorsal': 'Right-G_cingul-Post-dorsal',
    'Right-G_cingul-Post-ventral': 'Right-G_cingul-Post-ventral',
    'Right-G_cuneus': 'Right-G_cuneus',
    'Right-G_front_inf-Opercular': 'Right-G_front_inf-Opercular',
    'Right-G_front_inf-Orbital': 'Right-G_front_inf-Orbital',
    'Right-G_front_inf-Triangul': 'Right-G_front_inf-Triangul' ,
    'Right-G_front_middle': 'Right-G_front_middle',
    'Right-G_front_sup': 'Right-G_front_sup',
    'Right-G_Ins_lg_and_S_cent_ins': 'Right-G_Ins_lg_and_S_cent_ins',
    'Right-G_insular_short': 'Right-G_insular_short',
    'Right-G_occipital_middle': 'Right-G_occipital_middle',
    'Right-G_occipital_sup': 'Right-G_occipital_sup',
    'Right-G_oc-temp_lat-fusifor': 'Right-G_oc-temp_lat-fusifor',
    'Right-G_oc-temp_med-Lingual': 'Right-G_oc-temp_med-Lingual' ,
    'Right-G_oc-temp_med-Parahip': 'Right-G_oc-temp_med-Parahip' ,
    'Right-G_orbital': 'Right-G_orbital',
    'Right-G_pariet_inf-Angular': 'Right-G_pariet_inf-Angular',
    'Right-G_pariet_inf-Supramar': 'Right-G_pariet_inf-Supramar',
    'Right-G_parietal_sup': 'Right-G_parietal_sup',
    'Right-G_postcentral': 'Right-G_postcentral',
    'Right-G_precentral': 'Right-G_precentral',
    'Right-G_precuneus': 'Right-G_precuneus',
    'Right-G_rectus': 'Right-G_rectus',
    'Right-G_subcallosal': 'Right-G_subcallosal',
    'Right-G_temp_sup-G_T_transv': 'Right-G_temp_sup-G_T_transv',
    'Right-G_temp_sup-Lateral': 'Right-G_temp_sup-Lateral',
    'Right-G_temp_sup-Plan_polar': 'Right-G_temp_sup-Plan_polar' ,
    'Right-G_temp_sup-Plan_tempo': 'Right-G_temp_sup-Plan_tempo' ,
    'Right-G_temporal_inf': 'Right-G_temporal_inf',
    'Right-G_temporal_middle': 'Right-G_temporal_middle',
    'Right-Lat_Fis-ant-Horizont': 'Right-Lat_Fis-ant-Horizont',
    'Right-Lat_Fis-ant-Vertical': 'Right-Lat_Fis-ant-Vertical',
    'Right-Lat_Fis-post': 'Right-Lat_Fis-post',
    'Right-Pole_occipital': 'Right-Pole_occipital',
    'Right-Pole_temporal': 'Right-Pole_temporal',
    'Right-S_calcarine': 'Right-S_calcarine',
    'Right-S_central': 'Right-S_central',
    'Right-S_cingul-Marginalis': 'Right-S_cingul-Marginalis',
    'Right-S_circular_insula_ant': 'Right-S_circular_insula_ant',
    'Right-S_circular_insula_inf': 'Right-S_circular_insula_inf',
    'Right-S_circular_insula_sup': 'Right-S_circular_insula_sup',
    'Right-S_collat_transv_ant': 'Right-S_collat_transv_ant',
    'Right-S_collat_transv_post': 'Right-S_collat_transv_post',
    'Right-S_front_inf': 'Right-S_front_inf',
    'Right-S_front_middle': 'Right-S_front_middle',
    'Right-S_front_sup': 'Right-S_front_sup',
    'Right-S_interm_prim-Jensen': 'Right-S_interm_prim-Jensen',
    'Right-S_intrapariet_and_P_trans': 'Right-S_intrapariet_and_P_trans',
    'Right-S_oc_middle_and_Lunatus': 'Right-S_oc_middle_and_Lunatus',
    'Right-S_oc_sup_and_transversal': 'Right-S_oc_sup_and_transversal',
    'Right-S_occipital_ant': 'Right-S_occipital_ant',
    'Right-S_oc-temp_lat': 'Right-S_oc-temp_lat',
    'Right-S_oc-temp_med_and_Lingual': 'Right-S_oc-temp_med_and_Lingual',
    'Right-S_orbital_lateral': 'Right-S_orbital_lateral',
    'Right-S_orbital_med-olfact': 'Right-S_orbital_med-olfact',
    'Right-S_orbital-H_Shaped': 'Right-S_orbital-H_Shaped',
    'Right-S_parieto_occipital': 'Right-S_parieto_occipital',
    'Right-S_pericallosal': 'Right-S_pericallosal',
    'Right-S_postcentral': 'Right-S_postcentral',
    'Right-S_precentral-inf-part': 'Right-S_precentral-inf-part',
    'Right-S_precentral-sup-part': 'Right-S_precentral-sup-part',
    'Right-S_suborbital': 'Right-S_suborbital',
    'Right-S_subparietal': 'Right-S_subparietal',
    'Right-S_temporal_inf': 'Right-S_temporal_inf',
    'Right-S_temporal_sup': 'Right-S_temporal_sup',
    'Right-S_temporal_transverse': 'Right-S_temporal_transverse',
    'Right-Unknown':-1, # this is actually the middle region inside the cortical surface. color it as gray


    'Left-G_and_S_frontomargin': 'Left-G_and_S_frontomargin',
    'Left-G_and_S_occipital_inf': 'Left-G_and_S_occipital_inf',
    'Left-G_and_S_paracentral': 'Left-G_and_S_paracentral',
    'Left-G_and_S_subcentral': 'Left-G_and_S_subcentral',
    'Left-G_and_S_transv_frontopol': 'Left-G_and_S_transv_frontopol' ,
    'Left-G_and_S_cingul-Ant': 'Left-G_and_S_cingul-Ant',
    'Left-G_and_S_cingul-Mid-Ant': 'Left-G_and_S_cingul-Mid-Ant',
    'Left-G_and_S_cingul-Mid-Post': 'Left-G_and_S_cingul-Mid-Post',
    'Left-G_cingul-Post-dorsal': 'Left-G_cingul-Post-dorsal',
    'Left-G_cingul-Post-ventral': 'Left-G_cingul-Post-ventral',
    'Left-G_cuneus': 'Left-G_cuneus',
    'Left-G_front_inf-Opercular': 'Left-G_front_inf-Opercular',
    'Left-G_front_inf-Orbital': 'Left-G_front_inf-Orbital',
    'Left-G_front_inf-Triangul': 'Left-G_front_inf-Triangul' ,
    'Left-G_front_middle': 'Left-G_front_middle',
    'Left-G_front_sup': 'Left-G_front_sup',
    'Left-G_Ins_lg_and_S_cent_ins': 'Left-G_Ins_lg_and_S_cent_ins',
    'Left-G_insular_short': 'Left-G_insular_short',
    'Left-G_occipital_middle': 'Left-G_occipital_middle',
    'Left-G_occipital_sup': 'Left-G_occipital_sup',
    'Left-G_oc-temp_lat-fusifor': 'Left-G_oc-temp_lat-fusifor',
    'Left-G_oc-temp_med-Lingual': 'Left-G_oc-temp_med-Lingual' ,
    'Left-G_oc-temp_med-Parahip': 'Left-G_oc-temp_med-Parahip' ,
    'Left-G_orbital': 'Left-G_orbital',
    'Left-G_pariet_inf-Angular': 'Left-G_pariet_inf-Angular',
    'Left-G_pariet_inf-Supramar': 'Left-G_pariet_inf-Supramar',
    'Left-G_parietal_sup': 'Left-G_parietal_sup',
    'Left-G_postcentral': 'Left-G_postcentral',
    'Left-G_precentral': 'Left-G_precentral',
    'Left-G_precuneus': 'Left-G_precuneus',
    'Left-G_rectus': 'Left-G_rectus',
    'Left-G_subcallosal': 'Left-G_subcallosal',
    'Left-G_temp_sup-G_T_transv': 'Left-G_temp_sup-G_T_transv',
    'Left-G_temp_sup-Lateral': 'Left-G_temp_sup-Lateral',
    'Left-G_temp_sup-Plan_polar': 'Left-G_temp_sup-Plan_polar' ,
    'Left-G_temp_sup-Plan_tempo': 'Left-G_temp_sup-Plan_tempo' ,
    'Left-G_temporal_inf': 'Left-G_temporal_inf',
    'Left-G_temporal_middle': 'Left-G_temporal_middle',
    'Left-Lat_Fis-ant-Horizont': 'Left-Lat_Fis-ant-Horizont',
    'Left-Lat_Fis-ant-Vertical': 'Left-Lat_Fis-ant-Vertical',
    'Left-Lat_Fis-post': 'Left-Lat_Fis-post',
    'Left-Pole_occipital': 'Left-Pole_occipital',
    'Left-Pole_temporal': 'Left-Pole_temporal',
    'Left-S_calcarine': 'Left-S_calcarine',
    'Left-S_central': 'Left-S_central',
    'Left-S_cingul-Marginalis': 'Left-S_cingul-Marginalis',
    'Left-S_circular_insula_ant': 'Left-S_circular_insula_ant',
    'Left-S_circular_insula_inf': 'Left-S_circular_insula_inf',
    'Left-S_circular_insula_sup': 'Left-S_circular_insula_sup',
    'Left-S_collat_transv_ant': 'Left-S_collat_transv_ant',
    'Left-S_collat_transv_post': 'Left-S_collat_transv_post',
    'Left-S_front_inf': 'Left-S_front_inf',
    'Left-S_front_middle': 'Left-S_front_middle',
    'Left-S_front_sup': 'Left-S_front_sup',
    'Left-S_interm_prim-Jensen': 'Left-S_interm_prim-Jensen',
    'Left-S_intrapariet_and_P_trans': 'Left-S_intrapariet_and_P_trans',
    'Left-S_oc_middle_and_Lunatus': 'Left-S_oc_middle_and_Lunatus',
    'Left-S_oc_sup_and_transversal': 'Left-S_oc_sup_and_transversal',
    'Left-S_occipital_ant': 'Left-S_occipital_ant',
    'Left-S_oc-temp_lat': 'Left-S_oc-temp_lat',
    'Left-S_oc-temp_med_and_Lingual': 'Left-S_oc-temp_med_and_Lingual',
    'Left-S_orbital_lateral': 'Left-S_orbital_lateral',
    'Left-S_orbital_med-olfact': 'Left-S_orbital_med-olfact',
    'Left-S_orbital-H_Shaped': 'Left-S_orbital-H_Shaped',
    'Left-S_parieto_occipital': 'Left-S_parieto_occipital',
    'Left-S_pericallosal': 'Left-S_pericallosal',
    'Left-S_postcentral': 'Left-S_postcentral',
    'Left-S_precentral-inf-part': 'Left-S_precentral-inf-part',
    'Left-S_precentral-sup-part': 'Left-S_precentral-sup-part',
    'Left-S_suborbital': 'Left-S_suborbital',
    'Left-S_subparietal': 'Left-S_subparietal',
    'Left-S_temporal_inf': 'Left-S_temporal_inf',
    'Left-S_temporal_sup': 'Left-S_temporal_sup',
    'Left-S_temporal_transverse': 'Left-S_temporal_transverse',
    'Left-Unknown':-1, # this is actually the middle region inside the cortical surface. color it as gray
}

### Mouse brain atlas ###

# Left-Hand-Side = Blender Regions   Right-Hand-Side = Regions in custom input atlas (.csv INPUT_FILE)
cortAreasIndexMapMice = {
  
  'Right-Anterior-cingulate': 'Right-Anterior-cingulate',
  'Right-Auditory': 'Right-Auditory',
  'Right-Cortical-subplate': 'Right-Cortical-subplate',
  'Right-Gustatory': 'Right-Gustatory',
  'Right-Infralimbic': 'Right-Infralimbic',
  'Right-Medulla': 'Right-Medulla',
  'Right-Olfactory': 'Right-Olfactory',
  'Right-Pons': 'Right-Pons',
  'Right-Prelimbic': 'Right-Prelimbic',
  'Right-Retrosplenial': 'Right-Retrosplenial',
  'Right-Somatomotor': 'Right-Somatomotor',
  'Right-Somatosensory': 'Right-Somatosensory',
  'Right-Striatum': 'Right-Striatum',
  'Right-Visceral': 'Right-Visceral',
  'Right-Visual': 'Right-Visual', 
  'Right-Agranular-insular-area': 'Right-Agranular-insular-area', 
  'Right-Posterior-parietal-association-areas': 'Right-Posterior-parietal-association-areas', 
  'Right-Temporal-association-areas': 'Right-Temporal-association-areas',
  'Right-Perirhinal': 'Right-Perirhinal',
  'Right-Ectorhinal': 'Right-Ectorhinal',

  'Left-Anterior-cingulate': 'Left-Anterior-cingulate',
  'Left-Auditory': 'Left-Auditory',
  'Left-Cortical-subplate': 'Left-Cortical-subplate',
  'Left-Gustatory': 'Left-Gustatory',
  'Left-Infralimbic': 'Left-Infralimbic',
  'Left-Medulla': 'Left-Medulla',
  'Left-Olfactory': 'Left-Olfactory',
  'Left-Pons': 'Left-Pons',
  'Left-Prelimbic': 'Left-Prelimbic',
  'Left-Retrosplenial': 'Left-Retrosplenial',
  'Left-Somatomotor': 'Left-Somatomotor',
  'Left-Somatosensory': 'Left-Somatosensory',
  'Left-Striatum': 'Left-Striatum',
  'Left-Visceral': 'Left-Visceral',
  'Left-Visual': 'Left-Visual', 
  'Left-Agranular-insular-area': 'Left-Agranular-insular-area', 
  'Left-Posterior-parietal-association-areas': 'Left-Posterior-parietal-association-areas', 
  'Left-Temporal-association-areas': 'Left-Temporal-association-areas',
  'Left-Perirhinal': 'Left-Perirhinal',
  'Left-Ectorhinal': 'Left-Ectorhinal',
}

# subcortical areas for mouse atlas
subcortMouseAreasIndexMap = {
  'Left-Cerebellum':'Left-Cerebellum', # -1 means do not colour this region
  'Left-Hypothalamus':'Left-Hypothalamus',
  'Left-Frontal-pole': 'Left-Frontal-pole', # Acronym for Frontal pole, cerebral cortex,
  'Left-Hippocampus': 'Left-Hippocampus',
  'Left-Midbrain':'Left-Midbrain',
  'Left-Pallidum': 'Left-Pallidum',
  'Left-Thalamus':'Left-Thalamus',

  'Right-Cerebellum':'Right-Cerebellum', # -1 means do not colour this region
  'Right-Hypothalamus':'Right-Hypothalamus',
  'Right-Frontal-pole': 'Right-Frontal-pole', # Acronym for Frontal pole, cerebral cortex,
  'Right-Hippocampus': 'Right-Hippocampus',
  'Right-Midbrain':'Right-Midbrain',
  'Right-Pallidum': 'Right-Pallidum',
  'Right-Thalamus':'Right-Thalamus'
}


### Tourville atlas ###

# Left-Hand-Side = Blender Regions   Right-Hand-Side = Regions in custom input atlas (.csv INPUT_FILE)
cortAreasIndexMapTourville = {
  'Right-caudalanteriorcingulate': 'Right-caudalanteriorcingulate',
  'Right-caudalmiddlefrontal': 'Right-caudalmiddlefrontal',
  'Right-cuneus': 'Right-cuneus',
  'Right-entorhinal': 'Right-entorhinal',
  'Right-fusiform': 'Right-fusiform',
  'Right-inferiorparietal': 'Right-inferiorparietal',
  'Right-inferiortemporal': 'Right-inferiortemporal',
  'Right-insula': 'Right-insula',
  'Right-isthmuscingulate': 'Right-isthmuscingulate',
  'Right-lateraloccipital': 'Right-lateraloccipital',
  'Right-lateralorbitofrontal': 'Right-lateralorbitofrontal',
  'Right-lingual': 'Right-lingual',
  'Right-medialorbitofrontal': 'Right-medialorbitofrontal',
  'Right-middletemporal': 'Right-middletemporal',
  'Right-paracentral': 'Right-paracentral',
  'Right-parahippocampal': 'Right-parahippocampal',
  'Right-parsopercularis': 'Right-parsopercularis',
  'Right-parsorbitalis': 'Right-parsorbitalis',
  'Right-parstriangularis': 'Right-parstriangularis',
  'Right-pericalcarine': 'Right-pericalcarine',
  'Right-postcentral': 'Right-postcentral',
  'Right-posteriorcingulate': 'Right-posteriorcingulate',
  'Right-precentral': 'Right-precentral',
  'Right-precuneus': 'Right-precuneus',
  'Right-rostralanteriorcingulate': 'Right-rostralanteriorcingulate',
  'Right-rostralmiddlefrontal': 'Right-rostralmiddlefrontal',
  'Right-superiorfrontal': 'Right-superiorfrontal',
  'Right-superiorparietal': 'Right-superiorparietal',
  'Right-superiortemporal': 'Right-superiortemporal',
  'Right-supramarginal': 'Right-supramarginal',
  'Right-transversetemporal': 'Right-transversetemporal',
  'Right-unknown':-1, # this is actually the middle region inside the cortical surface. color it as gray

  'Left-caudalanteriorcingulate': 'Left-caudalanteriorcingulate',
  'Left-caudalmiddlefrontal': 'Left-caudalmiddlefrontal',
  'Left-cuneus': 'Left-cuneus',
  'Left-entorhinal': 'Left-entorhinal',
  'Left-fusiform': 'Left-fusiform',
  'Left-inferiorparietal': 'Left-inferiorparietal',
  'Left-inferiortemporal': 'Left-inferiortemporal',
  'Left-insula': 'Left-insula',
  'Left-isthmuscingulate': 'Left-isthmuscingulate',
  'Left-lateraloccipital': 'Left-lateraloccipital',
  'Left-lateralorbitofrontal': 'Left-lateralorbitofrontal',
  'Left-lingual': 'Left-lingual',
  'Left-medialorbitofrontal': 'Left-medialorbitofrontal',
  'Left-middletemporal': 'Left-middletemporal',
  'Left-paracentral': 'Left-paracentral',
  'Left-parahippocampal': 'Left-parahippocampal',
  'Left-parsopercularis': 'Left-parsopercularis',
  'Left-parsorbitalis': 'Left-parsorbitalis',
  'Left-parstriangularis': 'Left-parstriangularis',
  'Left-pericalcarine': 'Left-pericalcarine',
  'Left-postcentral': 'Left-postcentral',
  'Left-posteriorcingulate': 'Left-posteriorcingulate',
  'Left-precentral': 'Left-precentral',
  'Left-precuneus': 'Left-precuneus',
  'Left-rostralanteriorcingulate': 'Left-rostralanteriorcingulate',
  'Left-rostralmiddlefrontal': 'Left-rostralmiddlefrontal',
  'Left-superiorfrontal': 'Left-superiorfrontal',
  'Left-superiorparietal': 'Left-superiorparietal',
  'Left-superiortemporal': 'Left-superiortemporal',
  'Left-supramarginal': 'Left-supramarginal',
  'Left-transversetemporal': 'Left-transversetemporal',
  'Left-unknown':-1 # this is actually the middle region inside the cortical surface. color it as gray
}




### For Custom ATLAS #####

# MAP from custom atlas to DK. Left-Hand-Side = Blender Regions   Right-Hand-Side = Regions in custom input atlas (.csv INPUT_FILE)
cortAreasIndexMapCustom = {
  'Right-bankssts':-1, # -1 means do not colour this region
  'Right-caudalanteriorcingulate':'Right-anterior cingulate',
  'Right-caudalmiddlefrontal':'Right-medial frontal',
  'Right-cuneus':'Right-cuneus',
  'Right-entorhinal':'Right-entorhinal',
  'Right-frontalpole':'Right-frontal pole',
  'Right-fusiform':'Right-fusiform',
  'Right-inferiorparietal':'Right-angular',
  'Right-inferiortemporal':'Right-inferior temporal',
  'Right-insula':'Right-anterior insula',
  'Right-isthmuscingulate':'Right-posterior cingulate',
  'Right-lateraloccipital':'Right-inferior occipital',
  'Right-lateralorbitofrontal':'Right-medial frontal',
  'Right-lingual':'Right-lingual',
  'Right-medialorbitofrontal':'Right-medial frontal',
  'Right-middletemporal':'Right-middle temporal',
  'Right-paracentral':'Right-precentral',
  'Right-parahippocampal':'Right-parahippocampal',
  'Right-parsopercularis':'Right-central operculum',
  'Right-parsorbitalis':'Right-anterior orbital',
  'Right-parstriangularis':'Right-angular',
  'Right-pericalcarine':'Right-calcarine',
  'Right-postcentral':'Right-postcentral',
  'Right-posteriorcingulate':'Right-posterior cingulate',
  'Right-precentral':'Right-precentral',
  'Right-precuneus':'Right-precuneus',
  'Right-rostralanteriorcingulate':'Right-anterior cingulate',
  'Right-rostralmiddlefrontal':'Right-middle frontal',
  'Right-superiorfrontal':'Right-superior frontal',
  'Right-superiorparietal':'Right-superior parietal',
  'Right-superiortemporal':'Right-superior temporal',
  'Right-supramarginal':'Right-supramarginal',
  'Right-temporalpole':'Right-temporal pole',
  'Right-transversetemporal':'Right-planum temporale',
  'Right-unknown':-1, # this is actually the middle region inside the cortical surface. color it as gray

  'Left-bankssts':-1, # -1 means do not colour this region
  'Left-caudalanteriorcingulate':'Left-anterior cingulate',
  'Left-caudalmiddlefrontal':'Left-medial frontal',
  'Left-cuneus':'Left-cuneus',
  'Left-entorhinal':'Left-entorhinal',
  'Left-frontalpole':'Left-frontal pole',
  'Left-fusiform':'Left-fusiform',
  'Left-inferiorparietal':'Left-angular',
  'Left-inferiortemporal':'Left-inferior temporal',
  'Left-insula':'Left-anterior insula',
  'Left-isthmuscingulate':'Left-posterior cingulate',
  'Left-lateraloccipital':'Left-inferior occipital',
  'Left-lateralorbitofrontal':'Left-medial frontal',
  'Left-lingual':'Left-lingual',
  'Left-medialorbitofrontal':'Left-medial frontal',
  'Left-middletemporal':'Left-middle temporal',
  'Left-paracentral':'Left-precentral',
  'Left-parahippocampal':'Left-parahippocampal',
  'Left-parsopercularis':'Left-central operculum',
  'Left-parsorbitalis':'Left-anterior orbital',
  'Left-parstriangularis':'Left-angular',
  'Left-pericalcarine':'Left-calcarine',
  'Left-postcentral':'Left-postcentral',
  'Left-posteriorcingulate':'Left-posterior cingulate',
  'Left-precentral':'Left-precentral',
  'Left-precuneus':'Left-precuneus',
  'Left-rostralanteriorcingulate':'Left-anterior cingulate',
  'Left-rostralmiddlefrontal':'Left-middle frontal',
  'Left-superiorfrontal':'Left-superior frontal',
  'Left-superiorparietal':'Left-superior parietal',
  'Left-superiortemporal':'Left-superior temporal',
  'Left-supramarginal':'Left-supramarginal',
  'Left-temporalpole':'Left-temporal pole',
  'Left-transversetemporal':'Left-planum temporale',
  'Left-unknown':-1 # this is actually the middle region inside the cortical surface. color it as gray
}


# Subcortical areas
# this map is used by all atlases (DK, Destrieux, Tourville)
subcortAreasIndexMap = {
  'Left-Accumbens-area': 'Left-Accumbens-area', # -1 means do not colour this region
  'Left-Caudate': 'Left-Caudate',
  'Left-Cerebellum-White-Matter': 'Left-Cerebellum-White-Matter',
  'Left-Inf-Lat-Vent': 'Left-Inf-Lat-Vent',
  'Left-Pallidum': 'Left-Pallidum',
  'Left-Thalamus-Proper': 'Left-Thalamus-Proper',
  'Left-Amygdala': 'Left-Amygdala',
  'Left-Cerebellum-Cortex': 'Left-Cerebellum-Cortex',
  'Left-Hippocampus': 'Left-Hippocampus',
  'Left-Lateral-Ventricle': 'Left-Lateral-Ventricle',
  'Left-Putamen': 'Left-Putamen',
  'Left-VentralDC': 'Left-VentralDC', 

  'Right-Accumbens-area': 'Right-Accumbens-area', # -1 means do not colour this region
  'Right-Caudate': 'Right-Caudate',
  'Right-Cerebellum-White-Matter': 'Right-Cerebellum-White-Matter',
  'Right-Inf-Lat-Vent': 'Right-Inf-Lat-Vent',
  'Right-Pallidum': 'Right-Pallidum',
  'Right-Thalamus-Proper': 'Right-Thalamus-Proper',
  'Right-Amygdala': 'Right-Amygdala',
  'Right-Cerebellum-Cortex': 'Right-Cerebellum-Cortex',
  'Right-Hippocampus': 'Right-Hippocampus',
  'Right-Lateral-Ventricle': 'Right-Lateral-Ventricle',
  'Right-Putamen': 'Right-Putamen',
  'Right-VentralDC': 'Right-VentralDC'
  }


subcortAreasIndexMapCustom = {
  'Left-Accumbens-area':'Left-Accumbens-area', # -1 means do not colour this region
  'Left-Caudate':'Left-Caudate',
  'Left-Cerebellum-White-Matter':-1,
  'Left-Inf-Lat-Vent':-1,
  'Left-Pallidum':'Left-Pallidum',
  'Left-Thalamus-Proper':'Left-Thalamus',
  'Left-Amygdala':'Left-Amygdala',
  'Left-Cerebellum-Cortex':-1,
  'Left-Hippocampus':'Left-Hippocampus',
  'Left-Lateral-Ventricle':-1,
  'Left-Putamen':'Left-Putamen',
  'Left-VentralDC':'Left-VentralDC',

  'Right-Accumbens-area':'Right-Accumbens-area', # -1 means do not colour this region
  'Right-Caudate':'Right-Caudate',
  'Right-Cerebellum-White-Matter':-1,
  'Right-Inf-Lat-Vent':-1,
  'Right-Pallidum':'Right-Pallidum',
  'Right-Thalamus-Proper':'Right-Thalamus',
  'Right-Amygdala':'Right-Amygdala',
  'Right-Cerebellum-Cortex':-1,
  'Right-Hippocampus':'Right-Hippocampus',
  'Right-Lateral-Ventricle':-1,
  'Right-Putamen':'Right-Putamen',
  'Right-VentralDC':'Right-VentralDC'
}
