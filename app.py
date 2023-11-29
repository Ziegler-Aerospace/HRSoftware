import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from data_processing.excel_reader import read_excel
from data_processing.time_calculator import calculate_hours
from ui_components.tree_view import populate_treeview

# root = tk.Tk()
# root.title("Work Management Application")

# # Initialize global variable to store the calculated data
# calculated_df = None

# # Create Treeview widget
# tree = ttk.Treeview(root)
# tree.pack(pady=20, padx=20, fill='x', expand=True)

# # Add a scrollbar
# scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=tree.yview)
# scrollbar.pack(side=tk.RIGHT, fill='y')
# tree.configure(yscroll=scrollbar.set)

# # Function to open Excel file and display its content
# def open_file():
#     global file_path
#     file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls"), ("CSV files", "*.csv")])
#     if file_path:
#         df = read_excel(file_path)
#         populate_treeview(df, tree)

# # Function to calculate and display worked hours
# def calculate_hours_button_pressed():
#     global calculated_df
#     global file_path
#     if file_path:
#         df = read_excel(file_path)  # Use the global file_path
#         calculated_df = calculate_hours(df)
#         populate_treeview(calculated_df, tree)
#     else:
#         messagebox.showerror("Error", "Please open a file first.")

# # Function to download the calculated hours as an Excel file
# def download_file():
#     global calculated_df
#     if calculated_df is not None:
#         file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
#                                                  filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")])
#         if file_path:
#             calculated_df.to_excel(file_path, index=False)
#             messagebox.showinfo("Success", f"File has been saved to {file_path}")
#     else:
#         messagebox.showerror("Error", "No data to save. Calculate hours first.")

# # Button to open Excel file
# open_button = tk.Button(root, text="Open Excel File", command=open_file)
# open_button.pack(pady=20)

# # Button to calculate hours
# calculate_button = tk.Button(root, text="Calculate Hours", command=calculate_hours_button_pressed)
# calculate_button.pack(pady=20)

# # Button to download the file
# download_button = tk.Button(root, text="Download File", command=download_file)
# download_button.pack(pady=20)

# root.mainloop()


# The given file path for reading and writing
# input_file_path = './11Summary.xls'
input_file_path = './11Summary.xls'
output_file_path = './11final_file.xlsx'

# Read the Excel file directly from the given path
df = read_excel(input_file_path)

#input no. of PH
num_ph = int(input("Enter the number of Public Holidays (PH): "))

# Calculate the hours based on the read data
calculated_df = calculate_hours(df, num_ph)

# Save the calculated hours to an Excel file in the given path
calculated_df.to_excel(output_file_path, index=False)

print(f"The calculated data has been saved to {output_file_path}")