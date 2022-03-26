import pytask
from src.config import DATA
import pandas as pd
from src.config import BLD


@pytask.mark.depends_on(DATA / "processed.xlsx")
@pytask.mark.produces(BLD / "data/processed.dta")
def excel_data_process(depends_on, produces):
    """Excel file containing processed information from Angrist et. al. Paper.
    """

    df_comp = pd.read_excel(depends_on)

    df_comp['year'] = df_comp['year'].apply(pd.to_datetime)
    df_comp['months'] = df_comp['year'] 

    # Renaming for merging 

    df_comp['month'] = df_comp['year'].apply(lambda x : x.month)
    df_comp['year'] = df_comp['year'].apply(lambda x : x.year)
    df_comp.rename(columns={'year': 'Year', 'month': 'Month'}, inplace=True)
    
    return pd.DataFrame(df_comp).to_stata(produces)
    
