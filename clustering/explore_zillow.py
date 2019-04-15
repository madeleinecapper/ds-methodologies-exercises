import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def get_heat_pair_box(df, num_vars):
    '''creates heatmap, pairplot, box plot'''
    fig, ax = plt.subplots(figsize=(25,25))
    sns.heatmap(df[num_vars].corr(), cmap='coolwarm', annot=True, ax=ax, annot_kws={"size": 20})
    plt.show()
    for i, col in enumerate(num_vars):
        series = df[col]
        sns.boxplot(series, orient='h')
        plt.show()
    df[num_vars].hist(figsize=(16, 8), bins=10, log=False)
    sns.pairplot(df[num_vars])


def make_rel(df, x, y, hue):
    '''creates a relplot from a dataframe using two continuous and one categorical variable as hue'''
    sns.relplot(x=x,y=y, hue=hue, data = df)



def swarrrm(df, cat, num_vars):
    '''creates a series of swarm plots from a dataframe using a categorical variable and a list of continuous ones'''
    for i, col in enumerate(num_vars):
        i = i+1
        plt.figure(figsize=(len(num_vars)*2, 14))
        plt.subplot(len(num_vars), 1, i)
        sns.swarmplot(data=df, x=cat, y=col)

def bars(df, cat_cols, cont_var):
    ''' creates a series of bar plots for data from a dataframe df, list cat_cols, and a continuous variable cont_var'''
    for col in cat_cols:
        cats = len(df[col].unique())
        if cats > 10 and np.issubdtype(df[col].dtype, np.number):
           binz = pd.cut(df[col], bins=5)
           sns.barplot(data=df, x=binz, y=cont_var)
           plt.show()
        else:
            sns.barplot(data=df, x=col, y=cont_var)
            plt.show()


#  t-test loop with formatted printing you might want to use later: 
# for i in range(0,3):
#     tstat, pval = stats.ttest_ind(df[df.cluster_target == i].logerror,
#                     df[df.cluster_target == (i+1)].logerror)
#     print('Our t-statistic is {:.4} and the p-value is {:.10}'.format(tstat, pval))