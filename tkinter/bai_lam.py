import tkinter as tk
from tkcalendar import DateEntry
import csv
from datetime import datetime

# Khởi tạo cửa sổ chính
root = tk.Tk()
root.title("Thông tin nhân viên")

# Checkbox lựa chọn loại
checkbox_frame = tk.Frame(root)
checkbox_frame.grid(row=0, column=0, columnspan=3, pady=10, sticky="w")
tk.Label(checkbox_frame, text="Thông tin nhân viên", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=5,
                                                                                      sticky="w")
chk_customer = tk.Checkbutton(checkbox_frame, text="Là khách hàng")
chk_customer.grid(row=0, column=1, padx=10, sticky="w")
chk_supplier = tk.Checkbutton(checkbox_frame, text="Là nhà cung cấp")
chk_supplier.grid(row=0, column=2, padx=10, sticky="w")

# Các trường nhập liệu
# Dòng 1
row1_frame = tk.Frame(root)
row1_frame.grid(row=1, column=0, columnspan=4, pady=5, sticky="w")
tk.Label(row1_frame, text="Mã *").grid(row=0, column=0, padx=5, sticky="w")
entry_ma = tk.Entry(row1_frame, width=20)
entry_ma.grid(row=1, column=0, padx=5, pady=5)

tk.Label(row1_frame, text="Tên *").grid(row=0, column=1, padx=5, sticky="w")
entry_ten = tk.Entry(row1_frame, width=30)
entry_ten.grid(row=1, column=1, padx=5, pady=5)

tk.Label(row1_frame, text="Ngày sinh *").grid(row=0, column=2, padx=5, sticky="w")
entry_ngaysinh = DateEntry(row1_frame, width=20, date_pattern="dd/mm/yyyy")
entry_ngaysinh.grid(row=1, column=2, padx=5, pady=5)

# Giới tính
tk.Label(row1_frame, text="Giới tính").grid(row=0, column=3, padx=5, sticky="w")
gender_var = tk.StringVar(value="Nam")
tk.Radiobutton(row1_frame, text="Nam", variable=gender_var, value="Nam").grid(row=1, column=3, padx=5, sticky="w")
tk.Radiobutton(row1_frame, text="Nữ", variable=gender_var, value="Nữ").grid(row=1, column=4, padx=5, sticky="w")

# Dòng 2
row2_frame = tk.Frame(root)
row2_frame.grid(row=2, column=0, columnspan=2, pady=5, sticky="w")
tk.Label(row2_frame, text="Đơn vị *").grid(row=0, column=0, padx=5, sticky="w")
entry_donvi = tk.Entry(row2_frame, width=40)
entry_donvi.grid(row=1, column=0, padx=5, pady=5)

tk.Label(row2_frame, text="Số CMND*").grid(row=0, column=1, padx=5, sticky="w")
entry_chucdanh = tk.Entry(row2_frame, width=30)
entry_chucdanh.grid(row=1, column=1, padx=5, pady=5)

tk.Label(row2_frame, text="Ngày cấp").grid(row=0, column=2, padx=5, sticky="w")
entry_ngaycap = DateEntry(row2_frame, width=20, date_pattern="dd/mm/yyyy")
entry_ngaycap.grid(row=1, column=2, padx=5, pady=5)

# Dòng 3
row3_frame = tk.Frame(root)
row3_frame.grid(row=3, column=0, columnspan=2, pady=5, sticky="w")
tk.Label(row3_frame, text="Chức danh *").grid(row=0, column=0, padx=5, sticky="w")
entry_cmnd = tk.Entry(row3_frame, width=45)
entry_cmnd.grid(row=1, column=0, padx=5, pady=5)

tk.Label(row3_frame, text="Nơi cấp *").grid(row=0, column=1, padx=10, sticky="w")
entry_noicap = tk.Entry(row3_frame, width=45)
entry_noicap.grid(row=1, column=1, padx=5, pady=5)

# Dòng 4 (Các nút)
row4_frame = tk.Frame(root)
row4_frame.grid(row=4, column=0, columnspan=3, pady=15, sticky="w")


