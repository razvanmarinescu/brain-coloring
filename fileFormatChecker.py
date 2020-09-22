import numpy as np

def outputError(errorStr, getErrorAsStr):
  if getErrorAsStr:
    return errorStr
  else:
    raise ValueError(errorStr)


def checkInputDf(matDf, regionsThatShouldBeInTemplate, getErrorAsStr=False):


  colList = matDf.columns.to_list()
  colListOnlyNumbers = colList[1:]
  if colList[-1] == 'Image-text':
    print('last column is image text')
    colListOnlyNumbers = colListOnlyNumbers[:-1]

  if colList[0] != 'Image-name-unique':
    return outputError('First column in the input .csv file should be "Image-name-unique". '
                     'Please add this column at the beginning of the file, as per the template.', getErrorAsStr)

  if np.any(matDf.loc[:,colListOnlyNumbers] < 0):
    return outputError('Input csv file contains **negative** numbers. Numbers should be positive, ranging [0 - maxNrColours]. ', getErrorAsStr)

  colorTip = '\n\n Suggestion: If you do not want to color some regions, set the final (e.g. 4th) color in the ' \
             'color gradient to a default color (e.g. gray) and assign number 4 to those regions in the csv file.'

  if np.any(np.isnan(matDf.loc[:,colListOnlyNumbers])):
    return outputError('Input csv file contains missing/NaN numbers. Make sure to assign a number for each region.' + colorTip, getErrorAsStr)



  regionsThatShouldBeInTemplate = set(regionsThatShouldBeInTemplate) - set([-1, 'unknown'])
  print(regionsThatShouldBeInTemplate)
  missingRegions = list(set(regionsThatShouldBeInTemplate) - set(colListOnlyNumbers))
  print(missingRegions)
  if len(missingRegions) > 0:
    return outputError('The following regions are missing from the input .csv file: %s\n\n Make sure the correct atlas is '
                     'used, and double check the example template corresponding to that atlas.'
                     'Note that, currently, all regions from the template need to be assigned a number mapping to a color.'
                     % str(missingRegions) + colorTip, getErrorAsStr)


  # check that the number of columns are the same for each row
  matDfReset = matDf.reset_index()

  if np.any(matDfReset.columns.to_list()[0] == 'level_0'): # some column names are missing.
    return outputError('Some column names are missing. Make sure the number of elements per row in input csv file matches the number of columns.', getErrorAsStr)

  # nrCols = len(colList)
  # for i in range(matDf.shape[0]):
  #   print(matDf.loc[i,:])
  #   asda
  #   if matDf.loc[i,:].shape != nrCols:
  #     raise ValueError('Number of elements per row in input csv file does not match the number of columns.')

  return ''

