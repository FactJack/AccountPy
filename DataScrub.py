import pandas as pd
import re

# TO DO:
# ensure columns are adjusted for caps. ie: doesn't matter if date or Date
# experiement with split_df to take logic as an input for reusability line 29 & 150

def adj_credits_debit(row):
    """
    Implement a GAAP standard adjustment for credits and debits.
    Debits increase assets, decrease liabilities and equities.
    Effect is required to be either 'CREDIT' or 'DEBIT'.
    intended to be used with pandas DataFrame's apply method.

    Args:
        row: A pandas Series representing a row in the DataFrame with columns 'Type', 'Effect', and 'Amount'.
    """
    if row['Type'] == 'Asset':
        if row['Effect'] == 'CREDIT':
            return -abs(row['Amount'])
        else:
            return row['Amount']
    else:
        if row['Effect'] == 'DEBIT':
            return -abs(row['Amount'])
        else:
            return row['Amount']

def split_df(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]: # Intended to be reusable in clean_df function, needs further testing.
    """
    Splits a DataFrame into two based on categories containing 'expense' or 'revenue'.
    Requires the category column to be labeled 'Account'.
    Relies on regex for filtering.
    
    Args:
        df: DataFrame with 'date', 'Account', 'amount' columns
        
    Returns:
        tuple: (DataFrame with matching categories, DataFrame with non-matching categories)
    """
    pattern = re.compile(r'expense|revenue', flags=re.IGNORECASE)
    mask = df['Account'].str.contains(pattern, na=False) # Consider error handle for na values.
    matching_df = df[mask]
    non_matching_df = df[~mask]
    return matching_df, non_matching_df


