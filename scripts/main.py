from collect import collect
import dashboard.app
import dashboard.static_web_page
from transform.Ranking import Ranking
import utils
import os
import dashboard

def main():
    
    
    DATABASE_PATH = 'data/asc.db'
    MATCH_RESULTS_TABLE_NAME = 'MatchResults'
    WEB_PAGE_PATH = 'web/index.html'
    
    # getting match results and storing in the database
    match_results = collect.get_data_url()
    match_results = collect.get_columns_from_dataframe(df=match_results)
    
    # storing results in database
    utils.store_in_database(
        df=match_results, 
        database_path=DATABASE_PATH, 
        table_name=MATCH_RESULTS_TABLE_NAME
    )
    
    # reading data from database
    match_results = utils.read_table_from_database(
            database_path=DATABASE_PATH,
            table_name=MATCH_RESULTS_TABLE_NAME
        )
    
    # initializing ranking instance
    ranking_instance = Ranking(
        columns_of_players=[
            'Vitorioso 1', 
            'Vitorioso 2', 
            'Derrotado 1', 
            'Derrotado 2'
        ], 
        results=match_results
    )
    
    # computing ranking statistics: points, wins, losses, etc.
    ranking_statistics = ranking_instance.compute_statistics()
    
    # storing statistics in database
    utils.store_in_database(
        df=ranking_statistics, 
        database_path=DATABASE_PATH, 
        table_name='RankStatistics'
    )
    
    # getting history of mathces: current points per player in match, points balance per player in match, etc.
    history_points_per_match = ranking_instance.get_points_per_match()
    
    # storing history points in database
    utils.store_in_database(
        df=history_points_per_match, 
        database_path=DATABASE_PATH, 
        table_name='HistoryPerMatch'
    )
     
    ranking_statistics = utils.read_table_from_database(
        'data/asc.db',
        'RankStatistics'
    )
    
    # app = dashboard.app.DashApp(
    #     ranking_statistics_df=ranking_statistics,
    #     historic_match_results=history_points_per_match,
    #     title='Ranking ASC'
    # )
    
    # app.run()
    
    static_page = dashboard.static_web_page.StaticWebPage(
        ranking_statistics_df=ranking_statistics,
        historic_match_results=history_points_per_match,
        title='Ranking ASC'
    )

    # Generate and save HTML
    static_page.save_html(WEB_PAGE_PATH)
    
    
if __name__ == '__main__':
    main()