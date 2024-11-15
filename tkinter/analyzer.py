# import dataset
import tkinter as tk
from tkinter import ttk,filedialog,messagebox
import pandas as pd

rows,cols = 0,0
df = None

def load_dataset():
    global df
    filepath = filedialog.askopenfilename(title = "Select a file",filetypes = (("CSV Files",".csv"),("All Files","*.*")))
    if filepath:
        try:
            if '.xls' in filepath:
                df = pd.read_excel(filepath)
            elif '.csv' in filepath:
                df = pd.read_csv(filepath)
            
            clear_table()
            create_filter_entries()
            
            columns = [i.replace(" ","") for i in df.columns]
            tree["columns"] = columns
            
            for col in columns:
                tree.heading(col,text = col)
                tree.column(col,anchor = tk.CENTER,width=20,stretch = True)

            for row in df.iloc[:,:].itertuples(index=False):
                tree.insert("",tk.END,values=row)

            root.geometry(f"{len(df.columns) * 65}x400")
            root.title(f"Analyzer 1.0 {filepath}")
            rows,cols = df.shape[0],df.shape[1]
            bottom_text.configure(text=f"{rows} Total Rows, {cols} Cols")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {str(e)}")

def clear_table():
    for item in tree.get_children():
        tree.delete(item)

# Filter entries
def create_filter_entries():
    global filter_entries,df
    filter_entries = []
    
    # Clear existing filter entries if any
    for widget in filter_frame.winfo_children():
        widget.destroy()
    
    # for col in df.columns:
    #     label = tk.Label(filter_frame, text=col.replace(" ", ""))
    #     label.pack(side=tk.LEFT, padx=5)

    #     entry = tk.Entry(filter_frame)
    #     entry.pack(side=tk.LEFT, padx=5)
    #     # entry.bind("<KeyRelease>", filter_data)  # Bind key release event to filtering function

    #     filter_entries.append(entry)
    
    # Create entry fields for filtering
    for col in df.columns:
        label = tk.Label(filter_frame, text=col.replace(" ", ""))
        label.grid(row=0, column=len(filter_entries), sticky="ew")

        entry = tk.Entry(filter_frame)
        entry.grid(row=1, column=len(filter_entries), sticky="ew")
        entry.bind("<KeyRelease>", apply_filters)  # Bind key release event to filtering function

        filter_entries.append(entry)

# Function to update the table with rows based on a DataFrame
def update_table(data):
    clear_table()  # Clear the existing rows
    
    if data is None:
        return

    # Set column headers
    columns = [i.replace(" ","") for i in df.columns]
    tree["columns"] = list(data.columns)
    for col in data.columns:
        tree.heading(col, text=col)
        tree.column(col, anchor=tk.CENTER, width=100, stretch=True)  # Adjust column width

    # Get the selected row limit from the dropdown
    limit = row_limit.get()
    if limit != 'ALL':
        limit = int(limit)
        data = data.head(limit)  # Display only the limited number of rows

    # Insert rows into the Treeview
    for row in data.itertuples(index=False):
        tree.insert("", tk.END, values=row)

    root.geometry(f"{len(df.columns) * 65}x400")
    rows,cols = data.shape[0],data.shape[1]
    bottom_text.configure(text=f"{rows} Total Rows, {cols} Cols")

# Function to filter the DataFrame based on the input values in the filter entries
def apply_filters(event=None):
    global df

    if df is None:
        return

    # Create a mask for filtering
    mask = pd.Series([True] * len(df))

    # Apply filters based on the entries
    for entry, col in zip(filter_entries, df.columns):
        filter_value = entry.get()
        if filter_value:  # Only filter if the entry is not empty
            mask &= df[col].astype(str).str.contains(filter_value, case=False, na=False)

    # Get filtered data and update the table
    filtered_data = df[mask]
    update_table(filtered_data)

# Function to handle row limit change
def on_row_limit_change(event=None):
    if df is not None:
        apply_filters()  # Reapply filters when the row limit is changed

# Function to analyze dataset and show descriptive statistics in a new window
def analyze_dataset():
    if df is None:
        messagebox.showerror("Error", "No dataset loaded.")
        return

    # Create a new window for displaying the analysis
    analysis_window = tk.Toplevel(root)
    analysis_window.title("Dataset Analysis")
    analysis_window.geometry("600x400")

    # Add a text widget to display the analysis
    analysis_text = tk.Text(analysis_window, wrap=tk.WORD)
    analysis_text.pack(expand=True, fill=tk.BOTH)

    # Add descriptive statistics
    analysis_text.insert(tk.END, "Descriptive Statistics:\n\n")
    
    # Show number of null values in each column
    analysis_text.insert(tk.END, "Null Values per Column:\n")
    analysis_text.insert(tk.END, str(df.isnull().sum()) + "\n\n")

    # Show descriptive statistics for numerical columns
    analysis_text.insert(tk.END, "Numerical Summary (df.describe()):\n")
    try:
        describe_all = df.describe(include='all')  # Include all columns, not just numerical
        analysis_text.insert(tk.END, str(describe_all) + "\n\n")
    except Exception as e:
        analysis_text.insert(tk.END, f"Error in describe(): {str(e)}\n\n")

    # Show data types of the columns
    analysis_text.insert(tk.END, "Data Types:\n")
    analysis_text.insert(tk.END, str(df.dtypes) + "\n\n")

    # Show basic column information
    analysis_text.insert(tk.END, "Column Information:\n")
    df_info = df.info(buf=None)
    analysis_text.insert(tk.END, str(df_info) + "\n")


# GUI Design

root = tk.Tk()
root.title("Analyzer 1.0")
root.geometry("600x400")

# Frame for filters
filter_frame = tk.Frame(root)
filter_frame.pack(expand=True, fill = tk.BOTH)

table_frame = tk.Frame(root)
table_frame.pack(expand = True,fill = tk.BOTH)

tree = ttk.Treeview(table_frame,show = 'headings')

vsb = ttk.Scrollbar(table_frame,orient='vertical')
vsb.pack(side = tk.RIGHT,fill = tk.Y)

hsb = ttk.Scrollbar(table_frame,orient='horizontal')
hsb.pack(side = tk.BOTTOM,fill = tk.X)

tree.pack(side = tk.LEFT,expand = True, fill = tk.BOTH)
tree.configure(yscrollcommand=vsb.set)
vsb.config(command = tree.yview)
tree.configure(xscrollcommand=hsb.set)
hsb.config(command = tree.xview)

button_frame = tk.Frame(root)
button_frame.pack(fill = tk.X,pady=10)

button = tk.Button(table_frame,text="Load Dataset",command = load_dataset)
button.pack(pady = 10)

# Button to analyze dataset
analyze_button = tk.Button(table_frame, text="Analyze Dataset", command=analyze_dataset)
analyze_button.pack(pady=10)

# Combobox for selecting the number of rows to display
row_limit = ttk.Combobox(table_frame, values=["50","100","500","1000", "10000", "100000", "ALL"], state="readonly")
row_limit.current(0)  # Set default selection to 1000 rows
row_limit.pack(pady=10)
row_limit.bind("<<ComboboxSelected>>", on_row_limit_change)  # Bind event when selection changes



bottom_text = tk.Label(root,text=f"{rows} Rows, {cols} Cols")
bottom_text.pack(pady = 10,side = tk.RIGHT)

root.mainloop()