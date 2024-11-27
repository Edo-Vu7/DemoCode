import pandas as pd
import os
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
file_name_global = ""

def submit():
    global file_name_global
    file_name = entry.get()
    if not file_name:
        'báo lỗi khi không nhập file'
        messagebox.showerror("Error", "File name cannot be empty")
    else:
        'thông báo file được nập'
        messagebox.showinfo("Input", f'The file name you entered is: {file_name}')
        file_name_global = file_name
        root.destroy()

' Tạo cửa sổ chính'
root = tk.Tk()
root.title("Dự án nhóm 3")

' Try cập ảnh'
image_path = r'D:\Game\Du_An\Phan_tich_Du_Lieu\Code\PTIT_logo.png'
img = Image.open(image_path)

'Chỉnh sửa ảnh'
img = img.resize((150, 150))
photo = ImageTk.PhotoImage(img)
image_label = tk.Label(root, image=photo)
image_label.pack(padx=20, pady=10)

' Tạo nhãn và ô nhập liệu'
label = tk.Label(root, text="Nhập vào tên file:")
label.pack(padx=20, pady=10)
entry = tk.Entry(root, width=50)
entry.pack(padx=20, pady=10)

' Tạo nút submit '
button = tk.Button(root, text="Submit", command=submit)
button.pack(padx=20, pady=20)

' Chạy vòng lặp chính của ứng dụng'
root.mainloop()

def get_file_name():
    """Prompt the user to input the file name."""
    return file_name_global

def load_data(file_name, path):
    """Load a single CSV file into a DataFrame."""
    file_path = os.path.join(path, file_name)
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"No such file: '{file_path}'")
    return pd.read_csv(file_path)

def combine_csv_files(path):
    """Combine all CSV files in the specified directory into a single DataFrame."""
    frames = []
    for file in os.listdir(path):
        if file.endswith('.csv'):
            filepath = os.path.join(path, file)
            df = pd.read_csv(filepath)
            frames.append(df)
    return pd.concat(frames)


def preprocess_data(df):
    """Perform data preprocessing and calculations."""
    df['Month'] = df['Order Date'].str[0:2]  # Extract month from Order Date
    df = df.dropna(how='all')  # Remove rows where all values are missing
    df = df[df['Month'] != 'Or']  # Remove invalid month data
    df['Quantity Ordered'] = pd.to_numeric(df['Quantity Ordered'], errors='coerce', downcast='integer')
    df['Price Each'] = pd.to_numeric(df['Price Each'], errors='coerce', downcast='float')
    df = df.dropna(subset=['Quantity Ordered', 'Price Each', 'Order Date'])  # Remove invalid data
    df['Sales'] = df['Quantity Ordered'] * df['Price Each']  # Calculate sales
    df.insert(4, 'Sales', df.pop('Sales'))  # Adjust column position
    return df

def plot_sales_by_month(df, output_file='sales_by_month.png'):
    """Generate and save a plot for sales by month."""
    monthly_sales = df.groupby('Month').sum(numeric_only=True)['Sales']
    months = range(1, 13)
    plt.bar(months, monthly_sales)
    plt.xticks(months)
    plt.xlabel('Months')
    plt.ylabel('Sales in USD')
    plt.savefig(output_file)
    plt.close()


def plot_sales_by_city(df, output_file='sales_by_city.png'):
    """Generate and save a plot for sales by city."""
    df['City'] = df['Purchase Address'].apply(lambda address: address.split(', ')[1])
    city_sales = df.groupby('City').sum(numeric_only=True)['Sales']
    cities = city_sales.index
    plt.bar(cities, city_sales)
    plt.xticks(cities, rotation=90, size=7)
    plt.xlabel('City')
    plt.ylabel('Sales in USD')
    plt.savefig(output_file)
    plt.close()


def plot_sales_by_hour(df, output_file='sales_by_hour.png'):
    """Generate and save a plot for sales by hour."""
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Hour'] = df['Order Date'].dt.hour
    hourly_sales = df.groupby('Hour').sum(numeric_only=True)['Sales']
    hours = range(24)
    plt.plot(hours, hourly_sales)
    plt.xticks(hours, rotation=90, size=7)
    plt.grid()
    plt.xlabel('Hours')
    plt.ylabel('Sales in USD')
    plt.savefig(output_file)
    plt.close()


def save_top_10_products(df, output_file='top10_products.csv'):
    """Save the top 10 products by count to a CSV file."""
    df_dup = df[df['Order ID'].duplicated(keep=False)]
    df_dup['All Products'] = df_dup.groupby('Order ID')['Product'].transform(lambda x: ', '.join(x))
    df_dup = df_dup[['Order ID', 'All Products']].drop_duplicates()
    df_dup['All Products'].value_counts().head(10).to_csv(output_file)


def plot_quantity_by_product(df, output_file='quantity_by_product.png'):
    """Generate and save a plot for quantity by product."""
    product_quantity = df.groupby('Product').sum(numeric_only=True)['Quantity Ordered']
    products = product_quantity.index
    plt.bar(products, product_quantity)
    plt.xticks(products, rotation=90, size=7)
    plt.xlabel('Product')
    plt.ylabel('Quantity Ordered')
    plt.savefig(output_file)
    plt.close()

def plot_quantity_vs_price_by_product(df, output_file='price_vs_quantity_by_product.png'):
    """Generate and save a plot comparing quantity versus price by product."""
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
    plt.savefig(output_file)
    plt.close()

def main():
    """Main function to orchestrate the loading, processing, and plotting of data."""
    path = r'D:\Game\Du_An\Phan_tich_Du_Lieu\Du_Lieu\\'
    file_name = get_file_name()
    try:
        df = load_data(file_name, path)
    except FileNotFoundError as e:
        print(e)
        return

    combined_df = combine_csv_files(path)
    combined_df.to_csv('annualSales2019.csv', index=False)

    processed_df = preprocess_data(combined_df)

    plot_sales_by_month(processed_df)
    plot_sales_by_city(processed_df)
    plot_sales_by_hour(processed_df)
    save_top_10_products(processed_df)
    plot_quantity_by_product(processed_df)
    plot_quantity_vs_price_by_product(processed_df)

if __name__ == "__main__":
    main()
