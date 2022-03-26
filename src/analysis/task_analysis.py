import pytask
from src.config import BLD
from scipy.io import loadmat
from itertools import chain
from src.config import DATA
import pandas as pd


@pytask.mark.depends_on(DATA / "iv_lp.dta")
@pytask.mark.produces(BLD / "data/data_mon.dta")
def data_mon(depends_on, produces):
    """Takes the ivregression variable from Jorda et. al and and uses it to estimate LPs.
    """
    df_lp = pd.read_stata(depends_on)

    # We will only look into the data of USA 
    
    df_lp = df_lp[df_lp['iso'] == 'USA']
    df_lp['year'] = df_lp['year'].apply(pd.to_datetime)
    df_lp['Year'] = df_lp['year'].apply(lambda x : x.year)
    
    df_lp = df_lp[['Year', 'change_r', 'log_rgdppc',  'credit_to_gdp',  'log_cpi', 'lr_stocks']]


