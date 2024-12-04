from file_handling import input_file, new_folder, combine_csv_files
from preprocessing import preprocess_data
from processing import plot_sales_by_month, plot_sales_by_city, plot_sales_by_hour, plot_quantity_by_product, plot_quantity_vs_price_by_product
from analysis import save_top_10_products

def main():
    """Main Function"""
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
