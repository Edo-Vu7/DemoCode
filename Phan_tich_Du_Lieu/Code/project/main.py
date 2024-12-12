from file_handling import input_file, new_folder, combine_csv_files
from preprocessing import preprocess_data
from processing import plot_sales_by_month, plot_sales_by_city, plot_sales_by_hour, plot_quantity_by_product, plot_quantity_vs_price_by_product
from see_report import see_report
from analysis import top_10_products_saletogether

def main():
    """hàm chính"""
    path = r'D:\Game\Du_An\Phan_tich_Du_Lieu\Du_Lieu\\'
    input_file()
    new_folder()
    combined_df = combine_csv_files(path)
    processed_df = preprocess_data(combined_df)
    plot_sales_by_month(processed_df)
    plot_sales_by_city(processed_df)
    plot_sales_by_hour(processed_df)
    top_10_products_saletogether(processed_df)
    plot_quantity_by_product(processed_df)
    plot_quantity_vs_price_by_product(processed_df)
    see_report()
if __name__ == "__main__":
    main()
