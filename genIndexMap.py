from os import listdir
from os.path import isfile, join

mypath = './models/Dsurque_atlas_pial'

onlyfiles = [f for f in listdir(mypath)]

for region_name in sorted(onlyfiles):
    print(f"'{region_name}': '{region_name}',")