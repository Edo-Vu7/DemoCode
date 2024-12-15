import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
def see_report():
    """Trình bày các giá trị mới phân tích"""
    img_original = None  # Tham chiếu ảnh gốc
    def open_image():
        nonlocal img_original
        file_path = filedialog.askopenfilename(
            title="Chọn hình ảnh",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")]
        )
        if file_path:
            img_original = Image.open(file_path)
            update_image()  # Hiển thị ảnh sau khi mở
    def update_image(event=None):
        if img_original:
            # Lấy kích thước khung hiển thị
            frame_width = frame.winfo_width()
            frame_height = frame.winfo_height()
            # Thay đổi kích thước ảnh để vừa khung
            resized_img = img_original.resize((frame_width, frame_height))
            img = ImageTk.PhotoImage(resized_img)
            label_img.config(image=img)
            label_img.image = img  # Giữ tham chiếu ảnh để tránh bị xóa
    # Giao diện Tkinter
    root = tk.Tk()
    root.title("Báo cáo dữ liệu")
    # Nút chọn hình ảnh
    btn_open = tk.Button(root, text="Chọn hình ảnh", command=open_image)
    btn_open.pack(pady=10)
    # Khung để hiển thị ảnh
    frame = tk.Frame(root, width=400, height=300, bg="gray")
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    # Label hiển thị hình ảnh
    label_img = tk.Label(frame, bg="gray")
    label_img.pack(fill=tk.BOTH, expand=True)
    # Gắn sự kiện cập nhật khi khung thay đổi kích thước
    frame.bind("<Configure>", update_image)

    root.mainloop()