import dash
import pandas as pd
import plotly.graph_objects as go
from dash import dcc, html

class DashApp:
    def __init__(
        self, 
        ranking_statistics_df:pd.DataFrame=None, 
        historic_match_results:pd.DataFrame=None,
        title:str='Streamlit Title'
        ):
        self.ranking_statistics_df = ranking_statistics_df
        self.historic_match_results = historic_match_results
        self.title = title
        # Initialize the Dash app
        self.app = dash.Dash(__name__)
        self.layout_definition()
    
    def table_figure(self, df:pd.DataFrame) -> go.Figure:
        """Creates the table figure with plotly"""
        fig = go.Figure(
            data=
            [
                go.Table(
                    header=
                    dict(
                        values=list(df.columns),
                        fill_color='paleturquoise',
                        align='left'
                    ),
                    cells=
                    dict(
                        values=[df[col] for col in df.columns],
                        fill_color='lavender',
                        align='left'
                    )
                )
        ])
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), autosize=True)
        return fig

    def layout_definition(self):
        """Define the layout of the app"""
        self.app.layout = html.Div(
            children=[
                html.H1(self.title, style={'textAlign': 'center', 'fontSize': '3em', 'marginBottom': '20px'}),
                html.H2('Ranking Statistics', style={'textAlign': 'center', 'marginBottom': '0px', 'marginTop': '20px'}),
                html.Div(
                    dcc.Graph(id='rank-table', figure=self.table_figure(self.ranking_statistics_df)),
                    style={'width': '80%', 'display': 'inline-block'}
                ),
                html.H2('Historic Match Results', style={'textAlign': 'center', 'marginBottom': '0px', 'marginTop': '20px'}),
                html.Div(
                    dcc.Graph(id='historic-table', figure=self.table_figure(self.historic_match_results)),
                    style={'width': '90%', 'display': 'inline-block'}
                )
            ],
            style={'textAlign': 'center'}
        )
    
    def run(self):
        """Run the Dash app"""
        self.app.run_server(debug=True, port=8050)

if __name__ == '__main__':
    app = DashApp()
    app.run()