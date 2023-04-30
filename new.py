import pandas as pd
import json
import sys
 
txt_file = sys.argv[1]

with open(txt_file) as myFile:
  fileData = json.load(myFile)
  dataFrame = pd.DataFrame.from_dict(fileData)
  print(dataFrame)