import matplotlib.pyplot as plt
import pandas as pd
import os
from file_handling import get_base_path
folder_name = os.path.join(get_base_path(), 'Sales_Report')

def plot_sales_by_month(df):
    """bảng giá trị bán đươợc mỗi tháng"""
    monthly_sales = df.groupby('Month').sum(numeric_only=True)['Sales']
    months = range(1, 13)
    plt.bar(months, monthly_sales)
    plt.xticks(months)
    plt.xlabel('Months')
    plt.ylabel('Sales in USD')
    output_file = os.path.join(folder_name, 'sales_by_month.png')
    plt.savefig(output_file)
    plt.close()

def plot_sales_by_city(df):
    """bảng giá trị bán được theo thành phố"""
    df['City'] = df['Purchase Address'].apply(lambda address: address.split(', ')[1])
    city_sales = df.groupby('City').sum(numeric_only=True)['Sales']
    cities = city_sales.index
    plt.bar(cities, city_sales)
    plt.xticks(cities, rotation=90, size=7)
    plt.xlabel('City')
    plt.ylabel('Sales in USD')
    output_file = os.path.join(folder_name, 'sales_by_city.png')
    plt.savefig(output_file)
    plt.close()

def plot_sales_by_hour(df):
    """bản giá trị bán được theo giờ"""
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Hour'] = df['Order Date'].dt.hour
    hourly_sales = df.groupby('Hour').sum(numeric_only=True)['Sales']
    hours = range(24)
    plt.plot(hours, hourly_sales)
    plt.xticks(hours, rotation=90, size=7)
    plt.grid()
    plt.xlabel('Hours')
    plt.ylabel('Sales in USD')
    output_file = os.path.join(folder_name, 'sales_by_hour.png')
    plt.savefig(output_file)
    plt.close()

def plot_quantity_by_product(df):
    """bảng số lượng bán được của mỗi sản phẩm"""
    product_quantity = df.groupby('Product').sum(numeric_only=True)['Quantity Ordered']
    products = product_quantity.index
    plt.bar(products, product_quantity)
    plt.xticks(products, rotation=90, size=7)
    plt.xlabel('Product')
    plt.ylabel('Quantity Ordered')
    output_file = os.path.join(folder_name, 'quantity_by_product.png')
    plt.savefig(output_file)
    plt.close()

def plot_quantity_vs_price_by_product(df):
    """bảng so sánh số lượng sản phẩm với giá cả của từng sản phẩm"""
    product_quantity = df.groupby('Product').sum(numeric_only=True)['Quantity Ordered']
    product_prices = df.groupby('Product')['Price Each'].mean()
    products = product_quantity.index
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.bar(products, product_quantity, color='g')
    ax2.plot(products, product_prices, 'b')
    ax1.set_xticklabels(products, rotation=90, size=8)
    ax1.set_xlabel('Products')
    ax1.set_ylabel('Quantity Ordered', color='g')
    ax2.set_ylabel('Price Each', color='b')
    output_file = os.path.join(folder_name, 'price_vs_quantity_by_product.png')
    plt.savefig(output_file)
    plt.close()
