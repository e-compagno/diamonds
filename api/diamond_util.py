import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def filter_iqr(df, col, qlow=0.25, qhigh=0.75, whisker_width=1.5):
        """
        Filter data with quantile range.

        Parameters
        ---------
        df: pd.DataFrame
            data
        col: string
            name of the column to calculate the quantile range
        qlow: float
            low quantile threshold (default 25%)
        qhigh: float
            high quantile threshold (default 75%)
        whisker_width: float
            filtering factor (default 1.5)

        Returns
        -------
        pd.DataFrame
            filtered dataframe
        """
        qlow_threshold = df[col].quantile(qlow)
        qhigh_threshold = df[col].quantile(qhigh)
        iqr = qhigh_threshold - qlow_threshold
        cond = (df[col] >= qlow_threshold-whisker_width*iqr) & (df[col] <= qhigh_threshold+whisker_width*iqr)
        df_reduced = df[cond]
        return df_reduced

def eda_category_distr(df, col, save=False):
    """
    Plot category distribution.

    Params
    ------
    df: pd.DataFrame
        input dataframe
    col: string
        input column
    save: bool
        save to file
    Returns
    -------
    None
    """
    cat_order = df[col].dtype.categories.tolist()
    plt.figure()
    #fig= df[col].value_counts().plot(kind='bar')
    fig= sns.countplot(df[col], order=cat_order)
    plt.title(col + '_distribution')
    plt.ylabel('count')
    fig.set_xticklabels(fig.get_xticklabels(), rotation=45)
    plt.tight_layout()
    if save==True:
        plt.savefig('../images/'+col+'_distribution.png', dpi=300)
    plt.show()
    print(df[col].describe())

def eda_missing_value(df):
    """
    Find missing value in the dataset.

    Params
    ------
    df: pd.DataFrame
        input dataframe
    Returns
    -------
    None
    """
    print('Missing values:')
    print('---------------')
    for col in df.columns:
        msn_number = df[col].isnull().sum()
        msn_perc = round(msn_number / df.shape[0]*100, 2)
        print('{0}: {1} ({2} %)'.format(col, msn_number, msn_perc))

def label_cat_encode(df, col):
    """
    Label encode a category feature.
    
    Params
    ------
    df: pd.DataFrame
        input dataframe
    col: string
        category name to label encode
        
    Returns
    -------
    pd.DataFrame
        encoded dataframe
    
    """
    cat_col = df[col].unique()
    cat_encoding = dict(zip(cat_col, [*range(len(cat_col))]))

    df[col] = df[col].map(cat_encoding)
    return df
