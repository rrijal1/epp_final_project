import pandas as pd
from scipy.io import loadmat
from itertools import chain
from src.config import DATA


# Change Matlab to Panda Data Frame 


def unpack_matlab(input_file_name):
    """Update state estimates for a whole dataset.

    Let nstates be the number of states and nobs the number of observations.

    Args:
        states (np.ndarray): 2d array of size (nobs, nstates)
        root_covs (np.ndarray): 3d array of size (nobs, nstates, nstates)
        measurements (np.ndarray): 1d array of size (nobs)
        loadings (np.ndarray): 1d array of size (nstates)
        meas_var (float): a scalar float 

    Returns:
        updated_states (np.ndarray): 2d array of size (nobs, nstates)
        updated_root_covs (np.ndarray): 3d array of size (nobs, nstates, nstates)

    """
    input_ds = loadmat(DATA/f'{input_file_name}.mat')['s'][0, 0]
    core_data =  input_ds[0]

    col_names = _combining_cols(input_ds)
    
    data_points = [i.tolist() for i in core_data]
    
    return pd.DataFrame(data_points, columns=col_names)
    

def _combining_cols(input_data_stub):

    """Update state estimates for a whole dataset.

    Let nstates be the number of states and nobs the number of observations.

    Args:
        states (np.ndarray): 2d array of size (nobs, nstates)
        root_covs (np.ndarray): 3d array of size (nobs, nstates, nstates)
        measurements (np.ndarray): 1d array of size (nobs)
        loadings (np.ndarray): 1d array of size (nstates)
        meas_var (float): a scalar float 

    Returns:
        updated_states (np.ndarray): 2d array of size (nobs, nstates)
        updated_root_covs (np.ndarray): 3d array of size (nobs, nstates, nstates)

    """
    n_columns = range(len(input_data_stub))
    col_names_blocks = [input_data_stub[n_col].tolist() for n_col in n_columns if n_col > 0 ]

    col_name_elements = [col_names_blocks[t][0] for t in range(len(col_names_blocks))]

    col_names = list(dict.fromkeys(list(chain.from_iterable([cn.tolist() for cn in list(chain.from_iterable(col_name_elements))]))))
   
    return col_names


cee_macro_data = unpack_matlab('CEE_Macro Data_2012')

opf2_pscore_repdata = unpack_matlab('OPF2_PScore_RepData')


