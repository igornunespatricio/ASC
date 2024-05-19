import requests
from io import BytesIO

import pandas as pd
import numpy as np

from Ranking import Ranking

def get_data_url() -> pd.DataFrame:
    """uses requests to get data from a google sheet and returns a pandas dataframe

    Returns:
        pd.DataFrame: dataframe returned from the link of the google sheet
    """
    # URL to the Google Sheets document in Excel format
    url = "https://docs.google.com/spreadsheets/d/1PCQco4tHxm7YPmVs4ZDAtjaDGKC84kuYXhsetnHVdXs/export?format=xlsx"

    # Get the content of the file
    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful

    # Load the content into a pandas DataFrame
    df = pd.read_excel(BytesIO(response.content))

    # Display the DataFrame
    print(df)
    
def get_data_excel() -> pd.DataFrame:
    """get data from excel file, this is used for development so I dont need to request the data every time when developing the code.

    Returns:
        pd.DataFrame: a dtaframe with raw data from the excel file
    """
    PATH = r'./data/Ranking ASC.xlsx'
    df = pd.read_excel(PATH)
    return df

def get_columns_from_dataframe(df: pd.DataFrame, indexes_of_columns:list[int]=[9, 10, 11, 12, 13]) -> pd.DataFrame:
    """returns columns based on the indexes passed to the indexes_of_columns parameter.

    Args:
        df (pd.DataFrame): dataframe to return the columns from
        indexes_of_columns (list[int], optional): indexes of columns to return from dataframe. Defaults to [9, 10, 11, 12, 13].

    Returns:
        pd.DataFrame: pandas dataframe qith with the columns from indexes_of_columns list.
    """
    df_transformed = df.copy()
    df_transformed = df_transformed.iloc[:, indexes_of_columns]
    column_names = df_transformed.iloc[0, :]
    df_transformed.columns = column_names
    df_transformed.drop(0, axis=0, inplace=True)
    
    return df_transformed

    
if __name__== '__main__':
    df = get_data_excel()
    df = get_columns_from_dataframe(df=df)
    ranking_instance = Ranking(
        columns_of_players=[
            'Vitorioso 1', 
            'Vitorioso 2', 
            'Derrotado 1', 
            'Derrotado 2'
        ], 
        results=df
    )
    ranking_instance.compute_ranking()