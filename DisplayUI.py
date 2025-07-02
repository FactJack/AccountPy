import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.fonts import tt2ps
from csvLoaderGUI import csv_loader
from DataScrub import clean_df

# todo:
# export_to_pdf function has left and right margins running off the page, need to adjust
# export_to_pdf add a header to the pdf with the title of the table
# export_to_pdf function should handle empty DataFrames gracefully displaying empty instead of 0. 
def export_to_pdf(df, title):
    """
    Export a DataFrame to a PDF file with a table.
    
    Args:
        df (pandas.DataFrame): DataFrame to export.
        title (str): Title for the PDF and filename.
    """
    file_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")],
        title="Save PDF As",
        initialfile=f"{title}.pdf"
    )
    if not file_path:
        return

    try:
        # Use landscape orientation
        from reportlab.lib.pagesizes import landscape
        page_size = landscape(letter)  # 792 x 612 points
        doc = SimpleDocTemplate(
            file_path,
            pagesize=page_size,
            leftMargin=0.25 * inch,
            rightMargin=0.25 * inch,
            topMargin=0.25 * inch,
            bottomMargin=0.25 * inch
        )
        elements = []

        # Add title as a header
        styles = getSampleStyleSheet()
        title_style = styles['Heading1']
        title_style.alignment = 1  # Center alignment
        title_paragraph = Paragraph(title, title_style)
        elements.append(title_paragraph)
        elements.append(Paragraph("<br/>", styles['Normal']))  # Add spacing after title

        # Handle empty DataFrame
        if df.empty:
            elements.append(Paragraph("No data available.", styles['Normal']))
        else:
            # Prepare data for table, replacing zeros with empty strings
            data = [df.columns.tolist()]  # Headers
            for _, row in df.iterrows():
                display_row = ['' if isinstance(val, (int, float)) and val == 0 else val for val in row.tolist()]
                data.append(display_row)

            # Calculate dynamic column widths based on content
            num_cols = len(df.columns)
            page_width = page_size[0] - (doc.leftMargin + doc.rightMargin)  # Available width
            col_widths = []

            # Font settings for width calculation
            header_font = 'Helvetica-Bold'
            cell_font = 'Helvetica'
            header_font_size = 12
            cell_font_size = 10

            # Calculate maximum width for each column
            for col_idx in range(num_cols):
                # Get all values in this column, including header
                col_values = [str(row[col_idx]) for row in data]
                # Calculate width for header (bold font)
                header_width = stringWidth(
                    col_values[0],
                    tt2ps(header_font, 0, 0),
                    header_font_size
                )
                # Calculate width for data cells
                cell_widths = [
                    stringWidth(str(val), tt2ps(cell_font, 0, 0), cell_font_size)
                    for val in col_values[1:]
                ]
                # Use the maximum width (header or widest cell) plus padding
                max_width = max([header_width] + cell_widths) + 10  # Add padding (10 points)
                col_widths.append(max_width)

            # Scale widths to fit page if total exceeds page width
            total_width = sum(col_widths)
            if total_width > page_width:
                scale_factor = page_width / total_width
                col_widths = [w * scale_factor for w in col_widths]

            # Create table with dynamic column widths
            table = Table(data, colWidths=col_widths)

            # Apply table style
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BOX', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))

            elements.append(table)

        # Build PDF
        doc.build(elements)
        messagebox.showinfo("Success", f"PDF saved successfully to {file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to export PDF:\n{str(e)}")

def display_tables(dataframes, table_names):
    """
    Display multiple DataFrames as tables in a Tkinter GUI using ttk.Treeview.
    Includes an export to PDF button for each table.
    
    Args:
        dataframes (list): List of pandas DataFrames to display.
        table_names (list): List of table names for tab labels.
    """
    # Create main window
    root = tk.Tk()
    root.title("Data Tables")
    root.geometry("800x600")
    root.configure(bg="#f0f0f0")

    # Create notebook for tabs
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)

    # Style configuration for Treeview
    style = ttk.Style()
    style.configure("Treeview",
                    font=("Arial", 10),
                    rowheight=25,
                    background="white",
                    foreground="black")
    style.configure("Treeview.Heading",
                    font=("Arial", 11, "bold"),
                    background="#4a90e2",
                    foreground="white")
    style.map("Treeview",
              background=[("selected", "#e0e0e0")],
              foreground=[("selected", "black")])

    # Add each DataFrame as a table in a separate tab
    for df, name in zip(dataframes, table_names):
        # Create a frame for each tab
        tab = ttk.Frame(notebook)
        notebook.add(tab, text=name)

        # Create button frame for export button
        button_frame = ttk.Frame(tab)
        button_frame.pack(fill="x", padx=5, pady=5)

        # Add export to PDF button
        export_button = ttk.Button(
            button_frame,
            text="Export to PDF",
            command=lambda d=df, n=name: export_to_pdf(d, n),
            style="TButton"
        )
        export_button.pack(side="left")

        # Create Treeview
        tree = ttk.Treeview(tab, show="headings")
        tree.pack(fill="both", expand=True, padx=5, pady=5)

        # Add scrollbars
        yscroll = ttk.Scrollbar(tab, orient="vertical", command=tree.yview)
        xscroll = ttk.Scrollbar(tab, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)
        yscroll.pack(side="right", fill="y")
        xscroll.pack(side="bottom", fill="x")

        # Define columns
        columns = df.columns.tolist()
        tree["columns"] = columns
        for col in columns:
            tree.heading(col, text=col, anchor="w")
            tree.column(col, width=150, anchor="center")

        # Insert data
        for _, row in df.iterrows():
            display_values = ['' if isinstance(val, (int, float)) and val == 0 else val for val in row.tolist()]
            tree.insert("", "end", values=display_values)

        # Add alternating row colors for readability
        tree.tag_configure("evenrow", background="#f5f9fa")
        for i, item in enumerate(tree.get_children()):
            if i % 2 == 0:
                tree.item(item, tags=("evenrow",))

    # Configure button style
    style.configure("TButton",
                    font=("Arial", 10, "bold"),
                    padding=5)

    root.mainloop()

if __name__ == "__main__":
    ic, bs = clean_df(csv_loader())
    table_names = ["Income Statement", "Balance Sheet"]
    display_tables([ic, bs], table_names)