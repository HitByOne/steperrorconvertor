import streamlit as st
import pandas as pd
import re

# Set page configuration to wide mode
st.set_page_config(layout="wide")

# Function to extract 'Item' text from the input string
def extract_item(input_string):
    # Extract text between the first [ and ,
    match = re.search(r'\[([^\],]+),', input_string)
    if match:
        return match.group(1)
    return None

# Function to extract 'Error' text after '[Error:' and before '(FullSyndicate'
def extract_error(input_string):
    # Extract text after '[Error:' and before '(FullSyndicate'
    match = re.search(r'\[Error:\s*(.*?)\(FullSyndicate', input_string)
    if match:
        return match.group(1).strip()  # Strip to remove leading/trailing spaces
    # Fallback: If '(FullSyndicate' is not present, just extract after '[Error:'
    match = re.search(r'\[Error:\s*(.*)', input_string)
    if match:
        return match.group(1).strip()  # Strip to remove leading/trailing spaces
    return None

# Streamlit app
st.title('Excel/CSV Processor for Item and Error Extraction')

# Upload Excel or CSV file
uploaded_file = st.file_uploader("Choose an Excel or CSV file", type=["xlsx", "csv"])

if uploaded_file:
    # Handle Excel or CSV file based on the file extension
    if uploaded_file.name.endswith('.xlsx'):
        # Load the Excel file, assume no headers (header=None)
        df = pd.read_excel(uploaded_file, header=None)
    elif uploaded_file.name.endswith('.csv'):
        # Load the CSV file, assume no headers (header=None)
        df = pd.read_csv(uploaded_file, header=None)
    
    # Check if the file has at least 3 columns (column C would be index 2)
    if len(df.columns) > 2:
        column_c = df.iloc[:, 2]  # Select column C (third column)
        
        # Apply extraction functions to column C
        df['Item'] = column_c.apply(extract_item)
        df['Error'] = column_c.apply(extract_error)
        
        # Remove rows where 'Item' or 'Error' are blank (None or empty strings)
        df_cleaned = df.dropna(subset=['Item', 'Error'])  # Drop rows with NaN in 'Item' or 'Error'
        df_cleaned = df_cleaned[(df_cleaned['Item'] != '') & (df_cleaned['Error'] != '')]  # Remove empty strings
        
        # Display the processed DataFrame
        st.write("Processed Data:")
        st.dataframe(df_cleaned[['Item', 'Error']])
        
        # Option to download the resulting DataFrame as CSV
        csv = df_cleaned[['Item', 'Error']].to_csv(index=False)
        st.download_button(
            label="Download Processed Data as CSV",
            data=csv,
            file_name='processed_data.csv',
            mime='text/csv',
        )
    else:
        st.error("The uploaded file doesn't have enough columns.")
