# -*- coding: utf-8 -*-
"""4_trustedZone_Outliers.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_wTxQcRtdxYqf5qiwOO62mqwPoUApuh7

"""
import duckdb
import pandas as pd
import numpy as np
from scipy import stats
from scipy.spatial.distance import mahalanobis
import scipy as sp

import Zones.config as conf

"""### Functions
Functions to calculate Mahalanobis Distance to detect outliers
"""

def mahalanobis(x=None, data=None, cov=None):

    x_mu = x - np.mean(data)
    if not cov:
        cov = np.cov(data.values.T)
    inv_covmat = np.linalg.pinv(cov)
    left = np.dot(x_mu, inv_covmat)
    mahal = np.dot(left, x_mu.T)
    return mahal.diagonal()


def trustedZone_outliers():
  """### DB Mounting"""

  dbFile_trusted = conf.DBFILE_TRUSTED_ZONE_PATH

  con_trusted = duckdb.connect(dbFile_trusted)
  cursor_trusted = con_trusted.cursor()

  """### Detection and deletion of univariate outliers"""

  #Gets the tablenames except the control tables
  tablenames_trusted = set(cursor_trusted.execute("select tablename from pg_tables where tablename not in ('tables_loaded')").fetchdf()['tablename'])

  print('-------------------------')
  print('Univariate Outlier Detection Report')
  print('-------------------------')

  #It goes through the tables to detect outliers 
  for tablename in tablenames_trusted:
    df = cursor_trusted.execute('select * from '+tablename).fetchdf()
    df_num = df.select_dtypes(include='number')
    df_num = df_num.dropna(axis='columns', how='all')
    df_post =df
    
    #For each numeric column it calculates the z-score and then it will filter z-scoes higher than 3
    for col in df_num:
        df['zcore']  = np.abs(stats.zscore(df_num[col]))
        df_post.drop(df_post[df_post.zcore < 3].index, inplace=True)

        #We delete the additional columns
        df_post.drop(['zcore'], axis=1, inplace=True)

    #Reviews if there are any outliers

    #If there is outliers, it 'updates' the table deleting the outliers
    if len(df) > len(df_post):
      cursor_trusted.execute('drop table '+tablename)
      cursor_trusted.execute('create table  '+tablename+ ' as select * from df_post')
      print(tablename+': ' +str(len(df))+' -> '+ str(len(df_post)))
    
    #If there is not outliers it does not do anything
    else:
      print(tablename+': No outliers')

  """### Detection and deletion of multivariate outliers"""

  #Imports chi2 to get the p-value of each Mahalanobis distance
  from scipy.stats import chi2

  #Gets the tablenames except the control tables
  tablenames_trusted = set(cursor_trusted.execute("select tablename from pg_tables where tablename not in ('tables_loaded','observations')").fetchdf()['tablename'])

  #Define the numeric types for columns
  numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']

  print('-------------------------')
  print('Multivariate Outlier Detection Report')
  print('-------------------------')

  #It goes through the tables to detect outliers 
  for tablename in tablenames_trusted:
    df = cursor_trusted.execute('select * from '+tablename).fetchdf()
    df_post = df
    df_num = df_post.select_dtypes(include=numerics)
    df_num = df_num.dropna(axis='columns', how='all')
    
    if df_num.shape[1] > 1 and df_num.shape[0] > 1:
      k = df.shape[1] - 1
      df_post['mahalanobis'] = mahalanobis(x=df_num, data=df_num)

      #Calculate p-value for each mahalanobis distance with k = n° of variables - 1
      #degrees of freedom 
      df_post['p'] = 1 - chi2.cdf(df_post['mahalanobis'], k)

      #We delete the individuals with p-value less than 0.01
      df_post.drop(df_post[df_post.p < 0.01].index, inplace=True)
      
      #We delete the adsitional columns
      df_post.drop(['mahalanobis', 'p'], axis=1, inplace=True)

    #Reviews if there are any outliers

    #If there is outliers, it 'updates' the table deleting the outliers
    if len(df) > len(df_post):
      cursor_trusted.execute('drop table '+tablename)
      cursor_trusted.execute('create table  '+tablename+ ' as select * from df_post')
      print(tablename+': ' +str(len(df))+' -> '+ str(len(df_post)))
    
    #If there is not outliers it does not do anything
    else:
      print(tablename+': No outliers')

  con_trusted.close()