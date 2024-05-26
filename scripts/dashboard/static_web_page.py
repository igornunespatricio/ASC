import pandas as pd
import plotly.graph_objects as go
from jinja2 import Template


class StaticWebPage:
    def __init__(
        self, 
        ranking_statistics_df: pd.DataFrame = None, 
        historic_match_results: pd.DataFrame = None,
        title: str = 'Streamlit Title',
        template_path:str='assets/template.html'
    ):
        self.ranking_statistics_df = ranking_statistics_df
        self.historic_match_results = historic_match_results
        self.title = title
        self.template_path=template_path

    def table_figure(self, df: pd.DataFrame) -> str:
        """Creates the table figure with plotly and exports it to HTML"""
        fig = go.Figure(
            data=[
                go.Table(
                    header=dict(
                        values=list(df.columns),
                        fill_color='paleturquoise',
                        align='left'
                    ),
                    cells=dict(
                        values=[df[col] for col in df.columns],
                        fill_color='lavender',
                        align='left'
                    )
                )
            ]
        )
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), autosize=True)
        return fig.to_html(full_html=False, include_plotlyjs='cdn')

    def generate_html(self) -> str:
        """Generate the static HTML page"""
        # Load HTML template
        with open(self.template_path, 'r') as file:
            template_str = file.read()

        # Render HTML template
        template = Template(template_str)
        rendered_html = template.render(
            title=self.title,
            ranking_table=self.table_figure(self.ranking_statistics_df),
            historic_table=self.table_figure(self.historic_match_results)
        )

        return rendered_html

    def save_html(self, filename: str):
        """Save the generated HTML to a file"""
        with open(filename, 'w') as file:
            file.write(self.generate_html())

if __name__ == '__main__':
    # Create instance of StaticWebPage
    static_page = StaticWebPage()

    # Generate and save HTML
    static_page.save_html('index.html')