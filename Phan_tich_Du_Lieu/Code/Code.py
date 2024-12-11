import pandas as pd
import os
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk

file_name_global = ""
folder_name= ""
def input_file():
    def submit():
        global file_name_global
        file_name = filedialog.askopenfilename(
            title="Select a File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
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
    image_path = r'D:\Game\Du_An\Phan_tich_Du_Lieu\Code\project\PTIT_logo.png'
    img = Image.open(image_path)
    'Chỉnh sửa ảnh'
    img = img.resize((200, 200))
    photo = ImageTk.PhotoImage(img)
    image_label = tk.Label(root, image=photo)
    image_label.pack(padx=20, pady=10)
    ' Tạo nhãn và ô nhập liệu'
    label = tk.Label(root, text="Vui lòng chọn file:")
    label.pack(padx=20, pady=10)
    ' Tạo nút submit '
    button = tk.Button(root, text="Chọn file", command=submit)
    button.pack(padx=20, pady=20)
    ' Chạy vòng lặp chính của ứng dụng '
    root.mainloop()

def new_folder():
    global folder_name
    folder_name  = "Sales_Report"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def get_file_name():
    """Trả về file nhập vào từ app"""
    return file_name_global

def combine_csv_files(path):
    """Gộp tất cả các file .csv DataFrame."""
    frames = []
    for file in os.listdir(path):
        if file.endswith('.csv'):
            filepath = os.path.join(path, file)
            df = pd.read_csv(filepath)
            frames.append(df)
    output_file = os.path.join(folder_name, 'annualSales2019.csv')
    data = pd.concat(frames)
    data.to_csv(output_file, index=False)
    return data

def preprocess_data(df):
    """Thêm cột Month và Sales """
    df['Month'] = df['Order Date'].str[0:2]
    df = df.dropna(how='all')
    df = df[df['Month'] != 'Or']
    df['Quantity Ordered'] = pd.to_numeric(df['Quantity Ordered'], errors='coerce', downcast='integer')
    df['Price Each'] = pd.to_numeric(df['Price Each'], errors='coerce', downcast='float')
    df = df.dropna(subset=['Quantity Ordered', 'Price Each', 'Order Date'])
    df['Sales'] = df['Quantity Ordered'] * df['Price Each']
    df.insert(4, 'Sales', df.pop('Sales'))
    data = os.path.join(folder_name, 'Report_Sales_2019.csv')
    df.to_csv(data, index=False)
    return df

def plot_sales_by_month(df):
    """Biểu diễn Sale của mỗi tháng"""
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
    """Biểu diễn Sale của mỗi thành phố"""
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
    """Biểu diễn Sale tại mỗi khung giờ"""
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

def save_top_10_products(df):
    """10 sản phẩm bán chạy"""
    df_dup = df[df['Order ID'].duplicated(keep=False)]
    df_dup['All Products'] = df_dup.groupby('Order ID')['Product'].transform(lambda x: ', '.join(x))
    df_dup = df_dup[['Order ID', 'All Products']].drop_duplicates()
    output_file = os.path.join(folder_name, 'top10_products.csv')
    df_dup['All Products'].value_counts().head(10).to_csv(output_file)

def plot_quantity_by_product(df):
    """Số lượng bán được của mỗi sản phẩm"""
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
    """So sánh giá và số lượng sản phẩm bán được"""
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

def main():
    """Hàm chính"""
    path = r'D:\Game\Du_An\Phan_tich_Du_Lieu\Du_Lieu\\'
    input_file()
    new_folder()
    combined_df = combine_csv_files(path)
    processed_df = preprocess_data(combined_df)
    plot_sales_by_month(processed_df)
    plot_sales_by_city(processed_df)
    plot_sales_by_hour(processed_df)
    save_top_10_products(processed_df)
    plot_quantity_by_product(processed_df)
    plot_quantity_vs_price_by_product(processed_df)
if __name__ == "__main__":
    main()
