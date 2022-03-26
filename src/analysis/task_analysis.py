import pytask
from src.config import BLD
from src.config import DATA
import pandas as pd


@pytask.mark.depends_on(DATA / "iv_lp.dta")
@pytask.mark.produces(BLD / "data/data_mon.dta")
def data_mon(depends_on, produces):
    """Takes the ivregression variable from Jorda et. al and and uses it to estimate LPs.

    We will be using the data exclusively for carrying out further calculations.
    """
    df_lp = pd.read_stata(depends_on)

    # We will only look into the data of USA 
    
    df_lp = df_lp[df_lp['iso'] == 'USA']
    df_lp['year'] = df_lp['year'].apply(pd.to_datetime)
    df_lp['Year'] = df_lp['year'].apply(lambda x : x.year)
    
    df_lp = df_lp[['Year', 'change_r', 'log_rgdppc',  'credit_to_gdp',  'log_cpi', 'lr_stocks']]

    iv_parm = pd.merge(_import_mat(), df_lp, on="Year")
    iv_parm_df = pd.merge(iv_parm, _import_csv(), on=["Year", "Month"])

    dependent_vars = ['FFED', 'PCEH', 'IP', 'UNRATE' ]

    for var in dependent_vars:
        iv_parm_df.rename(columns = {var + '_x':var}, inplace = True)

    # Convert into Time Series Data
    
    iv_parm_df.set_index(iv_parm_df['months'], inplace=True)

    # remove redundant variables 
    
    unnecessary_var = ['Year','Month', 'months','FFED_y','PCEH_y','PCEH_y','IP_y', 'UNRATE_y',]
    iv_parm_df.drop(columns = unnecessary_var, inplace=True)

    # Building Lagged variables 

    _build_lagged_features(df=iv_parm_df, cols=dependent_vars, lag = 4)

    # Building Outcome Variables for Regression  

    _build_outcome_features(df=iv_parm_df, cols=dependent_vars, lag= 4)

    return  pd.DataFrame(iv_parm_df).to_stata(produces)


def _import_csv(): 
    return pd.read_stata(BLD/"data/processed.dta")

def _import_mat(): 
    return pd.read_stata(BLD/"data/cee_mac.dta")


def _build_lagged_features(df,cols, lag):
    '''
    Builds a modified DataFrame to facilitate regressing over all possible lagged features.
    '''
    for col_names in cols:
        for l in range(1,lag+1):
            df[col_names + str(l)] = df[col_names].shift(l)
    return pd.DataFrame(df)
    

def _build_outcome_features(df,cols,lag):
    '''
    Builds a modified DataFrame with output variable for IV Regression.
    '''
    for col_names in cols:
        for l in range(1,lag+1):
            df[col_names + str(l) + '_y'] = df[col_names] - df[col_names+str(l)]  
    return pd.DataFrame(df)


    

