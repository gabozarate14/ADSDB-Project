# -*- coding: utf-8 -*-
"""6_trustedZone_fixSampling.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TPqfzcKlde5mPMKSTOF9HX7NAoL6RR8m

"""

import duckdb
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import Zones.config as conf

def trustedZone_fixsampling():

  dbFile_trusted = conf.DBFILE_TRUSTED_ZONE_PATH

  con_trusted = duckdb.connect(dbFile_trusted)
  cursor_trusted = con_trusted.cursor()

  """## Function to fix Timestamp"""

  # If the timestamp is not to an exact quarter minute, it is forced to the exact value to facilitate the check and next tasks.
  def fixTimeStamp(stringTs):
    dt=datetime.strptime(stringTs, '%Y-%m-%d %H:%M:%S')
    if dt.minute >= 0 and dt.minute < 15: dt = dt.replace(minute=0,second=0)
    elif dt.minute >= 15 and dt.minute < 30: dt = dt.replace(minute=15,second=0)
    elif dt.minute >= 30 and dt.minute < 45: dt = dt.replace(minute=30,second=0)
    elif dt.minute >= 45 and dt.minute <= 59: dt = dt.replace(minute=45,second=0)
    return dt

  df_tables=cursor_trusted.execute('select * from pg_tables').fetchdf()
  tablesToCheck = ["humidity", "weather", "precipitations", "observations"]   # Tables with timestamps

  for tableName in df_tables['tablename']:
    if tableName in tablesToCheck:
      print(tableName)
      df=cursor_trusted.execute(f"select * from {tableName}").fetchdf()
      if "observations" in tableName:
        timeStampColName = "published_at"
        subsetDuplicates = [timeStampColName,'sensorid']
      else:
        timeStampColName = "timestamp"
        subsetDuplicates = [timeStampColName]

      # Fix TimeStamp format
      df[timeStampColName] = df.apply(lambda row: fixTimeStamp(str(row[timeStampColName])), axis=1)
      
      #if "weather" in tableName: display(df.iloc[6434:6445,:])      # Show the example in the report

      # Drop duplicates
      df.drop_duplicates(subset=subsetDuplicates, inplace=True)

      #if "weather" in tableName: display(df.iloc[6434:6445,:])      # Show the example in the report

      # Save the new dataframe with the corrections made.
      cursor_trusted.execute(f"drop table {tableName}")
      cursor_trusted.execute(f"create table  {tableName} as select * from df")

  """### Closing DB conection"""

  con_trusted.close()