import numpy as np


def checkInputDf(matDf, regionsThatShouldBeInTemplate):

  colList = matDf.columns.to_list()
  if colList[0] != 'Image-name-unique':
    raise ValueError('First column in the input .csv file should be "Image-name-unique". '
                     'Please add this column at the beginning of the file, as per the template.')

  if np.any(matDf.loc[:,colList[1]:] < 0):
    raise ValueError('Input csv file contains **negative** numbers. Numbers should be positive, ranging [0 - maxNrColours]. ')

  colorTip = '\n\n Suggestion: If you do not want to color some regions, set the final (e.g. 4th) color in the ' \
             'color gradient to a default color (e.g. gray) and assign number 4 to those regions in the csv file.'

  if np.any(np.isnan(matDf.loc[:,colList[1]:])):
    raise ValueError('Input csv file contains missing/NaN numbers. Make sure to assign a number for each region.' + colorTip)



  regionsThatShouldBeInTemplate = set(regionsThatShouldBeInTemplate) - set([-1, 'unknown'])
  print(regionsThatShouldBeInTemplate)
  missingRegions = list(set(regionsThatShouldBeInTemplate) - set(colList[1:]))
  print(missingRegions)
  if len(missingRegions) > 0:
    raise ValueError('The following regions are missing from the input .csv file: %s\n\n Make sure the correct atlas is '
                     'used, and double check the example template corresponding to that atlas.'
                     'Note that, currently, all regions from the template need to be assigned a number mapping to a color.' % str(missingRegions) + colorTip)


  # check that the number of columns are the same for each row
  matDfReset = matDf.reset_index()

  if np.any(matDfReset.columns.to_list()[0] == 'level_0'): # some column names are missing.
    raise ValueError('Some column names are missing. Make sure the number of elements per row in input csv file matches the number of columns.')

  # nrCols = len(colList)
  # for i in range(matDf.shape[0]):
  #   print(matDf.loc[i,:])
  #   asda
  #   if matDf.loc[i,:].shape != nrCols:
  #     raise ValueError('Number of elements per row in input csv file does not match the number of columns.')

