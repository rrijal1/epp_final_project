import numpy as np
import pandas as pd
import itertools
from src.config import DATA
import pytask
from linearmodels.iv import IV2SLS
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from src.config import BLD

def get_coef_table(res_ols, var):
    ''' lin_reg is a fitted  regression model
    Return a list containing coefficients, and the confidence intervals
    '''
    coeff = [res_ols.params[var], 
            res_ols.conf_int()['lower'][var],
            res_ols.conf_int()['upper'][var]]

    return coeff


#Running  all the regressions

def batch_regression(df, var,indep_items):
    '''lin_reg is a fitted  regression model
    Return a list containing coefficients, and the confidence intervals
    '''
    df = df.dropna()
    reg_coeffs= []
    for i in range(1,5): 
        reg_coeffs.append(get_coef_table(IV2SLS(df[var+str(i)+'_y'],
        df[indep_items], None, None).fit(cov_type="unadjusted"), 'change_r'))
    reg_coeffs_df = pd.DataFrame (reg_coeffs, columns = ['Effect', 'lower', 'upper'])
    reg_coeffs_df['Horizon'] = reg_coeffs_df.index + 1 
    reg_coeffs_df['Regress'] = var

    return reg_coeffs_df


def plot_effects(df_list, path):
    "Plot all the LP effects."
    nrows = int(np.ceil(len(df_list) / 2 - 0.01))
    ncols = 2

    fig = make_subplots(
        rows=nrows,
        cols=ncols,
        shared_xaxes=True)

    for row, col in itertools.product(range(nrows), range(ncols)):
        loc_d =2*row + col 
        fig = fig.add_trace(
            go.Scatter(
                x= df_list[loc_d]['Horizon'],
                y = df_list[loc_d]['Effect']),
             row=row + 1,
             col=col + 1)
    fig.write_image(path)


@pytask.mark.depends_on(BLD / "data/data_mon.dta")
@pytask.mark.produces(BLD / "data/data_plot.txt")
def task_plot_locations(depends_on, produces):
    dependent_vars = ['FFED', 'PCEH', 'IP', 'UNRATE']
    indep_items = [
                'SP1000',
                'CPILFENS',
                'DSPIC96',
                'INDPRO',
                'M1SL',
                'PPIACO',
                'CENSA',
                'FARAT',
                'PCE',
                'change_r',
                'FFED1',
                'FFED2',
                'FFED3',
                'FFED4',
                'PCEH1',
                'PCEH2',
                'PCEH3',
                'PCEH4',
                'IP1',
                'IP2',
                'IP3',
                'IP4',
                'UNRATE1',
                'UNRATE2',
                'UNRATE3',
                'UNRATE4']
    plot_data = [batch_regression(depends_on, var= i, indep_items=indep_items) for i in dependent_vars]
    
    return plot_effects(plot_data, produces)