def save_to_csv():
    # Lấy giá trị từ các trường nhập liệu
    ma = entry_ma.get()
    ten = entry_ten.get()
    ngaysinh = entry_ngaysinh.get_date().strftime("%d/%m/%Y")
    gioitinh = gender_var.get()
    donvi = entry_donvi.get()
    cmnd = entry_chucdanh.get()
    ngaycap = entry_ngaycap.get_date().strftime("%d/%m/%Y")
    chucdanh = entry_cmnd.get()
    noicap = entry_noicap.get()

    # Kiểm tra các trường có bị bỏ trống không
    if not all([ma, ten, ngaysinh, donvi, cmnd, ngaycap, chucdanh, noicap]):
        print("Vui lòng điền đầy đủ tất cả các trường!")
        return

    # Mở file CSV và ghi dữ liệu vào
    try:
        with open('employee_info.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([ma, ten, ngaysinh, gioitinh, donvi, cmnd, ngaycap, chucdanh, noicap])
        print("Dữ liệu đã được lưu!")
    except Exception as e:
        print(f"Đã có lỗi xảy ra khi lưu file CSV: {e}")


# Hàm hiển thị danh sách sinh nhật hôm nay
def show_birthday_today():
    today = datetime.today().strftime("%d/%m")  # Lấy ngày hiện tại (chỉ ngày/tháng)

    birthday_list = []

    # Đọc dữ liệu từ file CSV
    try:
        with open('employee_info.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                # Lấy ngày sinh từ cột thứ 3
                ngaysinh = row[2]
                if ngaysinh[0:5] == today:  # Kiểm tra nếu ngày sinh là hôm nay
                    birthday_list.append(row)

        # Nếu có nhân viên sinh nhật hôm nay, hiển thị danh sách
        if birthday_list:
            birthday_window = tk.Toplevel(root)
            birthday_window.title("Danh sách sinh nhật hôm nay")

            for idx, employee in enumerate(birthday_list):
                tk.Label(birthday_window, text=f"{employee[1]} - Ngày sinh: {employee[2]}").grid(row=idx, column=0,
                                                                                                 padx=10, pady=5)

        else:
            print("Không có nhân viên nào sinh nhật hôm nay.")

    except FileNotFoundError:
        print("File CSV không tồn tại.")
# Hàm tính tuổi
def calculate_age(birthday_str):
    birthday = datetime.strptime(birthday_str, "%d/%m/%Y")
    today = datetime.today()
    age = today.year - birthday.year
    if today.month < birthday.month or (today.month == birthday.month and today.day < birthday.day):
        age -= 1
    return age

# Hàm xuất danh sách nhân viên vào file CSV theo độ tuổi giảm dần
def export_sorted_list():
    employees = []

    # Đọc dữ liệu từ file CSV
    try:
        with open('employee_info.csv', mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Bỏ qua dòng header
            for row in reader:
                name = row[1]  # Tên
                birthday = row[2]  # Ngày sinh
                age = calculate_age(birthday)
                employees.append((name, birthday, age))

        # Sắp xếp danh sách theo độ tuổi giảm dần
        employees.sort(key=lambda x: x[2], reverse=True)

        # Xuất danh sách vào file CSV mới
        with open('sorted_employee_info.csv', mode='w', newline='', encoding='utf-8') as sorted_file:
            writer = csv.writer(sorted_file)
            writer.writerow(["Tên", "Ngày sinh", "Tuổi"])
            for employee in employees:
                writer.writerow([employee[0], employee[1], employee[2]])

        print("Danh sách đã được xuất vào file 'sorted_employee_info.csv'.")

    except FileNotFoundError:
        print("File CSV không tồn tại.")

# Nút lưu
button_save = tk.Button(row4_frame, text="Lưu", width=20, command=save_to_csv)
button_save.grid(row=0, column=0, padx=10)

button_birthday = tk.Button(row4_frame, text="Sinh nhật hôm nay", width=20, command=show_birthday_today)
button_birthday.grid(row=0, column=1, padx=10)

button_export = tk.Button(row4_frame, text="Xuất toàn bộ danh sách", width=20,command=export_sorted_list)
button_export.grid(row=0, column=2, padx=10)

root.mainloop()
