import pandas as pd

def read_excel(file_path):
    df = pd.read_excel(file_path, skiprows=3)  # Skip the header information

    # Assuming the first two columns are 'Employee ID' and 'Name'
    # and the rest are days of the month with multiple entries
    df.columns = ['No', 'Name'] + [f'Day {i}' for i in range(1, len(df.columns) - 1)]

    # Convert time entries from string to a list of time objects
    for col in df.columns[2:]:
        df[col] = df[col].astype(str).apply(lambda x: x.split() if 'nan' not in x else [])

    return df
