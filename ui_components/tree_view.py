# ui_components/tree_view.py
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont

def populate_treeview(df, tree):
    tree.delete(*tree.get_children())  # Clear existing data
    
    # Set up the columns
    tree['columns'] = list(df.columns)
    tree.column("#0", width=0, stretch=tk.NO)
    
    # Configure column widths and headings
    for ix, col in enumerate(df.columns):
        col_width = 100 if ix == 0 else 70  # Wider first column for dates
        tree.column(col, anchor=tk.W, width=col_width)
        tree.heading(col, text=col)

    # Populate the Treeview with data
    for index, row in df.iterrows():
        tree.insert("", tk.END, values=list(row))

    # Adjust the column widths to content
    for col in df.columns:
        tree.column(col, width=tkfont.Font().measure(col.title()))
