import pandas as pd
import numpy as np

from utils import *

class Ranking:
    def __init__(
        self, 
        columns_of_players:list[str], 
        results:pd.DataFrame,
        initial_points = 100,
        minimal_points = 10,
        lost_multiplier = 0.5,
        points_multiplier = 10    
    ):
        self.columns_of_players = columns_of_players
        self.results = results
        self.initial_points = initial_points
        self.minimal_points = minimal_points
        self.lost_multiplier = lost_multiplier
        self.points_multiplier = points_multiplier
        self.players_names = self.__get_all_players(columns_of_players)
        
        self.relationships = [
            ['Vitorioso 1', 'Current Points Vitorioso 1', 'Current Points Vitorioso 2', ['Current Points Derrotado 1', 'Current Points Derrotado 2']],
            ['Vitorioso 2', 'Current Points Vitorioso 2', 'Current Points Vitorioso 1', ['Current Points Derrotado 1', 'Current Points Derrotado 2']],
            ['Derrotado 1', 'Current Points Derrotado 1', 'Current Points Derrotado 2', ['Current Points Vitorioso 1', 'Current Points Vitorioso 2']],
            ['Derrotado 2', 'Current Points Derrotado 2', 'Current Points Derrotado 1', ['Current Points Vitorioso 1', 'Current Points Vitorioso 2']]
        ]
        self.player_col_names = [item[0] for item in self.relationships]
        self.match_balance_col_names = [f'Match Balance {item}' for item in self.player_col_names]
        self.current_points_columns = [
            'Current Points Vitorioso 1', 
            'Current Points Vitorioso 2', 
            'Current Points Derrotado 1', 
            'Current Points Derrotado 2'
        ]
        self.__temporary_results = None
        self.__temporary_points = self.__set_initial_points(initial_points=initial_points)
        self.__points_per_match = None
        
    def __get_all_players(self, columns_with_player_names:list[str]) -> list:
        return np.unique(self.results[columns_with_player_names].astype(str).values.flatten())
    
    
    def __set_initial_points(self, initial_points):
        initial_points_per_player = pd.DataFrame(
            {
                'Player': self.players_names,
                'Points': np.repeat(initial_points, len(self.players_names))
            }
        ).set_index('Player')
        
        return initial_points_per_player
    
    def __join_current_points_in_temporary_results(self):
        results_players_columns = ['Vitorioso 1', 'Vitorioso 2', 'Derrotado 1', 'Derrotado 2']
        for column in results_players_columns:
            self.__temporary_results = self.__temporary_results.\
                set_index(column).\
                    join(self.__temporary_points, how='left').\
                        reset_index(names=column).\
                            rename({'Points':f'Current Points {column}'}, axis=1)        
    
    def __join_points_balance_in_temporary_results(self):
        
        points_at_game = self.__temporary_results[self.current_points_columns].sum(axis=1)
        
        for relation in self.relationships:
            current_player_col_name = relation[0]
            player_col_name = relation[1]
            competitors_col_name = relation[3]
            partner_col_name = relation[2]
            competitors_points = self.__temporary_results[competitors_col_name].sum(axis=1)
            partner_points = self.__temporary_results[partner_col_name]
            if 'Derrotado' in player_col_name:
                points_player = - ( (1 - competitors_points/points_at_game) * partner_points/points_at_game) * self.points_multiplier
            else:
                points_player = (competitors_points/points_at_game) * (1 - partner_points/points_at_game) * self.points_multiplier
            points_player = pd.DataFrame(points_player, columns=[f'Match Balance {current_player_col_name}'])
            
            self.__temporary_results = self.__temporary_results.join(points_player)
    
    def __concatenate_temporary_results_in_points_per_match(self):
        self.__points_per_match = self.__points_per_match = pd.concat(
            [
                self.__points_per_match,
                self.__temporary_results
            ],
            axis=1
        )
    
    def __aggregate_temporary_points_per_person_in_temporary_points(self):
        grouped_points_per_player = []
        for player_col_name, match_balance_col_name in zip(self.player_col_names, self.match_balance_col_names):
            grouped_points_player = self.__temporary_results.groupby(player_col_name)[[match_balance_col_name]].agg('sum')
            grouped_points_per_player.append(grouped_points_player)
        grouped_points = pd.concat(grouped_points_per_player).groupby(level=0).sum().sum(axis=1)
        grouped_points.name = 'balance'
        self.__temporary_points = self.__temporary_points.join(grouped_points)
        self.__temporary_points = self.__temporary_points.sum(axis=1)
        
    def __adjust_temp_points(self):
        median_points = self.__temporary_points.loc[self.__temporary_points.index != 'Convidado',].median()
        self.__temporary_points.loc['Convidado',] = median_points
        self.__temporary_points.loc[self.__temporary_points < self.minimal_points, ]= self.minimal_points
        
    def compute_ranking(self, date_column_name:str='Data'):
        days_played = self.results[date_column_name].sort_values(ascending=True).unique()
        for day in days_played:
            print(day)
            
            self.__temporary_results = self.results[self.results[date_column_name] == day]
            
            self.__join_current_points_in_temporary_results()
            
            self.__join_points_balance_in_temporary_results()
            
            self.__concatenate_temporary_results_in_points_per_match()
            
            self.__aggregate_temporary_points_per_person_in_temporary_points()
            
            self.__adjust_temp_points()
            
            print(self.__temporary_points)
            
            # TODO: check if loop is working for all days
            # TODO: check if self.__points_per_match and self.__temporary_results stores all points per match (current points and balance points both)
            # TODO: check if in the end of the loop self.__temporary_points contains the final aggregation of points until the last day
            # TODO: add a method to calculate basic metrics like number of matches, wins, percentage of wins, etc.
            # TODO: add a method to return the final table with points, number of matches, percentage of wins, etc.
            # TODO: DONT FORGET TO REMOVE THE BREAK COMMAND BELOW TO TEST ALL THESE :)
            break
    
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