import pandas as pd
from datetime import datetime
from csvLoaderGUI import csv_loader
from DataScrub import clean_df

# may need to pip install Jinja2 if pandas styler import errors

# Set day for file naming
today = datetime.today().strftime('%Y%m%d_%H%M%S')

# Function to export DataFrame to HTML with boring style and easy exporting
def style_tables(dfs, titles):
    """
    Styles and exports DataFrames to HTML files with custom formatting.
    Args:
        dfs (list of pd.DataFrame): List of DataFrames to style and export.
        titles (list of str): List of titles for each DataFrame.
    Returns:
        None. Files are exported to HTML with the specified titles.
    """

    def zero_to_empty(val):
        if isinstance(val, (int, float)) and val == 0:
            return ''
        return f'{val:,.2f}'  # Format with commas and 2 decimal places

    # Apply styling to the DataFrame

    for df, title in zip(dfs, titles):
        (df.style
            .set_properties(**{
                'text-align': 'right',
                'font-family': 'Helvetica, Arial, sans-serif',
                'font-size': '14px',
                'padding': '10px'
            })
            .format(zero_to_empty, na_rep='')
            .set_table_styles([
                # General table styles
                {'selector': '', 'props': [
                    ('border-collapse', 'collapse'), 
                    ('width', '100%'),
                    ('border', '1px solid #ccc')
                ]},
                # Header styles
                {'selector': 'th', 'props': [
                    ('background-color', '#f0f0f0'),  # Light grey background for headers
                    ('color', '#333'),  # Dark grey text for headers
                    ('font-weight', 'bold'),
                    ('border-bottom', '2px solid #999'),  # Darker line under headers
                    ('text-align', 'right')
                ]},
                # Data cell styles
                {'selector': 'td', 'props': [
                    ('border', '1px dotted #ccc') # Subtle dotted borders around cells
                ]},
            ])
            .set_caption(title)
            .to_html(f'{title} {today}.html')
        )

if __name__ == "__main__":
    ic, bs = clean_df(csv_loader())
    table_names = ["Income Statement", "Balance Sheet"]
    style_tables([ic, bs], table_names)