def clean_df(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Cleans the DataFrame in preparation for financial reporting.
    Requires the DataFrame to have 'Date', 'Account', 'Type', 'Effect', and 'Amount' columns.
    This function has two main sub-functions:
        - clean_ic: Cleans and organizes the income statement DataFrame, pivots it, and calculates net income.
        - clean_bs: Cleans and organizes the balance sheet DataFrame, pivots it, and calculates totals.
    Args:
        df: DataFrame with 'Date', 'Account', 'Type', 'Effect', and 'Amount' columns.
    Returns:
        tuple: (DataFrame for income statement, DataFrame for balance sheet)
    """

    # Ensure required columns are present
    required_columns = ['Date', 'Account', 'Type', 'Effect', 'Amount']
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"Ledger must contain the following columns: {required_columns}")  
    
    # Convert 'Date' to datetime format and apply GAAP adjustments
    if df['Date'].dtype != 'datetime64[ns]':
        try:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')  # Convert to datetime, coerce errors to NaT
            # Need to ignore warnings
        except Exception as e:
            raise ValueError(f"Error converting 'Date' column to datetime: {e}")
 
    # Apply GAAP adjustments and establish new column.
    df['gaap_amount'] = df.apply(adj_credits_debit, axis = 1)

    # Resolve multiple day entries for the same account, add month index, and sort.
    daily = df.groupby([df['Date'].dt.date, 'Type', 'Account'])[['gaap_amount']].sum().reset_index()
    daily['year_month'] = daily['Date'].apply(lambda x: x.strftime('%Y-%m'))
    daily = daily.sort_values(['Account', 'year_month', 'Date']) # sort is required prior to cumsum

    # Split the DataFrame into income statement and balance sheet DataFrames
    ic, bs = split_df(daily)
    ic = ic.groupby(['Account', 'year_month'], as_index=False)['gaap_amount'].sum().round(2)
    bs = bs.groupby(['Account', 'Type', 'year_month'])['gaap_amount'].sum().groupby(level=0).cumsum().reset_index()

    def make_total_row(df, numeric_cols, label): # Need to incorporate into clean_ic revenue_totals, expense_totals
        """
        Create a total row DataFrame for the given section.
        Args:
            df: DataFrame (e.g., asset_items)
            numeric_cols: list of columns to sum
            label: string for the total row index (e.g., 'Total Assets')
        Returns:
            DataFrame with the total row, index set to label
        """
        total = df[numeric_cols].sum().to_frame().T
        total['Account'] = label
        total.set_index('Account', inplace=True)
        return total
    
    def numeric_cols(df: pd.DataFrame) -> list:
        return df.select_dtypes(include='number').columns
    
    # --- Income Statement Processing ---
    def clean_ic(ic: pd.DataFrame) -> pd.DataFrame:
        """
        Cleans the income statement DataFrame, pivots it, and calculates net income.
        Args:
            ic: DataFrame with 'Account', 'year_month', and 'gaap_amount' columns.
        Returns:
            DataFrame with cleaned income statement, split into revenues and expenses,
            with totals and net income calculated.
        """

        # Add a category column to distinguish revenues and expenses
        ic['Category'] = ic['Account'].str.contains(r'revenue', case=False, na=False).map({True: 'Revenue', False: 'Expense'})
        
        # Pivot the income statement: Accounts on rows, months as columns
        ic_pivot = ic.pivot_table(
            index=['Category', 'Account'], 
            columns='year_month', 
            values='gaap_amount', 
            aggfunc='sum', 
            fill_value=0
            ).reset_index()

        def calc_net_income(ic_pivot):
            """
            Calculate net income from the income statement pivot table.
            Net income is calculated as total revenues minus total expenses.
            
            Args:
                ic_pivot: DataFrame with 'Category' and 'Account' as index, months as columns.
                
            Returns:
                DataFrame with net income for each month.
            """
            month_cols = ic_pivot.select_dtypes(include='number').columns
            revenues = ic_pivot[ic_pivot['Category'] == 'Revenue'][month_cols].sum()
            expenses = ic_pivot[ic_pivot['Category'] == 'Expense'][month_cols].sum()
            net_income = revenues + expenses
            return pd.DataFrame([net_income])

        def split_expenses_revenues(ic_pivot): # Could optimize split_df to take reason as an input for reusability
            """
            Splits the pivoted income statement into expenses and revenues DataFrames,
            cleans up the Account names, and returns both.
            """
            ic_expenses = ic_pivot[ic_pivot['Category'] == 'Expense'].copy()
            ic_revenues = ic_pivot[ic_pivot['Category'] == 'Revenue'].copy()
            ic_expenses = ic_expenses.drop(columns=['Category'])
            ic_revenues = ic_revenues.drop(columns=['Category'])
            ic_expenses['Account'] = ic_expenses['Account'].str.replace(r'Expense\s*', '', regex=True)
            ic_revenues['Account'] = ic_revenues['Account'].str.replace(r'Revenue\s*', '', regex=True)
            ic_expenses.set_index('Account', inplace=True)
            ic_revenues.set_index('Account', inplace=True)
            return ic_expenses, ic_revenues
        
        # Split out revenues and expenses
        ic_expenses, ic_revenues = split_expenses_revenues(ic_pivot)

        # Calculate totals for each
        revenue_totals = make_total_row(ic_revenues, numeric_cols(ic_revenues), 'Total Revenues')
        expense_totals = make_total_row(ic_expenses, numeric_cols(ic_expenses), 'Total Expenses')

        # Calculate net income
        net_income_pivot = calc_net_income(ic_pivot)
        net_income_pivot['Account'] = 'Net Income'
        net_income_pivot.set_index('Account', inplace=True)

        # Concatenate in order: revenues, revenue total, expenses, expense total, net income
        ic_final = pd.concat(
            [ic_revenues, revenue_totals, -ic_expenses, -expense_totals, net_income_pivot], 
            keys = ['Revenues', '', 'Expenses', '', 'Net Income']
            )

        # Add year total column
        month_cols = [col for col in ic_final.columns if re.match(r'\d{4}-\d{2}', str(col))]
        ic_final['Year Total'] = ic_final[month_cols].sum(axis=1)
        ic_final = ic_final.round(2)

        return ic_final, net_income_pivot
    
    ic_final, net_income = clean_ic(ic)

    # --- Balance Sheet Processing ---
    def clean_bs(bs: pd.DataFrame, net_income:pd.DataFrame) -> pd.DataFrame:
        """
        Cleans the balance sheet DataFrame, pivots it, and calculates totals.
        Args:
            bs: DataFrame with 'Account', 'Type', 'year_month', and 'gaap_amount' columns.
        Returns:
            DataFrame with cleaned balance sheet, split into assets, liabilities, and equities,
            with totals calculated.
        """
        # Pivot the balance sheet: Accounts on rows, months as columns
        bs_pivot = bs.pivot_table(
            index=['Type', 'Account'], 
            columns='year_month', 
            values='gaap_amount', 
            aggfunc='sum'
            ).reset_index()

        numeric_cols = bs_pivot.select_dtypes(include='number').columns

        bs_pivot[numeric_cols] = bs_pivot[numeric_cols].fillna(method='ffill', axis=1)

        # Seperate the balance sheet into assets, liabilities, and equities
        asset_items = bs_pivot[bs_pivot['Type'] == 'Asset'].copy()
        asset_items.drop(columns=['Type'], inplace=True)
        asset_items.set_index('Account', inplace=True)

        liability_items = bs_pivot[bs_pivot['Type'] == 'Liability'].copy()
        liability_items.drop(columns=['Type'], inplace=True)
        liability_items.set_index('Account', inplace=True)

        equity_items = bs_pivot[bs_pivot['Type'] == 'Equity'].copy()
        equity_items.drop(columns=['Type'], inplace=True)
        equity_items.set_index('Account', inplace=True)
        equity_items = pd.concat([net_income.cumsum(axis=1), equity_items])

        # Calculate totals for each section
        total_assets = make_total_row(asset_items, numeric_cols, 'Total Assets')
        total_liabilities = make_total_row(liability_items, numeric_cols, 'Total Liabilities')
        total_equities = make_total_row(equity_items, numeric_cols, 'Total Equity')

        # Concatenate in order: assets, total assets, liabilities, total liabilities, equities, total equities
        bs_final = pd.concat(
            [asset_items, total_assets, liability_items, total_liabilities, equity_items, total_equities], 
            keys=['Assets', '', 'Liabilities', '', 'Equities', '']
            )
        bs_final = bs_final.round(2)

        return bs_final
    
    bs_final = clean_bs(bs, net_income)

    #bs_final.reset_index(inplace=True) # problem not showing accounts on display_table in main.py
    #ic_final.reset_index(inplace=True) # problem

    return ic_final, bs_final



