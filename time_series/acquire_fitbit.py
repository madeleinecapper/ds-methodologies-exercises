import pandas as pd
import numpy as np

# Making each csv a DataFrame that is split on new line

# assigning each csv to a variable
a = 'fitbit/2018-04-26_through_2018-05-26.csv'
b = 'fitbit/2018-05-27_through_2018-06-26.csv'
c = 'fitbit/2018-06-27_through_2018-07-27.csv'
d = 'fitbit/2018-07-28_through_2018-08-26.csv'
e = 'fitbit/2018-08-27_through_2018-09-26.csv'
g = 'fitbit/2018-09-27_through_2018-10-27.csv'
h = 'fitbit/2018-10-28_through-2018-11-27.csv'
i = 'fitbit/2018-11-28_through_2018-12-28.csv'

# Read each file and split on new lines: 
FILE = a
with open(FILE) as f:
    contents = f.read()
a = contents.split('\n')
a = pd.DataFrame(a)

FILE = b
with open(FILE) as f:
    contents = f.read()
b = contents.split('\n')
b = pd.DataFrame(b)

FILE = c
with open(FILE) as f:
    contents = f.read()
c = contents.split('\n')
c = pd.DataFrame(c)

FILE = d
with open(FILE) as f:
    contents = f.read()
d = contents.split('\n')
d = pd.DataFrame(d)

FILE = e
with open(FILE) as f:
    contents = f.read()
e = contents.split('\n')
e = pd.DataFrame(e)

FILE = g
with open(FILE) as f:
    contents = f.read()
g = contents.split('\n')
g = pd.DataFrame(g)

FILE = h
with open(FILE) as f:
    contents = f.read()
h = contents.split('\n')
h = pd.DataFrame(h)

FILE = i
with open(FILE) as f:
    contents = f.read()
i = contents.split('\n')
i = pd.DataFrame(i)

# just activities: 
a = a.iloc[35:67]
b = b.iloc[36:67]
c = c.iloc[36:67]
d = d.iloc[35:65]
e = e.iloc[36:67]
g = g.iloc[36:67]
h = h.iloc[36:67]
i = i.iloc[36:45]

def combine_logs():
    '''appends the different logs into one dataframe'''
    df = a.append(b).append(c).append(d).append(e).append(g).append(h).append(i)
    df = df.reset_index()
    return df


def split_cols(df):
    '''Separate the data into workable columns'''
    df = df[0].str.split('","', expand=True)
    return df

def rename_cols(df):
    '''Names columns of the dataframe appropriately based on fitbit csv'''
    df.rename(columns={0: 'date', 
                   1: 'calories_burned', 
                   2: 'steps', 
                   3: 'distance',
                   4: 'floors',
                   5: 'minutes_sedentary',
                   6: 'minutes_lightly_active',
                   7: 'minutes_fairly_active',
                   8: 'minutes_very_active',
                   9: 'activity_calories'}, inplace=True)
    df.drop(index=0, inplace=True)
    return df

def get_fitbit():
    '''compounds functions above into a single function call'''
    df = combine_logs()
    df = split_cols(df)
    df = rename_cols(df)
    return df
