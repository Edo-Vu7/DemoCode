import os
from file_handling import get_base_path
folder_name = os.path.join(get_base_path(), "Sales_Report")

def save_top_10_products(df):
    """10 sản phẩm được bán nhiều nhất"""
    df_dup = df[df['Order ID'].duplicated(keep=False)]
    df_dup['All Products'] = df_dup.groupby('Order ID')['Product'].transform(lambda x: ', '.join(x))
    df_dup = df_dup[['Order ID', 'All Products']].drop_duplicates()
    output_file = os.path.join(folder_name, 'top10_products.csv')
    df_dup['All Products'].value_counts().head(10).to_csv(output_file)
