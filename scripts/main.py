from utils import *
from Ranking import Ranking

def main():
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
    # TODO: change the final html file with the table provided from the Ranking class

if __name__ == '__main__':
    main()