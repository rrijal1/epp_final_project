import pytask
from src.config import BLD
from scipy.io import loadmat
from itertools import chain
from src.config import DATA
import pandas as pd


@pytask.mark.depends_on(DATA / "CEE_Macro Data_2012.mat")
@pytask.mark.produces(BLD / "data/cee_mac.dta")
def unpack_matlab(depends_on, produces):
    """Unpacks Matlab file and makes it into a stata file.

    Args:
        input_file_name (matlabfile): Matlab data type.
    Returns:
        updated_root_covs (np.ndarray): 3d array of size (nobs, nstates, nstates)

    """
    input_ds = loadmat(depends_on)['s'][0, 0]
    core_data =  input_ds[0]

    col_names = _combining_cols(input_ds)
    
    data_points = [i.tolist() for i in core_data]
    
    return pd.DataFrame(data_points, columns=col_names).to_stata(produces)
    

def _combining_cols(input_data_stub):

    """ The Matlab Files are arranged into rows and columns. 
        Column names are appended. 

    Args:
        input_data_stub (array): Matlab Data Array

    Returns:
        col_names: Returns the names of all columns

    """
    n_columns = range(len(input_data_stub))
    col_names_blocks = [input_data_stub[n_col].tolist() for n_col in n_columns if n_col > 0 ]

    col_name_elements = [col_names_blocks[t][0] for t in range(len(col_names_blocks))]

    col_names = list(dict.fromkeys(list(chain.from_iterable([cn.tolist() for cn in list(chain.from_iterable(col_name_elements))]))))
   
    return col_names



