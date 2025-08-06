**AccountPy** is a modular, user-friendly tool for generating professional accounting reports from CSV ledgers. Designed for tech-savvy accounting professionals, it automates business reporting and encourages community-driven improvements.

![Python](https://img.shields.io/badge/python-3.6%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Contributions](https://img.shields.io/badge/contributions-welcome-brightgreen)

---

## 🎯 Mission

Empower accounting professionals to manage ledgers without restrictive software, automate business reports, and collaborate for continuous improvement.

---

## 🚀 Quick Start

1. **Clone the repository**  
   ```sh
   git clone https://github.com/FactJack/AccountPy.git
   cd AccountPy
   ```

2. **Install dependencies**  
   ```sh
   pip install pandas tkinter Jinja2 reportlab
   ```

3. **Run the program**  
   ```sh
   python DisplayUI.py
   ```
   or for HTML export:
   ```sh
   python OutputHTML.py
   ```

---

## ✨ Features

- **Intuitive UI:**  
  Select your ledger file and view/export reports with a simple interface.
- **Modular Design:**  
  Plug-and-play UI experience for easy extension.
- **Financial Reports:**  
  - Monthly Income Statement with YTD totals  
  - Balance Sheet
- **Automatic Net Income Calculation:**  
  No need to ledger a net income amount—it's computed for you.
- **Export Options:**  
  - PDF export ([`DisplayUI.py`](DisplayUI.py))
  - HTML export ([`OutputHTML.py`](OutputHTML.py))

---

## 📋 Prerequisites

- **OS:** macOS or Windows (not optimized for Linux)
- **Python:** 3.6+
- **Packages:**  
  - pandas  
  - tkinter  
  - Jinja2 (for HTML export)  
  - reportlab (for PDF export)
- **General Ledger CSV:**  
  - **Format:** See [`Sample ledger.csv`](Sample%20ledger.csv)
  - **Required Columns:**  
    - `Date`
    - `Effect` (`CREDIT` or `DEBIT`)
    - `Account`
    - `Type` (`Asset`, `Liability`, `Equity`; case-insensitive)
    - `Amount`
  - **GAAP Compliant:** Dual entry (Credits = Debits)
  - **Temporary Accounts:**  
    - Include 'revenue' or 'expense' in the account name for income statement inclusion (case-insensitive).  
    - Others are included under equity in the balance sheet.

---

## 🛠️ How It Works

- **CSV Loader:**  
  Select your ledger file via a GUI ([`csvLoaderGUI.py`](csvLoaderGUI.py)).
- **Data Scrubbing:**  
  Data is cleaned and validated ([`DataScrub.py`](DataScrub.py)).
- **Report Generation:**  
  - View and export reports in PDF ([`DisplayUI.py`](DisplayUI.py))
  - Export styled HTML reports ([`OutputHTML.py`](OutputHTML.py))

---

## 🆕 Updates

- **7.2.2025:**  
  - V2 Release. Complete backend logic redesign for accurate balances and cumulative totals.
  - Modular, polymorphic functions for easier development.
  - Preview UI with PDF export.

---

## 🗺️ Roadmap

- V3: move from procedural to object-oreinted (`Transaction`, `Account` and `Ledger` classes) for building expanded reports, program GAAP rules into methods and scaling.
- Statement of Cash Flows
- Visualizations:
  - Income bar chart with comparative liability payments
  - Balance sheet 3-month trailing indicator
  - Expense quilt
  - More!

---

## 🤝 Contributing

Contributions are welcome!  
- Fork the repo and submit a pull request.
- Open issues for bugs or feature requests.

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.
