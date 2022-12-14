# -*- coding: utf-8 -*-
"""persistentLanding.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14D31wAVX5KBqlLNKYEbUh1LnTPRQLIC9

# Persistent Landing
"""

import os, shutil, time
from datetime import datetime
import Zones.config as conf


def persistentLanding():

  data_directory_temporal = conf.TEMPORAL_LANDING_ZONE_PATH
  data_directory_persistent = conf.PERSISTENT_LANDING_ZONE_PATH

  for root, subdirs, files in os.walk(data_directory_temporal):
    # Move to Persistent Landing
    if len(files) > 0:
      for file in files:
        src_path = f"{root}/{file}"
        sourceName = root.split('/')[-1]
        fileName, fileExtension = file.split('.')
        
        # Add metadata to file name!!!!!
        dt_m = datetime.fromtimestamp(os.path.getmtime(src_path)).strftime("%Y%m%d_%H%M%S")
        newFileName = f"{fileName.lower()}_{dt_m}"
        dest_path = f"{data_directory_persistent}/{newFileName}.{fileExtension}"

        shutil.copy(src_path, dest_path)

