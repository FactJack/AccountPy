# AccountPy
Python automated accounting reports

Run the program, generates reports! 

### Updates
 - New Visual! Account Forecast Calendar can project the balance of an account based on given deposits and withdraw schedule.

### Key Features:
 - Receives .csv GAAP compliant ledger.
 - Detailed Balance Sheet for end of month reporting.
 - Year end Balance Sheet for consolidated reporting
 - Detailed Income Summary for monthly budget reporting.
 - Outputs HTML for ease of viewing, printing and storing.

### Assumptions:
 - General Ledger is compliant with the foundations of Generally Accepted Accounting Principals.
 - Ledger columns: Date, Effect, Account, Amount, Type, Notes
 - Effect values are either CREDIT or DEBIT.
 - Type values are either Asset, Liability or Equity.
 - Income temporary accounts end in Revenue or Expense.

### Current Status:
 - AccountPy is a work in progress, open source solution for business reports.
 - Mission: Allow accounting professionals freedom to manage ledgers without restrictive software and automate business reports.
 - Inspiration: Software that requires subscriptions while restricting bookkeeper ability to manage ledgers.
 - Development Phase: AccountPy is in Exploration.

### To Do:
 - Statement of Cash Flows
 - Year end income summary
 - Case insensitive effect, account, and type values.
 - UI for ledger input.
 - Include required packages
 - Visuals!
    - Income Bar chart with comparative liability payments
    - Balance sheet 3 month trailing indicator
    - Expense Quilt
    - More! 
