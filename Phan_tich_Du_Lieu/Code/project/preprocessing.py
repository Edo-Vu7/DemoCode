import pandas as pd
import os
from file_handling import get_base_path

def preprocess_data(df):
    """chỉnh sửa lại dữ liệu"""
    folder_name = "Sales_Report"
    df['Month'] = df['Order Date'].str[0:2]
    df = df.dropna(how='all')
    df = df[df['Month'] != 'Or']
    df['Quantity Ordered'] = pd.to_numeric(df['Quantity Ordered'], errors='coerce', downcast='integer')
    df['Price Each'] = pd.to_numeric(df['Price Each'], errors='coerce', downcast='float')
    df = df.dropna(subset=['Quantity Ordered', 'Price Each', 'Order Date'])
    df['Sales'] = df['Quantity Ordered'] * df['Price Each']
    df.insert(4, 'Sales', df.pop('Sales'))
    folder = os.path.join(get_base_path(), folder_name)
    data = os.path.join(folder, 'Report_Sales_2019.csv')
    df.to_csv(data, index=False)
    return df
